from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from datetime import datetime, timedelta


# Utility class to handle Azure Key Vault and Storage operations
class AzureStorageUtil:
    def __init__(self):
        self.key_vault_name = "storage-account-01"
        self.secret_name = "younghub-storage-key"
        self.KVUri = f"https://{self.key_vault_name}.vault.azure.net/"
        self.credential = DefaultAzureCredential()  # Authenticate with Azure

    # Function to retrieve the storage account key from Key Vault
    def get_storage_account_key(self):
        secret_client = SecretClient(vault_url=self.KVUri, credential=self.credential)
        storage_account_key = secret_client.get_secret(self.secret_name).value
        return storage_account_key

    # Function to generate a SAS token
    def generate_sas_token(self, account_name, container_name, expiry_days=10):
        account_key = self.get_storage_account_key()
        sas_token = generate_container_sas(
            account_name=account_name,
            container_name=container_name,
            account_key=account_key,
            permission=ContainerSasPermissions(read=True, list=True),
            expiry=datetime.utcnow() + timedelta(days=expiry_days)  # SAS token expires in X days
        )
        return sas_token

    # Function to generate the connection string
    def get_connection_string(self, account_name):
        account_key = self.get_storage_account_key()
        return f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
