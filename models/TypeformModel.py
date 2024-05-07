from dataclasses import dataclass
from .BaseModel import BaseModel

@dataclass(init=False)
class TypeformModel(BaseModel):

    session_id: str = None
    mothers_name: str = None
    mothers_food: str = None
    mothers_lifestyle: str = None
    mothers_music: str = None

    def __init__(self, **kwargs):
        self.session_id = kwargs.get('session_id', None)
        self.mothers_name = kwargs.get('mothers_name', None)
        self.mothers_food = kwargs.get('mothers_food', None)
        self.mothers_lifestyle = kwargs.get('mothers_lifestyle', None)
        self.mothers_music = kwargs.get('mothers_music', None)
    
    def to_dto(self):
        # return the object as a dictionary
        return {
            "session_id": self.session_id,
            "mothers_name": self.mothers_name,
            "mothers_food": self.mothers_food,
            "mothers_lifestyle": self.mothers_lifestyle,
            "mothers_music": self.mothers_music
        }