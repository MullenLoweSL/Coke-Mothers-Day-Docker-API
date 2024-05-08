import azure.functions as func
import azure.durable_functions as df
import logging
from datetime import datetime, timedelta
from models.TypeformModel import TypeformModel
from services.SunoService import SunoService
from services.TypeformService import TypeformService
from controllers.SessionController import SessionController

handler = SessionController()

async def main(req: func.HttpRequest, starter: str):
    client = df.DurableOrchestrationClient(starter)


    # convert incoming webhook to a Typeform result
    typeform = TypeformService().convert_webhook_to_typeform(req.get_json())
    session_id = typeform.session_id

    # save result to DB
    _ = handler.save_typeform_results(session_id, typeform)

    # TODO: Call SunoService with payload params to generate actual suno song ID
    # suno_song_id = .... req.get_json().get("suno_song_id")
    prompt = "[Verse 1]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ\n\n[Verse 2]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ"
    tag = "Pop"
    title = "Enjoy Life"
    suno_song_id = SunoService().custom_generate(prompt, tag, title)

    # session_id = "abc123"
    # suno_song_id = "11260199-4693-4c53-936d-f9811e109312"
    print(f"Using suno_song_id: {suno_song_id}")

    if not suno_song_id:
        return func.HttpResponse(
            "Missing parameter 'suno_song_id'",
            status_code=400
        )

    polling_interval = 4  # seconds
    expiry_time = (datetime.utcnow() + timedelta(minutes=5)).isoformat()

    job = {
        "session_id": session_id,
        "suno_song_id": suno_song_id,
        "pollingInterval": polling_interval,
        "expiryTime": expiry_time
    }
    instance_id = await client.start_new('az_df_suno_orchestrator', f"genai-audio-{suno_song_id}", job)

    logging.info(f"Started GenAI Audio orchestration with ID = '{instance_id}'")
    return func.HttpResponse(f"GenAI Audio started with instance ID: {instance_id}", status_code=200)