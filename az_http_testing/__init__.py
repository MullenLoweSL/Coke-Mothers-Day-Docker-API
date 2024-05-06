import logging
import json
import azure.functions as func
from services.SunoService import SunoService
from services.ffmpegService import ffmpegService

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    # prompt = "[Verse 1]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ\n\n[Verse 2]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ"
    # tag = "Rock, with electric guitar"
    # title = "Enjoy Life"
    # suno_song_id = SunoService().custom_generate(prompt, tag, title)
    # return func.HttpResponse(json.dumps({"id": suno_song_id}), status_code=200, mimetype="application/json")


    mp3_path = "/Users/sohan/Desktop/Coke/test/sample.mp3"
    png_path = "/Users/sohan/Desktop/Coke/test/cover.png"
    output_path = "/Users/sohan/Desktop/Coke/test/output.mp4"
    result = ffmpegService().generate_mp4(mp3_path, png_path, output_path)
    return func.HttpResponse(json.dumps({"output_path": output_path}), status_code=200, mimetype="application/json")