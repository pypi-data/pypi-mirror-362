from datetime import datetime
from supabase import Client
from fyodorov_utils.config.supabase import get_supabase
from fyodorov_llm_agents.providers.provider_service import Provider
from fyodorov_llm_agents.models.llm_model import LLMModel

supabase: Client = get_supabase()

class LLM(LLMModel):

    @staticmethod
    async def update_model_in_db(access_token: str, user_id: str, name: str, update: dict) -> dict:
        if not user_id or not name:
            raise ValueError('Model name and User ID is required')
        try:
            result = supabase.table('models').update(update).eq('user_id', user_id).eq('name', name).execute()
            update = result.data[0]
            print('Updated model:', update)
            return update
        except Exception as e:
            print(f"Error updating model with user_id {user_id} and name {name} "
                  f"and update {update} ")
            raise e

    @staticmethod
    async def save_model_in_db(access_token: str, user_id: str, model: LLMModel) -> dict:
        try:
            supabase = get_supabase(access_token)
            provider = await Provider.get_or_create_provider(access_token, user_id, model.provider)
            model_dict = model.to_dict()
            model_dict['provider'] = provider.id
            model_dict['user_id'] = user_id
            result = supabase.table('models').upsert(model_dict).execute()
            model_dict = result.data[0]
            return model_dict
        except Exception as e:
            print('Error saving model', str(e))
            raise e

    @staticmethod
    async def delete_model_in_db(access_token: str, user_id: str, name: str, id: str) -> bool:
        try:
            supabase = get_supabase(access_token)
            if id:
                result = supabase.table('models').delete().eq('id', id).execute()
            elif user_id and name:
                result = supabase.table('models').delete().eq('user_id', user_id).eq('name', name).execute()
            else:
                raise ValueError('Some form of id is required to delete a model')
            print('Deleted model', result.data)
            return True
        except Exception as e:
            print('Error deleting model', str(e))
            raise e

    @staticmethod
    async def get_model(user_id: str = None, name: str = None, id: int = None) -> LLMModel:
        try:
            supabase = get_supabase()
            if id:
                print(f"Getting model with id: {id}")
                result = supabase.table('models').select('*').eq('id', str(id)).execute()
            elif user_id and name:
                print(f"Getting model with name: {name} and user_id: {user_id}")
                result = supabase.table('models').select('*').eq('user_id', user_id).eq('name', name).execute()
            else:
                raise ValueError('Some form of id is required to retrieve a model')
            print('Fetched model', result)
            if not result or not result.data:
                return None
            model_dict = result.data[0]
            model_dict['id'] = str(model_dict['id'])
            model_dict['provider'] = str(model_dict['provider'])
            model = LLMModel(**model_dict)
            return model
        except Exception as e:
            print('Error fetching model from db', str(e))
            raise e

    @staticmethod
    async def get_models(limit: int = 10, created_at_lt: datetime = datetime.now(), user_id: str = None) -> list[LLMModel]:
        try:
            if user_id:
                result = supabase.table('models') \
                            .select('*') \
                            .eq('user_id', user_id) \
                            .order('created_at', desc=True) \
                            .limit(limit) \
                            .lt('created_at', created_at_lt) \
                            .execute()
                data = result.data
            else:
                result = supabase.table('models') \
                            .select('*') \
                            .order('created_at', desc=True) \
                            .limit(limit) \
                            .lt('created_at', created_at_lt) \
                            .execute()
                data = result.data
            if not data:
                print("No models found")
                return []
            for model in data:
                if 'provider' in model and type(model['provider']) is int:
                    model['provider_id'] = model['provider']
                    del model['provider']
            models = [LLMModel(**model) for model in data]
            print('Fetched models', models)
            return models
        except Exception as e:
            print('Error fetching models', str(e))
            raise e
