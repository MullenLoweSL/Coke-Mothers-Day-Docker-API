import json
import azure.durable_functions as df
from datetime import datetime, timedelta
from controllers.SessionController import SessionController
from services.SlackService import SlackService

def orchestrator_function(context: df.DurableOrchestrationContext):
    job = context.get_input()
    session_id = job["session_id"]
    suno_song_id = job["suno_song_id"]
    polling_interval = job["pollingInterval"]
    expiry_time = datetime.fromisoformat(job["expiryTime"]).replace(tzinfo=None)

    while context.current_utc_datetime.replace(tzinfo=None) < expiry_time:
        job_status, song_url = yield context.call_activity("az_df_suno_activity", {"suno_song_id": suno_song_id})
        if job_status == "Completed":
            # TODO: DELETE THIS UNUSED "az_df_upload_activity"
            # print("Calling activity: az_df_upload_activity")
            # args = json.dumps({'session_id': session_id, 'song_url': song_url})
            # result = yield context.call_activity('az_df_upload_activity', args)
            # print(result)

            # TODO: Update DB
            handler = SessionController()
            result = handler.mark_song_song_created(session_id, suno_song_id)
            SlackService().post_to_slack_webhook(f"Suno: song generation completed (Session ID: {session_id})")
            print(f"Suno: song generation completed (Session ID: {session_id})")
            break

        next_check = context.current_utc_datetime.replace(tzinfo=None) + timedelta(seconds=polling_interval)
        yield context.create_timer(next_check)

    return f"Polling completed for song: {suno_song_id}"

main = df.Orchestrator.create(orchestrator_function)