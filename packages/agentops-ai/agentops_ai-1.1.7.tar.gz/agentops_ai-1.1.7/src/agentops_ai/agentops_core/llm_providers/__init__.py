"""Multi-Provider LLM Abstraction Layer for AgentOps.

This package provides a unified interface for multiple LLM providers,
allowing seamless switching between OpenAI, Azure OpenAI, and Google Gemini.

Key Features:
- Provider abstraction with standardized responses
- Automatic failover and load balancing
- Cost tracking and optimization
- Rate limiting and quota management
- Async support for high performance
"""

from .base_provider import BaseLLMProvider, LLMResponse, ProviderConnectionError, UnsupportedProviderError
from .openai_provider import OpenAIProvider
from .azure_provider import AzureOpenAIProvider
from .gemini_provider import GeminiProvider
from .provider_factory import LLMProviderFactory
from .provider_manager import ProviderManager, get_provider_manager

__all__ = [
    # Core abstractions
    "BaseLLMProvider",
    "LLMResponse", 
    "ProviderConnectionError",
    "UnsupportedProviderError",
    
    # Provider implementations
    "OpenAIProvider",
    "AzureOpenAIProvider", 
    "GeminiProvider",
    
    # Factory and management
    "LLMProviderFactory",
    "ProviderManager",
    "get_provider_manager",
]

# Version information
__version__ = "1.0.0"