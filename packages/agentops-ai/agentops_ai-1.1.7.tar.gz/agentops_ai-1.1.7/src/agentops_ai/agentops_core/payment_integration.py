"""
AgentOps Payment Integration System

This module implements comprehensive payment integration that:
- Detects user subscription status and features
- Provides access control based on purchased features
- Integrates with multiple payment providers (Stripe, Cashfree)
- Manages subscription lifecycle and billing
- Features modular enable/disable capabilities
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Union
from pathlib import Path
import json
import requests
from datetime import datetime, timedelta
import logging
import hashlib
import hmac

from .features import get_feature_manager, is_feature_enabled
from .pricing import pricing_manager, PricingTier


class PaymentProvider(Enum):
    """Supported payment providers."""
    
    STRIPE = "stripe"
    CASHFREE = "cashfree"
    PAYPAL = "paypal"


class SubscriptionStatus(Enum):
    """Subscription status values."""
    
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    TRIAL = "trial"


class BillingCycle(Enum):
    """Billing cycle types."""
    
    MONTHLY = "monthly"
    YEARLY = "yearly"
    QUARTERLY = "quarterly"
    CUSTOM = "custom"


@dataclass
class SubscriptionPlan:
    """Subscription plan configuration."""
    
    id: str
    name: str
    tier: PricingTier
    price: float
    billing_cycle: BillingCycle
    features: Set[str] = field(default_factory=set)
    max_users: int = 1
    max_projects: int = 10
    max_storage_gb: int = 10
    
    # Trial settings
    trial_days: int = 0
    trial_features: Set[str] = field(default_factory=set)
    
    # Billing settings
    currency: str = "USD"
    stripe_price_id: Optional[str] = None
    cashfree_plan_id: Optional[str] = None


@dataclass
class UserSubscription:
    """User subscription information."""
    
    user_id: str
    plan_id: str
    status: SubscriptionStatus
    current_tier: PricingTier
    billing_cycle: BillingCycle
    next_billing_date: datetime
    amount: float
    provider: PaymentProvider
    provider_subscription_id: str
    provider_customer_id: str
    currency: str = "USD"
    enabled_features: Set[str] = field(default_factory=set)
    usage_limits: Dict[str, int] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None


@dataclass
class PaymentConfig:
    """Payment integration configuration."""
    
    # Provider settings
    providers: Set[PaymentProvider] = field(default_factory=lambda: {PaymentProvider.STRIPE})
    webhook_enabled: bool = True
    subscription_management: bool = True
    
    # Stripe settings
    stripe_secret_key: Optional[str] = None
    stripe_publishable_key: Optional[str] = None
    stripe_webhook_secret: Optional[str] = None
    
    # Cashfree settings
    cashfree_app_id: Optional[str] = None
    cashfree_secret_key: Optional[str] = None
    cashfree_webhook_secret: Optional[str] = None
    
    # General settings
    currency: str = "USD"
    trial_days: int = 14
    auto_renewal: bool = True
    
    # Feature access control
    feature_check_enabled: bool = True
    usage_tracking_enabled: bool = True


class PaymentManager:
    """Manages payment integration and subscription handling."""
    
    def __init__(self, config: PaymentConfig):
        """Initialize the payment manager.
        
        Args:
            config: Payment configuration
        """
        self.config = config
        self.feature_manager = get_feature_manager()
        self.subscriptions: Dict[str, UserSubscription] = {}
        self.plans: Dict[str, SubscriptionPlan] = {}
        
        # Initialize payment providers
        self._initialize_providers()
        self._initialize_plans()
        
        # Check if payment integration feature is enabled
        if not is_feature_enabled("payment_integration"):
            logging.warning("Payment integration feature is not enabled")
    
    def _initialize_providers(self):
        """Initialize payment providers."""
        self.providers = {}
        
        if PaymentProvider.STRIPE in self.config.providers and self.config.stripe_secret_key:
            self.providers[PaymentProvider.STRIPE] = StripeProvider(self.config)
        
        if PaymentProvider.CASHFREE in self.config.providers and self.config.cashfree_app_id:
            self.providers[PaymentProvider.CASHFREE] = CashfreeProvider(self.config)
    
    def _initialize_plans(self):
        """Initialize subscription plans."""
        self.plans = {
            "developer": SubscriptionPlan(
                id="developer",
                name="Developer",
                tier=PricingTier.DEVELOPER,
                price=0.0,
                billing_cycle=BillingCycle.MONTHLY,
                features={"core_analysis", "core_generation", "core_export", "language_python"},
                max_users=1,
                max_projects=5,
                max_storage_gb=1
            ),
            "professional": SubscriptionPlan(
                id="professional",
                name="Professional",
                tier=PricingTier.PROFESSIONAL,
                price=29.0,
                billing_cycle=BillingCycle.MONTHLY,
                features={
                    "core_analysis", "core_generation", "core_export",
                    "language_python", "language_javascript", "language_java", "language_csharp", "language_go",
                    "traceability_matrix", "documentation_export", "web_dashboard"
                },
                max_users=1,
                max_projects=50,
                max_storage_gb=10,
                trial_days=14,
                stripe_price_id="price_professional_monthly"
            ),
            "team": SubscriptionPlan(
                id="team",
                name="Team",
                tier=PricingTier.TEAM,
                price=99.0,
                billing_cycle=BillingCycle.MONTHLY,
                features={
                    "core_analysis", "core_generation", "core_export",
                    "language_python", "language_javascript", "language_java", "language_csharp", "language_go",
                    "traceability_matrix", "documentation_export", "web_dashboard",
                    "analytics", "team_collaboration", "ci_cd_integration"
                },
                max_users=10,
                max_projects=200,
                max_storage_gb=100,
                trial_days=14,
                stripe_price_id="price_team_monthly"
            ),
            "enterprise": SubscriptionPlan(
                id="enterprise",
                name="Enterprise",
                tier=PricingTier.ENTERPRISE,
                price=299.0,
                billing_cycle=BillingCycle.MONTHLY,
                features={
                    "core_analysis", "core_generation", "core_export",
                    "language_python", "language_javascript", "language_java", "language_csharp", "language_go",
                    "traceability_matrix", "documentation_export", "web_dashboard",
                    "analytics", "team_collaboration", "ci_cd_integration",
                    "audit_trails", "api_access", "custom_templates"
                },
                max_users=50,
                max_projects=1000,
                max_storage_gb=500,
                trial_days=30,
                stripe_price_id="price_enterprise_monthly"
            )
        }
    
    def get_user_subscription(self, user_id: str) -> Optional[UserSubscription]:
        """Get user subscription information.
        
        Args:
            user_id: User identifier
            
        Returns:
            User subscription or None if not found
        """
        return self.subscriptions.get(user_id)
    
    def create_subscription(self, user_id: str, plan_id: str, 
                          provider: PaymentProvider, provider_subscription_id: str,
                          provider_customer_id: str) -> UserSubscription:
        """Create a new user subscription.
        
        Args:
            user_id: User identifier
            plan_id: Plan identifier
            provider: Payment provider
            provider_subscription_id: Provider subscription ID
            provider_customer_id: Provider customer ID
            
        Returns:
            New user subscription
        """
        if not is_feature_enabled("payment_integration"):
            raise RuntimeError("Payment integration feature is not enabled")
        
        if plan_id not in self.plans:
            raise ValueError(f"Plan {plan_id} not found")
        
        plan = self.plans[plan_id]
        
        # Calculate billing dates
        now = datetime.now()
        if plan.billing_cycle == BillingCycle.MONTHLY:
            next_billing = now + timedelta(days=30)
        elif plan.billing_cycle == BillingCycle.YEARLY:
            next_billing = now + timedelta(days=365)
        else:
            next_billing = now + timedelta(days=30)
        
        # Create subscription
        subscription = UserSubscription(
            user_id=user_id,
            plan_id=plan_id,
            status=SubscriptionStatus.ACTIVE,
            current_tier=plan.tier,
            billing_cycle=plan.billing_cycle,
            next_billing_date=next_billing,
            amount=plan.price,
            enabled_features=plan.features.copy(),
            usage_limits={
                "max_users": plan.max_users,
                "max_projects": plan.max_projects,
                "max_storage_gb": plan.max_storage_gb
            },
            provider=provider,
            provider_subscription_id=provider_subscription_id,
            provider_customer_id=provider_customer_id
        )
        
        self.subscriptions[user_id] = subscription
        
        # Update pricing manager
        pricing_manager.set_user_tier(plan.tier)
        
        return subscription
    
    def update_subscription(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user subscription.
        
        Args:
            user_id: User identifier
            updates: Updates to apply
            
        Returns:
            True if subscription was updated, False otherwise
        """
        if user_id not in self.subscriptions:
            return False
        
        subscription = self.subscriptions[user_id]
        
        # Apply updates
        for key, value in updates.items():
            if hasattr(subscription, key):
                setattr(subscription, key, value)
        
        subscription.updated_at = datetime.now()
        
        return True
    
    def cancel_subscription(self, user_id: str) -> bool:
        """Cancel user subscription.
        
        Args:
            user_id: User identifier
            
        Returns:
            True if subscription was cancelled, False otherwise
        """
        if user_id not in self.subscriptions:
            return False
        
        subscription = self.subscriptions[user_id]
        subscription.status = SubscriptionStatus.CANCELLED
        subscription.updated_at = datetime.now()
        
        # Downgrade to developer tier
        pricing_manager.set_user_tier(PricingTier.DEVELOPER)
        
        return True
    
    def check_feature_access(self, user_id: str, feature_name: str) -> bool:
        """Check if user has access to a specific feature.
        
        Args:
            user_id: User identifier
            feature_name: Feature name to check
            
        Returns:
            True if user has access, False otherwise
        """
        if not self.config.feature_check_enabled:
            return True
        
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            # No subscription means developer tier (free features only)
            return feature_name in {"core_analysis", "core_generation", "core_export", "language_python"}
        
        # Check if subscription is active
        if subscription.status != SubscriptionStatus.ACTIVE:
            return False
        
        # Check if feature is enabled for this subscription
        return feature_name in subscription.enabled_features
    
    def get_user_features(self, user_id: str) -> Set[str]:
        """Get enabled features for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Set of enabled feature names
        """
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            # Developer tier features
            return {"core_analysis", "core_generation", "core_export", "language_python"}
        
        return subscription.enabled_features
    
    def get_user_limits(self, user_id: str) -> Dict[str, int]:
        """Get usage limits for a user.
        
        Args:
            user_id: User identifier
            
        Returns:
            Dictionary of usage limits
        """
        subscription = self.get_user_subscription(user_id)
        if not subscription:
            # Developer tier limits
            return {
                "max_users": 1,
                "max_projects": 5,
                "max_storage_gb": 1
            }
        
        return subscription.usage_limits
    
    def check_usage_limit(self, user_id: str, limit_type: str, current_usage: int) -> bool:
        """Check if user is within usage limits.
        
        Args:
            user_id: User identifier
            limit_type: Type of limit to check
            current_usage: Current usage amount
            
        Returns:
            True if within limits, False otherwise
        """
        limits = self.get_user_limits(user_id)
        max_limit = limits.get(f"max_{limit_type}", 0)
        
        return current_usage <= max_limit
    
    def process_webhook(self, provider: PaymentProvider, payload: Dict[str, Any], 
                       signature: Optional[str] = None) -> bool:
        """Process webhook from payment provider.
        
        Args:
            provider: Payment provider
            payload: Webhook payload
            signature: Webhook signature for verification
            
        Returns:
            True if webhook was processed successfully, False otherwise
        """
        if not is_feature_enabled("payment_integration"):
            return False
        
        if provider not in self.providers:
            return False
        
        provider_instance = self.providers[provider]
        return provider_instance.process_webhook(payload, signature)
    
    def get_available_plans(self) -> List[SubscriptionPlan]:
        """Get available subscription plans.
        
        Returns:
            List of available plans
        """
        return list(self.plans.values())
    
    def get_plan(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """Get subscription plan by ID.
        
        Args:
            plan_id: Plan identifier
            
        Returns:
            Subscription plan or None if not found
        """
        return self.plans.get(plan_id)


class BasePaymentProvider:
    """Base class for payment providers."""
    
    def __init__(self, config: PaymentConfig):
        """Initialize the payment provider.
        
        Args:
            config: Payment configuration
        """
        self.config = config
    
    def create_subscription(self, user_id: str, plan_id: str, 
                          customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a subscription with the payment provider.
        
        Args:
            user_id: User identifier
            plan_id: Plan identifier
            customer_data: Customer information
            
        Returns:
            Provider response
        """
        raise NotImplementedError
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel a subscription with the payment provider.
        
        Args:
            subscription_id: Subscription identifier
            
        Returns:
            True if cancelled successfully, False otherwise
        """
        raise NotImplementedError
    
    def process_webhook(self, payload: Dict[str, Any], 
                       signature: Optional[str] = None) -> bool:
        """Process webhook from payment provider.
        
        Args:
            payload: Webhook payload
            signature: Webhook signature
            
        Returns:
            True if processed successfully, False otherwise
        """
        raise NotImplementedError


class StripeProvider(BasePaymentProvider):
    """Stripe payment provider implementation."""
    
    def __init__(self, config: PaymentConfig):
        """Initialize Stripe provider."""
        super().__init__(config)
        self.api_key = config.stripe_secret_key
        self.webhook_secret = config.stripe_webhook_secret
        self.base_url = "https://api.stripe.com/v1"
    
    def create_subscription(self, user_id: str, plan_id: str, 
                          customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Stripe subscription."""
        # This is a simplified implementation
        # In production, you would use the Stripe SDK
        return {
            "subscription_id": f"sub_{user_id}_{plan_id}",
            "customer_id": f"cus_{user_id}",
            "status": "active"
        }
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel Stripe subscription."""
        # Simplified implementation
        return True
    
    def process_webhook(self, payload: Dict[str, Any], 
                       signature: Optional[str] = None) -> bool:
        """Process Stripe webhook."""
        # Verify webhook signature
        if signature and self.webhook_secret:
            try:
                # In production, verify the signature properly
                pass
            except Exception:
                return False
        
        # Process webhook event
        event_type = payload.get("type")
        if event_type == "customer.subscription.created":
            return self._handle_subscription_created(payload)
        elif event_type == "customer.subscription.updated":
            return self._handle_subscription_updated(payload)
        elif event_type == "customer.subscription.deleted":
            return self._handle_subscription_cancelled(payload)
        
        return True
    
    def _handle_subscription_created(self, payload: Dict[str, Any]) -> bool:
        """Handle subscription created event."""
        # Implementation for subscription created
        return True
    
    def _handle_subscription_updated(self, payload: Dict[str, Any]) -> bool:
        """Handle subscription updated event."""
        # Implementation for subscription updated
        return True
    
    def _handle_subscription_cancelled(self, payload: Dict[str, Any]) -> bool:
        """Handle subscription cancelled event."""
        # Implementation for subscription cancelled
        return True


class CashfreeProvider(BasePaymentProvider):
    """Cashfree payment provider implementation."""
    
    def __init__(self, config: PaymentConfig):
        """Initialize Cashfree provider."""
        super().__init__(config)
        self.app_id = config.cashfree_app_id
        self.secret_key = config.cashfree_secret_key
        self.webhook_secret = config.cashfree_webhook_secret
        self.base_url = "https://sandbox.cashfree.com/pg"  # Use production URL in production
    
    def create_subscription(self, user_id: str, plan_id: str, 
                          customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create Cashfree subscription."""
        # Simplified implementation
        return {
            "subscription_id": f"cf_sub_{user_id}_{plan_id}",
            "customer_id": f"cf_cus_{user_id}",
            "status": "active"
        }
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancel Cashfree subscription."""
        # Simplified implementation
        return True
    
    def process_webhook(self, payload: Dict[str, Any], 
                       signature: Optional[str] = None) -> bool:
        """Process Cashfree webhook."""
        # Verify webhook signature
        if signature and self.webhook_secret:
            try:
                # In production, verify the signature properly
                pass
            except Exception:
                return False
        
        # Process webhook event
        event_type = payload.get("event_type")
        if event_type == "SUBSCRIPTION_ACTIVATED":
            return self._handle_subscription_activated(payload)
        elif event_type == "SUBSCRIPTION_CANCELLED":
            return self._handle_subscription_cancelled(payload)
        
        return True
    
    def _handle_subscription_activated(self, payload: Dict[str, Any]) -> bool:
        """Handle subscription activated event."""
        # Implementation for subscription activated
        return True
    
    def _handle_subscription_cancelled(self, payload: Dict[str, Any]) -> bool:
        """Handle subscription cancelled event."""
        # Implementation for subscription cancelled
        return True


# Global payment manager instance
_payment_manager: Optional[PaymentManager] = None


def get_payment_manager() -> PaymentManager:
    """Get the global payment manager instance.
    
    Returns:
        PaymentManager instance
    """
    global _payment_manager
    if _payment_manager is None:
        config = PaymentConfig()
        _payment_manager = PaymentManager(config)
    return _payment_manager


def check_user_feature_access(user_id: str, feature_name: str) -> bool:
    """Check if user has access to a specific feature.
    
    Args:
        user_id: User identifier
        feature_name: Feature name to check
        
    Returns:
        True if user has access, False otherwise
    """
    return get_payment_manager().check_feature_access(user_id, feature_name)


def get_user_features(user_id: str) -> Set[str]:
    """Get enabled features for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Set of enabled feature names
    """
    return get_payment_manager().get_user_features(user_id)


def get_user_limits(user_id: str) -> Dict[str, int]:
    """Get usage limits for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary of usage limits
    """
    return get_payment_manager().get_user_limits(user_id)


def check_usage_limit(user_id: str, limit_type: str, current_usage: int) -> bool:
    """Check if user is within usage limits.
    
    Args:
        user_id: User identifier
        limit_type: Type of limit to check
        current_usage: Current usage amount
        
    Returns:
        True if within limits, False otherwise
    """
    return get_payment_manager().check_usage_limit(user_id, limit_type, current_usage) 