from flask import Blueprint, jsonify, request
from app.util.azure_storage_util import AzureStorageUtil

account_name = 'younghubstorage'
container_name = 'short-video'

# Initialize the Blueprint for Flask
auth_bp = Blueprint('auth', __name__)

# Initialize the Azure Storage utility
storage_util = AzureStorageUtil()

# Define a route for the Swift app to request a SAS token for the container
@auth_bp.route('/get-sas-token', methods=['POST'])
def get_sas_token():
    # Generate a SAS token for the container with read and list permission
    sas_token = storage_util.generate_sas_token(account_name=account_name, container_name=container_name)

    # Build the full SAS URL for the container
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}?{sas_token}"

    return jsonify({'sas_url': sas_url})
