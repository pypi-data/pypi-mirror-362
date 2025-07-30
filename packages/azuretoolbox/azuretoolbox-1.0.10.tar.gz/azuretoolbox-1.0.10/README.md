# AzureToolbox

[![Build, test and Package](https://github.com/ciuliene/azuretoolbox/actions/workflows/CICD.yml/badge.svg)](https://github.com/ciuliene/azuretoolbox/actions/workflows/CICD.yml)

Utilities for working with Azure services. This version provides tools for:

- Keyvault
- Database

## Installation

```bash
pip install azuretoolbox
```

## Keyvault

Get secrets from Azure Keyvault.

### Prerequisites

To use the Keyvault utilities, you need to have the following environment variables set:

- AZURE_TENANT_ID
- AZURE_CLIENT_ID
- AZURE_CLIENT_SECRET

```sh
export AZURE_TENANT_ID="<your-tenant-id>"
export AZURE_CLIENT_ID="<your-client-id>"
export AZURE_CLIENT_SECRET="<your-client-secret>"
```

### Usage

```python
from azuretoolbox.keyvault import KeyVault

vault_url = "https://<keyvault-name>.vault.azure.net"
secret = KeyVault(vault_url).get_secret("SecretName")
print(secret)
```

## Database

Connect to and query an Azure SQL Database.

### Prequisites

To use the Database utilities, you need to have `ODBC Driver 18 for SQL Server` installed. You can download it from [here](https://learn.microsoft.com/en-us/sql/connect/odbc/microsoft-odbc-driver-for-sql-server?view=sql-server-ver16).

### Usage

```python
from azuretoolbox.database import Database

db = Database()
server = '<server>' # Typically 'tcp:<server-name>.database.windows.net,1433'
database = '<database-name>'
username = '<username>'
password = '<password>'
db.connect(server, database, username, password)

print(db.query('<query-string>'))
```