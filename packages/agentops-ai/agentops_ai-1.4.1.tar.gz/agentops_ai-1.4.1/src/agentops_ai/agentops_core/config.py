"""Configuration module for AgentOps.

Handles all configuration including LLM providers, API keys, and project settings.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


@dataclass
class LLMConfig:
    """Configuration for LLM providers."""

    provider: str = "openai"
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini"
    base_url: Optional[str] = None
    temperature: float = 0.0
    max_tokens: int = 2000

    def __post_init__(self):
        """Set default values from environment variables."""
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY")
        if self.model == "gpt-4o-mini" and os.environ.get("AGENTOPS_MODEL"):
            self.model = os.environ.get("AGENTOPS_MODEL")


@dataclass
class ProjectConfig:
    """Configuration for project settings."""

    project_root: str = "."
    test_framework: str = "pytest"
    test_output_dir: str = ".agentops/tests"
    requirements_file: str = ".agentops/requirements.gherkin"
    exclude_patterns: list = field(
        default_factory=lambda: [
            "tests",
            "__pycache__",
            ".pytest_cache",
            ".agentops",
            "venv",
            "env",
            ".venv",
            ".env",
            ".git",
            ".idea",
            ".vscode",
            "build",
            "dist",
            "*.egg-info",
            "node_modules",
            "coverage",
            ".coverage",
        ]
    )
    include_patterns: list = field(default_factory=list)


@dataclass
class ProblemDiscoveryConfig:
    """Configuration for Problem Discovery Module."""

    enabled: bool = True
    ai_model: str = "gpt-4o-mini"  # Can use different model for problem discovery
    max_conversation_turns: int = 20
    solution_count: int = 4
    auto_advance_stages: bool = False
    web_interface_enabled: bool = True
    web_interface_port: int = 8081
    session_timeout_minutes: int = 60
    save_conversations: bool = True
    conversation_history_limit: int = 100


@dataclass
class HumanInTheLoopConfig:
    """Configuration for Human-in-the-Loop Requirements Engineering."""

    enabled: bool = True
    ai_model: str = "gpt-4o-mini"
    business_context_required: bool = True
    domain_detection_enabled: bool = True
    compliance_detection_enabled: bool = True
    quality_threshold: float = 4.0  # Minimum quality score (1-5)
    max_questions_per_session: int = 15
    auto_approve_high_confidence: bool = (
        False  # Auto-approve requirements with >90% confidence
    )
    validation_required_for_low_confidence: bool = (
        True  # Require human validation for <70% confidence
    )
    learning_enabled: bool = True  # Learn from human feedback

    # Domain-specific knowledge bases
    healthcare_knowledge: bool = True
    finance_knowledge: bool = True
    ecommerce_knowledge: bool = True
    general_compliance: bool = True


@dataclass
class IntegrationConfig:
    """Configuration for integrations."""

    ci_provider: Optional[str] = None
    ide_provider: Optional[str] = None
    webhook_enabled: bool = False
    webhook_port: int = 8080
    webhook_secret: Optional[str] = None
    auto_approve: bool = False
    notification_channels: list = field(default_factory=list)

    # Cursor-specific configuration
    cursor_extension_enabled: bool = True
    cursor_auto_sync: bool = True
    cursor_real_time_validation: bool = True


@dataclass
class NotificationConfig:
    """Configuration for notifications and user feedback."""

    syntax_error_notifications: bool = True
    import_validation_warnings: bool = True
    test_generation_summary: bool = True
    console_output: bool = True
    log_file: Optional[str] = None
    notification_level: str = "info"  # debug, info, warning, error


@dataclass
class ModularFeaturesConfig:
    """Configuration for enabling/disabling modular features."""

    problem_discovery: ProblemDiscoveryConfig = field(
        default_factory=ProblemDiscoveryConfig
    )
    human_in_the_loop: HumanInTheLoopConfig = field(
        default_factory=HumanInTheLoopConfig
    )

    # Feature flags for major modules
    enable_problem_discovery: bool = True
    enable_enhanced_requirements: bool = True
    enable_legacy_requirements: bool = False  # Keep old requirements system as fallback
    enable_quality_assessment: bool = True
    enable_business_context_analysis: bool = True


@dataclass
class AgentOpsConfig:
    """Main configuration class for AgentOps."""

    llm: LLMConfig = field(default_factory=LLMConfig)
    project: ProjectConfig = field(default_factory=ProjectConfig)
    integration: IntegrationConfig = field(default_factory=IntegrationConfig)
    notification: NotificationConfig = field(default_factory=NotificationConfig)
    modules: ModularFeaturesConfig = field(default_factory=ModularFeaturesConfig)
    config_file: str = ".agentops/config.json"

    def __post_init__(self):
        """Load configuration from file if it exists."""
        self.load_config()

    def load_config(self) -> None:
        """Load configuration from file."""
        config_path = Path(self.config_file)
        if config_path.exists():
            try:
                with open(config_path, "r") as f:
                    config_data = json.load(f)
                self._update_from_dict(config_data)
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_file}: {e}")

    def save_config(self) -> None:
        """Save configuration to file."""
        config_path = Path(self.config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)

        config_data = {
            "llm": {
                "provider": self.llm.provider,
                "model": self.llm.model,
                "base_url": self.llm.base_url,
                "temperature": self.llm.temperature,
                "max_tokens": self.llm.max_tokens,
            },
            "project": {
                "test_framework": self.project.test_framework,
                "test_output_dir": self.project.test_output_dir,
                "requirements_file": self.project.requirements_file,
                "exclude_patterns": self.project.exclude_patterns,
                "include_patterns": self.project.include_patterns,
            },
            "integration": {
                "ci_provider": self.integration.ci_provider,
                "ide_provider": self.integration.ide_provider,
                "webhook_enabled": self.integration.webhook_enabled,
                "webhook_port": self.integration.webhook_port,
                "webhook_secret": self.integration.webhook_secret,
                "auto_approve": self.integration.auto_approve,
                "notification_channels": self.integration.notification_channels,
                "cursor_extension_enabled": self.integration.cursor_extension_enabled,
                "cursor_auto_sync": self.integration.cursor_auto_sync,
                "cursor_real_time_validation": self.integration.cursor_real_time_validation,
            },
            "notification": {
                "syntax_error_notifications": self.notification.syntax_error_notifications,
                "import_validation_warnings": self.notification.import_validation_warnings,
                "test_generation_summary": self.notification.test_generation_summary,
                "console_output": self.notification.console_output,
                "log_file": self.notification.log_file,
                "notification_level": self.notification.notification_level,
            },
            "modules": {
                "enable_problem_discovery": self.modules.enable_problem_discovery,
                "enable_enhanced_requirements": self.modules.enable_enhanced_requirements,
                "enable_legacy_requirements": self.modules.enable_legacy_requirements,
                "enable_quality_assessment": self.modules.enable_quality_assessment,
                "enable_business_context_analysis": self.modules.enable_business_context_analysis,
                "problem_discovery": {
                    "enabled": self.modules.problem_discovery.enabled,
                    "ai_model": self.modules.problem_discovery.ai_model,
                    "max_conversation_turns": self.modules.problem_discovery.max_conversation_turns,
                    "solution_count": self.modules.problem_discovery.solution_count,
                    "auto_advance_stages": self.modules.problem_discovery.auto_advance_stages,
                    "web_interface_enabled": self.modules.problem_discovery.web_interface_enabled,
                    "web_interface_port": self.modules.problem_discovery.web_interface_port,
                    "session_timeout_minutes": self.modules.problem_discovery.session_timeout_minutes,
                    "save_conversations": self.modules.problem_discovery.save_conversations,
                    "conversation_history_limit": self.modules.problem_discovery.conversation_history_limit,
                },
                "human_in_the_loop": {
                    "enabled": self.modules.human_in_the_loop.enabled,
                    "ai_model": self.modules.human_in_the_loop.ai_model,
                    "business_context_required": self.modules.human_in_the_loop.business_context_required,
                    "domain_detection_enabled": self.modules.human_in_the_loop.domain_detection_enabled,
                    "compliance_detection_enabled": self.modules.human_in_the_loop.compliance_detection_enabled,
                    "quality_threshold": self.modules.human_in_the_loop.quality_threshold,
                    "max_questions_per_session": self.modules.human_in_the_loop.max_questions_per_session,
                    "auto_approve_high_confidence": self.modules.human_in_the_loop.auto_approve_high_confidence,
                    "validation_required_for_low_confidence": self.modules.human_in_the_loop.validation_required_for_low_confidence,
                    "learning_enabled": self.modules.human_in_the_loop.learning_enabled,
                    "healthcare_knowledge": self.modules.human_in_the_loop.healthcare_knowledge,
                    "finance_knowledge": self.modules.human_in_the_loop.finance_knowledge,
                    "ecommerce_knowledge": self.modules.human_in_the_loop.ecommerce_knowledge,
                    "general_compliance": self.modules.human_in_the_loop.general_compliance,
                },
            },
        }

        try:
            with open(config_path, "w") as f:
                json.dump(config_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save config to {self.config_file}: {e}")

    def _update_from_dict(self, config_data: Dict[str, Any]) -> None:
        """Update configuration from dictionary."""
        if "llm" in config_data:
            llm_data = config_data["llm"]
            for key, value in llm_data.items():
                if hasattr(self.llm, key):
                    setattr(self.llm, key, value)

        if "project" in config_data:
            project_data = config_data["project"]
            for key, value in project_data.items():
                if hasattr(self.project, key):
                    setattr(self.project, key, value)

        if "integration" in config_data:
            integration_data = config_data["integration"]
            for key, value in integration_data.items():
                if hasattr(self.integration, key):
                    setattr(self.integration, key, value)

        if "notification" in config_data:
            notification_data = config_data["notification"]
            for key, value in notification_data.items():
                if hasattr(self.notification, key):
                    setattr(self.notification, key, value)

        if "modules" in config_data:
            modules_data = config_data["modules"]

            # Update top-level module flags
            for key in [
                "enable_problem_discovery",
                "enable_enhanced_requirements",
                "enable_legacy_requirements",
                "enable_quality_assessment",
                "enable_business_context_analysis",
            ]:
                if key in modules_data:
                    setattr(self.modules, key, modules_data[key])

            # Update problem discovery config
            if "problem_discovery" in modules_data:
                pd_data = modules_data["problem_discovery"]
                for key, value in pd_data.items():
                    if hasattr(self.modules.problem_discovery, key):
                        setattr(self.modules.problem_discovery, key, value)

            # Update human-in-the-loop config
            if "human_in_the_loop" in modules_data:
                hitl_data = modules_data["human_in_the_loop"]
                for key, value in hitl_data.items():
                    if hasattr(self.modules.human_in_the_loop, key):
                        setattr(self.modules.human_in_the_loop, key, value)

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.llm.api_key:
            print("Warning: No LLM API key configured")
            return False
        return True

    def initialize_project(self, project_root: str = ".") -> None:
        """Initialize project configuration."""
        self.project.project_root = project_root

        # Create necessary directories
        test_dir = Path(project_root) / self.project.test_output_dir
        test_dir.mkdir(parents=True, exist_ok=True)

        requirements_dir = (
            Path(project_root) / Path(self.project.requirements_file).parent
        )
        requirements_dir.mkdir(parents=True, exist_ok=True)

        config_dir = Path(project_root) / Path(self.config_file).parent
        config_dir.mkdir(parents=True, exist_ok=True)

        # Create additional directories for new modules
        if self.modules.enable_problem_discovery:
            pd_dir = Path(project_root) / ".agentops/problem_discovery"
            pd_dir.mkdir(parents=True, exist_ok=True)

        if self.modules.enable_enhanced_requirements:
            req_dir = Path(project_root) / ".agentops/requirements_db"
            req_dir.mkdir(parents=True, exist_ok=True)

        self.save_config()

    def is_module_enabled(self, module_name: str) -> bool:
        """Check if a specific module is enabled."""
        return getattr(self.modules, f"enable_{module_name}", False)


# Global configuration instance
_config: Optional[AgentOpsConfig] = None


def get_config() -> AgentOpsConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = AgentOpsConfig()
    return _config


def set_config(config: AgentOpsConfig) -> None:
    """Set the global configuration instance."""
    global _config
    _config = config


def reset_config() -> None:
    """Reset the global configuration instance."""
    global _config
    _config = None
