import logging
from models import SessionModel
from repositories import SessionRepo

session_repo = SessionRepo()

def az_df_ffmpeg_check_status(job):
    session_id = job["session_id"]

    # Check the status of the ffmpeg job (Mock)
    print(f"Checking status for ffmpeg job: {session_id}")

    session: SessionModel = session_repo.retrieve(session_id)

    try:
        # Retrieve item from Cosmos DB
        print(f"Retrieved item: {session.to_dto()}")

        # Check the status attribute
        if session.video_uploaded:
            return "Completed"
        else:
            return "InProgress"
    except Exception as e:
        logging.error(f"Error retrieving item from Cosmos DB: {e}")
        return False

def main(job: dict) -> str:
    return az_df_ffmpeg_check_status(job)
