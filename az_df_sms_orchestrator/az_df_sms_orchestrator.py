import logging
import azure.durable_functions as df
from datetime import datetime, timedelta

def orchestrator_function(context: df.DurableOrchestrationContext):
    job = context.get_input()
    logging.info(f"Received job: {job}")
    session_id = job["session_id"]
    polling_interval = job["pollingInterval"]
    expiry_time = datetime.fromisoformat(job["expiryTime"]).replace(tzinfo=None)

    # now that the photo has been uploaded, send the SMS
    while context.current_utc_datetime.replace(tzinfo=None) < expiry_time:
        job_status = yield context.call_activity("az_df_check_sms_status", {"session_id": session_id})
        if job_status == "Completed":
            break
        
        print("az_df_check_sms_status: InProgress")
        next_check = context.current_utc_datetime.replace(tzinfo=None) + timedelta(seconds=polling_interval)
        yield context.create_timer(next_check)

    return f"ffmpeg polling completed for session: {session_id}"

main = df.Orchestrator.create(orchestrator_function)
