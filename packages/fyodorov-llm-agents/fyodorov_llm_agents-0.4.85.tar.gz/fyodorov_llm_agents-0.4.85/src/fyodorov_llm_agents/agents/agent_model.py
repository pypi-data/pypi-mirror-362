import re
import requests
import yaml
from pydantic import BaseModel, HttpUrl
from typing import Optional
from fyodorov_llm_agents.models.llm_model import LLMModel
from fyodorov_llm_agents.models.llm_service import LLM
from fyodorov_llm_agents.providers.provider_model import ProviderModel
from datetime import datetime

MAX_NAME_LENGTH = 80
MAX_DESCRIPTION_LENGTH = 280
VALID_CHARACTERS_REGEX = r'^[a-zA-Z0-9\s.,!?:;\'"-_]+$'

class Agent(BaseModel):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    api_key: str | None = None
    api_url: HttpUrl | None = None
    tools: list[str] = []
    rag: list[dict] = []
    model: LLMModel | None = None
    provider: ProviderModel | None = None
    name: str = "My Agent"
    description: str = "My Agent Description"
    prompt: str = "My Prompt"
    prompt_size: int = 10000
    public: bool | None = False

    class Config:
        arbitrary_types_allowed = True

    def validate(self):
        Agent.validate_name(self.name)
        Agent.validate_description(self.description)
        Agent.validate_prompt(self.prompt, self.prompt_size)

    def resource_dict(self) -> dict:
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'description': self.description,
        }

    @staticmethod
    def validate_name(name: str) -> str:
        if not name:
            raise ValueError('Name is required')
        if len(name) > MAX_NAME_LENGTH:
            raise ValueError('Name exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, name):
            raise ValueError('Name contains invalid characters')
        return name

    @staticmethod
    def validate_description(description: str) -> str:
        if not description:
            raise ValueError('Description is required')
        if len(description) > MAX_DESCRIPTION_LENGTH:
            raise ValueError('Description exceeds maximum length')
        if not re.match(VALID_CHARACTERS_REGEX, description):
            raise ValueError('Description contains invalid characters')
        return description

    @staticmethod
    def validate_prompt(prompt: str, prompt_size: int) -> str:
        if not prompt:
            raise ValueError('Prompt is required')
        if len(prompt) > prompt_size:
            raise ValueError('Prompt exceeds maximum length')
        return prompt

    def to_dict(self) -> dict:
        agent = self.dict(exclude_none=True)
        del agent['model'] # to avoid problems when saving to db
        if self.model:
            agent['model_id'] = self.model.id
        return agent
        # return {
        #     'model': self.model,
        #     'name': self.name,
        #     'description': self.description,
        #     'prompt': self.prompt,
        #     'prompt_size': self.prompt_size,
        #     'tools': self.tools,
        #     'rag': self.rag,
        # }


    @staticmethod
    def call_api(url: str = "", method: str = "GET", body: dict = {}) -> dict:
        if not url:
            raise ValueError('API URL is required')
        try:
            res = requests.request(
                method=method,
                url=url,
                json=body,
            )
            if res.status_code != 200:
                raise ValueError(f"Error fetching API json from {url}: {res.status_code}")
            json = res.json()
            return json
        except Exception as e:
            print(f"Error calling API: {e}")
            raise

    @staticmethod
    def from_yaml(yaml_str: str):
        """Instantiate Agent from YAML."""
        if not yaml_str:
            raise ValueError('YAML string is required')
        agent_dict = yaml.safe_load(yaml_str)
        agent = Agent(**agent_dict)
        agent.validate()
        return agent

    @staticmethod
    async def from_dict(agent_dict: dict, user_id: str = None):
        """Instantiate Agent from dict."""
        if not agent_dict:
            raise ValueError('Agent dict is required')
        if 'model' in agent_dict and isinstance(agent_dict['model'], str):
            model = await LLM.get_model(user_id, agent_dict['model'])
            if model is None:
                model = await LLM.save_model_in_db(
                    access_token=None,  # Assuming no access token needed for this operation
                    user_id=user_id,
                    model_dict = LLMModel.from_dict(agent_dict['model'])
                )
            else:
                model_dict = model.to_dict()
            agent_dict['model'] = model_dict
            agent_dict['model_id'] = model.id
        agent = Agent(**agent_dict)
        agent.validate()
        return agent
