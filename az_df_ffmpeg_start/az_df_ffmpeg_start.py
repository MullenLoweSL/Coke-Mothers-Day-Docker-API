import logging
import uuid
import requests
import tempfile
import subprocess
from services.BlobService import BlobService

def az_df_ffmpeg_start(job):
    session_id = job["session_id"]

    # Start the ffmpeg job (Mock)
    ffmpeg_job_id = str(uuid.uuid4())
    logging.info(f"Starting ffmpeg job with ID: {ffmpeg_job_id} for session: {session_id}")

    # download song.mp3 and image_branded.png from Blob storage, then generate MP4 file
    song_url = BlobService().get_url_from_blob_path(session_id + "/song.mp3", expiration_minutes=5)
    image_url = BlobService().get_url_from_blob_path(session_id + "/image_branded.png", expiration_minutes=5)
    
    # Download the files
    song_response = requests.get(song_url)
    image_response = requests.get(image_url)

    # Write the files to temporary storage
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as song_file:
        song_file.write(song_response.content)
        song_path = song_file.name

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as image_file:
        image_file.write(image_response.content)
        image_path = image_file.name
    

    logging.info(f"DONE.... TEMP")

    # Replace this section with actual ffmpeg starting logic
    # Example:
    # os.system(f"ffmpeg -i {input_path} -vf scale=320:240 {output_path}")

    # Create a temporary file for the output
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as output_file:
        output_path = output_file.name

    # Run the ffmpeg -i operation
    command = [
        "ffmpeg", "-i", song_path, "-framerate", "1", "-i", image_path, "-c:v", "libx264", 
        "-preset", "veryslow", "-tune", "stillimage", "-crf", "18", "-pix_fmt", "yuv420p", 
        "-vf", "scale=300:300", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", 
        "+faststart", output_path
    ]
    subprocess.run(command, check=True)
    
    # subprocess.run(["ffmpeg", "-i", song_path, "-i", image_path, "-o", output_path])

    # Open the output file in binary mode and upload it to blob storage
    branded_blob_path = session_id + "/song.mp4"
    with open(output_path, 'rb') as data:
        BlobService().write_blob(branded_blob_path, data.read(), True)

    return ffmpeg_job_id

def main(job: dict) -> str:
    return az_df_ffmpeg_start(job)
