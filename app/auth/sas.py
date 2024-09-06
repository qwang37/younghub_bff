from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from datetime import datetime, timedelta
from flask import Blueprint, jsonify, request

auth_bp = Blueprint('auth', __name__)

# Replace with your Azure Storage Account details
account_name = 'younghubstorage'
account_key = '1SonEvWg1J8ftewzss+A9foSIx5iPSXAC6DzOeRZiLv9JpdTsmWvcfAI43U/bZ7PLrP+m+tnrThM+AStkfWykw=='
container_name = 'short-video'

# Define a route for the Swift app to request a SAS token for the container
@auth_bp.route('/get-sas-token', methods=['POST'])
def get_sas_token():
    # Generate a SAS token for the container with list permission
    sas_token = generate_container_sas(
        account_name=account_name,
        container_name=container_name,
        account_key=account_key,
        permission=ContainerSasPermissions(read=True, list=True),
        expiry=datetime.now() + timedelta(days=10)
    )

    # Build the full SAS URL for the container
    sas_url = f"https://{account_name}.blob.core.windows.net/{container_name}?{sas_token}"

    return jsonify({'sas_url': sas_url})
