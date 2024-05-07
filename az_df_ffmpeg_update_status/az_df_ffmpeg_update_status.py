import logging
from models import SessionModel
from repositories import SessionRepo

session_repo = SessionRepo()

def az_df_ffmpeg_update_status(job):
    session_id = job["session_id"]
    session: SessionModel = session_repo.retrieve(session_id)

    try:
        # Update the status attribute
        session.video_uploaded = True
        _ = session_repo.update(session)

        logging.info(f"Updated ffmpeg status for session: {session_id}")
        return "Success"
    except Exception as e:
        logging.error(f"Error updating item in Cosmos DB: {e}")
        return "Failure"

def main(job: dict) -> str:
    return az_df_ffmpeg_update_status(job)
