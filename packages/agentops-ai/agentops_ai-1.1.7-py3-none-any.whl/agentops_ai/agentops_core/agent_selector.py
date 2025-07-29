"""
AgentOps Agent Selection System

This module provides intelligent agent selection based on:
- Pricing tier access control
- User preferences and customization
- Workflow optimization
- Performance requirements
- Context engineering needs
"""

from typing import Dict, List, Set, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
from pathlib import Path

from .pricing import (
    PricingTier, AgentType, ContextEngineering, 
    pricing_manager, check_agent_access
)
from .documentation_export import ExportFormat


class WorkflowMode(Enum):
    """Different workflow execution modes."""
    
    MINIMAL = "minimal"           # Fastest, basic functionality
    STANDARD = "standard"         # Balanced speed and quality
    COMPREHENSIVE = "comprehensive"  # Full analysis, highest quality
    CUSTOM = "custom"            # User-defined agent selection


class AgentPriority(Enum):
    """Agent execution priority levels."""
    
    CRITICAL = "critical"        # Must run for basic functionality
    HIGH = "high"               # Important for quality
    MEDIUM = "medium"           # Valuable but optional
    LOW = "low"                 # Nice to have


@dataclass
class AgentConfig:
    """Configuration for individual agents."""
    
    agent_type: AgentType
    enabled: bool = True
    priority: AgentPriority = AgentPriority.MEDIUM
    parallel_compatible: bool = True
    dependencies: Set[AgentType] = field(default_factory=set)
    context_requirements: Set[ContextEngineering] = field(default_factory=set)
    
    # Performance settings
    timeout_seconds: int = 300
    retry_attempts: int = 2
    memory_limit_mb: int = 512
    
    # Quality settings
    confidence_threshold: float = 0.7
    quality_gate_enabled: bool = True
    
    # Model settings
    model_override: Optional[str] = None
    temperature_override: Optional[float] = None
    max_tokens_override: Optional[int] = None


@dataclass
class WorkflowConfig:
    """Complete workflow configuration."""
    
    mode: WorkflowMode
    selected_agents: Set[AgentType]
    agent_configs: Dict[AgentType, AgentConfig]
    
    # Execution settings
    parallel_execution: bool = True
    max_parallel_workers: int = 4
    fail_fast: bool = False
    continue_on_error: bool = True
    
    # Context engineering
    context_engineering_enabled: Set[ContextEngineering] = field(default_factory=set)
    
    # Output settings
    export_formats: Set[str] = field(default_factory=set)
    output_directory: str = ".agentops"
    
    # Quality settings
    quality_gates_enabled: bool = True
    minimum_quality_score: float = 0.6
    
    def copy(self) -> 'WorkflowConfig':
        """Create a copy of this configuration."""
        return WorkflowConfig(
            mode=self.mode,
            selected_agents=self.selected_agents.copy(),
            agent_configs=self.agent_configs.copy(),
            parallel_execution=self.parallel_execution,
            max_parallel_workers=self.max_parallel_workers,
            fail_fast=self.fail_fast,
            continue_on_error=self.continue_on_error,
            context_engineering_enabled=self.context_engineering_enabled.copy(),
            export_formats=self.export_formats.copy(),
            output_directory=self.output_directory,
            quality_gates_enabled=self.quality_gates_enabled,
            minimum_quality_score=self.minimum_quality_score
        )


class AgentSelector:
    """Intelligent agent selection and workflow configuration."""
    
    def __init__(self):
        """Initialize the agent selector with default configurations."""
        self.agent_registry = self._initialize_agent_registry()
        self.workflow_presets = self._initialize_workflow_presets()
        self.user_preferences = {}
    
    def _initialize_agent_registry(self) -> Dict[AgentType, AgentConfig]:
        """Initialize the registry of all available agents with their configurations."""
        
        return {
            # Core agents (essential for basic functionality)
            AgentType.CODE_ANALYZER: AgentConfig(
                agent_type=AgentType.CODE_ANALYZER,
                priority=AgentPriority.CRITICAL,
                parallel_compatible=True,
                dependencies=set(),
                context_requirements={
                    ContextEngineering.CURRENT_STATE_UNDERSTANDING
                },
                timeout_seconds=120,
                confidence_threshold=0.9
            ),
            
            AgentType.REQUIREMENTS_ENGINEER: AgentConfig(
                agent_type=AgentType.REQUIREMENTS_ENGINEER,
                priority=AgentPriority.CRITICAL,
                parallel_compatible=False,  # Needs code analysis first
                dependencies={AgentType.CODE_ANALYZER},
                context_requirements={
                    ContextEngineering.REQUIREMENTS_GENERATION
                },
                timeout_seconds=180,
                confidence_threshold=0.8
            ),
            
            AgentType.TEST_GENERATOR: AgentConfig(
                agent_type=AgentType.TEST_GENERATOR,
                priority=AgentPriority.CRITICAL,
                parallel_compatible=False,  # Needs requirements
                dependencies={AgentType.REQUIREMENTS_ENGINEER},
                timeout_seconds=240,
                confidence_threshold=0.7
            ),
            
            # Value-add agents (enhance quality and functionality)
            AgentType.TEST_ARCHITECT: AgentConfig(
                agent_type=AgentType.TEST_ARCHITECT,
                priority=AgentPriority.HIGH,
                parallel_compatible=False,
                dependencies={AgentType.REQUIREMENTS_ENGINEER},
                context_requirements={
                    ContextEngineering.ARCHITECTURE_GENERATION
                },
                timeout_seconds=150,
                confidence_threshold=0.8
            ),
            
            AgentType.QUALITY_ASSURANCE: AgentConfig(
                agent_type=AgentType.QUALITY_ASSURANCE,
                priority=AgentPriority.HIGH,
                parallel_compatible=False,
                dependencies={AgentType.TEST_GENERATOR},
                timeout_seconds=120,
                confidence_threshold=0.9,
                quality_gate_enabled=True
            ),
            
            AgentType.INTEGRATION_SPECIALIST: AgentConfig(
                agent_type=AgentType.INTEGRATION_SPECIALIST,
                priority=AgentPriority.MEDIUM,
                parallel_compatible=True,
                dependencies={AgentType.TEST_GENERATOR},
                timeout_seconds=90,
                confidence_threshold=0.7
            ),
            
            # Advanced context engineering agents
            AgentType.ARCHITECTURE_ANALYZER: AgentConfig(
                agent_type=AgentType.ARCHITECTURE_ANALYZER,
                priority=AgentPriority.MEDIUM,
                parallel_compatible=True,
                dependencies={AgentType.CODE_ANALYZER},
                context_requirements={
                    ContextEngineering.ARCHITECTURE_GENERATION
                },
                timeout_seconds=200,
                confidence_threshold=0.8
            ),
            
            AgentType.DATA_FLOW_ANALYZER: AgentConfig(
                agent_type=AgentType.DATA_FLOW_ANALYZER,
                priority=AgentPriority.MEDIUM,
                parallel_compatible=True,
                dependencies={AgentType.CODE_ANALYZER},
                context_requirements={
                    ContextEngineering.DATA_FLOWS_UNDERSTANDING
                },
                timeout_seconds=180,
                confidence_threshold=0.8
            ),
            
            AgentType.SUCCESS_CRITERIA_ANALYZER: AgentConfig(
                agent_type=AgentType.SUCCESS_CRITERIA_ANALYZER,
                priority=AgentPriority.LOW,
                parallel_compatible=True,
                dependencies={AgentType.REQUIREMENTS_ENGINEER},
                context_requirements={
                    ContextEngineering.SUCCESS_CRITERIA_UNDERSTANDING
                },
                timeout_seconds=120,
                confidence_threshold=0.7
            ),
            
            AgentType.CURRENT_STATE_ANALYZER: AgentConfig(
                agent_type=AgentType.CURRENT_STATE_ANALYZER,
                priority=AgentPriority.MEDIUM,
                parallel_compatible=True,
                dependencies={AgentType.CODE_ANALYZER},
                context_requirements={
                    ContextEngineering.CURRENT_STATE_UNDERSTANDING
                },
                timeout_seconds=150,
                confidence_threshold=0.8
            ),
            
            AgentType.BUSINESS_RULES_ANALYZER: AgentConfig(
                agent_type=AgentType.BUSINESS_RULES_ANALYZER,
                priority=AgentPriority.LOW,
                parallel_compatible=True,
                dependencies={AgentType.REQUIREMENTS_ENGINEER},
                timeout_seconds=130,
                confidence_threshold=0.7
            )
        }
    
    def _initialize_workflow_presets(self) -> Dict[WorkflowMode, WorkflowConfig]:
        """Initialize predefined workflow configurations."""
        
        return {
            WorkflowMode.MINIMAL: WorkflowConfig(
                mode=WorkflowMode.MINIMAL,
                selected_agents={
                    AgentType.REQUIREMENTS_ENGINEER,
                    AgentType.TEST_GENERATOR
                },
                agent_configs={},
                parallel_execution=False,
                max_parallel_workers=1,
                context_engineering_enabled={
                    ContextEngineering.REQUIREMENTS_GENERATION
                },
                export_formats={"gherkin"},
                quality_gates_enabled=False,
                minimum_quality_score=0.5
            ),
            
            WorkflowMode.STANDARD: WorkflowConfig(
                mode=WorkflowMode.STANDARD,
                selected_agents={
                    AgentType.CODE_ANALYZER,
                    AgentType.REQUIREMENTS_ENGINEER,
                    AgentType.TEST_ARCHITECT,
                    AgentType.TEST_GENERATOR,
                    AgentType.QUALITY_ASSURANCE
                },
                agent_configs={},
                parallel_execution=True,
                max_parallel_workers=4,
                context_engineering_enabled={
                    ContextEngineering.REQUIREMENTS_GENERATION,
                    ContextEngineering.ARCHITECTURE_GENERATION
                },
                export_formats={"gherkin", "markdown"},
                quality_gates_enabled=True,
                minimum_quality_score=0.7
            ),
            
            WorkflowMode.COMPREHENSIVE: WorkflowConfig(
                mode=WorkflowMode.COMPREHENSIVE,
                selected_agents=set(AgentType),  # All agents
                agent_configs={},
                parallel_execution=True,
                max_parallel_workers=8,
                context_engineering_enabled=set(ContextEngineering),  # All context
                export_formats={"gherkin", "markdown", "json", "yaml"},
                quality_gates_enabled=True,
                minimum_quality_score=0.8
            )
        }
    
    def select_agents_for_tier(self, tier: PricingTier, 
                              mode: WorkflowMode = WorkflowMode.STANDARD) -> WorkflowConfig:
        """Select appropriate agents based on pricing tier and workflow mode."""
        
        # Get tier features
        tier_features = pricing_manager.get_tier_features(tier)
        
        # Start with preset configuration
        base_config = self.workflow_presets[mode].copy() if mode != WorkflowMode.CUSTOM else WorkflowConfig(
            mode=WorkflowMode.CUSTOM,
            selected_agents=set(),
            agent_configs={}
        )
        
        # Filter agents based on tier access
        available_agents = tier_features.available_agents
        selected_agents = base_config.selected_agents.intersection(available_agents)
        
        # Ensure dependencies are met
        selected_agents = self._resolve_dependencies(selected_agents, available_agents)
        
        # Apply tier limitations
        base_config.selected_agents = selected_agents
        base_config.max_parallel_workers = min(
            base_config.max_parallel_workers,
            tier_features.max_parallel_workers
        )
        base_config.parallel_execution = (
            base_config.parallel_execution and tier_features.parallel_processing
        )
        
        # Filter context engineering based on tier
        base_config.context_engineering_enabled = (
            base_config.context_engineering_enabled.intersection(
                tier_features.context_engineering
            )
        )
        
        # Filter export formats based on tier
        available_formats = {fmt.value for fmt in tier_features.export_formats}
        base_config.export_formats = base_config.export_formats.intersection(available_formats)
        
        # Configure individual agents
        for agent_type in selected_agents:
            if agent_type in self.agent_registry:
                base_config.agent_configs[agent_type] = self.agent_registry[agent_type]
        
        return base_config
    
    def _resolve_dependencies(self, selected_agents: Set[AgentType], 
                            available_agents: Set[AgentType]) -> Set[AgentType]:
        """Resolve agent dependencies and add required agents."""
        
        resolved_agents = set(selected_agents)
        changed = True
        
        while changed:
            changed = False
            for agent_type in list(resolved_agents):
                if agent_type in self.agent_registry:
                    dependencies = self.agent_registry[agent_type].dependencies
                    for dep in dependencies:
                        if dep in available_agents and dep not in resolved_agents:
                            resolved_agents.add(dep)
                            changed = True
        
        return resolved_agents
    
    def customize_workflow(self, base_config: WorkflowConfig, 
                          customizations: Dict[str, Any]) -> WorkflowConfig:
        """Apply user customizations to a workflow configuration."""
        
        config = base_config.copy()
        
        # Apply agent selection customizations
        if "enabled_agents" in customizations:
            enabled = set(AgentType(a) for a in customizations["enabled_agents"])
            config.selected_agents = config.selected_agents.intersection(enabled)
        
        if "disabled_agents" in customizations:
            disabled = set(AgentType(a) for a in customizations["disabled_agents"])
            config.selected_agents = config.selected_agents - disabled
        
        # Apply performance customizations
        if "max_parallel_workers" in customizations:
            tier_max = pricing_manager.get_max_parallel_workers()
            config.max_parallel_workers = min(
                customizations["max_parallel_workers"], 
                tier_max
            )
        
        if "parallel_execution" in customizations:
            tier_parallel = pricing_manager.check_feature_access("parallel_processing")
            config.parallel_execution = customizations["parallel_execution"] and tier_parallel
        
        # Apply quality customizations
        if "minimum_quality_score" in customizations:
            config.minimum_quality_score = customizations["minimum_quality_score"]
        
        if "quality_gates_enabled" in customizations:
            config.quality_gates_enabled = customizations["quality_gates_enabled"]
        
        # Apply export format customizations
        if "export_formats" in customizations:
            requested_formats = set(customizations["export_formats"])
            available_formats = set(fmt.value for fmt in pricing_manager.get_available_export_formats())
            config.export_formats = requested_formats.intersection(available_formats)
        
        # Re-resolve dependencies after customization
        available_agents = pricing_manager.get_available_agents()
        config.selected_agents = self._resolve_dependencies(
            config.selected_agents, 
            set(available_agents)
        )
        
        return config
    
    def get_execution_plan(self, config: WorkflowConfig) -> List[List[AgentType]]:
        """Generate an execution plan based on dependencies and parallelization."""
        
        # Build dependency graph
        dependency_graph = {}
        for agent_type in config.selected_agents:
            if agent_type in self.agent_registry:
                dependencies = self.agent_registry[agent_type].dependencies
                dependency_graph[agent_type] = dependencies.intersection(config.selected_agents)
            else:
                dependency_graph[agent_type] = set()
        
        # Topological sort with parallelization
        execution_plan = []
        remaining_agents = set(config.selected_agents)
        
        while remaining_agents:
            # Find agents with no unmet dependencies
            ready_agents = []
            for agent in remaining_agents:
                if dependency_graph[agent].issubset(set().union(*execution_plan) if execution_plan else set()):
                    ready_agents.append(agent)
            
            if not ready_agents:
                # Circular dependency or missing dependency
                raise ValueError(f"Cannot resolve dependencies for agents: {remaining_agents}")
            
            # Group parallel-compatible agents
            if config.parallel_execution:
                parallel_group = []
                sequential_group = []
                
                for agent in ready_agents:
                    agent_config = self.agent_registry.get(agent)
                    if agent_config and agent_config.parallel_compatible:
                        parallel_group.append(agent)
                    else:
                        sequential_group.append(agent)
                
                # Add parallel group first, then sequential
                if parallel_group:
                    execution_plan.append(parallel_group)
                for agent in sequential_group:
                    execution_plan.append([agent])
            else:
                # Sequential execution
                for agent in ready_agents:
                    execution_plan.append([agent])
            
            # Remove processed agents
            remaining_agents -= set(ready_agents)
        
        return execution_plan
    
    def validate_configuration(self, config: WorkflowConfig) -> Tuple[bool, List[str]]:
        """Validate a workflow configuration for the current tier."""
        
        errors = []
        
        # Check tier access for selected agents
        for agent_type in config.selected_agents:
            if not pricing_manager.check_agent_access(agent_type):
                errors.append(f"Agent {agent_type.value} not available in current tier")
        
        # Check parallel processing limits
        if config.parallel_execution and not pricing_manager.check_feature_access("parallel_processing"):
            errors.append("Parallel processing not available in current tier")
        
        if config.max_parallel_workers > pricing_manager.get_max_parallel_workers():
            errors.append(f"Requested {config.max_parallel_workers} workers, but tier limit is {pricing_manager.get_max_parallel_workers()}")
        
        # Check export formats
        for export_format in config.export_formats:
            try:
                format_enum = ExportFormat(export_format)
                if not pricing_manager.check_export_format(format_enum):
                    errors.append(f"Export format {export_format} not available in current tier")
            except ValueError:
                errors.append(f"Unknown export format: {export_format}")
        
        # Check context engineering
        for context_type in config.context_engineering_enabled:
            if not pricing_manager.check_context_engineering(context_type):
                errors.append(f"Context engineering {context_type.value} not available in current tier")
        
        # Check dependencies
        try:
            execution_plan = self.get_execution_plan(config)
        except ValueError as e:
            errors.append(f"Dependency resolution failed: {str(e)}")
        
        return len(errors) == 0, errors
    
    def get_recommendations(self, tier: PricingTier, 
                          file_complexity: str = "medium") -> Dict[str, Any]:
        """Get workflow recommendations based on tier and file complexity."""
        
        recommendations = {
            "recommended_mode": WorkflowMode.STANDARD,
            "recommended_agents": [],
            "performance_tips": [],
            "upgrade_suggestions": []
        }
        
        # Recommend mode based on tier
        if tier == PricingTier.DEVELOPER:
            recommendations["recommended_mode"] = WorkflowMode.MINIMAL
        elif tier in [PricingTier.PROFESSIONAL, PricingTier.TEAM]:
            recommendations["recommended_mode"] = WorkflowMode.STANDARD
        else:
            recommendations["recommended_mode"] = WorkflowMode.COMPREHENSIVE
        
        # Recommend agents based on complexity
        if file_complexity == "low":
            recommendations["recommended_agents"] = [
                AgentType.REQUIREMENTS_ENGINEER,
                AgentType.TEST_GENERATOR
            ]
        elif file_complexity == "medium":
            recommendations["recommended_agents"] = [
                AgentType.CODE_ANALYZER,
                AgentType.REQUIREMENTS_ENGINEER,
                AgentType.TEST_ARCHITECT,
                AgentType.TEST_GENERATOR,
                AgentType.QUALITY_ASSURANCE
            ]
        else:  # high complexity
            recommendations["recommended_agents"] = list(AgentType)
        
        # Filter by tier access
        available_agents = pricing_manager.get_available_agents()
        recommendations["recommended_agents"] = [
            agent for agent in recommendations["recommended_agents"]
            if agent in available_agents
        ]
        
        # Performance tips
        tier_features = pricing_manager.get_tier_features(tier)
        if tier_features.parallel_processing:
            recommendations["performance_tips"].append(
                f"Enable parallel processing with up to {tier_features.max_parallel_workers} workers"
            )
        
        if len(tier_features.export_formats) > 1:
            recommendations["performance_tips"].append(
                "Use multiple export formats for better documentation"
            )
        
        # Upgrade suggestions
        if tier != PricingTier.ENTERPRISE_PLUS:
            next_tier_agents = set()
            for higher_tier in PricingTier:
                if higher_tier.value > tier.value:
                    higher_features = pricing_manager.get_tier_features(higher_tier)
                    next_tier_agents.update(higher_features.available_agents)
            
            missing_agents = next_tier_agents - set(available_agents)
            if missing_agents:
                recommendations["upgrade_suggestions"].append(
                    f"Upgrade to access additional agents: {[a.value for a in missing_agents]}"
                )
        
        return recommendations


# Global agent selector instance
agent_selector = AgentSelector() 