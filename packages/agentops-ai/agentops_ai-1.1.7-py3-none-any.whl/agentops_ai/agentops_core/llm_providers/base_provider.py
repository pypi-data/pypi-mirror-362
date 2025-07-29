"""Base provider abstraction for LLM providers.

This module defines the abstract interface that all LLM providers must implement,
ensuring consistent behavior across different providers.
"""

import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from enum import Enum


class ProviderStatus(Enum):
    """Provider status enumeration."""
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"
    RATE_LIMITED = "rate_limited"
    QUOTA_EXCEEDED = "quota_exceeded"


class UnsupportedProviderError(Exception):
    """Raised when a requested provider is not supported or available."""
    pass


class ProviderConnectionError(Exception):
    """Raised when connection to a provider fails."""
    pass


class ProviderRateLimitError(Exception):
    """Raised when provider rate limit is exceeded."""
    pass


@dataclass
class LLMResponse:
    """Standardized response from LLM providers."""
    
    content: str
    model: str
    provider: str
    usage: Dict[str, Any]
    cost_estimate: float
    response_time: float
    metadata: Dict[str, Any]
    
    @property
    def tokens_used(self) -> int:
        """Get total tokens used (prompt + completion)."""
        return self.usage.get("total_tokens", 0)
    
    @property
    def prompt_tokens(self) -> int:
        """Get prompt tokens used."""
        return self.usage.get("prompt_tokens", 0)
    
    @property
    def completion_tokens(self) -> int:
        """Get completion tokens used."""
        return self.usage.get("completion_tokens", 0)


@dataclass 
class ProviderConfig:
    """Configuration for LLM providers."""
    
    provider_name: str
    model: str
    api_key: str
    base_url: Optional[str] = None
    deployment_name: Optional[str] = None  # For Azure
    temperature: float = 0.1
    max_tokens: int = 4000
    timeout: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60
    cost_per_token: float = 0.0001  # Default cost estimate
    
    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.api_key:
            raise ValueError(f"API key is required for {self.provider_name}")
        if not self.model:
            raise ValueError(f"Model is required for {self.provider_name}")


class BaseLLMProvider(ABC):
    """Abstract base class for LLM providers.
    
    All LLM providers must implement this interface to ensure consistent
    behavior and enable seamless provider switching.
    """
    
    def __init__(self, config: ProviderConfig):
        """Initialize the provider with configuration.
        
        Args:
            config: Provider-specific configuration
        """
        self.config = config
        self.status = ProviderStatus.UNKNOWN
        self.last_error: Optional[str] = None
        self.last_request_time: Optional[float] = None
        self.request_count = 0
        self.total_cost = 0.0
        self.total_tokens = 0
        
        # Rate limiting
        self._request_times: List[float] = []
        
        # Initialize the client
        self._client = None
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self) -> Any:
        """Initialize the provider-specific client.
        
        Returns:
            Provider-specific client instance
        """
        pass
    
    @abstractmethod
    async def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion from the LLM provider.
        
        Args:
            prompt: User prompt text
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific parameters
            
        Returns:
            Standardized LLM response
            
        Raises:
            ProviderConnectionError: If connection fails
            ProviderRateLimitError: If rate limit exceeded
        """
        pass
    
    @abstractmethod
    def validate_config(self) -> bool:
        """Validate the provider configuration.
        
        Returns:
            True if configuration is valid
            
        Raises:
            ValueError: If configuration is invalid
        """
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test connection to the provider.
        
        Returns:
            True if connection successful
        """
        pass
    
    async def health_check(self) -> ProviderStatus:
        """Check if the provider is healthy and ready to use.
        
        Returns:
            Current provider status
        """
        try:
            if await self.test_connection():
                self.status = ProviderStatus.HEALTHY
                self.last_error = None
            else:
                self.status = ProviderStatus.UNHEALTHY
                self.last_error = "Health check failed"
        except ProviderRateLimitError:
            self.status = ProviderStatus.RATE_LIMITED
            self.last_error = "Rate limit exceeded"
        except Exception as e:
            self.status = ProviderStatus.UNHEALTHY
            self.last_error = str(e)
        
        return self.status
    
    def check_rate_limit(self) -> bool:
        """Check if request is within rate limits.
        
        Returns:
            True if request can proceed
        """
        now = time.time()
        
        # Clean old requests (older than 1 minute)
        cutoff = now - 60
        self._request_times = [t for t in self._request_times if t > cutoff]
        
        # Check if we're within rate limit
        if len(self._request_times) >= self.config.rate_limit_per_minute:
            return False
        
        # Record this request
        self._request_times.append(now)
        return True
    
    def update_metrics(self, response: LLMResponse) -> None:
        """Update provider metrics after a successful request.
        
        Args:
            response: The LLM response to track
        """
        self.request_count += 1
        self.total_cost += response.cost_estimate
        self.total_tokens += response.tokens_used
        self.last_request_time = time.time()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get provider performance metrics.
        
        Returns:
            Dictionary of provider metrics
        """
        return {
            "provider_name": self.config.provider_name,
            "status": self.status.value,
            "request_count": self.request_count,
            "total_cost": self.total_cost,
            "total_tokens": self.total_tokens,
            "last_request_time": self.last_request_time,
            "last_error": self.last_error,
            "rate_limit_remaining": max(0, self.config.rate_limit_per_minute - len(self._request_times))
        }
    
    def reset_metrics(self) -> None:
        """Reset provider metrics."""
        self.request_count = 0
        self.total_cost = 0.0
        self.total_tokens = 0
        self.last_request_time = None
        self._request_times.clear()
    
    def __str__(self) -> str:
        """String representation of the provider."""
        return f"{self.config.provider_name}({self.config.model})"
    
    def __repr__(self) -> str:
        """Detailed string representation of the provider."""
        return (
            f"{self.__class__.__name__}("
            f"provider={self.config.provider_name}, "
            f"model={self.config.model}, "
            f"status={self.status.value}"
            f")"
        )