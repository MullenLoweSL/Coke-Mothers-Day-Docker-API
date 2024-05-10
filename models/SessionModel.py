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
    song_created: bool = False
    suno_song_id: str = None
    image_uploaded: bool = False
    sms_sent: bool = False
    typeform_response: TypeformModel = None

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.ip_address = kwargs.get('ip_address', None)
        self.language = kwargs.get('language', None)
        self.first_name = kwargs.get('first_name', None)
        self.last_name = kwargs.get('last_name', None)
        self.phone_number = kwargs.get('phone_number', None)
        self.song_created = kwargs.get('song_created', False)
        self.suno_song_id = kwargs.get('suno_song_id', False)
        self.image_uploaded = kwargs.get('image_uploaded', False)
        self.sms_sent = kwargs.get('sms_sent', False)
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
            "song_created": self.song_created,
            "suno_song_id": self.suno_song_id,
            "image_uploaded": self.image_uploaded,
            "sms_sent": self.sms_sent,
            "typeform_response": self.typeform_response.to_dto() if self.typeform_response else None
        }