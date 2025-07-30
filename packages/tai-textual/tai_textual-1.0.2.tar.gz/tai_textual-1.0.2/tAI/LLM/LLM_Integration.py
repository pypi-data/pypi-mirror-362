from litellm import completion
import litellm
import json
from pydantic import BaseModel
from tAI.Utils.API import get_api_key
litellm.enable_json_schema_validation = True


class llm:
    def __init__(self, prompt: str, openrouter_all: bool):
        self.prompt = prompt
        self.openrouter_all = openrouter_all

    class Command(BaseModel):
        command: str
    
    def generate_command(self, model: str, query: str) -> str:
        messages = [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": query},
        ]
        if self.openrouter_all:

            # only changing when there is no openrouter before
            if not (model.startswith("openrouter/")):
                model = "openrouter/" + model
            api_key = get_api_key(model, self.openrouter_all)
        else:
            api_key = get_api_key(model,False)
        response = completion(
            model=model,
            messages=messages,
            api_key=api_key,
            response_format=self.Command,
        )
        response_json = json.loads(response.model_dump()['choices'][0]['message']['content'])
        command = response_json['command']
        return command