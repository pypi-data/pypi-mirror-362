from datetime import datetime
from .provider_model import ProviderModel
from supabase import Client
from fyodorov_utils.config.supabase import get_supabase

supabase: Client = get_supabase()


class Provider(ProviderModel):

    @staticmethod
    async def update_provider_in_db(id: str, update: dict) -> dict:
        if not id:
            raise ValueError('Provider ID is required')
        try:
            result = supabase.table('providers').update(update).eq('id', id).execute()
            update = result.data[0]
            print('Updated provider:', update)
            return update
        except Exception as e:
            print(f"Error updating provider with id {id} "
                  f"and update {update} ")
            raise e

    @staticmethod
    async def save_provider_in_db(access_token: str, provider: ProviderModel, user_id: str) -> dict:
        try:
            print('Access token for saving provider:', access_token)
            supabase = get_supabase(access_token)
            provider.name = provider.name.lower()
            if not provider.api_url or provider.api_url == "":
                if provider.name == "openai":
                    provider.api_url = "https://api.openai.com/v1"
                elif provider.name == "mistral":
                    provider.api_url = "https://api.mistral.ai/v1"
                elif provider.name == "ollama":
                    provider.api_url = "http://localhost:11434/v1"
                elif provider.name == "openrouter":
                    provider.api_url = "https://openrouter.ai/api/v1"
                elif provider.name == "gemini" or provider.name == "google":
                    provider.api_url = "https://generativelanguage.googleapis.com/v1beta/models/"
                else:
                    raise ValueError('No URL provided when creating a provider')
            print('Setting provider api_url to', provider.api_url)
            provider_dict = provider.to_dict()
            provider_dict['user_id'] = user_id
            print('Provider dict before merging existing row:', provider_dict)
            # Check if the provider already exists based on name and user_id
            existing_provider = await Provider.get_provider(access_token, user_id, provider.name)
            if existing_provider:
                tmp = {**existing_provider.to_dict(), **provider_dict}
                provider_dict = tmp
            print('Saving provider', provider_dict)
            result = supabase.table('providers').upsert(provider_dict).execute()
            provider = result.data[0]
            print('Saved provider', provider)
            return provider
        except Exception as e:
            print('Error saving provider', str(e))
            if e.code == '23505':
                print('Provider already exists')
                return provider
            raise e

    @staticmethod
    async def delete_provider_in_db(id) -> bool:
        if not id:
            raise ValueError('Provider ID is required')
        try:
            result = supabase.table('providers').delete().eq('id', id).execute()
            return True
        except Exception as e:
            print('Error deleting provider', str(e))
            raise e

    @staticmethod
    async def get_provider_by_id(id: str) -> ProviderModel:
        if not id:
            raise ValueError('Provider ID is required')
        try:
            supabase = get_supabase()
            result = supabase.table('providers').select('*').eq('id', id).limit(1).execute()
            provider_dict = result.data[0]
            print('[get_provider_by_id] Fetched provider', provider_dict)
            provider_dict['id'] = str(provider_dict['id'])
            provider = ProviderModel(**provider_dict)
            return provider
        except Exception as e:
            print('Error fetching provider', str(e))
            raise e

    @staticmethod
    async def get_provider(access_token: str, user_id: str, name: str) -> ProviderModel:
        print(f"Getting provider with name: {name} and user_id: {user_id}")
        if not name:
            raise ValueError('Provider name is required')
        if not user_id:
            raise ValueError('User ID is required')
        try:
            supabase = get_supabase(access_token)
            print('Got access token for getting provider:', access_token)
            result = supabase.table('providers').select('*')\
                .eq('user_id', user_id)\
                .eq('name', name.lower())\
                .limit(1).execute()
            print('Result of getting provider:', result)
            if not result or not result.data or len(result.data) == 0:
                print('Provider not found')
                return None
            provider_dict = result.data[0]
            print('[get_provider] Fetched provider', provider_dict)
            provider_dict['id'] = str(provider_dict['id'])
            provider = ProviderModel(**provider_dict)
            return provider
        except Exception as e:
            print('Error fetching provider', str(e))
            raise e

    @staticmethod
    async def get_or_create_provider(access_token: str, user_id: str, name: str) -> ProviderModel:
        try:
            provider = await Provider.get_provider(access_token, user_id, name)
            return provider
        except Exception as e:            
            provider = ProviderModel(name=name.lower())
            provider = await Provider.save_provider_in_db(access_token, provider, user_id)
            return provider

    @staticmethod
    async def get_providers(limit: int = 10, created_at_lt: datetime = datetime.now(), user_id: str = None) -> list[dict]:
        try:
            if user_id:
                print(f"Fetching providers for user_id: {user_id} with limit: {limit} and created_at_lt: {created_at_lt}")
                result = supabase.table('providers') \
                            .select('*') \
                            .eq('user_id', user_id) \
                            .order('created_at', desc=True) \
                            .limit(limit) \
                            .lt('created_at', created_at_lt) \
                            .execute()
                data = result.data
            else:
                result = supabase.table('providers') \
                            .select('*') \
                            .order('created_at', desc=True) \
                            .limit(limit) \
                            .lt('created_at', created_at_lt) \
                            .execute()
                data = result.data
            providers = [ProviderModel(**provider) for provider in data]
            print('Fetched providers', providers)
            return providers
        except Exception as e:
            print('Error fetching providers', str(e))
            raise e
