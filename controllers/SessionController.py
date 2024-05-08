import os
from typing import Tuple
from repositories import SessionRepo
from utils import RequestUtils
from models import SessionModel, TypeformModel

class SessionController:

    session_repo = SessionRepo()

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
        if data == "contact_details":
            session.language = payload.get('language')
            session.first_name = payload.get('first_name')
            session.last_name = payload.get('last_name')
            session.phone_number = payload.get('phone_number')
            # TODO: Save the +94 version of the phone number
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
        return session.song_uploaded and session.video_uploaded
    
    def mark_song_uploaded_session(self, session_id: str) -> bool:
        session: SessionModel = self.session_repo.retrieve(session_id)
        session.song_uploaded = True
        model: SessionModel = self.session_repo.update(session)
        if model == None: return False
        return True

    def mark_video_uploaded_session(self, session_id: str) -> bool:
        session: SessionModel = self.session_repo.retrieve(session_id)
        session.video_uploaded = True
        model: SessionModel = self.session_repo.update(session)
        if model == None: return False
        return True