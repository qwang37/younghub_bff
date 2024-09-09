from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request

# Replace with your Key Vault name and secret name
key_vault_name = "storage-account-01"
KVUri = f"https://{key_vault_name}.vault.azure.net/"
secret_name = "younghub-storage-key"  # This is the secret name you created in the portal

# Initialize the Blueprint for Flask
auth_bp = Blueprint('auth', __name__)

# Function to retrieve the secret (storage account key) from Azure Key Vault
def get_storage_account_key():
    # Use DefaultAzureCredential to authenticate
    credential = DefaultAzureCredential()

    # Create a SecretClient to access Key Vault
    secret_client = SecretClient(vault_url=KVUri, credential=credential)

    # Retrieve the storage account key from Key Vault
    storage_account_key = secret_client.get_secret(secret_name).value
    return storage_account_key

# Define a route for the Swift app to request a SAS token for the container
@auth_bp.route('/get-sas-token', methods=['POST'])
def get_sas_token():
    # Replace this with your actual storage account name and container name
    account_name = 'younghubstorage'
    container_name = 'short-video'

    # Get the storage account key from Key Vault
    account_key = get_storage_account_key()

    # Generate a SAS token for the container with read and list permission
    sas_token = generate_container_sas(
        account_name=account_name,
        container_name=container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True, list=True),
        expiry=datetime.utcnow() + timedelta(days=10)  # Use UTC for expiration
    )

    # Build the full SAS URL for the container
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}?{sas_token}"

    return jsonify({'sas_url': sas_url})
