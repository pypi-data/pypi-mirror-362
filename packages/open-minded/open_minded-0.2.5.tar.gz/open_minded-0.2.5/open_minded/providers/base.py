from abc import ABC, abstractmethod
from typing import AsyncContextManager, AsyncIterable, Optional, Sequence

from open_minded.models.llm_message import LlmMessage


class LlmApiProvider(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def __aenter__(self) -> "LlmApiProvider":
        pass

    @abstractmethod
    async def __aexit__(self, *_) -> None:
        pass

    @abstractmethod
    async def fetch_llm_completion(
        self, message_history: Sequence[LlmMessage], proxy: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    def fetch_llm_completion_and_stream(
        self, message_history: Sequence[LlmMessage], proxy: Optional[str] = None
    ) -> AsyncContextManager[AsyncIterable[str]]:
        pass
