"""LLM Provider Factory for AgentOps.

This module provides a factory pattern for creating and managing LLM providers,
enabling easy provider switching and configuration.
"""

import os
import logging
from typing import Dict, List, Optional, Type, Any

from .base_provider import BaseLLMProvider, ProviderConfig, UnsupportedProviderError
from .openai_provider import OpenAIProvider
from .azure_provider import AzureOpenAIProvider  
from .gemini_provider import GeminiProvider

logger = logging.getLogger(__name__)


class LLMProviderFactory:
    """Factory for creating LLM providers.
    
    Supports dynamic provider creation, configuration management,
    and provider discovery.
    """
    
    # Registry of available providers
    _providers: Dict[str, Type[BaseLLMProvider]] = {
        "openai": OpenAIProvider,
        "azure": AzureOpenAIProvider,
        "gemini": GeminiProvider,
    }
    
    @classmethod
    def create_provider(
        cls, 
        provider_name: str, 
        config: Optional[ProviderConfig] = None,
        **kwargs
    ) -> BaseLLMProvider:
        """Create a provider instance.
        
        Args:
            provider_name: Name of the provider to create
            config: Optional provider configuration
            **kwargs: Additional configuration parameters
            
        Returns:
            Configured provider instance
            
        Raises:
            UnsupportedProviderError: If provider not supported
            ValueError: If configuration is invalid
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            available = list(cls._providers.keys())
            raise UnsupportedProviderError(
                f"Provider '{provider_name}' not supported. Available: {available}"
            )
        
        provider_class = cls._providers[provider_name]
        
        # If no config provided, try to create from environment
        if config is None:
            try:
                config = cls._create_config_from_env(provider_name, **kwargs)
            except Exception as e:
                raise ValueError(f"Failed to create config for {provider_name}: {e}")
        
        # Override config with any provided kwargs
        if kwargs:
            config_dict = config.__dict__.copy()
            config_dict.update(kwargs)
            config = ProviderConfig(**config_dict)
        
        logger.info(f"Creating {provider_name} provider with model: {config.model}")
        
        try:
            provider = provider_class(config)
            return provider
        except Exception as e:
            raise ValueError(f"Failed to initialize {provider_name} provider: {e}")
    
    @classmethod
    def create_from_env(cls, provider_name: str) -> BaseLLMProvider:
        """Create provider from environment variables.
        
        Args:
            provider_name: Name of the provider to create
            
        Returns:
            Configured provider instance
        """
        provider_name = provider_name.lower()
        
        if provider_name not in cls._providers:
            available = list(cls._providers.keys())
            raise UnsupportedProviderError(
                f"Provider '{provider_name}' not supported. Available: {available}"
            )
        
        provider_class = cls._providers[provider_name]
        return provider_class.create_from_env()
    
    @classmethod
    def _create_config_from_env(cls, provider_name: str, **overrides) -> ProviderConfig:
        """Create provider configuration from environment variables.
        
        Args:
            provider_name: Name of the provider
            **overrides: Configuration overrides
            
        Returns:
            Provider configuration
        """
        if provider_name == "openai":
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
        elif provider_name == "azure":
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
        elif provider_name == "gemini":
            config = ProviderConfig(
                provider_name="gemini",
                model=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"),
                api_key=os.getenv("GEMINI_API_KEY", ""),
                temperature=float(os.getenv("GEMINI_TEMPERATURE", "0.1")),
                max_tokens=int(os.getenv("GEMINI_MAX_TOKENS", "4000")),
                timeout=int(os.getenv("GEMINI_TIMEOUT", "30")),
                rate_limit_per_minute=int(os.getenv("GEMINI_RATE_LIMIT", "60"))
            )
        else:
            raise UnsupportedProviderError(f"Unknown provider: {provider_name}")
        
        # Apply overrides
        if overrides:
            config_dict = config.__dict__.copy()
            config_dict.update(overrides)
            config = ProviderConfig(**config_dict)
        
        return config
    
    @classmethod
    def get_available_providers(cls) -> List[str]:
        """Get list of available provider names.
        
        Returns:
            List of provider names
        """
        return list(cls._providers.keys())
    
    @classmethod
    def register_provider(
        cls, 
        name: str, 
        provider_class: Type[BaseLLMProvider]
    ) -> None:
        """Register a new provider class.
        
        Args:
            name: Provider name
            provider_class: Provider class that extends BaseLLMProvider
            
        Raises:
            ValueError: If provider class is invalid
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise ValueError(
                f"Provider class must extend BaseLLMProvider, got {provider_class}"
            )
        
        cls._providers[name.lower()] = provider_class
        logger.info(f"Registered provider: {name}")
    
    @classmethod
    def unregister_provider(cls, name: str) -> None:
        """Unregister a provider.
        
        Args:
            name: Provider name to unregister
        """
        name = name.lower()
        if name in cls._providers:
            del cls._providers[name]
            logger.info(f"Unregistered provider: {name}")
    
    @classmethod
    def is_provider_available(cls, name: str) -> bool:
        """Check if a provider is available.
        
        Args:
            name: Provider name
            
        Returns:
            True if provider is available
        """
        name = name.lower()
        if name not in cls._providers:
            return False
        
        try:
            # Try to create a dummy instance to check availability
            provider_class = cls._providers[name]
            config = ProviderConfig(
                provider_name=name,
                model="test",
                api_key="test"
            )
            # Don't actually initialize, just check if class is importable
            return True
        except UnsupportedProviderError:
            return False
        except Exception:
            # Other exceptions don't necessarily mean unavailable
            return True
    
    @classmethod
    def get_provider_info(cls) -> Dict[str, Any]:
        """Get information about all registered providers.
        
        Returns:
            Dictionary with provider information
        """
        info = {}
        
        for name, provider_class in cls._providers.items():
            try:
                # Get available models if provider has the method
                models = []
                if hasattr(provider_class, 'get_available_models'):
                    # Create a temporary instance to get models
                    temp_config = ProviderConfig(
                        provider_name=name,
                        model="temp",
                        api_key="temp"
                    )
                    try:
                        temp_instance = provider_class(temp_config)
                        models = temp_instance.get_available_models()
                    except:
                        models = []
                
                info[name] = {
                    "class": provider_class.__name__,
                    "available": cls.is_provider_available(name),
                    "models": models,
                    "description": provider_class.__doc__ or "No description available"
                }
            except Exception as e:
                info[name] = {
                    "class": provider_class.__name__,
                    "available": False,
                    "error": str(e),
                    "models": [],
                    "description": "Error getting provider info"
                }
        
        return info