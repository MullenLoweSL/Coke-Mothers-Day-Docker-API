import logging
import json
import azure.functions as func
from services.SunoService import SunoService

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    prompt = "[Verse 1]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ\n\n[Verse 2]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ"
    tag = "Rock, with electric guitar"
    title = "Enjoy Life"
    suno_song_id = SunoService().custom_generate(prompt, tag, title)
    return func.HttpResponse(json.dumps({"id": suno_song_id}), status_code=200, mimetype="application/json")