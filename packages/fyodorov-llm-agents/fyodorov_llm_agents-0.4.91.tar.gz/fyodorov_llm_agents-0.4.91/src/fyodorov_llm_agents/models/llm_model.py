from pydantic import BaseModel

class LLMModel(BaseModel):
    id: int | None = None
    name: str
    provider: str | None = None
    provider_id: int | None = None
    params: dict | None = None
    mode: str = 'chat'
    base_model: str
    input_cost_per_token: float | None = None
    output_cost_per_token: float | None = None
    max_tokens: int | None = None

    def to_dict(self) -> dict:
        model = {
            'name': self.name,
            'provider': self.provider,
            'params': self.params,
            'mode': self.mode,
            'base_model': self.base_model,
            'input_cost_per_token': self.input_cost_per_token,
            'output_cost_per_token': self.output_cost_per_token,
            'max_tokens': self.max_tokens
        }
        if self.id:
            model['id'] = self.id
        if self.provider_id:
            model['provider_id'] = self.provider_id
        print(f"LLMModel to_dict: {model}")
        return model
    
    def resource_dict(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'provider': self.provider,
        }

    @staticmethod
    def from_dict(data) -> 'LLMModel':
        input_dict = {
            "name": data['name'],
            "provider": data['provider'],
        }
        if 'model_info' in data and 'base_model' in data['model_info']:
            input_dict['base_model'] = data['model_info']['base_model']
        if 'params' in data:
            input_dict['params'] = data['params']
        if 'mode' in data:
            input_dict['mode'] = data['mode']
        if 'input_cost_per_token' in data:
            input_dict['input_cost_per_token'] = data['input_cost_per_token']
        if 'output_cost_per_token' in data:
            input_dict['output_cost_per_token'] = data['output_cost_per_token']
        if 'max_tokens' in data:
            input_dict['max_tokens'] = data['max_tokens']
        print('Input dict for LLMModel:', input_dict)
        return LLMModel(**input_dict)
