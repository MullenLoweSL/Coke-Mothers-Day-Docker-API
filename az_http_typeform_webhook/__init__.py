import logging
import json
import azure.functions as func
from models.TypeformModel import TypeformModel
from controllers.SessionController import SessionController

# def format_list(my_list):
#     if len(my_list) > 1:
#         return ', '.join(my_list[:-1]) + ' and ' + my_list[-1]
#     elif my_list:
#         return my_list[0]
#     else:
#         return ''

handler = SessionController()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    req_body = req.get_json()

    session_id = req_body["form_response"]["hidden"]["session_id"]
    mothers_name = req_body["form_response"]["answers"][0]["text"]
    mothers_food = req_body["form_response"]["answers"][1]["choice"]["label"]
    mothers_lifestyle = req_body["form_response"]["answers"][2]["choice"]["label"]
    mothers_music = req_body["form_response"]["answers"][3]["choice"]["label"]

    typeform_args = {
        "session_id": session_id,
        "mothers_name": mothers_name,
        "mothers_food": mothers_food,
        "mothers_lifestyle": mothers_lifestyle,
        "mothers_music": mothers_music
    }
    typeform_response = TypeformModel(**typeform_args)

    return handler.save_typeform_results(session_id, typeform_response)

    # prompt = "[Verse 1]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ\n\n[Verse 2]\nයමන් බණ්ඩො වෙසක් බලන්ඩ\nගනින් බර බාගේ බඳින්ඩ\nපාර දිගේ එළි බල බල\nමහ පාරේ හරි කලබල‍\nයමන් බණ්ඩො වෙසක් බලන්ඩ"
    # tag = "Rock, with electric guitar"
    # title = "Enjoy Life"
    # suno_song_id = SunoService().custom_generate(prompt, tag, title)
    # return func.HttpResponse(json.dumps({"id": suno_song_id}), status_code=200, mimetype="application/json")


    # return func.HttpResponse(json.dumps({"output_path": "output_path"}), status_code=200, mimetype="application/json")