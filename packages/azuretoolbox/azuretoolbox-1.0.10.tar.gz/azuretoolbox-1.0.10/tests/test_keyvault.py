import unittest
from unittest.mock import patch
from tests.mocks import mock_imports

env_vars = {
    'AZURE_CLIENT_ID': '<client_id>',
    'AZURE_CLIENT_SECRET': '<client_secret>',
    'AZURE_TENANT_ID': '<tenant_id>'
}

class MockSecret:
    def __init__(self, value) -> None:
        self.value = value
        pass

class TestKeyVault(unittest.TestCase):
    @mock_imports()
    def get_keyvault(self):
        from src.azuretoolbox.keyvault import KeyVault
        return KeyVault('https://<keyvault_name>.vault.azure.net')

    @patch.dict('os.environ', env_vars)
    def test_keyvault_is_created(self):
        # Arrange
        keyvault = self.get_keyvault()

        # Act & Assert
        self.assertIsNotNone(keyvault)

    @patch.dict('os.environ', {})
    def test_keyvault_throws_exception_when_env_variables_are_not_defined(self):
        # Arrange
        from src.azuretoolbox.keyvault import EnvironmentError

        # Act & Assert
        with self.assertRaises(EnvironmentError):
            self.get_keyvault()

    @patch.dict('os.environ', env_vars)
    def test_getting_secret_returns_defined_secret_value(self):
        # Arrange
        keyvault = self.get_keyvault()

        # Act & Assert
        self.assertIsNotNone(keyvault.get_secret('secretName'))


if __name__ == '__main__':
    unittest.main()
