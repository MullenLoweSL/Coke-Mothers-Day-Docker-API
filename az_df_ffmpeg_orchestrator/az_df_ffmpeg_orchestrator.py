import logging
import azure.durable_functions as df
from datetime import datetime, timedelta

def orchestrator_function(context: df.DurableOrchestrationContext):
    job = context.get_input()
    logging.info(f"Received job: {job}")
    session_id = job["session_id"]
    polling_interval = job["pollingInterval"]
    expiry_time = datetime.fromisoformat(job["expiryTime"]).replace(tzinfo=None)

    # Start the ffmpeg job
    _ = yield context.call_activity("az_df_ffmpeg_start", {"session_id": session_id})

    while context.current_utc_datetime.replace(tzinfo=None) < expiry_time:
        job_status = yield context.call_activity("az_df_ffmpeg_check_status", {"session_id": session_id})
        if job_status == "Completed":
            print("az_df_ffmpeg_check_status: Completed")
            yield context.call_activity("az_df_ffmpeg_update_status", {"session_id": session_id})
            yield context.call_activity("az_df_ffmpeg_send_alert", {"session_id": session_id})
            break
        
        print("az_df_ffmpeg_check_status: InProgress")
        next_check = context.current_utc_datetime.replace(tzinfo=None) + timedelta(seconds=polling_interval)
        yield context.create_timer(next_check)

    return f"ffmpeg polling completed for session: {session_id}"

main = df.Orchestrator.create(orchestrator_function)
