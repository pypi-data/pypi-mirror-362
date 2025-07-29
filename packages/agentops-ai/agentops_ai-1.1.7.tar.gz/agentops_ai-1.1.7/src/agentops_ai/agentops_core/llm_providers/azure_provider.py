"""Azure OpenAI LLM provider implementation.

This module implements the Azure OpenAI provider for enterprise customers
requiring Azure-hosted OpenAI services with enhanced security and compliance.
"""

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
    from openai import AsyncAzureOpenAI
    from openai.types.chat import ChatCompletion
    AZURE_AVAILABLE = True
except ImportError:
    AsyncAzureOpenAI = None
    ChatCompletion = None
    AZURE_AVAILABLE = False

logger = logging.getLogger(__name__)


class AzureOpenAIProvider(BaseLLMProvider):
    """Azure OpenAI LLM provider implementation.
    
    Supports Azure-hosted OpenAI models with enterprise-grade security,
    compliance features, and regional data residency.
    """
    
    # Azure OpenAI token costs (same as OpenAI but through Azure)
    MODEL_COSTS = {
        "gpt-4": {"input": 0.03, "output": 0.06},
        "gpt-4-turbo": {"input": 0.01, "output": 0.03}, 
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "gpt-35-turbo": {"input": 0.001, "output": 0.002},
        "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
    }
    
    def _initialize_client(self) -> AsyncAzureOpenAI:
        """Initialize the Azure OpenAI async client.
        
        Returns:
            AsyncAzureOpenAI client instance
            
        Raises:
            UnsupportedProviderError: If Azure OpenAI not available
        """
        if not AZURE_AVAILABLE:
            raise UnsupportedProviderError(
                "Azure OpenAI not available. Install with: pip install openai"
            )
        
        if not self.config.base_url:
            raise ValueError("Azure OpenAI endpoint is required")
        
        if not self.config.deployment_name:
            raise ValueError("Azure deployment name is required")
        
        self._client = AsyncAzureOpenAI(
            api_key=self.config.api_key,
            azure_endpoint=self.config.base_url,
            api_version="2024-06-01",  # Latest stable version
            timeout=self.config.timeout,
            max_retries=self.config.max_retries
        )
        
        logger.info(
            f"Initialized Azure OpenAI client for deployment: {self.config.deployment_name}"
        )
        return self._client
    
    async def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Azure OpenAI.
        
        Args:
            prompt: User prompt text
            system_prompt: Optional system prompt
            **kwargs: Additional Azure OpenAI parameters
            
        Returns:
            Standardized LLM response
            
        Raises:
            ProviderConnectionError: If Azure OpenAI request fails
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
            
            # Prepare Azure OpenAI parameters
            azure_params = {
                "model": self.config.deployment_name,  # Use deployment name for Azure
                "messages": messages,
                "temperature": self.config.temperature,
                "max_tokens": self.config.max_tokens,
                **kwargs  # Allow override of defaults
            }
            
            logger.debug(
                f"Making Azure OpenAI request with deployment: {self.config.deployment_name}"
            )
            
            # Make the API call
            completion: ChatCompletion = await self._client.chat.completions.create(**azure_params)
            
            response_time = time.time() - start_time
            
            # Extract response data
            content = completion.choices[0].message.content or ""
            usage_data = completion.usage.model_dump() if completion.usage else {}
            
            # Calculate cost estimate
            cost_estimate = self._calculate_cost(usage_data)
            
            # Create standardized response
            response = LLMResponse(
                content=content,
                model=completion.model or self.config.deployment_name,
                provider="azure",
                usage=usage_data,
                cost_estimate=cost_estimate,
                response_time=response_time,
                metadata={
                    "completion_id": completion.id,
                    "created": completion.created,
                    "finish_reason": completion.choices[0].finish_reason,
                    "deployment_name": self.config.deployment_name,
                    "azure_endpoint": self.config.base_url,
                    "system_fingerprint": getattr(completion, "system_fingerprint", None)
                }
            )
            
            # Update provider metrics
            self.update_metrics(response)
            self.status = ProviderStatus.HEALTHY
            self.last_error = None
            
            logger.info(
                f"Azure OpenAI request successful: {usage_data.get('total_tokens', 0)} tokens, "
                f"${cost_estimate:.4f}, {response_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            error_msg = f"Azure OpenAI request failed: {str(e)}"
            logger.error(error_msg)
            
            # Check for specific error types
            if "rate_limit" in str(e).lower() or "429" in str(e):
                self.status = ProviderStatus.RATE_LIMITED
                raise ProviderRateLimitError(error_msg)
            elif "quota" in str(e).lower() or "insufficient_quota" in str(e).lower():
                self.status = ProviderStatus.QUOTA_EXCEEDED
                raise ProviderConnectionError(error_msg)
            else:
                self.status = ProviderStatus.UNHEALTHY
                self.last_error = error_msg
                raise ProviderConnectionError(error_msg)
    
    def _calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost estimate for the Azure OpenAI request.
        
        Args:
            usage: Usage data from Azure OpenAI response
            
        Returns:
            Estimated cost in USD
        """
        if not usage:
            return 0.0
        
        # Map deployment name to model for cost calculation
        model_name = self.config.model.lower()
        
        # Handle Azure model naming conventions
        if "gpt-35" in model_name:
            model_name = "gpt-35-turbo"
        elif "gpt-4" in model_name and "turbo" in model_name:
            model_name = "gpt-4-turbo"
        elif "gpt-4" in model_name:
            model_name = "gpt-4"
        
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
        """Validate Azure OpenAI configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.api_key:
            raise ValueError("Azure OpenAI API key is required")
        
        if not self.config.base_url:
            raise ValueError("Azure OpenAI endpoint is required")
        
        if not self.config.base_url.endswith(".openai.azure.com"):
            raise ValueError("Azure OpenAI endpoint must end with '.openai.azure.com'")
        
        if not self.config.deployment_name:
            raise ValueError("Azure deployment name is required")
        
        if not self.config.model:
            raise ValueError("Azure OpenAI model is required")
        
        return True
    
    async def test_connection(self) -> bool:
        """Test connection to Azure OpenAI.
        
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
            
            logger.info("Azure OpenAI connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"Azure OpenAI connection test failed: {e}")
            return False
    
    @classmethod
    def create_from_env(cls) -> "AzureOpenAIProvider":
        """Create Azure OpenAI provider from environment variables.
        
        Returns:
            Configured Azure OpenAI provider instance
        """
        import os
        
        config = ProviderConfig(
            provider_name="azure",
            model=os.getenv("AZURE_OPENAI_MODEL", "gpt-4"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
            base_url=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
            deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT", ""),
            temperature=float(os.getenv("AZURE_OPENAI_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("AZURE_OPENAI_MAX_TOKENS", "4000")),
            timeout=int(os.getenv("AZURE_OPENAI_TIMEOUT", "30")),
            rate_limit_per_minute=int(os.getenv("AZURE_OPENAI_RATE_LIMIT", "60"))
        )
        
        return cls(config)
    
    def get_available_models(self) -> List[str]:
        """Get list of available Azure OpenAI models.
        
        Returns:
            List of model names
        """
        return [
            "gpt-4o",
            "gpt-4-turbo",
            "gpt-4",
            "gpt-35-turbo",
            "gpt-3.5-turbo"
        ]