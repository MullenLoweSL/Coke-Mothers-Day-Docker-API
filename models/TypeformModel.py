from dataclasses import dataclass
from .BaseModel import BaseModel

@dataclass(init=False)
class TypeformModel(BaseModel):

    session_id: str = None
    language: str = None
    mothers_name: str = None
    mothers_food: str = None
    mothers_personality: str = None
    mothers_fun: str = None
    mothers_music: str = None

    def __init__(self, **kwargs):
        self.session_id = kwargs.get('session_id', None)
        self.language = kwargs.get('language', None)
        self.mothers_name = kwargs.get('mothers_name', None)
        self.mothers_food = kwargs.get('mothers_food', None)
        self.mothers_personality = kwargs.get('mothers_personality', None)
        self.mothers_fun = kwargs.get('mothers_fun', None)
        self.mothers_music = kwargs.get('mothers_music', None)
    
    def get_render_string(self):
        # return a string with all info in the object
        return f"Language: *{self.language or ''}*. Mother's name: *{self.mothers_name or ''}*, food: *{self.mothers_food or ''}*, personality: *{self.mothers_personality or ''}*, hobby: *{self.mothers_fun or ''}*, music: *{self.mothers_music or ''}*"

    def to_dto(self):
        # return the object as a dictionary
        return {
            "session_id": self.session_id,
            "language": self.language,
            "mothers_name": self.mothers_name,
            "mothers_food": self.mothers_food,
            "mothers_personality": self.mothers_personality,
            "mothers_fun": self.mothers_fun,
            "mothers_music": self.mothers_music
        }