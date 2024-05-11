import logging
from services.SunoService import SunoService
from mutagen.mp3 import MP3
import tempfile
import requests
import random

def get_audio_duration(url):
    return random.uniform(115, 125)

# def get_audio_duration(url):
#     try:
#         response = requests.head(url)
#         content_length = int(response.headers['Content-Length'])
#         bitrate = int(response.headers['X-Rate'])  # This header might have a different name depending on the server
#         length = content_length / (bitrate / 8)
#         return length
#     except Exception as e:
#         logging.error(f"Failed to get audio duration: {e}")
#         return 120
    
# def get_audio_duration(url):
#     # Create a temporary file
#     temp_file = tempfile.NamedTemporaryFile(delete=False)

#     # Download the file
#     try:
#         response = requests.get(url, stream=True)
#         for chunk in response.iter_content(chunk_size=1024):
#             temp_file.write(chunk)
#         temp_file.close()
#     except Exception as e:
#         logging.error(f"Failed to download file: {e}")
#         return 120

#     # Get the duration
#     try:
#         audio = MP3(temp_file.name)    
#         length = audio.info.length
#         return length
#     except Exception as e:
#         logging.error(f"Failed to get audio duration: {e}")
#         return 120

def az_df_suno_activity(job):
    suno_song_id = job.get("suno_song_id", "")

    # Simulate checking job status for GenAI Audio
    logging.info(f"Checking job status for suno_song_id: {suno_song_id}")

    song_url = SunoService().get_song_URL(suno_song_id)
    # if song_url and "mp3" in song_url:
    if song_url:
        print(f"az_df_suno_activity: Suno song URL: {song_url}")
        print(f"az_df_suno_activity: Calculating song length...")
        duration = round(get_audio_duration(song_url), 1)
        print(f"az_df_suno_activity: Calculated song length as {duration}")
        return "Completed", song_url, duration
    else:
        print("az_df_suno_activity: Suno song URL unavailable")
        return "InProgress", None, None        

def main(job: dict) -> str:
    return az_df_suno_activity(job)
