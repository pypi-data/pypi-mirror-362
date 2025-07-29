from pydantic import BaseModel, HttpUrl, Field
import re

MAX_TITLE_LENGTH = 80
VALID_CHARACTERS_REGEX = r'^[a-zA-Z0-9\s.,!?:;\'"-]+$'

class InstanceModel(BaseModel):
    id: int = Field(None, alias='id')
    agent_id: int # Links to AgentModel.id
    title: str = ""
    chat_history: list[dict] = []

    def validate(self) -> bool:
        try:
            InstanceModel.validate_title(self.title)
        except ValueError as e:
            print("Instance model validation error:", e)
            return False
        else:
            return True
        
    def resource_dict(self) -> dict:
        return {
            'id': self.id,
            'agent_id': self.agent_id,
            'title': self.title,
        }

    def to_dict(self) -> dict:
        data = {
            'agent_id': self.agent_id,
            'title': self.title,
            'chat_history': self.chat_history,
        }
        if self.id is not None:
            data['id'] = self.id
        return data

    @staticmethod
    def validate_title(title: str) -> str:
        if not title:
            raise ValueError('Title is required')
        if len(title) > MAX_TITLE_LENGTH:
            raise ValueError('Title exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, title):
            raise ValueError('Title contains invalid characters')
        return title