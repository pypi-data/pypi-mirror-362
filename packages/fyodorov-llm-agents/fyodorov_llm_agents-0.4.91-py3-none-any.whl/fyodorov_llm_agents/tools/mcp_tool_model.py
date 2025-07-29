from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, Literal
import re
from datetime import datetime
import yaml
import requests
import json

APIUrlTypes = Literal['openapi']

# Example regex for validating textual fields; adjust as needed
VALID_CHARACTERS_REGEX = r'^[a-zA-Z0-9\s.,!?:;\'"\-_]+$'
MAX_NAME_LENGTH = 80
MAX_DESCRIPTION_LENGTH = 1000

class MCPTool(BaseModel):
    """
    Pydantic model corresponding to the 'mcp_tools' table.
    """
    # Database columns
    id: Optional[int] = None                          # bigserial (int8) primary key
    created_at: Optional[datetime] = None             # timestamptz
    updated_at: Optional[datetime] = None             # timestamptz

    name: Optional[str] = Field(..., max_length=MAX_NAME_LENGTH)
    handle: Optional[str] = None
    description: Optional[str] = Field(None, max_length=MAX_DESCRIPTION_LENGTH)
    logo_url: Optional[str] = None                    # stored as text; could be a URL
    user_id: Optional[str] = None                     # uuid

    public: Optional[bool] = False
    api_type: Optional[str] = None
    api_url: Optional[str] = None                     # stored as text; could also be HttpUrl
    auth_method: Optional[str] = None
    auth_info: Optional[Dict[str, Any]] = None        # jsonb
    capabilities: Optional[Dict[str, Any]] = None     # jsonb
    health_status: Optional[str] = None
    usage_notes: Optional[str] = None

    # Fields for launching local tools
    launch_command: Optional[str] = None              # The command to execute (e.g., "npx", "python")
    launch_args: Optional[list[str]] = None           # Arguments for the command (e.g., ["-y", "mcp-remote@latest"])
    launch_working_directory: Optional[str] = None    # Working directory for the command

    # Example validations below. Adjust/extend to fit your needs.

    def validate(self) -> bool:
        """
        Run custom validations on the model fields.
        Returns True if all validations pass, otherwise raises ValueError.
        """
        if self.name:
            self._validate_name(self.name)
        if self.description:
            self._validate_description(self.description)
        # Add more validations as desired...
        return True

    def resource_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
        }

    @staticmethod
    def _validate_name(name: str) -> None:
        if not re.match(VALID_CHARACTERS_REGEX, name):
            raise ValueError("name contains invalid characters.")

    @staticmethod
    def _validate_description(description: str) -> None:
        if not re.match(VALID_CHARACTERS_REGEX, description):
            raise ValueError("description contains invalid characters.")

    @staticmethod
    def from_yaml(yaml_str: str):
        """Instantiate Tool from YAML."""
        if not yaml_str:
            raise ValueError('YAML string is required')
        tool_dict = yaml.safe_load(yaml_str)
        if not isinstance(tool_dict, dict):
            raise ValueError('YAML string must represent a dictionary')
        tool = MCPTool(**tool_dict)
        if not tool.validate():
            print(f"Invalid tool data: {tool_dict}")
            return None
        return tool

    def get_function(self) -> dict:
        """
        Convert this MCP tool into a function definition usable by LLMs (OpenAI-style).
        """
        if not self.capabilities or "functions" not in self.capabilities:
            raise ValueError(f"Tool '{self.name}' is missing `capabilities.functions`")

        # For now: return the first declared capability
        func = self.capabilities["functions"][0]
        return {
            "name": func["name"],
            "description": func.get("description", "No description provided."),
            "parameters": func.get("parameters", {}),
        }

    def call(self, args: dict) -> str:
        if not self.api_url:
            raise ValueError("MCP tool is missing an `api_url`")

        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Fyodorov-Agent/1.0",
        }

        # Handle authentication
        if self.auth_method == "bearer":
            token = self.auth_info.get("token")
            if not token:
                raise ValueError("Bearer token required but not provided in `auth_info`")
            headers["Authorization"] = f"Bearer {token}"
        elif self.auth_method == "basic":
            user = self.auth_info.get("username")
            pwd = self.auth_info.get("password")
            if not user or not pwd:
                raise ValueError("Basic auth requires `username` and `password` in `auth_info`")
            auth = (user, pwd)
        else:
            auth = None  # anonymous access

        try:
            print(f"Calling MCP tool at {self.api_url} with args: {args}")
            response = requests.post(self.api_url, json=args, headers=headers, auth=auth)
            response.raise_for_status()
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                return json.dumps(response.json(), indent=2)
            return response.text
        except requests.RequestException as e:
            print(f"Error calling MCP tool: {e}")
            return f"Error calling tool: {e}"


    def to_dict(self) -> dict:
        """
        Convert this Pydantic model to a plain dict (e.g., for inserting into Supabase).
        """
        return self.dict(exclude_none=True)
