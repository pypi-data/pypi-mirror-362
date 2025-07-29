from typing import Literal, TypedDict


class LlmMessage(TypedDict):
    role: Literal["user", "assistant", "system"]
    content: str
