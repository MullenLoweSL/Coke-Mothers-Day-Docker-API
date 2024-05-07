import io
import os
import logging
import datetime
import requests
from azure.storage.blob import ContainerClient
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import BlobClient
from utils.helpers import get_path_for_temporary_file
from azure.storage.blob import generate_blob_sas, AccountSasPermissions
from azure.core.exceptions import ResourceExistsError
from utils.Singleton import Singleton

class BlobService(metaclass=Singleton):

    def __init__(self):
        # Instantiate a BlobServiceClient using a connection details
        storage_connection_string = os.environ['STORAGE_ACCOUNT_CONNECTION_STRING']
        storage_container = os.environ['STORAGE_ACCOUNT_CONTAINER_NAME']
        self.blob_service_client: BlobServiceClient = BlobServiceClient.from_connection_string(conn_str=storage_connection_string)
        
        # Instantiate the ContainerClient and create container
        self.container_client: ContainerClient = self.blob_service_client.get_container_client(container=storage_container)        

    # def refresh_entry_model_upload_urls(self, entry: EntryModel):
    #     """This method refreshes the upload URLs for all the blobs in the EntryModel""" 
    #     # refresh digital_presentation_image_blob_url
    #     if entry.digital_presentation_image_blob_url:
    #         entry.digital_presentation_image_blob_url.filepathURL = self.get_url_from_blob_path(entry.digital_presentation_image_blob_url.filepath, expiration_minutes=60)
    #     # refresh static_work_blob_url
    #     for upload in entry.static_work_blob_url:
    #         upload.filepathURL = self.get_url_from_blob_path(upload.filepath, expiration_minutes=60)    
    #     # refresh airing_proof_blob_url
    #     for upload in entry.airing_proof_blob_url:
    #         upload.filepathURL = self.get_url_from_blob_path(upload.filepath, expiration_minutes=60)
    #     # refresh client_confirmation_blob_url
    #     if entry.client_confirmation_blob_url:
    #         entry.client_confirmation_blob_url.filepathURL = self.get_url_from_blob_path(entry.client_confirmation_blob_url.filepath, expiration_minutes=60)
    #     # refresh additional_image_links
    #     for upload in entry.additional_image_links:
    #         upload.filepathURL = self.get_url_from_blob_path(upload.filepath, expiration_minutes=60)    
    #     for upload in entry.additional_supporting_docs:
    #         upload.filepathURL = self.get_url_from_blob_path(upload.filepath, expiration_minutes=60)
    #     return entry
    
    def get_url_from_blob_path(self, blob_path: str, expiration_minutes=None):
        blob_client: BlobClient = self.container_client.get_blob_client(blob=blob_path)
        url = blob_client.url
        if expiration_minutes is None:
            # no SAS token request, just return URL
            return url
        else:
            # SAS token requested
            sas_token = self.generate_sas_token(blob_client=blob_client, blob_path=blob_path, expiration_minutes=expiration_minutes)
            url_with_sas = f"{url}?{sas_token}"
        return url_with_sas
    
    def generate_sas_token(self, blob_client: BlobClient, blob_path: str, expiration_minutes):
        return generate_blob_sas(
            account_name=blob_client.account_name,
            account_key=blob_client.credential.account_key,
            container_name=os.environ['STORAGE_ACCOUNT_CONTAINER_NAME'],
            blob_name=blob_path,
            permission=AccountSasPermissions(read=True),
            expiry=datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes))
    
    def upload_file_from_url(self, session_id: str, filename: str, file_url: str) -> bool:
        """Writes a bytes object to Blob storage (using session_id as the path)."""
        try:
            # Download the file in streaming mode
            response = requests.get(file_url, stream=True)
            response.raise_for_status()  # Ensure the response is valid

            # Create a BytesIO object and save the streamed data into it
            file_bytes = io.BytesIO()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # Filter out keep-alive new chunks
                    file_bytes.write(chunk)

            # Reset the file pointer to the beginning of the stream
            file_bytes.seek(0)

            # Upload the file bytes to blob storage (Example code)
            self.upload_file(session_id, filename, file_bytes)
            return True

        except requests.RequestException as e:
            logging.error(f"Failed to upload file from URL: {e}")
            return False
    
    def upload_file(self, session_id: str, filename: str, file_bytes: bytes) -> bool:
        """This method:
        - writes a bytes object to Blob storage (using session_id as the path)
        If overwrite = False, FileService will attempt to reupload by appending (1), (2), etc to the filename
        """

        # TODO: Use try-catch

        # create the blob name with path
        blob_folder = session_id + "/"
        
        # attempt to upload until successful
        blob_path = blob_folder + filename
        _ = BlobService().write_blob(blob_path, blob_bytes=file_bytes, overwrite=True)
        return True

    def write_blob(self, blob_path: str, blob_bytes: bytes, overwrite=False, expiration_minutes=None):
        """This method writes a bytes object to Blob storage, using the specified blob_path
        If expiration_minutes is provided, a URL with SAS token with corresponding expiry time is returned
        Otherwise, just the URL is returned
        """
        
        # create the container if it doesn't exist
        try:
            self.container_client.create_container()
        except ResourceExistsError:
            pass
     
        # write blob to container
        try:
            blob_client: BlobClient = self.container_client.get_blob_client(blob=blob_path)
            blob_client.upload_blob(blob_bytes, overwrite=overwrite)
            return self.get_url_from_blob_path(blob_path=blob_path, expiration_minutes=expiration_minutes)
        except ResourceExistsError:
            return None
    
    def generate_sas_url_from_upload_container(self, zipfile_prefix: str, container_path: str, expiration_minutes: int):
        """Uploads the zipped assets to blob storage and return the SAS URL
        zip_path is None if no files were uploaded"""
        
        zip_path = self.generate_zip_from_blob_container(zipfile_prefix=zipfile_prefix, container_path=container_path)
        if zip_path:
            # copy this file to blob storage
            zip_file = open(zip_path, "rb") # opening for [r]eading as [b]inary
            zip_bytes = zip_file.read()
            zip_file.close()
            blob_path = container_path + "/" + "system" + "/" + zipfile_prefix + ".zip"
            url_with_sas = BlobService().write_blob(blob_path=blob_path,
                                                    blob_bytes=zip_bytes,
                                                    overwrite=True,
                                                    expiration_minutes=expiration_minutes)
            return url_with_sas
        return None