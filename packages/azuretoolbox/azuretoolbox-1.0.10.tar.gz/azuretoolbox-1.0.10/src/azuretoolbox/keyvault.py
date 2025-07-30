from azure.core.exceptions import ResourceNotFoundError
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential
import os


class EnvironmentError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class KeyVault:
    def __init__(self, vault_url: str) -> None:
        self._check_env()

        credential = DefaultAzureCredential()
        self._secret_client = SecretClient(
            vault_url=vault_url,
            credential=credential
        )
        pass

    def _check_env(self) -> None:
        required_env_vars = [
            'AZURE_CLIENT_ID',
            'AZURE_CLIENT_SECRET',
            'AZURE_TENANT_ID']

        for var in required_env_vars:
            if var not in os.environ:
                raise EnvironmentError(
                    f"{var} not found in environment variables")

    def get_secret(self, secret_name: str) -> str | None:
        try:
            return self._secret_client.get_secret(secret_name).value
        except ResourceNotFoundError:  # pragma: no cover
            return None
        except Exception as e:  # pragma: no cover
            raise e
