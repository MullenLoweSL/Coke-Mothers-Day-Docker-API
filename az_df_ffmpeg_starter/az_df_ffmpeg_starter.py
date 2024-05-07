import azure.functions as func
import azure.durable_functions as df
import logging
from datetime import datetime, timedelta

async def main(req: func.HttpRequest, starter: str):
    client = df.DurableOrchestrationClient(starter)
    # session_id = req.get_json().get("session_id")
    session_id = "ee4f8403-da9e-41f8-8f6c-29d76ce3aa29"

    if not session_id:
        return func.HttpResponse(
            "Missing parameter 'session_id'",
            status_code=400
        )

    # Define the polling interval and expiry time
    polling_interval = 3  # seconds
    expiry_time = (datetime.utcnow() + timedelta(hours=2)).isoformat()

    # Start the ffmpeg orchestrator
    job = {
        "session_id": session_id,
        "pollingInterval": polling_interval,
        "expiryTime": expiry_time
    }
    instance_id = await client.start_new('az_df_ffmpeg_orchestrator', f"ffmpeg-{session_id}", job)

    logging.info(f"Started ffmpeg orchestration with ID = '{instance_id}'")
    return func.HttpResponse(f"ffmpeg orchestration started with instance ID: {instance_id}", status_code=200)
