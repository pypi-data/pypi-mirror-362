"""Provider Manager for AgentOps LLM providers.

This module manages multiple LLM providers, handles failover, load balancing,
and provides a unified interface for the multi-agent system.
"""

import asyncio
import logging
import time
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass
from enum import Enum

from .base_provider import (
    BaseLLMProvider, 
    LLMResponse, 
    ProviderStatus,
    ProviderConnectionError,
    ProviderRateLimitError
)
from .provider_factory import LLMProviderFactory

logger = logging.getLogger(__name__)


class LoadBalancingStrategy(Enum):
    """Load balancing strategies for multiple providers."""
    ROUND_ROBIN = "round_robin"
    LEAST_LOADED = "least_loaded"
    FASTEST_RESPONSE = "fastest_response"
    COST_OPTIMIZED = "cost_optimized"
    PRIMARY_FALLBACK = "primary_fallback"


@dataclass
class ProviderWeight:
    """Provider weight configuration for load balancing."""
    provider_name: str
    weight: float = 1.0
    max_requests_per_minute: int = 60
    cost_multiplier: float = 1.0


class ProviderManager:
    """Manages multiple LLM providers with failover and load balancing.
    
    Features:
    - Automatic failover between providers
    - Load balancing with multiple strategies
    - Health monitoring and circuit breaker pattern
    - Cost tracking and optimization
    - Rate limiting across providers
    """
    
    def __init__(self, strategy: LoadBalancingStrategy = LoadBalancingStrategy.PRIMARY_FALLBACK):
        """Initialize the provider manager.
        
        Args:
            strategy: Load balancing strategy to use
        """
        self.strategy = strategy
        self.providers: Dict[str, BaseLLMProvider] = {}
        self.provider_weights: Dict[str, ProviderWeight] = {}
        self.failed_providers: Set[str] = set()
        self.primary_provider: Optional[str] = None
        
        # Round-robin state
        self._round_robin_index = 0
        
        # Circuit breaker state
        self._failure_counts: Dict[str, int] = {}
        self._last_failure_time: Dict[str, float] = {}
        self._circuit_breaker_threshold = 5
        self._circuit_breaker_timeout = 300  # 5 minutes
        
        logger.info(f"Initialized ProviderManager with strategy: {strategy.value}")
    
    def add_provider(
        self, 
        provider: BaseLLMProvider, 
        weight: float = 1.0,
        is_primary: bool = False
    ) -> None:
        """Add a provider to the manager.
        
        Args:
            provider: Provider instance to add
            weight: Weight for load balancing (higher = more requests)
            is_primary: Whether this is the primary provider
        """
        provider_name = provider.config.provider_name
        
        self.providers[provider_name] = provider
        self.provider_weights[provider_name] = ProviderWeight(
            provider_name=provider_name,
            weight=weight,
            max_requests_per_minute=provider.config.rate_limit_per_minute
        )
        
        if is_primary or self.primary_provider is None:
            self.primary_provider = provider_name
        
        # Initialize failure tracking
        self._failure_counts[provider_name] = 0
        self._last_failure_time[provider_name] = 0
        
        logger.info(
            f"Added provider: {provider_name} (primary: {is_primary}, weight: {weight})"
        )
    
    def remove_provider(self, provider_name: str) -> None:
        """Remove a provider from the manager.
        
        Args:
            provider_name: Name of provider to remove
        """
        if provider_name in self.providers:
            del self.providers[provider_name]
            del self.provider_weights[provider_name]
            
            if provider_name in self.failed_providers:
                self.failed_providers.remove(provider_name)
            
            if self.primary_provider == provider_name:
                # Set new primary if available
                if self.providers:
                    self.primary_provider = next(iter(self.providers.keys()))
                else:
                    self.primary_provider = None
            
            logger.info(f"Removed provider: {provider_name}")
    
    async def generate(
        self, 
        prompt: str,
        system_prompt: Optional[str] = None,
        preferred_provider: Optional[str] = None,
        **kwargs
    ) -> LLMResponse:
        """Generate completion using managed providers.
        
        Args:
            prompt: User prompt text
            system_prompt: Optional system prompt
            preferred_provider: Preferred provider name (optional)
            **kwargs: Additional parameters
            
        Returns:
            LLM response from successful provider
            
        Raises:
            ProviderConnectionError: If all providers fail
        """
        if not self.providers:
            raise ProviderConnectionError("No providers available")
        
        # Get ordered list of providers to try
        providers_to_try = self._get_providers_to_try(preferred_provider)
        
        last_error = None
        
        for provider_name in providers_to_try:
            if self._is_circuit_breaker_open(provider_name):
                logger.debug(f"Skipping {provider_name} - circuit breaker open")
                continue
            
            provider = self.providers[provider_name]
            
            try:
                logger.debug(f"Attempting request with provider: {provider_name}")
                
                response = await provider.generate(
                    prompt=prompt,
                    system_prompt=system_prompt,
                    **kwargs
                )
                
                # Reset failure count on success
                self._failure_counts[provider_name] = 0
                if provider_name in self.failed_providers:
                    self.failed_providers.remove(provider_name)
                    logger.info(f"Provider {provider_name} recovered")
                
                logger.info(
                    f"Request successful with {provider_name}: "
                    f"{response.tokens_used} tokens, ${response.cost_estimate:.4f}"
                )
                
                return response
                
            except ProviderRateLimitError as e:
                logger.warning(f"Rate limit hit for {provider_name}: {e}")
                self._mark_provider_failed(provider_name, temporary=True)
                last_error = e
                continue
                
            except ProviderConnectionError as e:
                logger.warning(f"Provider {provider_name} failed: {e}")
                self._mark_provider_failed(provider_name)
                last_error = e
                continue
                
            except Exception as e:
                logger.error(f"Unexpected error with {provider_name}: {e}")
                self._mark_provider_failed(provider_name)
                last_error = e
                continue
        
        # All providers failed
        raise ProviderConnectionError(
            f"All providers failed. Last error: {last_error}"
        )
    
    def _get_providers_to_try(self, preferred_provider: Optional[str] = None) -> List[str]:
        """Get ordered list of providers to try based on strategy.
        
        Args:
            preferred_provider: Preferred provider name
            
        Returns:
            Ordered list of provider names
        """
        available_providers = [
            name for name in self.providers.keys() 
            if name not in self.failed_providers
        ]
        
        if not available_providers:
            # Try failed providers as last resort
            available_providers = list(self.providers.keys())
        
        # If preferred provider is specified and available, try it first
        if preferred_provider and preferred_provider in available_providers:
            providers = [preferred_provider]
            remaining = [p for p in available_providers if p != preferred_provider]
            providers.extend(remaining)
            return providers
        
        # Apply load balancing strategy
        if self.strategy == LoadBalancingStrategy.PRIMARY_FALLBACK:
            if self.primary_provider and self.primary_provider in available_providers:
                providers = [self.primary_provider]
                remaining = [p for p in available_providers if p != self.primary_provider]
                providers.extend(remaining)
                return providers
            else:
                return available_providers
        
        elif self.strategy == LoadBalancingStrategy.ROUND_ROBIN:
            # Rotate through providers
            if available_providers:
                start_idx = self._round_robin_index % len(available_providers)
                providers = available_providers[start_idx:] + available_providers[:start_idx]
                self._round_robin_index += 1
                return providers
        
        elif self.strategy == LoadBalancingStrategy.LEAST_LOADED:
            # Sort by request count (least loaded first)
            return sorted(
                available_providers,
                key=lambda p: self.providers[p].request_count
            )
        
        elif self.strategy == LoadBalancingStrategy.FASTEST_RESPONSE:
            # Sort by average response time
            def avg_response_time(provider_name: str) -> float:
                provider = self.providers[provider_name]
                if provider.request_count == 0:
                    return 0.0  # New providers get priority
                # This is a simplified metric - in reality you'd track response times
                return provider.total_cost / provider.request_count  # Use cost as proxy
            
            return sorted(available_providers, key=avg_response_time)
        
        elif self.strategy == LoadBalancingStrategy.COST_OPTIMIZED:
            # Sort by cost per token (cheapest first)
            def avg_cost_per_token(provider_name: str) -> float:
                provider = self.providers[provider_name]
                if provider.total_tokens == 0:
                    return 0.0
                return provider.total_cost / provider.total_tokens
            
            return sorted(available_providers, key=avg_cost_per_token)
        
        return available_providers
    
    def _mark_provider_failed(self, provider_name: str, temporary: bool = False) -> None:
        """Mark a provider as failed and update circuit breaker state.
        
        Args:
            provider_name: Name of failed provider
            temporary: Whether this is a temporary failure (rate limit)
        """
        self._failure_counts[provider_name] += 1
        self._last_failure_time[provider_name] = time.time()
        
        if not temporary:
            self.failed_providers.add(provider_name)
        
        logger.warning(
            f"Provider {provider_name} failed "
            f"({self._failure_counts[provider_name]} failures)"
        )
    
    def _is_circuit_breaker_open(self, provider_name: str) -> bool:
        """Check if circuit breaker is open for a provider.
        
        Args:
            provider_name: Provider name to check
            
        Returns:
            True if circuit breaker is open
        """
        failure_count = self._failure_counts.get(provider_name, 0)
        last_failure = self._last_failure_time.get(provider_name, 0)
        
        # Circuit breaker is open if too many failures recently
        if failure_count >= self._circuit_breaker_threshold:
            time_since_failure = time.time() - last_failure
            if time_since_failure < self._circuit_breaker_timeout:
                return True
            else:
                # Reset failure count after timeout
                self._failure_counts[provider_name] = 0
                return False
        
        return False
    
    async def health_check_all(self) -> Dict[str, Any]:
        """Perform health check on all providers.
        
        Returns:
            Dictionary with health status of all providers
        """
        results = {}
        
        health_tasks = []
        for name, provider in self.providers.items():
            task = asyncio.create_task(
                self._check_provider_health(name, provider)
            )
            health_tasks.append((name, task))
        
        for name, task in health_tasks:
            try:
                results[name] = await task
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results
    
    async def _check_provider_health(self, name: str, provider: BaseLLMProvider) -> Dict[str, Any]:
        """Check health of a single provider.
        
        Args:
            name: Provider name
            provider: Provider instance
            
        Returns:
            Health status dictionary
        """
        try:
            status = await provider.health_check()
            metrics = provider.get_metrics()
            
            return {
                "status": status.value,
                "healthy": status == ProviderStatus.HEALTHY,
                "metrics": metrics,
                "circuit_breaker_open": self._is_circuit_breaker_open(name),
                "failure_count": self._failure_counts.get(name, 0)
            }
        except Exception as e:
            return {
                "status": "error",
                "healthy": False,
                "error": str(e),
                "circuit_breaker_open": self._is_circuit_breaker_open(name),
                "failure_count": self._failure_counts.get(name, 0)
            }
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the provider manager.
        
        Returns:
            Status dictionary
        """
        return {
            "strategy": self.strategy.value,
            "primary_provider": self.primary_provider,
            "total_providers": len(self.providers),
            "available_providers": len(self.providers) - len(self.failed_providers),
            "failed_providers": list(self.failed_providers),
            "provider_names": list(self.providers.keys())
        }
    
    def reset_failures(self) -> None:
        """Reset all failure tracking."""
        self.failed_providers.clear()
        self._failure_counts.clear()
        self._last_failure_time.clear()
        logger.info("Reset all provider failure tracking")


# Global provider manager instance
_global_provider_manager: Optional[ProviderManager] = None


def get_provider_manager() -> ProviderManager:
    """Get the global provider manager instance.
    
    Returns:
        Global ProviderManager instance
    """
    global _global_provider_manager
    
    if _global_provider_manager is None:
        _global_provider_manager = ProviderManager()
        
        # Try to auto-configure from environment
        try:
            _auto_configure_providers(_global_provider_manager)
        except Exception as e:
            logger.warning(f"Failed to auto-configure providers: {e}")
    
    return _global_provider_manager


def _auto_configure_providers(manager: ProviderManager) -> None:
    """Auto-configure providers from environment variables.
    
    Args:
        manager: Provider manager to configure
    """
    import os
    
    # Try to add OpenAI provider
    if os.getenv("OPENAI_API_KEY"):
        try:
            openai_provider = LLMProviderFactory.create_from_env("openai")
            manager.add_provider(openai_provider, weight=1.0, is_primary=True)
            logger.info("Auto-configured OpenAI provider")
        except Exception as e:
            logger.warning(f"Failed to configure OpenAI provider: {e}")
    
    # Try to add Azure OpenAI provider
    if os.getenv("AZURE_OPENAI_API_KEY") and os.getenv("AZURE_OPENAI_ENDPOINT"):
        try:
            azure_provider = LLMProviderFactory.create_from_env("azure")
            manager.add_provider(azure_provider, weight=0.8)
            logger.info("Auto-configured Azure OpenAI provider")
        except Exception as e:
            logger.warning(f"Failed to configure Azure OpenAI provider: {e}")
    
    # Try to add Gemini provider
    if os.getenv("GEMINI_API_KEY"):
        try:
            gemini_provider = LLMProviderFactory.create_from_env("gemini")
            manager.add_provider(gemini_provider, weight=0.6)
            logger.info("Auto-configured Gemini provider")
        except Exception as e:
            logger.warning(f"Failed to configure Gemini provider: {e}")


def set_provider_manager(manager: ProviderManager) -> None:
    """Set the global provider manager instance.
    
    Args:
        manager: Provider manager to set as global
    """
    global _global_provider_manager
    _global_provider_manager = manager