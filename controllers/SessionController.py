import os
from typing import Tuple
from repositories import SessionRepo
from utils import RequestUtils
from models import SessionModel, TypeformModel

class SessionController:

    session_repo = SessionRepo()

    def parse_phone_number(self, phone_number):
        if len(phone_number) == 12 and phone_number.startswith('+947'):
            return phone_number[1:]
        elif len(phone_number) == 10 and phone_number.startswith('07'):
            return '94' + phone_number[1:]
        elif len(phone_number) == 11 and phone_number.startswith('947'):
            return phone_number
        else:
            raise ValueError("Invalid phone number format")
    
    @RequestUtils.api_response
    def post_session(self, session_model: SessionModel) -> Tuple[int, dict]:
        result: SessionModel = self.session_repo.update(session_model)
        if result == None: return (404, {'error': 'Could not create result'})

        return (200, {
            "id": result.id
        })
    
    @RequestUtils.api_response
    def save_typeform_results(self, session_id: str, typeform: TypeformModel) -> Tuple[int, dict]:
        session: SessionModel = self.session_repo.retrieve(session_id)
        session.typeform_response = typeform
        model: SessionController = self.session_repo.update(session)
        if model == None: return (404, {'error': 'Could not update session'})
        return (200, {
            "result": session.to_dto()
        })

    @RequestUtils.api_response
    def patch_session(self, session_id: str, data: str, payload: dict) -> Tuple[int, dict]:
        session: SessionModel = self.session_repo.retrieve(session_id)

        phone_number = payload.get('phone_number')
        parsed_phone_number = self.parse_phone_number(phone_number)
        # user's phone will always be in one of these three forms:
        # +94777123456 (12 chars, starting with +947)
        # 94777123456 (11 chars, starting with 947)
        # 0777123456 (10 chars, starting with 07)
        # give me a parsed string, that always looks like: 94777123456


        if data == "contact_details":
            session.language = payload.get('language')
            session.first_name = payload.get('first_name')
            session.last_name = payload.get('last_name')
            session.phone_number = parsed_phone_number
        elif data == "photo":
            return (200, {
                "result": session.to_dto()
            })
        else:
            return (400, {
                "error": f"Unknown data requested for PATCH: {data}"
            })  

        model: SessionModel = self.session_repo.update(session)
        if model == None: return (404, {'error': 'Could not update session'})

        return (200, {
            "result": session.to_dto()
        })
    
    def is_session_completed(self, session_id: str) -> bool:
        session: SessionModel = self.session_repo.retrieve(session_id)
        return session.song_created and session.image_uploaded
    
    def get_suno_song_id(self, session_id: str) -> str:
        session: SessionModel = self.session_repo.retrieve(session_id)
        return session.suno_song_id
    
    def mark_song_song_created(self, session_id: str, suno_song_id: str) -> bool:
        session: SessionModel = self.session_repo.retrieve(session_id)
        session.song_created = True
        session.suno_song_id = suno_song_id
        model: SessionModel = self.session_repo.update(session)
        if model == None: return False
        return True

    def mark_image_uploaded(self, session_id: str) -> bool:
        session: SessionModel = self.session_repo.retrieve(session_id)
        session.image_uploaded = True
        model: SessionModel = self.session_repo.update(session)
        if model == None: return False
        return True