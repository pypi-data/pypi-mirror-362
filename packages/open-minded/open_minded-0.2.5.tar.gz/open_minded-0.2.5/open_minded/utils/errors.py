class OpenMindedError(Exception):
    """Base exception for all Open-Minded errors."""

    pass


class FailedToFindSuitableProviderError(OpenMindedError):
    def __init__(self):
        super().__init__("Failed to find suitable LLM API provider")


class InvalidLlmApiResponseError(OpenMindedError):
    """Raised when the LLM API returns an invalid response."""

    pass


class LlmApiHttpStatusError(OpenMindedError):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

        message = f"LLM API returned an error with code {status_code}: {detail}"

        super().__init__(message)
