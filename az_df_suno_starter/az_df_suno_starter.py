import random
import azure.functions as func
import azure.durable_functions as df
import logging
from datetime import datetime, timedelta
from models.TypeformModel import TypeformModel
from services.SunoService import SunoService
from services.TypeformService import TypeformService
from services.SlackService import SlackService
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

    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # # CUSTOM LYRICS
    # prompt = "[Verse 1]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ\n\n[Verse 2]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ"
    # tag = "Pop"
    # title = "Enjoy Life"
    # suno_song_id = SunoService().custom_generate(prompt, tag, title)
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------
    # ------------------------------------------------------------------

    if typeform.mothers_music == "Surprise me!":
        styles = ["opera", "rap", "K-pop", "romantic samba", "uplifting rap", "futuristic anime", "melodic soul", "smooth house"]
        style = random.choice(styles)
    elif typeform.mothers_music == "Pop":
        style = "Happy pop"
    else:
        style = typeform.mothers_music

    # decide if E/S/T lyrics
    if typeform.language == "en":
        # AI LYRICS    

        prompt = f"A mother's day song for my mother who's name is '{typeform.mothers_name}'. Mention her favourite food {typeform.mothers_food}, her {typeform.mothers_personality} personality and her favourite pasttime {typeform.mothers_fun}. In {style} style"
        SlackService().post_to_slack_webhook(f"Typeform: Added en song to queue (Session ID: {session_id})")
        suno_song_id = SunoService().ai_generate(prompt)
    elif typeform.language == "si":
        # assume sinhala
        prompt = f"[Intro]\nආදරනීය {typeform.mothers_name}\n\n[Verse 1]\nඇති දැඩි කරලා අප හට පණ දුන්නා\nකරුණාවෙන් අපි සැම රැකගත්තා\nකාලය ගෙවිලා අපි හැඩි දැඩි වුවා\nනෑනේ වෙනසක් අපේ {typeform.mothers_personality} අම්මා\n\n[Verse 2]\nඅපි කැමතිම කෑමට මුල් තැන දෙන්නා\nරස ගුණ ගලපා සැමවිට බෙලා දුන්නා\nඔබ කැමතිම කෑමත් දැන් අපි දන්නා\nකමුදෝ {typeform.mothers_food} අපි එක්වීලා\n\n[Verse 3]\nහැමදේ ගැන අප හට කියලා දීලා\nටික ටික ඔබේ ජිවිතේ ගෙවිලා ගිහිල්ලා\nකරමුද කැමතිම දේ සමගින් අම්මා\n{typeform.mothers_fun} අපි එක්වීලා"
        tag = style
        title = session_id
        suno_song_id = SunoService().custom_generate(prompt, tag, title)
        SlackService().post_to_slack_webhook(f"Typeform: Added si song to queue (Session ID: {session_id})")
    else:
        # assume sinhala
        prompt = f"[Intro]\nஅன்பான {typeform.mothers_name}\n\n[Verse 1]\nஉயிர் தந்தாள்\nஉதிரம் தந்தாள்\nகருவறையில்\nஇடம் தந்தாள்\nஅம்மா அம்மா\nஎன் {typeform.mothers_personality} அம்மா\n\n[Verse 2]\nஒருவாய் ஊட்ட\nஓடோடி வருவாள்\nபிடித்ததெல்லாம்\nரசித்து செய்வாள்\n{typeform.mothers_food}\nஅவளுக்கு பிடிக்கும்\nஅவள் கைப்பக்குவம்\nஎனக்கும் பிடிக்கும்\n\n[Verse 3]\nவாழ்க்கையை வாழ\nசொல்லி தந்தாள்\nஅனுபவத்தால்\nகற்றுத் தந்தாள்\n{typeform.mothers_fun}\nஅவள் பொழுதுபோக்கு\nஎனக்கும் அதுவே\nபொழுதுபோக்கு"
        tag = style
        title = session_id
        suno_song_id = SunoService().custom_generate(prompt, tag, title)
        SlackService().post_to_slack_webhook(f"Typeform: Added ta song to queue (Session ID: {session_id})")

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