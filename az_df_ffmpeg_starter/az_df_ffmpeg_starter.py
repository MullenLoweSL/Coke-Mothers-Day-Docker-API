import os
import tempfile
import pathlib
import azure.functions as func
import azure.durable_functions as df
import logging
from datetime import datetime, timedelta
from services.BlobService import BlobService
from services.SlackService import SlackService
from controllers.SessionController import SessionController
from PIL import Image
from io import BytesIO

def get_path_for_temporary_file():
    filepath = tempfile.NamedTemporaryFile().name
    path = pathlib.Path(filepath)
    return str(path.parent) + '/'

async def main(req: func.HttpRequest, starter: str):
    """
    This function:
    - uploads the image, to the container with folder name = session_id as "image.png"
    - overlays the Coke branding as "image_branded.png"
    - generates and uploads the MP4 file as "video.mp4" and
    - update cosmos DB with image_uploaded = True
    """
    
    client = df.DurableOrchestrationClient(starter)
    session_id: str = req.route_params.get('session_id')

    if not session_id:
        return func.HttpResponse(
            "Missing parameter 'session_id'",
            status_code=400
        )

    # --------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------------------------    

    # TODO: Move this to separate file
    # - uploads the image, to the container with folder name = session_id as "image.png"
    SlackService().post_to_slack_webhook(f"Upload: Image collage to blob storage")
    filebytes = req.files['file'].read()
    blob_path = session_id + "/" + "image.png"
    BlobService().write_blob(blob_path, filebytes, True)

    # Write the filebytes to a temporary file
    temp_file_path = get_path_for_temporary_file() + "image.png"
    with open(temp_file_path, 'wb') as temp_file:
        temp_file.write(filebytes)
    
    # - overlays the Coke branding as "image_branded.png"
    # Load both images
    rect_image_path = os.getcwd() + "/assets/strip.png"
    square_image = Image.open(temp_file_path)
    rect_image = Image.open(rect_image_path)

    # Resize the rectangular image to the same width as the square image, keeping aspect ratio
    new_width = square_image.width
    aspect_ratio = rect_image.height / rect_image.width
    new_height = int(aspect_ratio * new_width)
    rect_image_resized = rect_image.resize((new_width, new_height), Image.ANTIALIAS)

    # Create a new image with the same dimensions as the square image
    # but with enough space at the bottom for the rectangular image
    new_image = Image.new("RGB", (square_image.width, square_image.height), (255, 255, 255))
    new_image.paste(square_image, (0, 0))

    # Overlay the resized rectangular image at the bottom of the square image
    y_offset = square_image.height - new_height
    new_image.paste(rect_image_resized, (0, y_offset))

    # # Save the new image
    # new_image.save("image_branded.png")

    # Save the new image to a BytesIO object
    image_stream = BytesIO()
    new_image.save(image_stream, format='PNG')
    image_stream.seek(0)  # Seek back to the start of the file

    # Define the blob path
    branded_blob_path = session_id + "/" + "image_branded.png"

    # Upload the image to blob storage
    BlobService().write_blob(branded_blob_path, image_stream.read(), True)

    # mark this session as image uploaded
    handler = SessionController()
    _ = handler.mark_image_uploaded(session_id)
    
    # --------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------------------------------------------------------------    

    # Define the polling interval and expiry time
    polling_interval = 20  # seconds
    expiry_time = (datetime.utcnow() + timedelta(minutes=1)).isoformat()

    # Start the ffmpeg orchestrator
    job = {
        "session_id": session_id,
        "pollingInterval": polling_interval,
        "expiryTime": expiry_time
    }
    instance_id = await client.start_new('az_df_sms_orchestrator', f"sms-{session_id}", job)

    logging.info(f"Started SMS orchestration with ID = '{instance_id}'")
    return func.HttpResponse(f"SMS orchestration started with instance ID: {instance_id}", status_code=200)
