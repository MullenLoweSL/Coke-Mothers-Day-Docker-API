import os
from typing import Tuple
from repositories import SessionRepo
from utils import RequestUtils
from models import SessionModel

class SessionController:

    session_repo = SessionRepo()

    # @RequestUtils.api_response
    # def update_session(self, id: str, payload: dict) -> Tuple[int, dict]:
    #     session_model: SessionModel
    #     session_model = self.result_repo.retrieve(id)
    #     if session_model == None:
    #         return (404, {'error': 'Session not found'})
        
    #     session_model.first_name = payload.get('first_name')
    #     session_model.last_name= payload.get('last_name')
    #     session_model.phone_number = payload.get('phone_number')

    #     return (200, {
    #         "success": True
    #     })

    @RequestUtils.api_response
    def post_session(self, session_model: SessionModel) -> Tuple[int, dict]:
        result: SessionModel = self.session_repo.update(session_model)
        if result == None: return (404, {'error': 'Could not create result'})

        return (200, {
            "id": result.id
        })
    
    @RequestUtils.api_response
    def patch_session(self, session_id: str, data: str, payload: dict) -> Tuple[int, dict]:
        session: SessionModel = self.session_repo.retrieve(session_id)
        if data == "language":
            session.language = payload.get('language')
        elif data == "contact_details":
            session.first_name = payload.get('first_name')
            session.last_name = payload.get('last_name')
            session.phone_number = payload.get('phone_number')
            # TODO: Save the +94 version of the phone number
        else:
            return (400, {
                "error": f"Unknown data requested for PATCH: {data}"
            })  

        model: SessionController = self.session_repo.update(session)
        if model == None: return (404, {'error': 'Could not update session'})

        return (200, {
            "id": session.to_dto()
        })