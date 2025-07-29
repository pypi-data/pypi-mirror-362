from datetime import datetime
import json
from typing import Any, Optional

import requests
from fyodorov_utils.config.supabase import get_supabase
from .mcp_tool_model import MCPTool as ToolModel


class MCPTool():

    @staticmethod
    async def create_or_update_in_db(access_token: str, tool: ToolModel, user_id: str) -> ToolModel:
        print(f"Creating or updating tool with handle {tool.handle} for user {user_id}")
        tool_w_id = await MCPTool.get_by_name_and_user_id(access_token, tool.handle, user_id)
        if tool_w_id:
            print(f"Tool with handle {tool.handle} already exists, updating it.")
            return await MCPTool.update_in_db(access_token, tool_w_id.id, tool)
        else:
            print(f"Tool with handle {tool.handle} does not exist, creating it.")
            return await MCPTool.create_in_db(access_token, tool, user_id)

    @staticmethod    
    async def create_in_db(access_token: str, tool: ToolModel, user_id: str) -> ToolModel:
        try:
            supabase = get_supabase(access_token)
            tool_dict = tool.to_dict()
            tool_dict['user_id'] = user_id
            if 'id' in tool_dict:
                del tool_dict['id']
            if 'created_at' in tool_dict:
                del tool_dict['created_at']
            if 'updated_at' in tool_dict:
                del tool_dict['updated_at']
            print('creating tool in db', tool_dict)
            result = supabase.table('mcp_tools').insert(tool_dict).execute()
            print('created tool in db', result)
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('Error creating tool', str(e))
            raise e

    @staticmethod
    async def update_in_db(access_token: str, id: str, tool: ToolModel) -> ToolModel:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            tool_dict = tool.to_dict()
            print('updating tool in db', tool_dict)
            result = supabase.table('mcp_tools').update(tool_dict).eq('id', id).execute()
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('An error occurred while updating tool:', id, str(e))
            raise

    @staticmethod
    async def delete_in_db(access_token: str, id: str) -> bool:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            print(f"Deleting tool with ID {id}")
            result = supabase.table('mcp_tools').delete().eq('id', id).execute()
            print('Deleted tool', result)
            return True
        except Exception as e:
            print('Error deleting tool', str(e))
            raise e

    @staticmethod
    async def get_in_db(access_token: str, id: str) -> ToolModel:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('mcp_tools').select('*').eq('id', id).limit(1).execute()
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    async def get_by_name_and_user_id(access_token: str, handle: str, user_id: str) -> ToolModel:
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('mcp_tools').select('*').eq('user_id', user_id).eq('handle', handle).limit(1).execute()
            if not result or not result.data or len(result.data) == 0: # If no tools found for this user check for public tools with same name
                print(f"No tool found with the given handle {handle} and user ID {user_id}: {result}")
                result = supabase.table('mcp_tools').select('*').eq('handle', handle).eq('public', True).limit(1).execute()
            if not result or not result.data or len(result.data) == 0:
                print(f"No public tool found with the given handle {handle}: {result}")
                return None
            tool_dict = result.data[0]
            tool = ToolModel(**tool_dict)
            return tool
        except Exception as e:
            print('Error fetching tool', str(e))
            raise e

    @staticmethod
    async def get_all_in_db(limit: int = 10, created_at_lt: datetime = datetime.now(), user_id: str = None) -> list[ToolModel]:
        try:
            supabase = get_supabase()
            print('getting tools from db for user', user_id)
            tools = []
            if user_id:
                result = supabase.from_('mcp_tools') \
                    .select("*") \
                    .eq('user_id', user_id) \
                    .limit(limit) \
                    .lt('created_at', created_at_lt) \
                    .order('created_at', desc=True) \
                    .execute()
            else:
                result = supabase.from_('mcp_tools') \
                    .select("*") \
                    .limit(limit) \
                    .lt('created_at', created_at_lt) \
                    .order('created_at', desc=True) \
                    .execute()
            for tool in result.data:
                tool["id"] = str(tool["id"])
                tool["user_id"] = str(tool["user_id"])
                tool["created_at"] = str(tool["created_at"])
                tool["updated_at"] = str(tool["updated_at"])
                if tool and (tool['public'] or (user_id and 'user_id' in tool and tool['user_id'] == user_id)):
                    print('tool is public or belongs to user', tool)
                    tool_model = ToolModel(**tool)
                    if tool_model.validate():
                        tools.append(tool_model)
                    else:
                        print(f"Invalid tool data: {tool}")
            print(f"got {len(tools)} tools from db")
            return tools
        except Exception as e:
            print('Error fetching tools', str(e))
            raise e

    @staticmethod
    async def get_tool_agents(access_token: str, id: str) -> list[int]:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            result = supabase.table('agent_mcp_tool').select('*').eq('mcp_tool_id', id).execute()
            tool_agents = [item['agent_id'] for item in result.data if 'agent_id' in item]
            return tool_agents
        except Exception as e:
            print('Error fetching tool agents', str(e))
            raise

    @staticmethod
    async def set_tool_agents(access_token: str, id: str, agent_ids: list[int]) -> list[int]:
        if not id:
            raise ValueError('Tool ID is required')
        try:
            supabase = get_supabase(access_token)
            for agent_id in agent_ids:
                # Check if agent is valid and exists in the database
                agent_result = supabase.table('agents').select('*').eq('id', agent_id).limit(1).execute()
                if not agent_result.data:
                    print(f"Agent with ID {agent_id} does not exist.")
                    continue
                # Insert the agent-tool relationship
                supabase.table('agent_mcp_tool').insert({'mcp_tool_id': id, 'agent_id': agent_id}).execute()
            print('Inserted tool agents', agent_ids)
            return agent_ids
        except Exception as e:
            print('Error setting tool agents', str(e))
            raise e

    @staticmethod
    async def call_mcp_server(id: str, access_token: Optional[str] = None, args: Optional[dict[str, Any]] = None) -> str:
        """Invoke an MCP tool via the tool's configured MCP server."""
        if not id:
            raise ValueError('Tool ID is required')
        tool = await MCPTool.get_in_db(access_token, id)
        if not tool:
            raise ValueError('Tool not found')
        if not tool.handle:
            raise ValueError('Tool handle is required')
        if not tool.api_url:
            raise ValueError('Tool api_url is required')

        url = f"{tool.api_url}:call"
        headers = {'Content-Type': 'application/json'}
        if access_token:
            headers['Authorization'] = f'Bearer {access_token}'
        if args is None:
            args = {}

        try:
            print(f"Calling MCP server at {url} with args {args}")
            response = requests.post(url, headers=headers, json=args, timeout=30)
            response.raise_for_status()
            content_type = response.headers.get('Content-Type', '')
            if 'application/json' in content_type:
                return json.dumps(response.json())
            return response.text
        except requests.RequestException as e:
            print('Error calling MCP server', str(e))
            raise e
