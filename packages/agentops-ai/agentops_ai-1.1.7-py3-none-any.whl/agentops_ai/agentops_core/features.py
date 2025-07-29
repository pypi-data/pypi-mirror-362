"""
AgentOps Feature Management System

This module implements a comprehensive feature flag system that controls:
- Multi-language support (Python, JavaScript, Java, C#, Go)
- Web dashboard capabilities
- Traceability matrix features
- Documentation export capabilities
- Payment integration features
- All features are modular with switch on/off capabilities
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Union
from pathlib import Path
import json
import os
from datetime import datetime


class FeatureCategory(Enum):
    """Categories of features in AgentOps."""
    
    # Core Features
    CORE_ANALYSIS = "core_analysis"
    CORE_GENERATION = "core_generation"
    CORE_EXPORT = "core_export"
    
    # Language Support
    LANGUAGE_PYTHON = "language_python"
    LANGUAGE_JAVASCRIPT = "language_javascript"
    LANGUAGE_JAVA = "language_java"
    LANGUAGE_CSHARP = "language_csharp"
    LANGUAGE_GO = "language_go"
    
    # Advanced Features
    WEB_DASHBOARD = "web_dashboard"
    TRACEABILITY_MATRIX = "traceability_matrix"
    DOCUMENTATION_EXPORT = "documentation_export"
    PAYMENT_INTEGRATION = "payment_integration"
    
    # Quality Features
    QUALITY_GATES = "quality_gates"
    ANALYTICS = "analytics"
    AUDIT_TRAILS = "audit_trails"
    
    # Integration Features
    CI_CD_INTEGRATION = "ci_cd_integration"
    IDE_INTEGRATION = "ide_integration"
    API_ACCESS = "api_access"


class FeatureStatus(Enum):
    """Status of a feature."""
    
    ENABLED = "enabled"
    DISABLED = "disabled"
    BETA = "beta"
    DEPRECATED = "deprecated"


@dataclass
class FeatureConfig:
    """Configuration for a specific feature."""
    
    name: str
    category: FeatureCategory
    status: FeatureStatus
    description: str
    
    # Feature capabilities
    enabled: bool = True
    beta_enabled: bool = False
    deprecated: bool = False
    
    # Dependencies
    dependencies: Set[str] = field(default_factory=set)
    conflicts: Set[str] = field(default_factory=set)
    
    # Configuration
    config_options: Dict[str, Any] = field(default_factory=dict)
    default_config: Dict[str, Any] = field(default_factory=dict)
    
    # Usage tracking
    usage_count: int = 0
    last_used: Optional[datetime] = None
    
    # Tier requirements
    required_tier: Optional[str] = None
    tier_override: bool = False


class FeatureManager:
    """Manages all feature flags and capabilities."""
    
    def __init__(self, config_file: str = ".agentops/features.json"):
        """Initialize the feature manager.
        
        Args:
            config_file: Path to feature configuration file
        """
        self.config_file = Path(config_file)
        self.features: Dict[str, FeatureConfig] = {}
        self.enabled_features: Set[str] = set()
        self.disabled_features: Set[str] = set()
        
        # Initialize default features
        self._initialize_default_features()
        
        # Load configuration
        self.load_config()
    
    def _initialize_default_features(self):
        """Initialize all default features."""
        
        default_features = {
            # Core Features (Always Available)
            "core_analysis": FeatureConfig(
                name="Core Analysis",
                category=FeatureCategory.CORE_ANALYSIS,
                status=FeatureStatus.ENABLED,
                description="Basic code analysis and requirements extraction",
                enabled=True,
                required_tier="developer"
            ),
            
            "core_generation": FeatureConfig(
                name="Core Generation",
                category=FeatureCategory.CORE_GENERATION,
                status=FeatureStatus.ENABLED,
                description="Basic test generation capabilities",
                enabled=True,
                dependencies={"core_analysis"},
                required_tier="developer"
            ),
            
            "core_export": FeatureConfig(
                name="Core Export",
                category=FeatureCategory.CORE_EXPORT,
                status=FeatureStatus.ENABLED,
                description="Basic export capabilities (Gherkin)",
                enabled=True,
                dependencies={"core_generation"},
                required_tier="developer"
            ),
            
            # Language Support Features
            "language_python": FeatureConfig(
                name="Python Support",
                category=FeatureCategory.LANGUAGE_PYTHON,
                status=FeatureStatus.ENABLED,
                description="Full Python language support with AST analysis",
                enabled=True,
                required_tier="developer"
            ),
            
            "language_javascript": FeatureConfig(
                name="JavaScript Support",
                category=FeatureCategory.LANGUAGE_JAVASCRIPT,
                status=FeatureStatus.BETA,
                description="JavaScript/TypeScript language support",
                enabled=False,
                beta_enabled=True,
                required_tier="professional",
                config_options={
                    "framework": "jest",
                    "parser": "babel",
                    "test_runner": "jest"
                },
                default_config={
                    "framework": "jest",
                    "parser": "babel"
                }
            ),
            
            "language_java": FeatureConfig(
                name="Java Support",
                category=FeatureCategory.LANGUAGE_JAVA,
                status=FeatureStatus.BETA,
                description="Java language support with Maven/Gradle",
                enabled=False,
                beta_enabled=True,
                required_tier="professional",
                config_options={
                    "framework": "junit",
                    "build_tool": "maven",
                    "test_runner": "junit"
                },
                default_config={
                    "framework": "junit",
                    "build_tool": "maven"
                }
            ),
            
            "language_csharp": FeatureConfig(
                name="C# Support",
                category=FeatureCategory.LANGUAGE_CSHARP,
                status=FeatureStatus.BETA,
                description="C# language support with .NET",
                enabled=False,
                beta_enabled=True,
                required_tier="professional",
                config_options={
                    "framework": "nunit",
                    "build_tool": "dotnet",
                    "test_runner": "nunit"
                },
                default_config={
                    "framework": "nunit",
                    "build_tool": "dotnet"
                }
            ),
            
            "language_go": FeatureConfig(
                name="Go Support",
                category=FeatureCategory.LANGUAGE_GO,
                status=FeatureStatus.BETA,
                description="Go language support with testing",
                enabled=False,
                beta_enabled=True,
                required_tier="professional",
                config_options={
                    "framework": "testing",
                    "build_tool": "go",
                    "test_runner": "go test"
                },
                default_config={
                    "framework": "testing",
                    "build_tool": "go"
                }
            ),
            
            # Advanced Features
            "web_dashboard": FeatureConfig(
                name="Web Dashboard",
                category=FeatureCategory.WEB_DASHBOARD,
                status=FeatureStatus.BETA,
                description="Web-based dashboard for project management",
                enabled=False,
                beta_enabled=True,
                required_tier="team",
                config_options={
                    "port": 3000,
                    "host": "localhost",
                    "auth_enabled": True,
                    "analytics_enabled": True
                },
                default_config={
                    "port": 3000,
                    "host": "localhost",
                    "auth_enabled": True
                }
            ),
            
            "traceability_matrix": FeatureConfig(
                name="Traceability Matrix",
                category=FeatureCategory.TRACEABILITY_MATRIX,
                status=FeatureStatus.ENABLED,
                description="Bidirectional traceability between requirements and tests",
                enabled=False,
                required_tier="professional",
                config_options={
                    "export_formats": ["markdown", "json", "yaml"],
                    "include_coverage": True,
                    "auto_update": True
                },
                default_config={
                    "export_formats": ["markdown"],
                    "include_coverage": True
                }
            ),
            
            "documentation_export": FeatureConfig(
                name="Documentation Export",
                category=FeatureCategory.DOCUMENTATION_EXPORT,
                status=FeatureStatus.ENABLED,
                description="Professional documentation export capabilities",
                enabled=False,
                required_tier="professional",
                config_options={
                    "formats": ["markdown", "json", "yaml"],
                    "templates": ["professional", "minimal", "detailed"],
                    "include_diagrams": True
                },
                default_config={
                    "formats": ["markdown"],
                    "templates": ["professional"]
                }
            ),
            
            "payment_integration": FeatureConfig(
                name="Payment Integration",
                category=FeatureCategory.PAYMENT_INTEGRATION,
                status=FeatureStatus.ENABLED,
                description="Payment processing and feature access control",
                enabled=False,
                required_tier="developer",  # Available to all tiers
                config_options={
                    "providers": ["stripe", "cashfree"],
                    "webhook_enabled": True,
                    "subscription_management": True
                },
                default_config={
                    "providers": ["stripe"],
                    "webhook_enabled": True
                }
            ),
            
            # Quality Features
            "quality_gates": FeatureConfig(
                name="Quality Gates",
                category=FeatureCategory.QUALITY_GATES,
                status=FeatureStatus.ENABLED,
                description="Quality assurance and validation gates",
                enabled=False,
                required_tier="professional",
                config_options={
                    "coverage_threshold": 80,
                    "quality_score_threshold": 0.7,
                    "auto_approval": False
                },
                default_config={
                    "coverage_threshold": 80,
                    "quality_score_threshold": 0.7
                }
            ),
            
            "analytics": FeatureConfig(
                name="Analytics",
                category=FeatureCategory.ANALYTICS,
                status=FeatureStatus.ENABLED,
                description="Usage analytics and reporting",
                enabled=False,
                required_tier="team",
                config_options={
                    "track_usage": True,
                    "performance_metrics": True,
                    "user_behavior": True
                },
                default_config={
                    "track_usage": True,
                    "performance_metrics": True
                }
            ),
            
            "audit_trails": FeatureConfig(
                name="Audit Trails",
                category=FeatureCategory.AUDIT_TRAILS,
                status=FeatureStatus.ENABLED,
                description="Comprehensive audit logging",
                enabled=False,
                required_tier="enterprise",
                config_options={
                    "log_level": "info",
                    "retention_days": 90,
                    "encryption": True
                },
                default_config={
                    "log_level": "info",
                    "retention_days": 90
                }
            ),
            
            # Integration Features
            "ci_cd_integration": FeatureConfig(
                name="CI/CD Integration",
                category=FeatureCategory.CI_CD_INTEGRATION,
                status=FeatureStatus.ENABLED,
                description="Continuous integration and deployment support",
                enabled=False,
                required_tier="professional",
                config_options={
                    "providers": ["github", "gitlab", "jenkins", "circleci"],
                    "webhook_support": True,
                    "auto_deploy": False
                },
                default_config={
                    "providers": ["github"],
                    "webhook_support": True
                }
            ),
            
            "ide_integration": FeatureConfig(
                name="IDE Integration",
                category=FeatureCategory.IDE_INTEGRATION,
                status=FeatureStatus.ENABLED,
                description="IDE plugin and extension support",
                enabled=False,
                required_tier="professional",
                config_options={
                    "ides": ["vscode", "pycharm", "intellij"],
                    "auto_sync": True,
                    "real_time_updates": True
                },
                default_config={
                    "ides": ["vscode"],
                    "auto_sync": True
                }
            ),
            
            "api_access": FeatureConfig(
                name="API Access",
                category=FeatureCategory.API_ACCESS,
                status=FeatureStatus.ENABLED,
                description="REST API access for automation",
                enabled=False,
                required_tier="team",
                config_options={
                    "rate_limit": 1000,
                    "authentication": "jwt",
                    "webhook_support": True
                },
                default_config={
                    "rate_limit": 1000,
                    "authentication": "jwt"
                }
            )
        }
        
        self.features = default_features
    
    def load_config(self):
        """Load feature configuration from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                
                # Update feature states
                if 'enabled_features' in config_data:
                    self.enabled_features = set(config_data['enabled_features'])
                
                if 'disabled_features' in config_data:
                    self.disabled_features = set(config_data['disabled_features'])
                
                # Update feature configurations
                if 'feature_configs' in config_data:
                    for feature_name, config in config_data['feature_configs'].items():
                        if feature_name in self.features:
                            self.features[feature_name].enabled = config.get('enabled', True)
                            self.features[feature_name].config_options.update(config.get('config_options', {}))
                
            except Exception as e:
                print(f"Warning: Failed to load feature config: {e}")
    
    def save_config(self):
        """Save feature configuration to file."""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        config_data = {
            'enabled_features': list(self.enabled_features),
            'disabled_features': list(self.disabled_features),
            'feature_configs': {
                name: {
                    'enabled': feature.enabled,
                    'config_options': feature.config_options
                }
                for name, feature in self.features.items()
            }
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save feature config: {e}")
    
    def enable_feature(self, feature_name: str) -> bool:
        """Enable a specific feature.
        
        Args:
            feature_name: Name of the feature to enable
            
        Returns:
            True if feature was enabled, False otherwise
        """
        if feature_name not in self.features:
            return False
        
        feature = self.features[feature_name]
        
        # Check dependencies
        for dep in feature.dependencies:
            if not self.is_feature_enabled(dep):
                print(f"Warning: Cannot enable {feature_name}, dependency {dep} is not enabled")
                return False
        
        # Check conflicts
        for conflict in feature.conflicts:
            if self.is_feature_enabled(conflict):
                print(f"Warning: Cannot enable {feature_name}, conflicts with {conflict}")
                return False
        
        feature.enabled = True
        self.enabled_features.add(feature_name)
        self.disabled_features.discard(feature_name)
        
        self.save_config()
        return True
    
    def disable_feature(self, feature_name: str) -> bool:
        """Disable a specific feature.
        
        Args:
            feature_name: Name of the feature to disable
            
        Returns:
            True if feature was disabled, False otherwise
        """
        if feature_name not in self.features:
            return False
        
        # Check if other features depend on this one
        dependent_features = [
            name for name, feature in self.features.items()
            if feature_name in feature.dependencies and feature.enabled
        ]
        
        if dependent_features:
            print(f"Warning: Cannot disable {feature_name}, features depend on it: {dependent_features}")
            return False
        
        self.features[feature_name].enabled = False
        self.enabled_features.discard(feature_name)
        self.disabled_features.add(feature_name)
        
        self.save_config()
        return True
    
    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if a feature is enabled.
        
        Args:
            feature_name: Name of the feature to check
            
        Returns:
            True if feature is enabled, False otherwise
        """
        if feature_name not in self.features:
            return False
        
        feature = self.features[feature_name]
        return feature.enabled and feature.status != FeatureStatus.DEPRECATED
    
    def get_enabled_features(self) -> List[str]:
        """Get list of all enabled features.
        
        Returns:
            List of enabled feature names
        """
        return [name for name in self.features.keys() if self.is_feature_enabled(name)]
    
    def get_feature_config(self, feature_name: str) -> Optional[FeatureConfig]:
        """Get configuration for a specific feature.
        
        Args:
            feature_name: Name of the feature
            
        Returns:
            Feature configuration or None if not found
        """
        return self.features.get(feature_name)
    
    def get_features_by_category(self, category: FeatureCategory) -> List[str]:
        """Get all features in a specific category.
        
        Args:
            category: Feature category to filter by
            
        Returns:
            List of feature names in the category
        """
        return [
            name for name, feature in self.features.items()
            if feature.category == category
        ]
    
    def get_language_features(self) -> List[str]:
        """Get all language support features.
        
        Returns:
            List of language feature names
        """
        language_categories = [
            FeatureCategory.LANGUAGE_PYTHON,
            FeatureCategory.LANGUAGE_JAVASCRIPT,
            FeatureCategory.LANGUAGE_JAVA,
            FeatureCategory.LANGUAGE_CSHARP,
            FeatureCategory.LANGUAGE_GO
        ]
        
        features = []
        for category in language_categories:
            features.extend(self.get_features_by_category(category))
        
        return features
    
    def get_enabled_languages(self) -> List[str]:
        """Get list of enabled language features.
        
        Returns:
            List of enabled language names
        """
        language_features = self.get_language_features()
        return [name for name in language_features if self.is_feature_enabled(name)]
    
    def set_feature_config(self, feature_name: str, config: Dict[str, Any]) -> bool:
        """Set configuration for a specific feature.
        
        Args:
            feature_name: Name of the feature
            config: Configuration dictionary
            
        Returns:
            True if configuration was set, False otherwise
        """
        if feature_name not in self.features:
            return False
        
        feature = self.features[feature_name]
        feature.config_options.update(config)
        
        self.save_config()
        return True
    
    def check_feature_access(self, feature_name: str, tier: str = "developer") -> bool:
        """Check if a feature is accessible for a given tier.
        
        Args:
            feature_name: Name of the feature to check
            tier: User's pricing tier
            
        Returns:
            True if feature is accessible, False otherwise
        """
        if feature_name not in self.features:
            return False
        
        feature = self.features[feature_name]
        
        # Check if feature is enabled
        if not feature.enabled:
            return False
        
        # Check tier requirements
        if feature.required_tier and not self._check_tier_access(tier, feature.required_tier):
            return False
        
        return True
    
    def _check_tier_access(self, user_tier: str, required_tier: str) -> bool:
        """Check if user tier meets required tier.
        
        Args:
            user_tier: User's pricing tier
            required_tier: Required pricing tier
            
        Returns:
            True if user tier meets requirement, False otherwise
        """
        tier_hierarchy = {
            "developer": 0,
            "professional": 1,
            "team": 2,
            "enterprise": 3,
            "enterprise_plus": 4
        }
        
        user_level = tier_hierarchy.get(user_tier, 0)
        required_level = tier_hierarchy.get(required_tier, 0)
        
        return user_level >= required_level
    
    def get_feature_status_summary(self) -> Dict[str, Any]:
        """Get a summary of all feature statuses.
        
        Returns:
            Dictionary with feature status summary
        """
        summary = {
            'total_features': len(self.features),
            'enabled_features': len(self.get_enabled_features()),
            'disabled_features': len(self.disabled_features),
            'beta_features': len([f for f in self.features.values() if f.status == FeatureStatus.BETA]),
            'categories': {}
        }
        
        # Group by category
        for category in FeatureCategory:
            category_features = self.get_features_by_category(category)
            enabled_count = len([f for f in category_features if self.is_feature_enabled(f)])
            summary['categories'][category.value] = {
                'total': len(category_features),
                'enabled': enabled_count,
                'features': category_features
            }
        
        return summary


# Global feature manager instance
_feature_manager: Optional[FeatureManager] = None


def get_feature_manager() -> FeatureManager:
    """Get the global feature manager instance.
    
    Returns:
        FeatureManager instance
    """
    global _feature_manager
    if _feature_manager is None:
        _feature_manager = FeatureManager()
    return _feature_manager


def enable_feature(feature_name: str) -> bool:
    """Enable a feature globally.
    
    Args:
        feature_name: Name of the feature to enable
        
    Returns:
        True if feature was enabled, False otherwise
    """
    return get_feature_manager().enable_feature(feature_name)


def disable_feature(feature_name: str) -> bool:
    """Disable a feature globally.
    
    Args:
        feature_name: Name of the feature to disable
        
    Returns:
        True if feature was disabled, False otherwise
    """
    return get_feature_manager().disable_feature(feature_name)


def is_feature_enabled(feature_name: str) -> bool:
    """Check if a feature is enabled globally.
    
    Args:
        feature_name: Name of the feature to check
        
    Returns:
        True if feature is enabled, False otherwise
    """
    return get_feature_manager().is_feature_enabled(feature_name)


def check_feature_access(feature_name: str, tier: str = "developer") -> bool:
    """Check if a feature is accessible for a given tier.
    
    Args:
        feature_name: Name of the feature to check
        tier: User's pricing tier
        
    Returns:
        True if feature is accessible, False otherwise
    """
    return get_feature_manager().check_feature_access(feature_name, tier) 