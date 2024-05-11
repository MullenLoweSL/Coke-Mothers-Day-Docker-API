import logging
from services.SunoService import SunoService

def az_df_suno_activity(job):
    suno_song_id = job.get("suno_song_id", "")

    # Simulate checking job status for GenAI Audio
    logging.info(f"Checking job status for suno_song_id: {suno_song_id}")

    song_url = SunoService().get_song_URL(suno_song_id)
    # if song_url and "mp3" in song_url:
    if song_url:
        print(f"az_df_suno_activity: Suno song URL: {song_url}")
        job_status = True
    else:
        print("az_df_suno_activity: Suno song URL unavailable")
        job_status = False
        
    if job_status:
        return "Completed", song_url
    else:
        return "InProgress", None

def main(job: dict) -> str:
    return az_df_suno_activity(job)
