import logging
import uuid

def az_df_ffmpeg_start(job):
    session_id = job["session_id"]

    # Start the ffmpeg job (Mock)
    ffmpeg_job_id = str(uuid.uuid4())
    logging.info(f"Starting ffmpeg job with ID: {ffmpeg_job_id} for session: {session_id}")
    logging.info(f"DONE.... TEMP")

    # Replace this section with actual ffmpeg starting logic
    # Example:
    # os.system(f"ffmpeg -i {input_path} -vf scale=320:240 {output_path}")

    return ffmpeg_job_id

def main(job: dict) -> str:
    return az_df_ffmpeg_start(job)
