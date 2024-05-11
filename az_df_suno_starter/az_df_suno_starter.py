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
import asyncio

async def monitor_status(client, instance_id):
    while True:
        status = await client.get_status(instance_id)
        if status.runtime_status in [df.OrchestrationRuntimeStatus.Completed, df.OrchestrationRuntimeStatus.Failed]:
            if status.runtime_status == df.OrchestrationRuntimeStatus.Failed:
                logging.error(f"Orchestration with ID = '{instance_id}' failed")
                SlackService().post_to_slack_webhook(f"Error: Suno Orchestration with ID = '{instance_id}' failed")
            break
        await asyncio.sleep(6)  # wait for 6 seconds before checking the status again

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
        styles = ["rock", "opera", "rap", "K-pop", "romantic samba", "uplifting rap", "futuristic anime", "melodic soul", "smooth house"]
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

        # randomly replace the occurance of the words
        prompt = prompt.replace("ඉතාලි කෑම", random.choice(["ඉතාලි කෑම", "පැස්ටා", "පිට්සා", "ස්පැගෙටි"]))
        prompt = prompt.replace("චීන කෑම", random.choice(["චීන කෑම", "ෆ්‍රයිඩ් රයිස්", "නූඩ්ල්ස්", "සුප්"]))
        prompt = prompt.replace("ශ්‍රී ලංකන් කෑම", random.choice(["ශ්‍රී ලංකන් කෑම", "කොත්තු", "ඉඳිආප්ප", "පොල් රොටි"]))
        prompt = prompt.replace("ඉන්දියානු කෑම", random.choice(["ඉන්දියානු කෑම", "බුරියානි", "බටර් නාන්", "සමෝසා"]))
        prompt = prompt.replace("පැනිරස කෑම", random.choice(["පැනිරස කෑම", "වටලප්පන්", "අයිස් ක්රීම්", "පුඩිං"]))

        prompt = prompt.replace("බලමු ෆිල්ම් එකක්", random.choice(["බලමු ෆිල්ම් එකක්", "හින්දි ෆිල්ම් බලමු", "ඉංග්රීසි ෆිල්ම් බලමු", "කොරියන් ෆිල්ම් බලමු"]))
        prompt = prompt.replace("හදමුද කෑම එකක්", random.choice(["හදමුද කෑම එකක්", "cake එකක් හදමු", "රස කෑමක් හදමු"]))
        prompt = prompt.replace("දාමු ද Walk එකක්", random.choice(["දාමු ද Walk එකක්", "hike ඒකක් යමු", "jog ඒකක් යමු", "walk ඒකක් යමු"]))
        prompt = prompt.replace("හිටවමුද මල් පැළයක් ", random.choice(["හිටවමුද මල් පැළයක්", "මල් පැළයක් හිටවමු"]))
        prompt = prompt.replace("Chat එකක් දාමු ", random.choice(["Chat එකක් දාමු", "කතාවක් කියමු"]))

        
        suno_song_id = SunoService().custom_generate(prompt, tag, title)
        SlackService().post_to_slack_webhook(f"Typeform: Added si song to queue (Session ID: {session_id})")
    else:
        # tamil
        prompt = f"[Intro]\nஅன்பான {typeform.mothers_name}\n\n[Verse 1]\nஉயிர் தந்தாள்\n உதிரம் தந்தாள்\n கருவறையில்\n\nஇடம் தந்தாள்\nஎன் {typeform.mothers_personality}  அம்மா\n அன்பு\n அம்மா\n\n[Verse 2]\nஎனக்கு பிடித்ததெல்லாம்  \nரசித்து ருசித்து செய்வாள்\nகைப்பக்குவத்தால் \nஅறுசுவை ஊட்டுவாள் \n{typeform.mothers_food}\nஅவளுக்கு பிடிக்கும் \nஅவளுக்கு பிடித்ததெல்லாம்\nஎனக்கும் பிடிக்கும்\n\n[Verse 3]\nவாழ்க்கையை வாழ\nவழிகள் சொல்லி தந்தாள்\nஅனுபவத்தால்\n\nகற்றுத் தந்தாள்\n n{typeform.mothers_fun} \n அவளுக்கு பிடிக்கும்\nஅவளுக்கு பிடித்ததெல்லாம் \nஎனக்கும் பிடிக்கும்\n\nஉயிர் தந்தாள்\nஉதிரம் தந்தாள்\nகருவறையில்\nஇடம் தந்தாள்\nஎன் {typeform.mothers_personality} அம்மா\nஅன்பு\nஅம்மா"
        tag = style
        title = session_id
        
        # randomly replace the occurance of the words
        prompt = prompt.replace("இத்தாலிய உணவு", random.choice(["இத்தாலிய உணவு", "பாஸ்தா", "பீட்ஸா", "ஸ்பெகட்டி"]))
        prompt = prompt.replace("சைனீஸ் உணவு", random.choice(["சைனீஸ் உணவு", "பிரைட் ரைஸ்", "நூடில்ஸ்", "சூப்"]))
        prompt = prompt.replace("இலங்கை உணவு", random.choice(["இலங்கை உணவு", "கொத்து", "இடியாப்பம்", "ரொட்டி"]))
        prompt = prompt.replace("இந்தியன் உணவு", random.choice(["இந்தியன் உணவு", "பிரியாணி", "பிட்டு", "இட்லி", "தோசை", "வடை", "சமோசா"]))
        prompt = prompt.replace("இனிப்புகள்", random.choice(["இனிப்புகள்", "ஐஸ்கிரீம்", "புட்டிங்", "வட்டலப்பம்"]))

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

    polling_interval = 5  # seconds
    expiry_time = (datetime.utcnow() + timedelta(minutes=3)).isoformat()

    job = {
        "session_id": session_id,
        "suno_song_id": suno_song_id,
        "pollingInterval": polling_interval,
        "expiryTime": expiry_time
    }
    instance_id = await client.start_new('az_df_suno_orchestrator', f"genai-audio-{suno_song_id}", job)

    logging.info(f"Started GenAI Audio orchestration with ID = '{instance_id}'")

    # Start monitoring the status of the orchestration
    asyncio.create_task(monitor_status(client, instance_id))

    return func.HttpResponse(f"GenAI Audio started with instance ID: {instance_id}", status_code=200)