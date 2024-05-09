import io
import logging
import requests
from services.BlobService import BlobService
from services.SlackService import SlackService
import json

def main(args: str) -> str:
    args_dict = json.loads(args)
    session_id = args_dict['session_id']
    song_url = args_dict['song_url']
    # rest of your code
    # Your code to upload the file from the URL goes here.
    # This is just a placeholder implementation.
    
    """Writes a bytes object to Blob storage (using session_id as the path)."""
    try:
        # Download the file in streaming mode
        response = requests.get(song_url, stream=True)
        response.raise_for_status()  # Ensure the response is valid

        # Create a BytesIO object and save the streamed data into it
        SlackService().post_to_slack_webhook(f"Download: Starting song download from URL: {song_url}")
        file_bytes = io.BytesIO()
        for chunk in response.iter_content(chunk_size=262144):  # Increased chunk size to 256 KB
            if chunk:  # Filter out keep-alive new chunks
                file_bytes.write(chunk)
                print("Downloaded 256 KB of chunk data...")

        # Reset the file pointer to the beginning of the stream
        file_bytes.seek(0)

        # Upload the file bytes to blob storage
        blob_path = session_id + "/song.mp3"
        _ = BlobService().write_blob(blob_path, blob_bytes=file_bytes, overwrite=True)
        SlackService().post_to_slack_webhook(f"Download: Completed song download from URL: {song_url}")
        return f"File uploaded successfully to {blob_path}"

    except requests.RequestException as e:
        logging.error(f"Failed to upload file from URL: {e}")
        return None