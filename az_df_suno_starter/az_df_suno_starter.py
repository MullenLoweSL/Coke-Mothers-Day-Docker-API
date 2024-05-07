import azure.functions as func
import azure.durable_functions as df
import logging
from datetime import datetime, timedelta
from services.SunoService import SunoService

async def main(req: func.HttpRequest, starter: str):
    client = df.DurableOrchestrationClient(starter)

    # TODO: Call SunoService with payload params to generate actual suno song ID
    # suno_song_id = .... req.get_json().get("suno_song_id")

    prompt = "[Verse 1]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ\n\n[Verse 2]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ"
    tag = "Smooth jazz"
    title = "Enjoy Life"
    suno_song_id = SunoService().custom_generate(prompt, tag, title)

    # suno_song_id = "835f797a-31b1-4b8d-9aab-7c974dda6acb"
    print(f"Using suno_song_id: {suno_song_id}")

    if not suno_song_id:
        return func.HttpResponse(
            "Missing parameter 'suno_song_id'",
            status_code=400
        )

    polling_interval = 4  # seconds
    expiry_time = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

    job = {
        "suno_song_id": suno_song_id,
        "pollingInterval": polling_interval,
        "expiryTime": expiry_time
    }
    instance_id = await client.start_new('az_df_suno_orchestrator', f"genai-audio-{suno_song_id}", job)

    logging.info(f"Started GenAI Audio orchestration with ID = '{instance_id}'")
    return func.HttpResponse(f"GenAI Audio started with instance ID: {instance_id}", status_code=200)