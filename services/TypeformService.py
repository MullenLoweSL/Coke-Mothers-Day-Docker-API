from .Singleton import Singleton
from models.TypeformModel import TypeformModel

class TypeformService(metaclass=Singleton):

    def __init__(self):
        pass

    def convert_webhook_to_typeform(self, typeform_webhook: dict) -> TypeformModel:

        typeform_id = typeform_webhook["form_response"]["form_id"]
        if typeform_id == "oV7MdGlt":
            language = "en"
        elif typeform_id == "CLqDRGST":
            language = "si"
        elif typeform_id == "EdPYTm6s":
            language = "ta"
        else:
            language = "en"

        session_id = typeform_webhook["form_response"]["hidden"]["session_id"]
        mothers_name = typeform_webhook["form_response"]["answers"][0]["text"]
        mothers_food = typeform_webhook["form_response"]["answers"][1]["choice"]["label"]
        mothers_personality = typeform_webhook["form_response"]["answers"][2]["choice"]["label"]
        mothers_fun = typeform_webhook["form_response"]["answers"][3]["choice"]["label"]
        mothers_music = typeform_webhook["form_response"]["answers"][4]["choice"]["label"]

        typeform_args = {
            "session_id": session_id,
            "language": language,
            "mothers_name": mothers_name,
            "mothers_food": mothers_food,
            "mothers_personality": mothers_personality,
            "mothers_fun": mothers_fun,
            "mothers_music": mothers_music
        }
        return TypeformModel(**typeform_args)
