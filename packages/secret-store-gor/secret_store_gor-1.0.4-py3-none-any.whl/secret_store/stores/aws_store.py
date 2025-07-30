import base64
import logging
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

from secret_store import SecretStore, SecretNotFoundError


class AWSStore(SecretStore):
    """A secret store that reads secrets from the Amazon Secrets Manager.
    """
    NAME = 'aws'

    def __init__(self,
                 aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 region: Optional[str] = None):
        """Instantiate a connection to the AWS Secrets Manager.

        Args:
            region (Optional[str]): The AWS region to connect to.
            aws_access_key_id (Optional[str]): AWS access key ID.
            aws_secret_access_key (Optional[str]):  AWS secret access key.

            Note: If all arguments are undefined (None), will attempt to
                connect via env-vars, config, IAM role.
        """
        self.region = region

        session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

        self.client = session.client(
            service_name='secretsmanager',
            region_name=region
        )

    def set(self, name: str, value: Any) -> None:
        """Set a secret value by name.

        Args:
            name (str): The name of the secret.
            value (str): The value of the secret.

        Returns:
            None
        """
        logging.debug(f"Setting secret '{name}' to '{value}' in AWS Secrets "
                      f"Manager in region '{self.region}'.")

        # No "Does secret exist?" functionality...
        try:
            self.client.create_secret(
                Name=name,
                SecretString=value
            )
        except ClientError as e:
            # Fail for any reason other than the secret existing.
            if e.response['Error']['Code'] != 'ResourceExistsException':
                raise e

        self.client.put_secret_value(
            SecretId=name,
            SecretString=value
        )

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
        logging.debug(f"Retrieving secret '{name}' from AWS Secrets Manager "
                      f"in region '{self.region}''.")

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=name
            )
        except ClientError as e:
            if default == SecretStore.no_default:
                raise SecretNotFoundError(f"Unable to retrieve secret with "
                                          f"name '{name}'. Error Code: "
                                          f"'{e.response['Error']['Code']}'.")
            value = default
        else:
            if 'SecretString' in get_secret_value_response:
                value = get_secret_value_response['SecretString']
            else:
                value = base64.b64decode(
                    get_secret_value_response['SecretBinary']
                )

        return value
