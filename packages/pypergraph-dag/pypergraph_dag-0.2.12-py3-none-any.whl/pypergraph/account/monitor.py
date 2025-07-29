# TODO: wait_for
#       Storage path

import asyncio
import logging
import time
import json

# from dataclasses import dataclass
from typing import Dict, Union, List, Optional, Any, Callable

from pydantic import BaseModel, Field
from rx import operators as ops, of, empty, Observable
from rx.core.abc import Disposable
from rx.scheduler.eventloop import AsyncIOScheduler
from rx.subject import BehaviorSubject

from pypergraph.account.tests import secret
from pypergraph.core.cross_platform.state_storage_db import StateStorageDb
from pypergraph.network.models.network import NetworkInfo
from pypergraph.network.models.transaction import TransactionStatus, PendingTransaction
from pypergraph.network.models.block_explorer import Transaction

TWELVE_MINUTES = 12 * 60 * 1000


# @dataclass
# class WaitFor:
#     future: asyncio.Future
#     resolve: callable


class DagWalletMonitorUpdate(BaseModel):
    pending_has_confirmed: bool = False
    trans_txs: List[PendingTransaction] = Field(default_factory=list)
    tx_changed: bool = False


class Monitor:
    def __init__(self, account, state_storage_file_path: str):
        """
        Monitors events and stores states.

        :param account: DagAccount()
        :param state_storage_file_path: Full path and filename to storage (with file extension).
        """
        self.account = account
        self._scheduler = AsyncIOScheduler(asyncio.get_event_loop())
        self._mem_pool_change = BehaviorSubject(DagWalletMonitorUpdate().model_dump())
        self.last_timer = 0.0
        self.pending_timer = 0.0
        # self.wait_for_map: Dict[str, WaitFor] = {}
        self.cache_utils = StateStorageDb(file_path=state_storage_file_path)
        self.cache_utils.set_prefix("pypergraph-")

    def subscribe_mem_pool(self, callback: Callable[[Any], Observable]) -> Disposable:
        """
        Listen for account events like login and logout.
        Event = {"module": "account", "event": "logout"}
        """
        subscription = self._mem_pool_change.pipe(
            ops.observe_on(self._scheduler),
            ops.flat_map(callback),
            ops.catch(
                lambda e, src: (
                    logging.error(f"Monitor :: {e}", exc_info=True),
                    empty(),
                )[1]
            ),  # Using tuple indexing to return empty()
        ).subscribe()
        return subscription  # subscription.dispose() to unsub

    def subscribe_account(self, callback: Callable[[Any], Observable]) -> Disposable:
        """
        Listen for account events like login and logout.
        Event = {"module": "account", "event": "logout"}
        """
        subscription = self.account._session_change.pipe(
            ops.observe_on(self._scheduler),
            ops.flat_map(callback),
            ops.catch(
                lambda e, src: (
                    logging.error(f"Monitor :: {e}", exc_info=True),
                    empty(),
                )[1]
            ),  # Using tuple indexing to return empty()
        ).subscribe()
        return subscription  # subscription.dispose() to unsub

    def subscribe_network(self, callback: Callable[[Any], Observable]) -> Disposable:
        """
        Listen for network events like network_change.
        Event = {
                    "module": "network",
                    "type": "network_change",
                    "event": self.get_network(),
                }
        """
        subscription = self.account.network._network_change.pipe(
            ops.observe_on(self._scheduler),
            ops.flat_map(callback),
            ops.catch(
                lambda e, src: (
                    logging.error(f"Monitor :: {e}", exc_info=True),
                    empty(),
                )[1]
            ),  # Using tuple indexing to return empty()
        ).subscribe()
        return subscription  # subscription.dispose() to unsub

    async def set_to_mem_pool_monitor(self, pool: List[PendingTransaction]):
        network_info = self.account.network.get_network()
        key = f"network-{network_info['network_id'].lower()}-mempool"
        await self.cache_utils.set(key, [tx.model_dump() for tx in pool])

    async def get_mem_pool_from_monitor(
        self, address: Optional[str] = None
    ) -> List[PendingTransaction]:
        address = address or self.account.address
        network_info = self.account.network.get_network()

        try:
            txs: List[json] = (
                await self.cache_utils.get(
                    f"network-{network_info['network_id'].lower()}-mempool"
                )
                or []
            )
            txs = (
                [
                    PendingTransaction(**json.loads(tx))
                    if not isinstance(tx, dict)
                    else PendingTransaction(**tx)
                    for tx in txs
                ]
                if txs
                else []
            )
        except Exception as e:
            logging.warning(f"Monitor :: {e}, will return empty list.", exc_info=True)
            return []
        return [
            tx
            for tx in txs
            if not address
            or not tx.receiver
            or tx.receiver == address
            or tx.sender == address
        ]

    async def add_to_mem_pool_monitor(
        self, value: PendingTransaction
    ):  # 'value' can be a dict or string
        network_info = NetworkInfo(**self.account.network.get_network())
        key = f"network-{network_info.network_id}-mempool"

        # Get cached payload or initialize empty list
        cached = await self.cache_utils.get(key)
        payload = cached if isinstance(cached, list) else []
        payload = [PendingTransaction(**p) for p in payload]

        # Create transaction object
        if isinstance(value, str):
            tx = PendingTransaction(
                **{"hash": value, "timestamp": int(time.time() * 1000)}
            )
        elif isinstance(value, PendingTransaction):
            tx = value
        else:
            raise ValueError("Monitor :: Must be PendingTransaction or hash.")

        # Check for existing transaction
        if not any(p.hash == tx.hash for p in payload):
            payload.append(tx)
            payload = [tx.model_dump_json(indent=2) for tx in payload]
            await self.cache_utils.set(key, payload)
            self.last_timer = int(time.time() * 1000)
            self.pending_timer = 1000

        asyncio.create_task(self.poll_pending_txs())
        return tx.model_dump()

    async def poll_pending_txs(self):
        try:
            current_time = int(time.time() * 1000)
            if current_time - self.last_timer + 1000 < self.pending_timer:
                logging.debug("Monitor :: Canceling extra timer.")
                return

            pending_result = await self.process_pending_txs()
            pending_txs = pending_result["pending_txs"]
            tx_changed = pending_result["tx_changed"]
            trans_txs = pending_result["trans_txs"]
            pending_has_confirmed = pending_result["pending_has_confirmed"]
            pool_count = pending_result["pool_count"]

            if pending_txs:
                await self.set_to_mem_pool_monitor(pending_txs)
                self.pending_timer = 1000
                self.last_timer = current_time
                await asyncio.sleep(10)
                asyncio.create_task(self.poll_pending_txs())
            elif pool_count > 0:
                await self.set_to_mem_pool_monitor([])

            self._mem_pool_change.on_next(
                DagWalletMonitorUpdate(
                    tx_changed=tx_changed,
                    trans_txs=trans_txs,
                    pending_has_confirmed=pending_has_confirmed,
                ).model_dump()
            )
            logging.debug(
                f"Monitor :: Memory pool updated: {self._mem_pool_change.value}"
            )
        except Exception as e:
            logging.error(f"Monitor :: {e}", exc_info=True)

    async def process_pending_txs(self) -> Dict[str, Any]:
        try:
            pool = await self.get_mem_pool_from_monitor()
            trans_txs = []
            next_pool = []
            pending_has_confirmed = False
            tx_changed = False

            for index, pending_tx in enumerate(pool):
                pending_tx = pool[index]
                try:
                    tx_hash = pending_tx.hash
                    try:
                        be_tx = await self.account.network.get_transaction(tx_hash)
                        if be_tx:
                            pending_tx.timestamp = int(
                                be_tx.timestamp.timestamp() * 1000
                            )
                            pending_has_confirmed = True
                            tx_changed = True
                            pending_tx.pending = False
                            pending_tx.status = TransactionStatus.CONFIRMED.value
                            pending_tx.pending_msg = "Confirmed"
                            # if tx_hash in self.wait_for_map:
                            #     self.wait_for_map[tx_hash].resolve(True)
                            #     del self.wait_for_map[tx_hash]
                        else:
                            if (
                                pending_tx.status != "CHECKPOINT_ACCEPTED"
                                and pending_tx.status
                                != TransactionStatus.GLOBAL_STATE_PENDING.value
                                and pending_tx.timestamp + TWELVE_MINUTES
                                < int(time.time() * 1000)
                            ):
                                pending_tx.status = TransactionStatus.DROPPED.value
                                pending_tx.pending = False
                                tx_changed = True
                            else:
                                if (
                                    pending_tx.status
                                    != TransactionStatus.GLOBAL_STATE_PENDING.value
                                ):
                                    pending_tx.status = (
                                        TransactionStatus.GLOBAL_STATE_PENDING.value
                                    )
                                    pending_tx.pending_msg = "Will confirm shortly..."
                                    tx_changed = True
                                elif not pending_tx.status:
                                    pending_tx.status = "UNKNOWN"
                                    pending_tx.pending_msg = "Transaction not found..."
                                next_pool.append(pending_tx)
                    except Exception as e:
                        logging.error(f"Monitor :: {e}", exc_info=True)

                    trans_txs.append(pending_tx)
                except Exception as e:
                    logging.error(f"Monitor :: {e}", exc_info=True)

            return {
                "pending_txs": next_pool,
                "tx_changed": tx_changed,
                "trans_txs": trans_txs,
                "pending_has_confirmed": pending_has_confirmed,
                "pool_count": len(pool),
            }
        except Exception as e:
            logging.error(f"Monitor :: {e}", exc_info=True)

    # async def wait_for_transaction(self, hash: str) -> asyncio.Future:
    #     """Execute function after transaction has finished."""
    #     # TODO
    #     if hash not in self.wait_for_map:
    #         loop = asyncio.get_event_loop()
    #         future = loop.create_future()
    #         self.wait_for_map[hash] = WaitFor(
    #             future=future,
    #             resolve=lambda result: future.set_result(result)
    #         )
    #     return self.wait_for_map[hash].future

    def start_monitor(self):
        asyncio.create_task(self.poll_pending_txs())

    async def get_latest_transactions(
        self,
        address: str,
        limit: Optional[int] = None,
        search_after: Optional[str] = None,
    ) -> List[Union[PendingTransaction, Transaction]]:
        c_txs = await self.account.network.get_transactions_by_address(
            address, limit, search_after
        )
        pending_result = await self.process_pending_txs()
        pending_transactions = [p for p in pending_result["pending_txs"]]

        return pending_transactions + c_txs if c_txs else pending_transactions + []


async def main():
    from pypergraph import DagAccount

    account = DagAccount()
    monitor = Monitor(account, state_storage_file_path="state_storage.json")

    def safe_network_process_event(observable: dict):
        """Process an event safely, catching errors."""
        # Simulate event processing (replace with your logic)
        print(f"Monitor :: Injected callable network event subscription: {observable}")
        return of(observable)  # Emit the event downstream

    def safe_account_process_event(observable):
        if observable["event"] == "logout":
            print("Monitor :: Injected callable account event: logout signal received.")
        elif observable["event"] == "login":
            print("Monitor :: Injected callable account event: login signal received.")
        else:
            print(
                f"Monitor :: Unknown signal received by injected callable account event: {observable}"
            )
        return of(observable)

    def safe_mem_pool_process_event(observable):
        print(f"Observable: {observable}")
        return of(observable)

    mem_pool_sub = monitor.subscribe_mem_pool(safe_mem_pool_process_event)
    network_sub = monitor.subscribe_network(safe_network_process_event)
    # monitor.start_monitor()
    account_sub = monitor.subscribe_account(safe_account_process_event)
    account.connect("integrationnet")
    account.login_with_seed_phrase(secret.mnemo)
    pending_tx = await account.transfer(secret.to_address, 50000, 200000)
    await monitor.add_to_mem_pool_monitor(pending_tx)
    txs = await monitor.get_latest_transactions(address=account.address, limit=20)
    print(txs)
    network_sub.dispose()
    await asyncio.sleep(120)
    account.logout()
    await asyncio.sleep(1)
    mem_pool_sub.dispose()
    account_sub.dispose()
    network_sub.dispose()


if __name__ == "__main__":
    asyncio.run(main())
