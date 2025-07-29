"""
AgentOps Pricing and Feature Management System

This module implements a comprehensive pricing tier system that controls:
- Agent availability and selection
- Feature access and limitations
- Usage quotas and restrictions
- Model access and configuration
- Export format availability
- Parallel processing limits
- Context engineering capabilities
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Union
from datetime import datetime, timedelta
import json
from pathlib import Path


class PricingTier(Enum):
    """AgentOps pricing tiers with increasing capabilities."""
    
    DEVELOPER = "developer"          # Free tier
    PROFESSIONAL = "professional"    # $29/month
    TEAM = "team"                   # $99/month  
    ENTERPRISE = "enterprise"       # $299/month
    ENTERPRISE_PLUS = "enterprise_plus"  # Custom pricing


class AgentType(Enum):
    """Available agent types in the AgentOps system."""
    
    # Core agents (essential functionality)
    CODE_ANALYZER = "code_analyzer"
    REQUIREMENTS_ENGINEER = "requirements_engineer"
    TEST_GENERATOR = "test_generator"
    
    # Value-add agents (enhanced functionality)
    TEST_ARCHITECT = "test_architect"
    QUALITY_ASSURANCE = "quality_assurance"
    INTEGRATION_SPECIALIST = "integration_specialist"
    
    # Advanced context engineering agents
    ARCHITECTURE_ANALYZER = "architecture_analyzer"
    DATA_FLOW_ANALYZER = "data_flow_analyzer"
    SUCCESS_CRITERIA_ANALYZER = "success_criteria_analyzer"
    CURRENT_STATE_ANALYZER = "current_state_analyzer"
    BUSINESS_RULES_ANALYZER = "business_rules_analyzer"


class ContextEngineering(Enum):
    """Context engineering capabilities."""
    
    REQUIREMENTS_GENERATION = "requirements_generation"
    ARCHITECTURE_GENERATION = "architecture_generation"
    CURRENT_STATE_UNDERSTANDING = "current_state_understanding"
    DATA_FLOWS_UNDERSTANDING = "data_flows_understanding"
    SUCCESS_CRITERIA_UNDERSTANDING = "success_criteria_understanding"


class ExportFormat(Enum):
    """Available export formats for requirements and reports."""
    
    GHERKIN = "gherkin"
    MARKDOWN = "markdown"
    JSON = "json"
    YAML = "yaml"
    CSV = "csv"
    XML = "xml"


class ModelProvider(Enum):
    """Model provider options."""
    
    BYOK = "bring_your_own_key"      # User provides OpenAI/other API keys
    AGENTOPS_OPTIMIZED = "agentops_optimized"  # AgentOps-optimized models
    CUSTOM_FINETUNED = "custom_finetuned"      # Custom fine-tuned models


@dataclass
class UsageQuota:
    """Usage quotas and limits for different pricing tiers."""
    
    files_per_month: int
    lines_of_code_per_month: int
    requirements_per_month: int
    tests_per_month: int
    api_calls_per_month: int
    parallel_workers: int
    max_file_size_mb: int
    
    # Reset tracking
    current_usage: Dict[str, int] = field(default_factory=dict)
    last_reset: datetime = field(default_factory=datetime.now)
    
    def reset_if_needed(self) -> bool:
        """Reset usage counters if a month has passed."""
        now = datetime.now()
        if now - self.last_reset > timedelta(days=30):
            self.current_usage = {}
            self.last_reset = now
            return True
        return False
    
    def check_quota(self, metric: str, amount: int = 1) -> bool:
        """Check if usage is within quota limits."""
        self.reset_if_needed()
        current = self.current_usage.get(metric, 0)
        limit = getattr(self, f"{metric}_per_month", float('inf'))
        return current + amount <= limit
    
    def consume_quota(self, metric: str, amount: int = 1) -> bool:
        """Consume quota if available."""
        if self.check_quota(metric, amount):
            self.current_usage[metric] = self.current_usage.get(metric, 0) + amount
            return True
        return False


@dataclass
class TierFeatures:
    """Feature set for a specific pricing tier."""
    
    # Core features
    tier: PricingTier
    price_per_month: float
    description: str
    
    # Agent access
    available_agents: Set[AgentType]
    agent_selection_enabled: bool = False
    
    # Context engineering
    context_engineering: Set[ContextEngineering] = field(default_factory=set)
    
    # Export capabilities
    export_formats: Set[ExportFormat] = field(default_factory=set)
    
    # Processing capabilities
    parallel_processing: bool = False
    max_parallel_workers: int = 1
    
    # Model access
    model_providers: Set[ModelProvider] = field(default_factory=set)
    
    # Usage quotas
    usage_quota: UsageQuota = field(default_factory=lambda: UsageQuota(0, 0, 0, 0, 0, 1, 10))
    
    # Collaboration features
    team_size_limit: int = 1
    approval_workflows: bool = False
    auto_approval_enabled: bool = False
    role_based_access: bool = False
    
    # Support and SLA
    support_level: str = "community"
    response_time_hours: int = 72
    uptime_sla: float = 0.99
    
    # Advanced features
    ci_cd_integrations: bool = False
    ide_integrations: bool = False
    analytics_dashboard: bool = False
    audit_trails: bool = False
    custom_templates: bool = False
    api_access: bool = False


class PricingManager:
    """Manages pricing tiers, feature access, and usage quotas."""
    
    def __init__(self):
        """Initialize the pricing manager with tier definitions."""
        self.tiers = self._initialize_tiers()
        self.tier = PricingTier.ENTERPRISE  # Force highest tier
        self.current_tier = self.tier  # Compatibility for legacy code
        self.user_config = {}
    
    def _initialize_tiers(self) -> Dict[PricingTier, TierFeatures]:
        """Initialize all pricing tier configurations."""
        
        return {
            PricingTier.DEVELOPER: TierFeatures(
                tier=PricingTier.DEVELOPER,
                price_per_month=0.0,
                description="Free tier for individual developers and open source",
                available_agents={
                    AgentType.REQUIREMENTS_ENGINEER,
                    AgentType.TEST_GENERATOR
                },
                context_engineering={
                    ContextEngineering.REQUIREMENTS_GENERATION
                },
                export_formats={
                    ExportFormat.GHERKIN,
                    ExportFormat.MARKDOWN
                },
                model_providers={
                    ModelProvider.BYOK
                },
                usage_quota=UsageQuota(
                    files_per_month=50,
                    lines_of_code_per_month=10000,
                    requirements_per_month=100,
                    tests_per_month=200,
                    api_calls_per_month=1000,
                    parallel_workers=1,
                    max_file_size_mb=5
                ),
                support_level="community"
            ),
            
            PricingTier.PROFESSIONAL: TierFeatures(
                tier=PricingTier.PROFESSIONAL,
                price_per_month=29.0,
                description="Full workflow for professional developers",
                available_agents={
                    AgentType.CODE_ANALYZER,
                    AgentType.REQUIREMENTS_ENGINEER,
                    AgentType.TEST_ARCHITECT,
                    AgentType.TEST_GENERATOR,
                    AgentType.QUALITY_ASSURANCE,
                    AgentType.INTEGRATION_SPECIALIST
                },
                agent_selection_enabled=True,
                context_engineering={
                    ContextEngineering.REQUIREMENTS_GENERATION,
                    ContextEngineering.ARCHITECTURE_GENERATION,
                    ContextEngineering.DATA_FLOWS_UNDERSTANDING
                },
                export_formats={
                    ExportFormat.GHERKIN,
                    ExportFormat.MARKDOWN,
                    ExportFormat.JSON
                },
                parallel_processing=True,
                max_parallel_workers=4,
                model_providers={
                    ModelProvider.BYOK,
                    ModelProvider.AGENTOPS_OPTIMIZED
                },
                usage_quota=UsageQuota(
                    files_per_month=500,
                    lines_of_code_per_month=100000,
                    requirements_per_month=1000,
                    tests_per_month=2000,
                    api_calls_per_month=10000,
                    parallel_workers=4,
                    max_file_size_mb=25
                ),
                ci_cd_integrations=True,
                ide_integrations=True,
                support_level="email",
                response_time_hours=24
            ),
            
            PricingTier.TEAM: TierFeatures(
                tier=PricingTier.TEAM,
                price_per_month=99.0,
                description="Advanced features for development teams",
                available_agents=set(AgentType),  # All agents
                agent_selection_enabled=True,
                context_engineering=set(ContextEngineering),  # All context engineering
                export_formats={
                    ExportFormat.GHERKIN,
                    ExportFormat.MARKDOWN,
                    ExportFormat.JSON,
                    ExportFormat.YAML,
                    ExportFormat.CSV
                },
                parallel_processing=True,
                max_parallel_workers=8,
                model_providers={
                    ModelProvider.BYOK,
                    ModelProvider.AGENTOPS_OPTIMIZED
                },
                usage_quota=UsageQuota(
                    files_per_month=2000,
                    lines_of_code_per_month=500000,
                    requirements_per_month=5000,
                    tests_per_month=10000,
                    api_calls_per_month=50000,
                    parallel_workers=8,
                    max_file_size_mb=100
                ),
                team_size_limit=10,
                approval_workflows=True,
                auto_approval_enabled=True,
                ci_cd_integrations=True,
                ide_integrations=True,
                analytics_dashboard=True,
                custom_templates=True,
                api_access=True,
                support_level="priority",
                response_time_hours=8,
                uptime_sla=0.995
            ),
            
            PricingTier.ENTERPRISE: TierFeatures(
                tier=PricingTier.ENTERPRISE,
                price_per_month=299.0,
                description="Enterprise-grade features and support",
                available_agents=set(AgentType),  # All agents
                agent_selection_enabled=True,
                context_engineering=set(ContextEngineering),  # All context engineering
                export_formats=set(ExportFormat),  # All formats
                parallel_processing=True,
                max_parallel_workers=16,
                model_providers=set(ModelProvider),  # All providers
                usage_quota=UsageQuota(
                    files_per_month=10000,
                    lines_of_code_per_month=2000000,
                    requirements_per_month=25000,
                    tests_per_month=50000,
                    api_calls_per_month=250000,
                    parallel_workers=16,
                    max_file_size_mb=500
                ),
                team_size_limit=50,
                approval_workflows=True,
                auto_approval_enabled=True,
                role_based_access=True,
                ci_cd_integrations=True,
                ide_integrations=True,
                analytics_dashboard=True,
                audit_trails=True,
                custom_templates=True,
                api_access=True,
                support_level="dedicated",
                response_time_hours=2,
                uptime_sla=0.999
            ),
            
            PricingTier.ENTERPRISE_PLUS: TierFeatures(
                tier=PricingTier.ENTERPRISE_PLUS,
                price_per_month=0.0,  # Custom pricing
                description="White-label and custom enterprise solutions",
                available_agents=set(AgentType),  # All agents + custom
                agent_selection_enabled=True,
                context_engineering=set(ContextEngineering),  # All + custom
                export_formats=set(ExportFormat),  # All + custom
                parallel_processing=True,
                max_parallel_workers=32,
                model_providers=set(ModelProvider),  # All + custom
                usage_quota=UsageQuota(
                    files_per_month=float('inf'),
                    lines_of_code_per_month=float('inf'),
                    requirements_per_month=float('inf'),
                    tests_per_month=float('inf'),
                    api_calls_per_month=float('inf'),
                    parallel_workers=32,
                    max_file_size_mb=1000
                ),
                team_size_limit=float('inf'),
                approval_workflows=True,
                auto_approval_enabled=True,
                role_based_access=True,
                ci_cd_integrations=True,
                ide_integrations=True,
                analytics_dashboard=True,
                audit_trails=True,
                custom_templates=True,
                api_access=True,
                support_level="white_glove",
                response_time_hours=1,
                uptime_sla=0.9999
            )
        }
    
    def get_tier_features(self, tier: PricingTier) -> TierFeatures:
        """Get features for a specific tier."""
        return self.tiers[tier]
    
    def set_user_tier(self, tier: PricingTier):
        """Set the current user's pricing tier."""
        self.current_tier = tier
    
    def check_agent_access(self, agent_type: AgentType) -> bool:
        """Check if current tier has access to specific agent."""
        current_features = self.tiers[self.current_tier]
        return agent_type in current_features.available_agents
    
    def check_feature_access(self, feature: str) -> bool:
        """Check if current tier has access to specific feature."""
        current_features = self.tiers[self.current_tier]
        return getattr(current_features, feature, False)
    
    def check_export_format(self, format_type: ExportFormat) -> bool:
        """Check if current tier supports specific export format."""
        current_features = self.tiers[self.current_tier]
        return format_type in current_features.export_formats
    
    def check_context_engineering(self, context_type: ContextEngineering) -> bool:
        """Check if current tier supports specific context engineering."""
        current_features = self.tiers[self.current_tier]
        return context_type in current_features.context_engineering
    
    def check_usage_quota(self, metric: str, amount: int = 1) -> bool:
        """Check if usage is within quota for current tier."""
        current_features = self.tiers[self.current_tier]
        return current_features.usage_quota.check_quota(metric, amount)
    
    def consume_usage(self, metric: str, amount: int = 1) -> bool:
        """Consume usage quota if available."""
        current_features = self.tiers[self.current_tier]
        return current_features.usage_quota.consume_quota(metric, amount)
    
    def get_available_agents(self) -> List[AgentType]:
        """Get list of agents available for current tier."""
        current_features = self.tiers[self.current_tier]
        return list(current_features.available_agents)
    
    def get_max_parallel_workers(self) -> int:
        """Get maximum parallel workers for current tier."""
        current_features = self.tiers[self.current_tier]
        return current_features.max_parallel_workers
    
    def get_available_export_formats(self) -> List[ExportFormat]:
        """Get available export formats for current tier."""
        current_features = self.tiers[self.current_tier]
        return list(current_features.export_formats)
    
    def get_tier_comparison(self) -> Dict[str, Any]:
        """Get comparison table of all tiers."""
        comparison = {}
        for tier, features in self.tiers.items():
            comparison[tier.value] = {
                "price": features.price_per_month,
                "description": features.description,
                "agents": len(features.available_agents),
                "export_formats": len(features.export_formats),
                "max_workers": features.max_parallel_workers,
                "files_per_month": features.usage_quota.files_per_month,
                "support_level": features.support_level
            }
        return comparison
    
    def upgrade_required_message(self, feature: str, required_tier: PricingTier) -> str:
        """Generate upgrade message for restricted features."""
        current_tier_name = self.current_tier.value.title()
        required_tier_name = required_tier.value.title()
        required_price = self.tiers[required_tier].price_per_month
        
        return (
            f"🔒 {feature} requires {required_tier_name} tier (${required_price}/month)\n"
            f"Current tier: {current_tier_name}\n"
            f"Upgrade to unlock this feature: agentops upgrade {required_tier.value}"
        )


# Global pricing manager instance
pricing_manager = PricingManager()


def check_tier_access(required_tier: PricingTier):
    """Decorator to check tier access for functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if pricing_manager.current_tier.value < required_tier.value:
                raise PermissionError(
                    pricing_manager.upgrade_required_message(
                        func.__name__, required_tier
                    )
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_agent_access(agent_type: AgentType):
    """Decorator to check agent access for functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not pricing_manager.check_agent_access(agent_type):
                available_tiers = [
                    tier.value for tier, features in pricing_manager.tiers.items()
                    if agent_type in features.available_agents
                ]
                raise PermissionError(
                    f"🔒 {agent_type.value} agent not available in current tier.\n"
                    f"Available in: {', '.join(available_tiers)}\n"
                    f"Current tier: {pricing_manager.current_tier.value}"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def check_usage_quota(metric: str, amount: int = 1):
    """Decorator to check and consume usage quota."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not pricing_manager.consume_usage(metric, amount):
                current_features = pricing_manager.tiers[pricing_manager.current_tier]
                limit = getattr(current_features.usage_quota, f"{metric}_per_month", "unlimited")
                raise PermissionError(
                    f"🔒 Monthly {metric} quota exceeded.\n"
                    f"Limit: {limit}\n"
                    f"Upgrade for higher limits: agentops upgrade"
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator 