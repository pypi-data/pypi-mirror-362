"""OpenAI LLM provider implementation.

This module implements the OpenAI provider for the AgentOps multi-provider
LLM system, supporting both GPT-3.5 and GPT-4 models.
"""

import asyncio
import time
from typing import Optional, Any, Dict, List
import logging

from .base_provider import (
    BaseLLMProvider, 
    LLMResponse, 
    ProviderConfig, 
    ProviderConnectionError,
    ProviderRateLimitError,
    ProviderStatus,
    UnsupportedProviderError
)

# Optional imports with fallbacks
try:
    from openai import AsyncOpenAI
    from openai.types.chat import ChatCompletion
    OPENAI_AVAILABLE = True
except ImportError:
    AsyncOpenAI = None
    ChatCompletion = None
    OPENAI_AVAILABLE = False

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation.
    
    Supports GPT-3.5-turbo, GPT-4, and other OpenAI models with async operations,
    rate limiting, and comprehensive error handling.
    """
    
    # Token costs per 1K tokens (as of December 2024)
    MODEL_COSTS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
        "gpt-3.5-turbo-instruct": {"input": 0.0015, "output": 0.002},
    }
    
    def _initialize_client(self) -> AsyncOpenAI:
        """Initialize the OpenAI async client.
        
        Returns:
            AsyncOpenAI client instance
            
        Raises:
            UnsupportedProviderError: If OpenAI not available
        """
        if not OPENAI_AVAILABLE:
            raise UnsupportedProviderError(
                "OpenAI not available. Install with: pip install openai"
            )
        
        self._client = AsyncOpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            timeout=self.config.timeout,
            max_retries=self.config.max_retries
        )
        
        logger.info(f"Initialized OpenAI client for model: {self.config.model}")
        return self._client
    
    async def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using OpenAI.
        
        Args:
            prompt: User prompt text
            system_prompt: Optional system prompt
            **kwargs: Additional OpenAI parameters
            
        Returns:
            Standardized LLM response
            
        Raises:
            ProviderConnectionError: If OpenAI request fails
            ProviderRateLimitError: If rate limit exceeded
        """
        if not self.check_rate_limit():
            raise ProviderRateLimitError(
                f"Rate limit exceeded for {self.config.provider_name}"
            )
        
        start_time = time.time()
        
        try:
            # Prepare messages
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            # Prepare OpenAI parameters
            openai_params = {
                "model": self.config.model,
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                **kwargs  # Allow override of defaults
            }
            
            logger.debug(f"Making OpenAI request with model: {self.config.model}")
            
            # Make the API call
            completion: ChatCompletion = await self._client.chat.completions.create(**openai_params)
            
            response_time = time.time() - start_time
            
            # Extract response data
            content = completion.choices[0].message.content or ""
            usage_data = completion.usage.model_dump() if completion.usage else {}
            
            # Calculate cost estimate
            cost_estimate = self._calculate_cost(usage_data)
            
            # Create standardized response
            response = LLMResponse(
                content=content,
                model=completion.model,
                provider="openai",
                usage=usage_data,
                cost_estimate=cost_estimate,
                response_time=response_time,
                metadata={
                    "completion_id": completion.id,
                    "created": completion.created,
                    "finish_reason": completion.choices[0].finish_reason,
                    "system_fingerprint": getattr(completion, "system_fingerprint", None)
                }
            )
            
            # Update provider metrics
            self.update_metrics(response)
            self.status = ProviderStatus.HEALTHY
            self.last_error = None
            
            logger.info(
                f"OpenAI request successful: {usage_data.get('total_tokens', 0)} tokens, "
                f"${cost_estimate:.4f}, {response_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            error_msg = f"OpenAI request failed: {str(e)}"
            logger.error(error_msg)
            
            # Check for specific error types
            if "rate_limit" in str(e).lower():
                self.status = ProviderStatus.RATE_LIMITED
                raise ProviderRateLimitError(error_msg)
            elif "quota" in str(e).lower():
                self.status = ProviderStatus.QUOTA_EXCEEDED
                raise ProviderConnectionError(error_msg)
            else:
                self.status = ProviderStatus.UNHEALTHY
                self.last_error = error_msg
                raise ProviderConnectionError(error_msg)
    
    def _calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost estimate for the request.
        
        Args:
            usage: Usage data from OpenAI response
            
        Returns:
            Estimated cost in USD
        """
        if not usage:
            return 0.0
        
        model_name = self.config.model.lower()
        
        # Find matching cost structure
        costs = None
        for model_key, model_costs in self.MODEL_COSTS.items():
            if model_key in model_name:
                costs = model_costs
                break
        
        if not costs:
            # Fallback to GPT-4 pricing for unknown models
            costs = self.MODEL_COSTS["gpt-4"]
        
        # Calculate cost based on token usage
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        
        prompt_cost = (prompt_tokens / 1000) * costs["input"]
        completion_cost = (completion_tokens / 1000) * costs["output"]
        
        return prompt_cost + completion_cost
    
    def validate_config(self) -> bool:
        """Validate OpenAI configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.api_key:
            raise ValueError("OpenAI API key is required")
        
        if not self.config.api_key.startswith("sk-"):
            raise ValueError("OpenAI API key must start with 'sk-'")
        
        if not self.config.model:
            raise ValueError("OpenAI model is required")
        
        # Validate model is supported
        supported_models = [
            "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini",
            "gpt-3.5-turbo", "gpt-3.5-turbo-instruct"
        ]
        
        model_supported = any(
            supported in self.config.model.lower() 
            for supported in supported_models
        )
        
        if not model_supported:
            logger.warning(
                f"Model {self.config.model} may not be supported. "
                f"Supported models: {supported_models}"
            )
        
        return True
    
    async def test_connection(self) -> bool:
        """Test connection to OpenAI.
        
        Returns:
            True if connection successful
        """
        try:
            # Make a minimal test request
            test_response = await self.generate(
                prompt="Test",
                max_tokens=1,
                temperature=0
            )
            
            logger.info("OpenAI connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
    
    @classmethod
    def create_from_env(cls) -> "OpenAIProvider":
        """Create OpenAI provider from environment variables.
        
        Returns:
            Configured OpenAI provider instance
        """
        import os
        
        config = ProviderConfig(
            provider_name="openai",
            model=os.getenv("OPENAI_MODEL", "gpt-4o"),
            api_key=os.getenv("OPENAI_API_KEY", ""),
            base_url=os.getenv("OPENAI_BASE_URL"),
            temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "4000")),
            timeout=int(os.getenv("OPENAI_TIMEOUT", "30")),
            rate_limit_per_minute=int(os.getenv("OPENAI_RATE_LIMIT", "60"))
        )
        
        return cls(config)
    
    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models.
        
        Returns:
            List of model names
        """
        return [
            "gpt-4o",
            "gpt-4o-mini", 
            "gpt-4-turbo",
            "gpt-4",
            "gpt-3.5-turbo",
            "gpt-3.5-turbo-instruct"
        ]