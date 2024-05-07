import azure.durable_functions as df
from datetime import datetime, timedelta

def orchestrator_function(context: df.DurableOrchestrationContext):
    job = context.get_input()
    suno_song_id = job["suno_song_id"]
    polling_interval = job["pollingInterval"]
    expiry_time = datetime.fromisoformat(job["expiryTime"]).replace(tzinfo=None)

    while context.current_utc_datetime.replace(tzinfo=None) < expiry_time:
        job_status = yield context.call_activity("az_df_suno_activity", {"suno_song_id": suno_song_id})
        if job_status == "Completed":
            yield context.call_activity("SendAlert", suno_song_id)
            break

        next_check = context.current_utc_datetime.replace(tzinfo=None) + timedelta(seconds=polling_interval)
        yield context.create_timer(next_check)

    return f"Polling completed for song: {suno_song_id}"

main = df.Orchestrator.create(orchestrator_function)