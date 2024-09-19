from flask import Blueprint, jsonify
from app.util.azure_storage_util import AzureStorageUtil
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta

# Replace with your Key Vault and secret name
key_vault_name = "storage-account-01"
secret_name = "younghub-storage-key"
account_name = 'younghubstorage'
container_name = 'short-video'

video_bp = Blueprint('videos', __name__)

# Initialize the Azure Storage utility
storage_util = AzureStorageUtil(key_vault_name=key_vault_name, secret_name=secret_name)


# Function to list all video blobs in the container and generate SAS URLs
def list_video_blobs_with_sas():
    # Get the connection string using the AzureStorageUtil class
    connection_string = storage_util.get_connection_string(account_name)

    # Initialize the BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # List blobs in the container
    blobs = container_client.list_blobs()

    # Prepare a list of videos (with SAS URLs)
    video_list = []
    for idx, blob in enumerate(blobs):
        # Generate a SAS token for each blob
        sas_token = generate_blob_sas(
            account_name=account_name,
            container_name=container_name,
            blob_name=blob.name,
            account_key=storage_util.get_storage_account_key(),  # Retrieve the account key from Key Vault
            permission=BlobSasPermissions(read=True),
            expiry=datetime.utcnow() + timedelta(hours=1)  # SAS token valid for 1 hour
        )

        # Build the full SAS URL for the blob
        sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob.name}?{sas_token}"

        # Append to the video list with the SAS URL
        video_list.append({
            "ID": idx,
            "VideoURL": sas_url
        })

    return video_list


# Route to list all videos dynamically with SAS URLs
@video_bp.route('/videos')
def list_videos():
    videos = list_video_blobs_with_sas()
    return jsonify(videos)
