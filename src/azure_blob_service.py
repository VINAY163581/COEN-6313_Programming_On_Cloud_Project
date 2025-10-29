# app/azure_blob_service.py

from azure.storage.blob import BlobServiceClient
from config import AZURE_STORAGE_CONNECTION_STRING, AZURE_CONTAINER_NAME
import os

# Create the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

def upload_to_blob(local_file_path, blob_name):
    """Uploads a file to Azure Blob Storage."""
    with open(local_file_path, "rb") as data:
        container_client.upload_blob(name=blob_name, data=data, overwrite=True)
    print(f"✅ Uploaded {blob_name} to Azure Blob Storage")

def download_from_blob(blob_name, download_path):
    """Downloads a file from Azure Blob Storage."""
    blob_client = container_client.get_blob_client(blob_name)
    with open(download_path, "wb") as download_file:
        download_file.write(blob_client.download_blob().readall())
    print(f"⬇️ Downloaded {blob_name} to {download_path}")
