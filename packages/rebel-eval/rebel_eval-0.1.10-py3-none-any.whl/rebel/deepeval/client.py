from deepeval.models.base_model import DeepEvalBaseLLM
import os
import json
from openai import OpenAI, AsyncOpenAI


class OpenAIClientLLM(DeepEvalBaseLLM):
    def __init__(self, model_name = None, *args, **kwargs):
        judge_llm_config_path = os.environ['JUDGE_LLM_CONFIG_PATH']
        with open(judge_llm_config_path) as f:
            config = json.load(f)

        self.client = OpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )


        self.aclient = AsyncOpenAI(
            api_key=config['api_key'],
            base_url=config['base_url']
        )

        client_params = { 'model': config['model'] }
        optional_client_params = ['temperature', 'max_tokens', 'timeout']    

        for param in optional_client_params:
            value = config.get(param)
            if value is not None:
                client_params[param] = value

        self.client_params = client_params

        super().__init__(model_name, *args, **kwargs)


    def load_model(self, *args, **kwargs):
        return None


    def generate(self, prompt: str) -> str:
        return self.client.chat.completions.create(
            messages=[{'role': 'user', 'content': prompt}],
            **self.client_params
        ).choices[0].message.content


    async def a_generate(self, prompt: str):
        completions = await self.aclient.chat.completions.create(
            messages=[{'role': 'user', 'content': prompt}],
            **self.client_params
        )

        return completions.choices[0].message.content


    def get_model_name(self, *args, **kwargs):
        return 'OpenAI client based custom LLM'
