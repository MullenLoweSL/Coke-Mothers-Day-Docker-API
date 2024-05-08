import random
import logging
import json
import azure.functions as func
from controllers.SessionController import SessionController
from services.BlobService import BlobService

def random_boolean():
    return random.random() < 0.5

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # TODO: Clean up
    session_id: str = req.route_params.get('session_id')
    handler = SessionController()
    ready = handler.is_session_completed(session_id)
    if ready:
        result = {
            "image_url": BlobService().get_url_from_blob_path(session_id + "/image_branded.png", expiration_minutes=5),
            "audio_url": BlobService().get_url_from_blob_path(session_id + "/song.mp3", expiration_minutes=5),
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