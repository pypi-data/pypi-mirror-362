import logging
from typing import Any

from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

from secret_store import SecretStore, SecretNotFoundError


class AzureStore(SecretStore):
    """A secret store that reads secrets from an Azure KeyVault.
    """
    NAME = 'azure'

    def __init__(self, key_vault_name: str):
        """Instantiate a connection to an Azure KeyVault.

        Args:
            key_vault_name (str): The name of the Azure KeyVault.
        """
        self.key_vault_name = key_vault_name
        KVUri = f"https://{self.key_vault_name}.vault.azure.net"

        credential = DefaultAzureCredential()
        self.client = SecretClient(vault_url=KVUri, credential=credential)

    def set(self, name: str, value: Any) -> None:
        """Set a secret value by name.

        Args:
            name (str): The name of the secret.
            value (str): The value of the secret.

        Returns:
            None
        """
        logging.debug(f"Setting secret '{name}' to '{value}' in Azure "
                      f"Secret Key Vault '{self.key_vault_name}'.")

        self.client.set_secret(name, value)

    def get(self, name: str, default: Any = SecretStore.no_default) -> Any:
        """Get the value of a secret by name.

        Args:
            name (str): The name of the secret.
            default (Any, optional): A value to return if the secret does not
                exist or retrieving it fails.

        Raises:
            Exception: If the secret does not exist or cannot be retrieved and
                |default| is not set.

        Returns:
            Any: The value of the secret. This will be a string unless
                |default| is set and the secret is not found, then the type
                will be that of |default|.
        """
        logging.debug(f"Retrieving secret '{name}' from Azure Secret Key "
                      f"Vault '{self.key_vault_name}'.")

        try:
            secret = self.client.get_secret(name)
            value = secret.value
        except Exception:
            if default == SecretStore.no_default:
                raise SecretNotFoundError("Unable to retrieve secret with "
                                          f"name '{name}'.")
            value = default

        return value
