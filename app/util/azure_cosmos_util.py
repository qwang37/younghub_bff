from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions


class AzureCosmosUtil:
    def __init__(self):
        self.key_vault_name = "storage-account-01"
        self.secret_name = "younghub-cosmos-master-key"
        self.KVUri = f"https://{self.key_vault_name}.vault.azure.net/"
        self.credential = DefaultAzureCredential()  # Authenticate with Azure

        self.host = 'https://younghub.documents.azure.com:443/'
        self.db_name = 'Article'
        self.container_id = 'List'

    def get_container(self):
        secret_client = SecretClient(vault_url=self.KVUri, credential=self.credential)
        master_key = secret_client.get_secret(self.secret_name).value

        client = cosmos_client.CosmosClient(self.host, {'masterKey': master_key}, user_agent="yuonghub_cosmos",
                                            user_agent_overwrite=True)

        try:
            # Access the existing database
            db = client.get_database_client(self.db_name)
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error accessing database: {e}')
            return None

        try:
            # Access the existing container
            container = db.get_container_client(self.container_id)
            print(f"Container '{self.container_id}' accessed successfully.")
            return container
        except exceptions.CosmosHttpResponseError as e:
            print(f'Error accessing container: {e}')
            return None

    def read_article_list(self):
        """
        Reads all items from the container and returns them as a list of dictionaries.
        """
        container = self.get_container()
        if container:
            return self.read_items(container)

    def read_items(self, container):
        try:
            # Query all items in the container
            items = container.query_items(
                query="SELECT * FROM c",
                enable_cross_partition_query=True
            )

            result_list = []
            for item in items:
                result_list.append({
                    "OrderID": item.get("OrderID"),
                    "Title": item.get("Title"),
                    "Description": item.get("Description"),
                    "ContentURL": item.get("ContentURL"),
                    "Author": item.get("Author"),
                    "PictureURL": item.get("PictureURL")
                })

            return result_list

        except exceptions.CosmosHttpResponseError as e:
            print(f'Failed to read items: {e}')
            return []
