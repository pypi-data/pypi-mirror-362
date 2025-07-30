import os
from typing import Dict, List
from huggingface_hub import InferenceClient

from gai_tool.src import print_tokens
from gai_tool.api.token_counter_lite import TokenCounterLite
from gai_tool.src.utils import get_api_huggingface_key, validate_messages


class HuggingClient:
    def __init__(self,
                 model: str,
                 temperature: int,
                 max_tokens: int) -> str:

        self.client = InferenceClient(
            api_key=get_api_huggingface_key(),
        )
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

        self.TokenCounter = TokenCounterLite(
            model=self.model,
        )

    def run(self):
        print("Huggingface client running")

    def get_chat_completion(self,
                            user_message: List[Dict[str, str]]
                            ):

        validate_messages(messages=user_message)

        tokens = self.TokenCounter.count_tokens(user_message)
        remaining_tokens = self.TokenCounter.adjust_max_tokens(user_message, self.max_tokens)

        print_tokens(tokens, remaining_tokens)

        response = self.client.chat.completions.create(
            messages=user_message,
            model=self.model,
            max_tokens=remaining_tokens,
            temperature=self.temperature,
            stream=False,
        )
        return response.choices[0].message.content
