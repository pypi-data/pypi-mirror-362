import re
from typing import Optional, List, Dict, Any, Union

from pydantic import Field, model_serializer, model_validator, BaseModel

from pypergraph.core import KeyringAssetType, KeyringWalletType, NetworkId

from .shared import sid_manager
from ..accounts.dag_account import DagAccount
from ..accounts.eth_account import EthAccount
from ..keyrings.simple_keyring import SimpleKeyring


class MultiKeyWallet(BaseModel):
    type: str = Field(default=KeyringWalletType.MultiKeyWallet.value)
    id: str = Field(default=None)
    supported_assets: List[str] = Field(default=[])
    label: Optional[str] = Field(default=None, max_length=12)
    keyrings: List[SimpleKeyring] = Field(default=[])
    network: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def compute_id(self):
        """Automatically computes the id based on injected SID value."""
        self.id = sid_manager.next_sid(self.type)
        return self

    @model_serializer
    def model_serialize(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "label": self.label,
            "rings": [ring.model_dump() for ring in self.keyrings],
        }

    def create(self, network: str, label: str):
        """
        Create new multi key wallet. Accounts must be imported.

        :param network: "Constellation" or "Ethereum"
        :param label: The wallet name.
        """

        self.deserialize(label=label, network=network)

    def set_label(self, val: str):
        """
        Set the name of the wallet.

        :param val: The wallet name.
        """
        if not val:
            raise ValueError("MultiKeyWallet :: No label set.")
        self.label = val

    def get_label(self) -> str:
        """
        Get the name of the wallet.

        :return: The wallet name.
        """
        return self.label

    @staticmethod
    def get_network():
        """Not supported by MKW."""
        raise NotImplementedError(
            "MultiChainWallet :: Multi key wallets does not support this method."
        )

    def get_state(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type,
            "label": self.label,
            "network": self.network,
            "supported_assets": self.supported_assets,
            "accounts": [
                {
                    "address": a.get_address(),
                    "label": a.get_label(),
                }
                for a in self.get_accounts()
            ],
        }

    def deserialize(self, label: str, network: str, accounts: Optional[list] = None):
        self.set_label(label)
        self.network = network
        self.keyrings = []

        if accounts is not None:
            for account in accounts:
                self.import_account(account.get("private_key"), account.get("label"))

        if self.network == NetworkId.Ethereum:
            self.supported_assets.extend(
                [KeyringAssetType.ETH.value, KeyringAssetType.ERC20.value]
            )
        elif self.network == NetworkId.Constellation:
            self.supported_assets.append(KeyringAssetType.DAG.value)

    def import_account(
        self, private_key: str, label: str
    ) -> Union[DagAccount, EthAccount]:
        """
        Imports an account using private key, sets a label, creates a keyring and adds it to the list of keyrings.

        :param private_key: The private key of the account to import.
        :param label: Name of the account.
        :return: The account.
        """
        keyring = SimpleKeyring()
        valid = re.fullmatch(r"^[a-fA-F0-9]{64}$", private_key)
        if not valid:
            ValueError("MultiAccountWallet :: Private key is invalid.")
        keyring.deserialize(
            network=self.network,
            accounts=[{"private_key": private_key, "label": label}],
        )
        self.keyrings.append(keyring)
        # Only one account at index 0 present for this wallet type
        return keyring.get_accounts()[0]

    def get_accounts(self) -> List[Union[DagAccount, EthAccount]]:
        """
        Get a list of all MKW accounts.

        :return: List of imported MKW accounts.
        """

        return [
            account for keyring in self.keyrings for account in keyring.get_accounts()
        ]

    def get_account_by_address(self, address: str) -> Union[DagAccount, EthAccount]:
        """
        Get the account matching the specified address.

        :param address: The address matching the account.
        """
        account = None
        for keyring in self.keyrings:
            account = keyring.get_account_by_address(address)
            if account:
                break
        return account

    @staticmethod
    def remove_account():
        """Not supported by MKW."""
        raise ValueError("MultiKeyWallet :: Does not allow removing accounts.")

    @staticmethod
    def export_secret_key():
        """Not supported by MKW."""
        raise ValueError("MultiKeyWallet :: Does not allow exporting secrets.")

    @staticmethod
    def reset_sid():
        sid_manager.reset_sid()
