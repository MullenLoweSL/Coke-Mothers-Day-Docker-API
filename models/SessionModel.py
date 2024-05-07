from dataclasses import dataclass
from .BaseModel import BaseModel
from models.TypeformModel import TypeformModel

@dataclass(init=False)
class SessionModel(BaseModel):

    id: str = None
    ip_address: str = None
    language: str = None
    name: str = None
    first_name: str = None
    last_name: str = None
    phone_number: str = None
    song_uploaded: bool = False
    video_uploaded: bool = False
    typeform_response: TypeformModel = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.ip_address = kwargs.get('ip_address', None)
        self.language = kwargs.get('language', None)
        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)
        self.phone_number = kwargs.get('phone_number', None)
        self.song_uploaded = kwargs.get('song_uploaded', False)
        self.video_uploaded = kwargs.get('video_uploaded', False)
        if kwargs.get('typeform_response'):
            self.typeform_response = TypeformModel(**kwargs.get('typeform_response'))
        else:
            self.typeform_response = None
    
    def to_dto(self):
        # return the object as a dictionary
        return {
            "id": self.id,
            "ip_address": self.ip_address,
            "language": self.language,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "song_uploaded": self.song_uploaded,
            "video_uploaded": self.video_uploaded,
            "typeform_response": self.typeform_response.to_dto() if self.typeform_response else None
        }