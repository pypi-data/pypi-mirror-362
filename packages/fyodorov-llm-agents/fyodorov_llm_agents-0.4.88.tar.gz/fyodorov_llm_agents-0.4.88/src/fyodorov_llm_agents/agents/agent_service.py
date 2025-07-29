from datetime import datetime
import os
from supabase import Client
import litellm
import requests

from fyodorov_utils.config.supabase import get_supabase
from fyodorov_utils.config.service_discovery import get_service_url
from fyodorov_llm_agents.agents.agent_model import Agent as AgentModel
from fyodorov_llm_agents.tools.mcp_tool_model import MCPTool as ToolModel
from fyodorov_llm_agents.tools.mcp_tool_service import MCPTool as ToolService
from fyodorov_llm_agents.models.llm_service import LLM

supabase: Client = get_supabase()

class Agent(AgentModel):

    def __init__(self, agent: AgentModel):
        super().__init__(
            **agent.to_dict()
        )

    @staticmethod
    async def create_in_db(access_token: str, agent: AgentModel) -> str:
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('agents').upsert(agent.to_dict()).execute()
            agent_id = result.data[0]['id']
            return agent_id
        except Exception as e:
            print('Error creating agent', str(e))
            raise e

    @staticmethod
    async def create_agent_in_db(access_token: str, agent: dict, user_id: str) -> str:
        try:
            supabase = get_supabase(access_token)
            agent['user_id'] = user_id
            result = supabase.table('agents').upsert(agent).execute()
            agent_dict = result.data[0]
            return agent_dict
        except Exception as e:
            print('Error creating agent in db', str(e))
            raise e

    @staticmethod
    async def update_in_db(id: str, agent: dict) -> dict:
        if not id:
            raise ValueError('Agent ID is required')
        try:
            result = supabase.table('agents').update(agent).eq('id', id).execute()
            return result.data[0]
        except Exception as e:
            print('An error occurred while updating agent:', id, str(e))
            raise

    @staticmethod
    async def delete_in_db(id: str) -> bool:
        if not id:
            raise ValueError('Agent ID is required')
        try:
            result = supabase.table('agents').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print('Error deleting agent', str(e))
            raise e

    @staticmethod
    async def get_in_db(id: str) -> AgentModel:
        if not id:
            raise ValueError('Agent ID is required')
        try:
            supabase = get_supabase()
            result = supabase.table('agents').select('*').eq('id', id).limit(1).execute()
            agent_dict = result.data[0]
            print(f"Fetched agent: {agent_dict}")
            model = await LLM.get_model(id = agent_dict["model_id"])
            agent = AgentModel(**agent_dict)
            agent.model = model
            return agent
        except Exception as e:
            print('Error fetching agent', str(e))
            raise e

    @staticmethod
    async def get_all_in_db(limit: int = 10, created_at_lt: datetime = datetime.now(), user_id: str = None) -> list[AgentModel]:
        try:
            supabase = get_supabase()
            if user_id:
                result = supabase.from_('agents') \
                    .select("*") \
                    .eq('user_id', user_id) \
                    .limit(limit) \
                    .lt('created_at', created_at_lt) \
                    .order('created_at', desc=True) \
                    .execute()
            else:
                result = supabase.from_('agents') \
                    .select("*") \
                    .eq('public', True) \
                    .limit(limit) \
                    .lt('created_at', created_at_lt) \
                    .order('created_at', desc=True) \
                    .execute()
            if not result.data:
                return []
            agents = [AgentModel(**agent) for agent in result.data]
            print(f"Fetched agents: {agents}")
            return agents   
        except Exception as e:
            print('Error fetching agents', str(e))
            raise e

    @staticmethod
    async def save_from_dict(access_token: str, user_id: str, agent_dict):
        agent = await AgentModel.from_dict(agent_dict, user_id)
        print('Saving agent', agent)
        agent = await Agent.create_in_db(access_token, agent)
        return agent

    @staticmethod
    async def get_agent_tools(access_token: str, agent_id: str) -> list:
        if not agent_id:
            raise ValueError('Agent ID is required')
        supabase = get_supabase(access_token)
        result = supabase.table('agent_mcp_tools').select('*').eq('agent_id', agent_id).execute()
        tool_ids = [item['mcp_tool_id'] for item in result.data if 'mcp_tool_id' in item]
        result = []
        for tool_id in tool_ids:
            tool = supabase.table('mcp_tools').select('*').eq('id', tool_id).limit(1).execute()
            if tool and tool.data:
                tool_dict = tool.data[0]
                tool_dict['id'] = str(tool_dict['id'])
                result.append(tool_dict)
        return result

    @staticmethod
    async def assign_agent_tools(access_token: str, agent_id: str, tool_ids: list[ToolModel]) -> list:
        if not tool_ids:
            raise ValueError('Agent IDs are required')
        supabase = get_supabase(access_token)
        result = []
        for tool_id in tool_ids:
            # Check if tool is valid and exists in the database
            tool_result = supabase.table('mcp_tools').select('*').eq('id', tool_id).limit(1).execute()
            if not tool_result.data:
                print(f"Tool with ID {tool_id} does not exist.")
                continue
            supabase.table('agent_mcp_tools').insert({'mcp_tool_id': tool_id, 'agent_id': agent_id}).execute()
            print('Inserted tool', tool_id, 'for agent', agent_id)
            result.append(tool_id)
        return result

    @staticmethod
    async def delete_agent_tool_connection(access_token: str, agent_id: str, tool_id: str) -> list:
        if not agent_id:
            raise ValueError('Agent ID is required')
        if not tool_id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('agent_mcp_tools').delete().eq('agent_id', agent_id).eq('mcp_tool_id', tool_id).execute()
            return True
        except Exception as e:
            print('Error deleting agent tool', str(e))
            raise e

    async def call_with_fn_calling(self, input: str = "", history = [], user_id: str = "") -> dict:
        print('call_with_fn_calling')
        litellm.set_verbose = True
        # Set environmental variable
        print(f"[call_with_fn_calling] self.model: {self.model}")
        if self.provider:
            self.api_key = self.provider.api_key
            self.api_url = self.provider.api_url
            if self.provider.name == "gemini":
                model = 'gemini/'+self.model.name
                os.environ["GEMINI_API_KEY"] = self.api_key
        elif self.api_key.startswith('sk-'):
            model = 'openai/'+self.model.name
            os.environ["OPENAI_API_KEY"] = self.api_key
            self.api_url = "https://api.openai.com/v1"
        elif self.api_key and self.api_key != '':
            model = 'mistral/'+self.model.name
            os.environ["MISTRAL_API_KEY"] = self.api_key
            self.api_url = "https://api.mistral.ai/v1"
        else:
            print("Provider Ollama")
            model = 'ollama/'+self.model.name
            if self.api_url is None:
                self.api_url = "https://api.ollama.ai/v1"

        base_url = str(self.api_url).rstrip('/')
        messages: list[dict] = [
            {"content": self.prompt, "role": "system"},
            *history,
            { "content": input, "role": "user"},
        ]
        # tools
        print(f"Tools: {self.tools}")
        mcp_tools = []
        for tool in self.tools:
            try:
                tool_instance = await ToolService.get_by_name_and_user_id(tool, user_id)
                mcp_tools.append(tool_instance)
            except Exception as e:
                print(f"Error fetching tool {tool}: {e}")
        
        tool_schemas = [tool.get_function() for tool in mcp_tools]
        print(f"Tool schemas: {tool_schemas}")
        if tool_schemas:
            print(f"calling litellm with model {model}, messages: {messages}, max_retries: 0, history: {history}, base_url: {base_url}, tools: {tool_schemas}")
            response = litellm.completion(model=model, messages=messages, max_retries=0, base_url=base_url)
        else:     
            print(f"calling litellm with model {model}, messages: {messages}, max_retries: 0, history: {history}, base_url: {base_url}")
            response = litellm.completion(model=model, messages=messages, max_retries=0, base_url=base_url)
        print(f"Response: {response}")

        message = response.choices[0].message

        if hasattr(message, "tool_calls") and message.tool_calls:
            tool_call = message.tool_calls[0]
            fn_name = tool_call.function.name
            args = tool_call.function.arguments

            mcp_tool = mcp_tools.get(fn_name)
            if not mcp_tool:
                raise ValueError(f"Tool '{fn_name}' not found in loaded MCP tools")

            # Forward tool call to Tsiolkovsky instead of calling locally
            tool_output = await self._forward_tool_call_to_tsiolkovsky(
                mcp_tool.id, args, user_session
            )

            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call],
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_output,
            })

            followup = litellm.completion(
                model=model,
                messages=messages,
                max_retries=0,
                base_url=base_url,
            )
            return {"answer": followup.choices[0].message.content}
        
        answer = message.content
        print(f"Answer: {answer}")
        return {
            "answer": answer,
        }
    
    async def _forward_tool_call_to_tsiolkovsky(self, tool_id: str, args: str, user_session: str) -> str:
        """Forward function call to Tsiolkovsky for execution"""
        try:
            tsiolkovsky_url = get_service_url('Tsiolkovsky')
            
            response = await asyncio.to_thread(
                requests.post,
                f"{tsiolkovsky_url}/tools/{tool_id}/call",
                json={"args": args},
                headers={"Authorization": f"Bearer {user_session}"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("result", "")
            else:
                return f"Error calling tool: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error forwarding tool call: {str(e)}"