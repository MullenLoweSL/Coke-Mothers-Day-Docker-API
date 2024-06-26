import os
import logging
from models import SessionModel
from repositories import SessionRepo
from services.DialogService import DialogService
from services.SlackService import SlackService

session_repo = SessionRepo()

def az_df_check_sms_status(job):
    # don't send SMS if the environment variable is not set
    if not os.environ["SEND_SMS"].lower() == 'true':
        return "Completed"

    session_id = job["session_id"]

    # Check the status of the ffmpeg job (Mock)
    print(f"Checking SMS status for job: {session_id}")

    session: SessionModel = session_repo.retrieve(session_id)
    text = ""
    share_url = os.environ["WEBAPP_SHARE_URL"]
    if session.language == "sn":
        text = f"ඔබේ Coke Mother's Day ගීතය සූදානම්! එය මෙතැනින් සවන් දෙන්න: {share_url + session_id}"
    elif session.language == "ta":
        text = f"உங்கள் Coke அன்னையர் தினப் பாடலை இங்கே கேட்டு மகிழவும்: {share_url + session_id}"
    else:
        text = f"Your Coke mother's day song is ready! Listen to it here: {share_url + session_id}"

    try:
        # recipient = "94777660664"
        recipient = session.phone_number
        result = DialogService().send_sms(text, recipient)
        if result:
            # successfully sent, mark as sent
            session.sms_sent = True
            _ = session_repo.update(session)
            SlackService().post_to_slack_webhook(f"SMS: Sent to user: {session.typeform_response.get_render_string()} with text: {text}")

        # Check the status attribute
        if session.sms_sent:
            return "Completed"
        else:
            return "InProgress"
    except Exception as e:
        logging.error(f"Error retrieving item from Cosmos DB: {e}")
        return False
    
def main(job: dict) -> str:
    return az_df_check_sms_status(job)    