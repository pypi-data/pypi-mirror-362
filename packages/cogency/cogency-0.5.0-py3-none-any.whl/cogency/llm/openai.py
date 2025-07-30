from typing import AsyncIterator, Dict, List, Optional, Union

try:
    import openai
except ImportError:
    raise ImportError("OpenAI support not installed. Use `pip install cogency[openai]`")

from cogency.llm.base import BaseLLM
from cogency.llm.key_rotator import KeyRotator
from cogency.utils.errors import ConfigurationError


class OpenAILLM(BaseLLM):
    def __init__(
        self,
        api_keys: Union[str, List[str]] = None,
        model: str = "gpt-4o",
        timeout: float = 15.0,
        temperature: float = 0.7,
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
        self.max_retries = max_retries

        # Build kwargs for OpenAI chat completions (filtering client-level params)
        self.kwargs = {
            "temperature": temperature,
            **kwargs,
        }
        self.client_kwargs = {
            "timeout": timeout,
            "max_retries": max_retries,
        }

        self._client: Optional[openai.AsyncOpenAI] = None
        self._init_client()

    def _init_client(self):
        """Init OpenAI client."""
        key = self.key_rotator.get_key() if self.key_rotator else self.api_key
        if not key:
            raise ConfigurationError(
                "API key required.",
                error_code="NO_CURRENT_API_KEY",
            )
        self._client = openai.AsyncOpenAI(api_key=key, **self.client_kwargs)

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
        msgs = self._convert_msgs(messages)
        res = await self._client.chat.completions.create(
            model=self.model,
            messages=msgs,
            **self.kwargs,
            **kwargs,
        )
        return res.choices[0].message.content

    async def stream(self, messages: List[Dict[str, str]], yield_interval: float = 0.0, **kwargs) -> AsyncIterator[str]:
        self._rotate_client()
        msgs = self._convert_msgs(messages)
        stream = await self._client.chat.completions.create(
            model=self.model,
            messages=msgs,
            stream=True,
            **self.kwargs,
            **kwargs,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content