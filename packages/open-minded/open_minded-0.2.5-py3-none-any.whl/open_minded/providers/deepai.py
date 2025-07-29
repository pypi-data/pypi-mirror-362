import json
from contextlib import asynccontextmanager
from typing import Optional, Sequence

import httpx

from open_minded.models.llm_message import LlmMessage
from open_minded.providers.base import LlmApiProvider
from open_minded.utils.errors import LlmApiHttpStatusError
from open_minded.utils.user_agent import IPHONE_USER_AGENT

DEEPAI_API_BASE_URL = "https://api.deepai.org"


class DeepAiProvider(LlmApiProvider):
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass

    @property
    def name(self):
        return "DeepAI (https://deepai.org)"

    async def fetch_llm_completion(self, message_history, proxy=None):
        async with self.fetch_llm_completion_response(
            message_history, proxy
        ) as response:
            return (await response.aread()).decode()

    @asynccontextmanager
    async def fetch_llm_completion_and_stream(self, message_history, proxy=None):
        async with self.fetch_llm_completion_response(
            message_history, proxy
        ) as response:
            yield response.aiter_text()

    @asynccontextmanager
    async def fetch_llm_completion_response(
        self,
        message_history: Sequence[LlmMessage],
        proxy: Optional[str] = None,
    ):
        # TODO: Do not recreate client on each completion. The problem is how to pass a proxy?

        async with httpx.AsyncClient(
            base_url=DEEPAI_API_BASE_URL, proxy=proxy
        ) as httpx_client:
            async with (
                httpx_client.stream(
                    method="POST",
                    url="/hacking_is_a_serious_crime",
                    headers={
                        "accept": "*/*",
                        "accept-language": "en-US,en;q=0.6",
                        "cache-control": "no-cache",
                        "origin": "https://deepai.org",
                        "pragma": "no-cache",
                        "user-agent": IPHONE_USER_AGENT,
                    },
                    data={
                        "chat_style": "chat",
                        "chatHistory": json.dumps(message_history),
                        "model": "standard",
                        "hacker_is_stinky": "very_stinky",  # Request must contain this field, do not ask me why
                    },
                    files={},
                ) as response
            ):
                if response.is_error:
                    raise LlmApiHttpStatusError(
                        response.status_code,
                        f"Failed to fetch GPT completion from deepai.com: {response.text}",
                    )

                yield response
