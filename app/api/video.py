from flask import Blueprint, jsonify
from app.util.azure_storage_util import AzureStorageUtil
from azure.storage.blob import BlobServiceClient

# Replace with your Key Vault and secret name
key_vault_name = "storage-account-01"
secret_name = "younghub-storage-key"
account_name = 'younghubstorage'
container_name = 'short-video'

video_bp = Blueprint('videos', __name__)

# Initialize the Azure Storage utility
storage_util = AzureStorageUtil(key_vault_name=key_vault_name, secret_name=secret_name)

# Function to list all video blobs in the container
def list_video_blobs():
    # Get the connection string using the AzureStorageUtil class
    connection_string = storage_util.get_connection_string(account_name)

    # Initialize the BlobServiceClient using the connection string
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Get the container client
    container_client = blob_service_client.get_container_client(container_name)

    # List blobs in the container
    blobs = container_client.list_blobs()

    # Base URL for the blobs
    video_url = f"https://{blob_service_client.account_name}.blob.core.windows.net/{container_name}"

    # Prepare a list of videos (with IDs and URLs)
    video_list = [{"ID": idx, "VideoURL": f"{video_url}/{blob.name}"} for idx, blob in enumerate(blobs)]

    return video_list

# Route to list all videos dynamically
@video_bp.route('/videos')
def list_videos():
    videos = list_video_blobs()
    return jsonify(videos)
