import os
from typing import AsyncIterator, Dict, List, Optional, Union

import google.generativeai as genai

from cogency.llm.base import BaseLLM
from cogency.llm.key_rotator import KeyRotator
from cogency.utils.errors import ConfigurationError
from cogency.core.resilience import with_resilience, with_retry, RateLimitedError, CircuitOpenError, RateLimiterConfig, CircuitBreakerConfig


class GeminiLLM(BaseLLM):
    def __init__(
        self,
        api_keys: Union[str, List[str]] = None,
        model: str = "gemini-2.5-flash",
        timeout: float = 15.0,
        temperature: float = 0.7,
        max_retries: int = 3,
        **kwargs,
    ):
        # Auto-detect API keys from environment if not provided
        if api_keys is None:
            # Try numbered keys first (GEMINI_API_KEY_1, etc.)
            detected_keys = []
            for i in range(1, 4):  # Check 1-3
                key = os.getenv(f'GEMINI_API_KEY_{i}')
                if key:
                    detected_keys.append(key)
            
            # Fall back to base GEMINI_API_KEY
            if not detected_keys:
                base_key = os.getenv('GEMINI_API_KEY')
                if base_key:
                    detected_keys = [base_key]
                    
            if detected_keys:
                api_keys = detected_keys
            else:
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

        # Build kwargs for Gemini client
        self.kwargs = {
            "timeout": timeout,
            "temperature": temperature,
            "max_retries": max_retries,
            **kwargs,
        }

        self._model_instances: Dict[str, genai.GenerativeModel] = {}  # Cache for model instances
        self._current_model: Optional[genai.GenerativeModel] = None  # Currently active model instance
        self._init_current_model()  # Initialize the first model instance

    def _init_current_model(self):
        """Initializes or retrieves the current model instance based on the active key."""
        current_key = self.key_rotator.get_key() if self.key_rotator else self.api_key

        if not current_key:
            raise ConfigurationError(
                "API key must be provided either directly or via KeyRotator.",
                error_code="NO_CURRENT_API_KEY",
            )

        if current_key not in self._model_instances:
            genai.configure(api_key=current_key)
            # Only pass GenerationConfig-compatible parameters
            generation_params = {
                "temperature": self.temperature,
                # Add other valid GenerationConfig params as needed
            }
            # Filter out non-GenerationConfig params like timeout, max_retries
            for k, v in self.kwargs.items():
                if k in ["temperature", "max_output_tokens", "top_p", "top_k", "candidate_count", "stop_sequences"]:
                    generation_params[k] = v
            
            self._model_instances[current_key] = genai.GenerativeModel(
                model_name=self.model,
                generation_config=genai.types.GenerationConfig(**generation_params)
            )

        self._current_model = self._model_instances[current_key]

    def _get_client(self):
        """Get model instance."""
        return self._current_model

    def _init_client(self):
        """Alias for _init_current_model to match mixin interface."""
        self._init_current_model()

    def _rotate_client(self):
        """Rotate to the next key and re-initialize the client."""
        if self.key_rotator:
            self._init_client()

    @with_resilience(
        rate_limiter="gemini",
        circuit_breaker="gemini",
        rate_config=RateLimiterConfig(requests_per_minute=10, burst_size=3),  # Conservative for free tier
        circuit_config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=120)
    )
    @with_retry(max_attempts=3, exceptions=(Exception,))
    async def invoke(self, messages: List[Dict[str, str]], **kwargs) -> str:
        self._rotate_client()

        # Convert messages to Gemini format (simple text concatenation for now)
        # Gemini's chat format is different - it expects conversation history
        prompt = "".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        try:
            res = await self._current_model.generate_content_async(prompt, **kwargs)
            return res.text
        except Exception as e:
            # Handle rate limiting gracefully
            if "429" in str(e) or "quota" in str(e).lower():
                raise RateLimitedError(f"Gemini rate limited: {e}")
            raise

    @with_resilience(
        rate_limiter="gemini_stream",
        circuit_breaker="gemini",
        rate_config=RateLimiterConfig(requests_per_minute=10, burst_size=3),
        circuit_config=CircuitBreakerConfig(failure_threshold=3, recovery_timeout=120)
    )
    async def stream(self, messages: List[Dict[str, str]], yield_interval: float = 0.0, **kwargs) -> AsyncIterator[str]:
        self._rotate_client()

        # Convert messages to Gemini format (simple text concatenation for now)
        prompt = "".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        try:
            response = await self._current_model.generate_content_async(
                prompt, stream=True, **kwargs
            )
            
            async for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            # Handle rate limiting gracefully
            if "429" in str(e) or "quota" in str(e).lower():
                raise RateLimitedError(f"Gemini streaming rate limited: {e}")
            raise