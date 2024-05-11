import random
import logging
import json
import azure.functions as func
from controllers.SessionController import SessionController
from services.BlobService import BlobService
from services.SunoService import SunoService
from mutagen.mp3 import MP3
import tempfile
import requests

def get_audio_duration(url):
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)

    # Download the file
    try:
        response = requests.get(url, stream=True)
        for chunk in response.iter_content(chunk_size=512):
            temp_file.write(chunk)
        temp_file.close()
    except Exception as e:
        logging.error(f"Failed to download file: {e}")
        return 120

    # Get the duration
    try:
        audio = MP3(temp_file.name)
        length = audio.info.length
        return length
    except Exception as e:
        logging.error(f"Failed to get audio duration: {e}")
        return 120

def random_boolean():
    return random.random() < 0.5

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # TODO: Clean up
    session_id: str = req.route_params.get('session_id')
    handler = SessionController()
    ready = handler.is_session_completed(session_id)
    if ready:

        # get song URL from Suno
        suno_song_id = handler.get_suno_song_id(session_id)
        song_url = SunoService().get_song_URL(suno_song_id)
        duration = get_audio_duration(song_url)
        # duration = None
        result = {
            "image_url": BlobService().get_url_from_blob_path(session_id + "/image_branded.png", expiration_minutes=5),
            "audio_url": song_url,
            "duration": duration,
            "title":"DUMMY TITLE",
            "description":"DUMMY DESCRIPTION"
        }
    else:
        result = None

    # # session_id: str = req.route_params.get('session_id')
    # result = None
    # if random_boolean():
    #     result = {
    #         "image_url":"https://i.ibb.co/1JsmZQm/653-400x400.jpg",
    #         "audio_url":"https://mullenlowedemo.blob.core.windows.net/coke-mothers-day/test/song.mp3?sp=r&st=2024-04-30T15:13:38Z&se=2024-08-27T23:13:38Z&sv=2022-11-02&sr=b&sig=k4aquYkICPMmu8M0ZDgBipv2fS5xvRVCuSqmARm18H8%3D",
    #         "title":"DUMMY TITLE",
    #         "description":"DUMMY DESCRIPTION"
    #     }
    return func.HttpResponse(json.dumps({"result": result}), status_code=200, mimetype="application/json")