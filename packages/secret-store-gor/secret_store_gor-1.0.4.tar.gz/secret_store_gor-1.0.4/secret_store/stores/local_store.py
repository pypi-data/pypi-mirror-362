import logging
import os
from pathlib import Path
import re
from typing import Any

from secret_store import SecretStore, SecretNotFoundError


class LocalStore(SecretStore):
    """A secret store that reads secrets from a file stored on disk. The file
    format bust be compatible with the |source| command (eg one KEY=VALUE
    pair per line)
    """
    NAME = 'local'
    env_pat = re.compile(r'''^([^\s=]+)=(?:[\s"']*)(.+?)(?:[\s"']*)$''')

    def __init__(self, path):
        """Instantiate a local secret store.

        Note: If the secret file at |path| does not exist, an empty one will
              be created.

        Args:
            path (str): The path to the secret store on disk.
        """
        self.path = path

        if not os.path.isfile(self.path):
            logging.info("Creating new local secret store at "
                         f"'{self.path}'.")
            Path(self.path).touch()
        else:
            logging.info(f"Connecting to existing local secret store at "
                         f"'{self.path}'.")

    def set(self, name: str, value: Any) -> None:
        """Set a secret value by name.

        Note: The value will be cast to a string before it is stored.

        Args:
            name (str): The name of the secret.
            value (str): The value of the secret.

        Returns:
            None
        """
        value = str(value)

        logging.debug(f"Setting secret '{name}' to '{value}' in local "
                      f"secret store at path '{self.path}'.")

        found = False
        lines = []
        with open(self.path, 'r') as secrets_file:
            for line in secrets_file:
                match = self.env_pat.match(line)
                if match is not None and match.group(1) == name:
                    lines.append(f'{name}={value}\n')
                    found = True
                else:
                    lines.append(line)

        with open(self.path, 'w') as secrets_file:
            for line in lines:
                secrets_file.write(line)

        if not found:
            with open(self.path, 'a') as secrets_file:
                secrets_file.write(f'{name}={value}\n')

    def get(self, name: str, default: Any = SecretStore.no_default) -> Any:
        """Get the value of a secret by name.

        Args:
            name (str): The name of the secret.
            default (Any, optional): A value to return if the secret does not
                exist or retrieving it fails.

        Raises:
            KeyError: If the secret does not exist and |default| is not set.

        Returns:
            Any: The value of the secret. This will be a string unless
                |default| is set and the secret is not found, then the type
                will be that of |default|.
        """
        logging.debug(f"Retrieving secret '{name}' from local secret store at "
                      f"path '{self.path}'.")

        with open(self.path) as secrets_file:
            for line in secrets_file:
                match = self.env_pat.match(line)
                if match is not None and name == match.group(1):
                    return match.group(2)

        if default == SecretStore.no_default:
            raise SecretNotFoundError("Unable to retrieve secret with name "
                                      f"'{name}'.")

        return default
