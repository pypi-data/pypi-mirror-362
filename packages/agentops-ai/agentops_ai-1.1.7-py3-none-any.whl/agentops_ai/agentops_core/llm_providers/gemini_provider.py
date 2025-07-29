"""Google Gemini LLM provider implementation.

This module implements the Google Gemini provider for the AgentOps multi-provider
LLM system, supporting Gemini Pro and other Google AI models.
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
    import google.generativeai as genai
    from google.generativeai.types import GenerateContentResponse
    GEMINI_AVAILABLE = True
except ImportError:
    genai = None
    GenerateContentResponse = None
    GEMINI_AVAILABLE = False

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    """Google Gemini LLM provider implementation.
    
    Supports Gemini Pro, Gemini Pro Vision, and other Google AI models
    with competitive pricing and strong performance.
    """
    
    # Gemini token costs per 1M tokens (as of December 2024)
    MODEL_COSTS = {
        "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
        "gemini-1.5-flash": {"input": 0.000075, "output": 0.0003},
        "gemini-pro": {"input": 0.0005, "output": 0.0015},
        "gemini-pro-vision": {"input": 0.00025, "output": 0.0005},
    }
    
    def _initialize_client(self) -> Any:
        """Initialize the Gemini client.
        
        Returns:
            Configured Gemini model instance
            
        Raises:
            UnsupportedProviderError: If Gemini not available
        """
        if not GEMINI_AVAILABLE:
            raise UnsupportedProviderError(
                "Google Gemini not available. Install with: pip install google-generativeai"
            )
        
        # Configure the Gemini API
        genai.configure(api_key=self.config.api_key)
        
        # Initialize the model
        self._client = genai.GenerativeModel(
            model_name=self.config.model,
            generation_config=genai.types.GenerationConfig(
                temperature=self.config.temperature,
                max_output_tokens=self.config.max_tokens,
            )
        )
        
        logger.info(f"Initialized Gemini client for model: {self.config.model}")
        return self._client
    
    async def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using Google Gemini.
        
        Args:
            prompt: User prompt text
            system_prompt: Optional system prompt
            **kwargs: Additional Gemini parameters
            
        Returns:
            Standardized LLM response
            
        Raises:
            ProviderConnectionError: If Gemini request fails
            ProviderRateLimitError: If rate limit exceeded
        """
        if not self.check_rate_limit():
            raise ProviderRateLimitError(
                f"Rate limit exceeded for {self.config.provider_name}"
            )
        
        start_time = time.time()
        
        try:
            # Combine system and user prompts for Gemini
            full_prompt = prompt
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {prompt}"
            
            logger.debug(f"Making Gemini request with model: {self.config.model}")
            
            # Make the API call (Gemini uses sync API, wrap in async)
            import asyncio
            response = await asyncio.get_event_loop().run_in_executor(
                None, 
                self._client.generate_content,
                full_prompt
            )
            
            response_time = time.time() - start_time
            
            # Extract response data
            content = response.text if response.text else ""
            
            # Estimate token usage (Gemini doesn't always provide exact counts)
            estimated_prompt_tokens = len(full_prompt.split()) * 1.3  # Rough estimate
            estimated_completion_tokens = len(content.split()) * 1.3
            estimated_total_tokens = estimated_prompt_tokens + estimated_completion_tokens
            
            usage_data = {
                "prompt_tokens": int(estimated_prompt_tokens),
                "completion_tokens": int(estimated_completion_tokens),
                "total_tokens": int(estimated_total_tokens)
            }
            
            # Calculate cost estimate
            cost_estimate = self._calculate_cost(usage_data)
            
            # Create standardized response
            response = LLMResponse(
                content=content,
                model=self.config.model,
                provider="gemini",
                usage=usage_data,
                cost_estimate=cost_estimate,
                response_time=response_time,
                metadata={
                    "finish_reason": "stop",  # Gemini doesn't provide detailed finish reasons
                    "safety_ratings": getattr(response, "prompt_feedback", None),
                    "estimated_usage": True  # Indicate that usage is estimated
                }
            )
            
            # Update provider metrics
            self.update_metrics(response)
            self.status = ProviderStatus.HEALTHY
            self.last_error = None
            
            logger.info(
                f"Gemini request successful: ~{usage_data.get('total_tokens', 0)} tokens, "
                f"${cost_estimate:.4f}, {response_time:.2f}s"
            )
            
            return response
            
        except Exception as e:
            error_msg = f"Gemini request failed: {str(e)}"
            logger.error(error_msg)
            
            # Check for specific error types
            if "quota" in str(e).lower() or "limit" in str(e).lower():
                if "rate" in str(e).lower():
                    self.status = ProviderStatus.RATE_LIMITED
                    raise ProviderRateLimitError(error_msg)
                else:
                    self.status = ProviderStatus.QUOTA_EXCEEDED
                    raise ProviderConnectionError(error_msg)
            else:
                self.status = ProviderStatus.UNHEALTHY
                self.last_error = error_msg
                raise ProviderConnectionError(error_msg)
    
    def _calculate_cost(self, usage: Dict[str, Any]) -> float:
        """Calculate cost estimate for the Gemini request.
        
        Args:
            usage: Usage data (estimated for Gemini)
            
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
            # Fallback to Gemini Pro pricing for unknown models
            costs = self.MODEL_COSTS["gemini-pro"]
        
        # Calculate cost based on token usage (per million tokens)
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)
        
        prompt_cost = (prompt_tokens / 1_000_000) * costs["input"]
        completion_cost = (completion_tokens / 1_000_000) * costs["output"]
        
        return prompt_cost + completion_cost
    
    def validate_config(self) -> bool:
        """Validate Gemini configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        if not self.config.api_key:
            raise ValueError("Gemini API key is required")
        
        if not self.config.model:
            raise ValueError("Gemini model is required")
        
        # Validate model is supported
        supported_models = [
            "gemini-1.5-pro", "gemini-1.5-flash", 
            "gemini-pro", "gemini-pro-vision"
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
        """Test connection to Gemini.
        
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
            
            logger.info("Gemini connection test successful")
            return True
            
        except Exception as e:
            logger.error(f"Gemini connection test failed: {e}")
            return False
    
    @classmethod
    def create_from_env(cls) -> "GeminiProvider":
        """Create Gemini provider from environment variables.
        
        Returns:
            Configured Gemini provider instance
        """
        import os
        
        config = ProviderConfig(
            provider_name="gemini",
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
            api_key=os.getenv("GEMINI_API_KEY", ""),
            temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "4000")),
            timeout=int(os.getenv("GEMINI_TIMEOUT", "30")),
            rate_limit_per_minute=int(os.getenv("GEMINI_RATE_LIMIT", "60"))
        )
        
        return cls(config)
    
    def get_available_models(self) -> List[str]:
        """Get list of available Gemini models.
        
        Returns:
            List of model names
        """
        return [
            "gemini-1.5-pro",
            "gemini-1.5-flash",
            "gemini-pro",
            "gemini-pro-vision"
        ]