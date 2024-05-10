import os
import io
import logging
import requests
from azure.storage.blob import BlobType
from services.BlobService import BlobService
from azure.storage.blob import BlobClient
from services.SlackService import SlackService
import json

from azure.storage.blob import BlobServiceClient

storage_connection_string = os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
storage_container = os.environ['STORAGE_ACCOUNT_CONTAINER_NAME']

def main(args: str) -> str:
    args_dict = json.loads(args)
    session_id = args_dict['session_id']
    song_url = args_dict['song_url']

    try:
        # Open a stream to the file URL
        response = requests.get(song_url, stream=True)
        response.raise_for_status()  # Ensure the response is valid

        # Create a BlobClient
        blob_path = session_id + "/song.mp3"
        blob_service_client = BlobServiceClient.from_connection_string(storage_connection_string)
        blob_client = blob_service_client.get_blob_client(storage_container, blob_path)

        # Stream the file to blob storage
        print(f"Download: Starting song download from URL: {song_url}")
        SlackService().post_to_slack_webhook(f"Download: Starting song download from URL: {song_url}")
        # blob_client.upload_blob(response.raw, overwrite=True)
        blob_client.upload_blob(response.raw, blob_type=BlobType.BlockBlob, overwrite=True)
        print(f"Download: Completed song download from URL: {song_url}")
        SlackService().post_to_slack_webhook(f"Download: Completed song download from URL: {song_url}")

        return f"File uploaded successfully to {blob_path}"

    except requests.RequestException as e:
        logging.error(f"Failed to upload file from URL: {e}")
        return None