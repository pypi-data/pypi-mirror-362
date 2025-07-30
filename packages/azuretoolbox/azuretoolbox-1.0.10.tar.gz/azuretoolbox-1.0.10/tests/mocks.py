from unittest.mock import patch


def mock_imports(**mocked_imports):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with patch('pyodbc.connect', **mocked_imports):
                with patch('azure.keyvault.secrets.SecretClient', **mocked_imports):
                    with patch('azure.identity.DefaultAzureCredential', **mocked_imports):
                        return func(*args, **kwargs)
        return wrapper
    return decorator
