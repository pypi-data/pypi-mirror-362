import json
from contextlib import asynccontextmanager
from typing import Optional, Sequence

import httpx

from open_minded.models.llm_message import LlmMessage
from open_minded.providers.base import LlmApiProvider
from open_minded.utils.errors import LlmApiHttpStatusError

_API_BASE_URL = "https://text.pollinations.ai"


class PollinationsProvider(LlmApiProvider):
    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        pass

    @property
    def name(self):
        return "Pollinations (https://pollinations.ai/)"

    async def fetch_llm_completion(self, message_history, proxy=None):
        async with self.fetch_llm_completion_response(
            message_history, False, proxy
        ) as response:
            response_data = json.loads((await response.aread()).decode())
            return response_data["choices"][0]["message"]["content"]

    @asynccontextmanager
    async def fetch_llm_completion_and_stream(self, message_history, proxy=None):
        async with self.fetch_llm_completion_response(
            message_history, True, proxy
        ) as response:

            async def stream_response():
                buffer = ""
                async for chunk in response.aiter_text():
                    buffer += chunk
                    lines = buffer.split("\n")
                    buffer = lines.pop()  # Save incomplete JSON

                    for line in lines:
                        line = line.strip()
                        if line.startswith("data: "):
                            data = line.replace("data: ", "").strip()
                            if data == "[DONE]":
                                return

                            try:
                                parsed = json.loads(data)
                                content = (
                                    parsed.get("choices", [{}])[0]
                                    .get("delta", {})
                                    .get("content")
                                )
                                if content:
                                    yield content
                            except (json.JSONDecodeError, IndexError, AttributeError):
                                continue

            yield stream_response()

    @asynccontextmanager
    async def fetch_llm_completion_response(
        self,
        message_history: Sequence[LlmMessage],
        stream: bool,
        proxy: Optional[str] = None,
    ):
        async with httpx.AsyncClient(
            base_url=_API_BASE_URL, proxy=proxy
        ) as httpx_client:
            async with httpx_client.stream(
                method="POST",
                url="/openai",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "text/event-stream",
                },
                json={
                    "model": "openai",
                    "messages": message_history,
                    "private": True,
                    "stream": stream,
                },
            ) as response:
                if response.is_error:
                    raise LlmApiHttpStatusError(
                        response.status_code,
                        f"Failed to fetch GPT completion from deepai.com: {response.text}",
                    )

                yield response
