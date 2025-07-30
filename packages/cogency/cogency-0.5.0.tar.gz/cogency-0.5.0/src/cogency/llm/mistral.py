from typing import AsyncIterator, Dict, List, Optional, Union

try:
    from mistralai import Mistral
except ImportError:
    raise ImportError("Mistral support not installed. Use `pip install cogency[mistral]`")

from cogency.llm.base import BaseLLM
from cogency.llm.key_rotator import KeyRotator
from cogency.utils.errors import ConfigurationError


class MistralLLM(BaseLLM):
    def __init__(
        self,
        api_keys: Union[str, List[str]] = None,
        model: str = "mistral-large-latest",
        timeout: float = 15.0,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        max_retries: int = 3,
        **kwargs,
    ):
        # Validate inputs
        if not api_keys:
            raise ConfigurationError("API keys must be provided", error_code="NO_API_KEYS")

        # Handle the cleaner interface: if list provided, create key rotator internally
        if isinstance(api_keys, list) and len(api_keys) > 1:
            key_rotator = KeyRotator(api_keys)
            api_key = None
        elif isinstance(api_keys, list) and len(api_keys) == 1:
            key_rotator = None
            api_key = api_keys[0]
        else:
            key_rotator = None
            api_key = api_keys

        super().__init__(api_key, key_rotator)
        self.model = model

        # Configuration parameters
        self.timeout = timeout
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.max_retries = max_retries

        # Build kwargs for Mistral client
        self.kwargs = {
            "temperature": temperature,
            "max_tokens": max_tokens,
            **kwargs,
        }

        self._client: Optional[Mistral] = None
        self._init_client()  # Initialize the client

    def _init_client(self):
        """Initializes the Mistral client based on the active key."""
        current_key = self.key_rotator.get_key() if self.key_rotator else self.api_key

        if not current_key:
            raise ConfigurationError(
                "API key must be provided either directly or via KeyRotator.",
                error_code="NO_CURRENT_API_KEY",
            )

        self._client = Mistral(api_key=current_key)

    def _get_client(self):
        """Get client instance."""
        return self._client

    def _rotate_client(self):
        """Rotate to the next key and re-initialize the client."""
        if self.key_rotator:
            self._init_client()

    def _convert_msgs(self, msgs: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Convert to provider format."""
        return [{"role": m["role"], "content": m["content"]} for m in msgs]

    async def invoke(self, messages: List[Dict[str, str]], **kwargs) -> str:
        self._rotate_client()
        mistral_messages = self._convert_msgs(messages)

        res = await self._client.chat.complete_async(
            model=self.model,
            messages=mistral_messages,
            **self.kwargs,
            **kwargs,
        )
        return res.choices[0].message.content

    async def stream(self, messages: List[Dict[str, str]], yield_interval: float = 0.0, **kwargs) -> AsyncIterator[str]:
        self._rotate_client()
        mistral_messages = self._convert_msgs(messages)

        stream = await self._client.chat.stream_async(
            model=self.model,
            messages=mistral_messages,
            **self.kwargs,
            **kwargs,
        )

        async for chunk in stream:
            if chunk.data.choices[0].delta.content:
                yield chunk.data.choices[0].delta.content
