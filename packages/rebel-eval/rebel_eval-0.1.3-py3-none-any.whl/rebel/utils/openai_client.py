from typing import List, Dict, Any
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
import instructor


class OpenAIClientWrapper:
    def __init__(self, config: dict):
        self.client = OpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )
        self.patched_client = instructor.from_openai(self.client)

        client_params = { 'model': config['model'] }
        
        optional_client_params = ['temperature', 'max_tokens', 'timeout']    
        for param in optional_client_params:
            value = config.get(param)
            if value is not None:
                client_params[param] = value
        
        self.client_params = client_params
    
    def generate(self, messages: List[Dict]) -> ChatCompletion:
        return self.client.chat.completions.create(
            messages=messages,
            **self.client_params
        )

    def generate_instructed(self, messages: List[Dict], response_model: Any):
        result, raw_response = self.patched_client.chat.completions.create_with_completion(
            response_model=response_model,
            messages=messages,
            **self.client_params
        )
        
        return result
