from dataclasses import asdict
from .Repository import Repository
from models import SessionModel

class SessionRepo(Repository[SessionModel]):
    CONTAINER_NAME = "Coke-AI-songs"
    def __init__(self):
        super().__init__(self.CONTAINER_NAME)
    def parse_item(self, message: dict) -> SessionModel:
        return SessionModel(**message)
    def dump_item(self, message: SessionModel) -> dict:
        return asdict(message)