"""
AgentOps Export Manager

Comprehensive export system supporting multiple formats:
- Gherkin (BDD/ATDD workflows)
- Markdown (Human-readable documentation)
- JSON (API integration and programmatic access)
- YAML (Configuration management and CI/CD)
- CSV (Spreadsheet analysis and reporting)
- XML (Enterprise integration)
- PDF (Professional reports)

Features:
- Template-based export with customization
- Tier-based format access control
- Version control and change tracking
- Cross-reference linking between formats
- Batch export capabilities
"""

from typing import Dict, List, Optional, Any, Set, Union
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import json
import yaml
import csv
import xml.etree.ElementTree as ET
from datetime import datetime
import re
from jinja2 import Template, Environment, FileSystemLoader
import io

from .pricing import ExportFormat, pricing_manager, check_tier_access, PricingTier
from .requirement_store import Requirement


@dataclass
class ExportConfig:
    """Configuration for export operations."""
    
    formats: Set[ExportFormat]
    output_directory: str = ".agentops/exports"
    template_directory: str = ".agentops/templates"
    include_metadata: bool = True
    include_timestamps: bool = True
    cross_reference: bool = True
    version_control: bool = False
    
    # Template customization
    custom_templates: Dict[ExportFormat, str] = field(default_factory=dict)
    template_variables: Dict[str, Any] = field(default_factory=dict)
    
    # Filter options
    status_filter: Optional[List[str]] = None
    priority_filter: Optional[List[str]] = None
    file_filter: Optional[List[str]] = None
    date_range: Optional[tuple] = None


@dataclass
class ExportResult:
    """Result of export operation."""
    
    format: ExportFormat
    success: bool
    file_path: str
    size_bytes: int = 0
    record_count: int = 0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    export_time: datetime = field(default_factory=datetime.now)


class BaseExporter:
    """Base class for format-specific exporters."""
    
    def __init__(self, format_type: ExportFormat):
        """Initialize the exporter."""
        self.format_type = format_type
        self.template_env = None
    
    def setup_templates(self, template_directory: str):
        """Setup Jinja2 template environment."""
        if Path(template_directory).exists():
            self.template_env = Environment(
                loader=FileSystemLoader(template_directory),
                trim_blocks=True,
                lstrip_blocks=True
            )
    
    def export(self, requirements: List[Requirement], 
              config: ExportConfig, 
              context_data: Dict[str, Any] = None) -> ExportResult:
        """Export requirements to specific format."""
        raise NotImplementedError
    
    def _filter_requirements(self, requirements: List[Requirement], 
                           config: ExportConfig) -> List[Requirement]:
        """Apply filters to requirements list."""
        filtered = requirements
        
        if config.status_filter:
            filtered = [r for r in filtered if r.status in config.status_filter]
        
        if config.file_filter:
            filtered = [r for r in filtered if any(pattern in r.file_path for pattern in config.file_filter)]
        
        if config.date_range:
            start_date, end_date = config.date_range
            filtered = [r for r in filtered if start_date <= r.created_at <= end_date]
        
        return filtered
    
    def _prepare_template_data(self, requirements: List[Requirement], 
                              config: ExportConfig,
                              context_data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Prepare data for template rendering."""
        
        # Group requirements by file
        files_requirements = {}
        for req in requirements:
            if req.file_path not in files_requirements:
                files_requirements[req.file_path] = []
            files_requirements[req.file_path].append(req)
        
        # Prepare template data
        template_data = {
            'requirements': requirements,
            'files_requirements': files_requirements,
            'total_count': len(requirements),
            'export_timestamp': datetime.now().isoformat(),
            'format': self.format_type.value,
            'project_name': config.template_variables.get('project_name', 'AgentOps Project'),
            'version': config.template_variables.get('version', '1.0.0'),
            'author': config.template_variables.get('author', 'AgentOps'),
            'include_metadata': config.include_metadata,
            'include_timestamps': config.include_timestamps,
            'cross_reference': config.cross_reference
        }
        
        # Add custom template variables
        template_data.update(config.template_variables)
        
        # Add context data if provided
        if context_data:
            template_data['context'] = context_data
        
        return template_data

    def _get_requirement_context(self, requirement: Requirement) -> Dict[str, Any]:
        """Get additional context for a requirement including clarifications."""
        try:
            from .requirements_clarification import RequirementsClarificationEngine
            engine = RequirementsClarificationEngine()
            
            # Get clarification audit history for this requirement
            audits = engine.get_audit_history(requirement.id)
            
            # Get the most recent clarification if any
            latest_clarification = None
            clarification_count = len(audits)
            
            if audits:
                latest_audit = audits[0]  # Most recent first
                latest_clarification = {
                    'clarified_text': latest_audit.clarified_requirement,
                    'reason': latest_audit.clarification_reason,
                    'timestamp': latest_audit.timestamp,
                    'method': latest_audit.update_method
                }
            
            return {
                'has_clarifications': clarification_count > 0,
                'clarification_count': clarification_count,
                'latest_clarification': latest_clarification,
                'audit_id': latest_audit.audit_id if audits else None
            }
        except Exception:
            # If clarification system not available, return basic info
            return {
                'has_clarifications': False,
                'clarification_count': 0,
                'latest_clarification': None,
                'audit_id': None
            }


class GherkinExporter(BaseExporter):
    """Gherkin format exporter for BDD/ATDD workflows."""
    
    def __init__(self):
        super().__init__(ExportFormat.GHERKIN)
    
    def setup_templates(self, template_directory: str):
        super().setup_templates(template_directory)
        # Register 'basename' filter for Jinja2
        import os
        if self.template_env:
            self.template_env.filters['basename'] = lambda path: os.path.basename(path)
    
    def export(self, requirements: List[Requirement], 
              config: ExportConfig, 
              context_data: Dict[str, Any] = None) -> ExportResult:
        """Export requirements to Gherkin format."""
        
        try:
            filtered_requirements = self._filter_requirements(requirements, config)
            import os
            from jinja2 import Environment, Template
            # Use custom template if provided
            if self.format_type in config.custom_templates:
                template_content = config.custom_templates[self.format_type]
                template = Template(template_content)
            else:
                # Use default template with clarification support
                template_content = self._get_default_gherkin_template()
                template = Template(template_content)
            
            # Prepare context data with clarifications
            context = {
                'requirements': filtered_requirements,
                'project_name': config.template_variables.get('project_name', 'AgentOps Project'),
                'version': config.template_variables.get('version', '1.0.0'),
                'timestamp': datetime.now().isoformat(),
                'total_requirements': len(filtered_requirements)
            }
            
            # Add clarification context for each requirement
            for req in filtered_requirements:
                req.clarification_context = self._get_requirement_context(req)
            
            # Render template
            output = template.render(**context)
            
            # Write to file
            output_file = os.path.join(config.output_directory, "requirements.gherkin")
            os.makedirs(config.output_directory, exist_ok=True)
            
            with open(output_file, 'w') as f:
                f.write(output)
            
            return ExportResult(
                success=True,
                output_file=output_file,
                format_type=self.format_type,
                requirement_count=len(filtered_requirements)
            )
            
        except Exception as e:
            return ExportResult(
                success=False,
                error=str(e),
                format_type=self.format_type
            )
    
    def _get_default_gherkin_template(self) -> str:
        """Get the default Gherkin template with clarification support."""
        return """# AgentOps Requirements File
# Generated: {{ timestamp }}
# Project: {{ project_name }} v{{ version }}
# Total Requirements: {{ total_requirements }}

{% for requirement in requirements %}
# File: {{ requirement.file_path }}
Feature: {{ requirement.code_symbol }} functionality

# Requirement {{ loop.index }} (Global ID: {{ requirement.id }})
  # Status: {{ requirement.status }}
  # Confidence: {{ "%.1f"|format(requirement.confidence * 100) }}%
  # Created: {{ requirement.created_at }}
{% if requirement.clarification_context.has_clarifications %}
  # Clarifications: {{ requirement.clarification_context.clarification_count }} (Latest: {{ requirement.clarification_context.latest_clarification.timestamp }})
  # Audit ID: {{ requirement.clarification_context.audit_id }}
{% endif %}
Scenario: {{ requirement.requirement_text }}
    Given the {{ requirement.code_symbol }} module
    When I use the functionality
    Then it should {{ requirement.requirement_text.lower() }}
{% if requirement.clarification_context.has_clarifications %}
# CLARIFICATION HISTORY:
# Original: {{ requirement.requirement_text }}
# Clarified: {{ requirement.clarification_context.latest_clarification.clarified_text }}
# Reason: {{ requirement.clarification_context.latest_clarification.reason }}
# Method: {{ requirement.clarification_context.latest_clarification.method }}
# For full audit trail, run: agentops audit-history --requirement-id {{ requirement.id }}
{% endif %}

{% endfor %}
"""


class MarkdownExporter(BaseExporter):
    """Markdown format exporter for human-readable documentation."""
    
    def __init__(self):
        super().__init__(ExportFormat.MARKDOWN)
    
    def export(self, requirements: List[Requirement], 
              config: ExportConfig, 
              context_data: Dict[str, Any] = None) -> ExportResult:
        """Export requirements to Markdown format."""
        
        try:
            filtered_requirements = self._filter_requirements(requirements, config)
            # Add sequential numbering for export
            for idx, req in enumerate(filtered_requirements, 1):
                req.export_number = idx
            template_content = self._get_default_markdown_template()
            template = Template(template_content)
            
            template_data = self._prepare_template_data(filtered_requirements, config, context_data)
            content = template.render(**template_data)
            
            output_path = Path(config.output_directory) / "requirements.md"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return ExportResult(
                format=self.format_type,
                success=True,
                file_path=str(output_path),
                size_bytes=len(content.encode('utf-8')),
                record_count=len(filtered_requirements),
                metadata={
                    'files_covered': len(set(req.file_path for req in filtered_requirements)),
                    'status_breakdown': self._get_status_breakdown(filtered_requirements)
                }
            )
            
        except Exception as e:
            return ExportResult(
                format=self.format_type,
                success=False,
                file_path="",
                errors=[str(e)]
            )
    
    def _get_default_markdown_template(self) -> str:
        """Get default Markdown template."""
        return """# {{ project_name }} Requirements

**Generated:** {{ export_timestamp }}  
**Version:** {{ version }}  
**Total Requirements:** {{ total_count }}

## Summary

This document contains {{ total_count }} requirements extracted from {{ files_requirements | length }} files.

{% if context -%}
## Context Analysis

{% if context.architecture -%}
### Architecture Overview
{{ context.architecture.system_overview }}

**Components:** {{ context.architecture.components | length }}  
**Patterns:** {{ context.architecture.patterns | join(', ') }}  
**Technology Stack:** {{ context.architecture.technology_stack | join(', ') }}
{% endif %}
{% endif %}

## Requirements by File

{% for file_path, file_requirements in files_requirements.items() -%}
### {{ file_path }}

{% for req in file_requirements -%}
#### Requirement {{ req.export_number }} (Global ID: {{ req.id }})

**Status:** {{ req.status | title }}  
**Confidence:** {{ "%.1f%%" | format(req.confidence * 100) }}  
{% if include_timestamps -%}
**Created:** {{ req.created_at }}  
{% endif -%}
**Code Symbol:** `{{ req.code_symbol }}`

{{ req.requirement_text }}

{% if req.metadata -%}
**Metadata:**
{% for key, value in req.metadata.items() -%}
- **{{ key | title }}:** {{ value }}
{% endfor %}
{% endif %}

---

{% endfor %}
{% endfor %}

## Statistics

- **Total Requirements:** {{ total_count }}
- **Files Covered:** {{ files_requirements | length }}
- **Average Confidence:** {{ "%.1f%%" | format((requirements | map(attribute='confidence') | sum) / requirements | length * 100) }}

{% if include_metadata -%}
*Generated by AgentOps v{{ version }} on {{ export_timestamp }}*
{% endif %}"""
    
    def _get_status_breakdown(self, requirements: List[Requirement]) -> Dict[str, int]:
        """Get breakdown of requirements by status."""
        breakdown = {}
        for req in requirements:
            breakdown[req.status] = breakdown.get(req.status, 0) + 1
        return breakdown


class JSONExporter(BaseExporter):
    """JSON format exporter for API integration and programmatic access."""
    
    def __init__(self):
        super().__init__(ExportFormat.JSON)
    
    def export(self, requirements: List[Requirement], 
              config: ExportConfig, 
              context_data: Dict[str, Any] = None) -> ExportResult:
        """Export requirements to JSON format."""
        
        try:
            filtered_requirements = self._filter_requirements(requirements, config)
            
            # Convert requirements to dict format
            requirements_data = []
            for req in filtered_requirements:
                req_dict = {
                    'id': req.id,
                    'requirement_text': req.requirement_text,
                    'file_path': req.file_path,
                    'code_symbol': req.code_symbol,
                    'status': req.status,
                    'confidence': req.confidence,
                    'created_at': req.created_at,
                    'metadata': req.metadata or {}
                }
                
                if config.include_metadata:
                    req_dict['commit_hash'] = req.commit_hash
                
                requirements_data.append(req_dict)
            
            # Prepare export data
            export_data = {
                'project': {
                    'name': config.template_variables.get('project_name', 'AgentOps Project'),
                    'version': config.template_variables.get('version', '1.0.0'),
                    'export_timestamp': datetime.now().isoformat(),
                    'total_requirements': len(filtered_requirements)
                },
                'requirements': requirements_data
            }
            
            # Add context data if provided
            if context_data and config.include_metadata:
                export_data['context'] = context_data
            
            # Add statistics
            export_data['statistics'] = {
                'total_count': len(filtered_requirements),
                'files_count': len(set(req.file_path for req in filtered_requirements)),
                'status_breakdown': self._get_status_breakdown(filtered_requirements),
                'average_confidence': sum(req.confidence for req in filtered_requirements) / len(filtered_requirements) if filtered_requirements else 0
            }
            
            output_path = Path(config.output_directory) / "requirements.json"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            return ExportResult(
                format=self.format_type,
                success=True,
                file_path=str(output_path),
                size_bytes=output_path.stat().st_size,
                record_count=len(filtered_requirements),
                metadata=export_data['statistics']
            )
            
        except Exception as e:
            return ExportResult(
                format=self.format_type,
                success=False,
                file_path="",
                errors=[str(e)]
            )
    
    def _get_status_breakdown(self, requirements: List[Requirement]) -> Dict[str, int]:
        """Get breakdown of requirements by status."""
        breakdown = {}
        for req in requirements:
            breakdown[req.status] = breakdown.get(req.status, 0) + 1
        return breakdown


class YAMLExporter(BaseExporter):
    """YAML format exporter for configuration management and CI/CD."""
    
    def __init__(self):
        super().__init__(ExportFormat.YAML)
    
    def export(self, requirements: List[Requirement], 
              config: ExportConfig, 
              context_data: Dict[str, Any] = None) -> ExportResult:
        """Export requirements to YAML format."""
        
        try:
            filtered_requirements = self._filter_requirements(requirements, config)
            
            # Group requirements by file for better YAML structure
            files_data = {}
            for req in filtered_requirements:
                if req.file_path not in files_data:
                    files_data[req.file_path] = []
                
                req_data = {
                    'id': req.id,
                    'text': req.requirement_text,
                    'code_symbol': req.code_symbol,
                    'status': req.status,
                    'confidence': req.confidence,
                    'created_at': req.created_at
                }
                
                if config.include_metadata and req.metadata:
                    req_data['metadata'] = req.metadata
                
                files_data[req.file_path].append(req_data)
            
            # Prepare YAML structure
            yaml_data = {
                'project': {
                    'name': config.template_variables.get('project_name', 'AgentOps Project'),
                    'version': config.template_variables.get('version', '1.0.0'),
                    'export_timestamp': datetime.now().isoformat()
                },
                'requirements': {
                    'total_count': len(filtered_requirements),
                    'files': files_data
                }
            }
            
            if context_data and config.include_metadata:
                yaml_data['context'] = context_data
            
            output_path = Path(config.output_directory) / "requirements.yaml"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            
            return ExportResult(
                format=self.format_type,
                success=True,
                file_path=str(output_path),
                size_bytes=output_path.stat().st_size,
                record_count=len(filtered_requirements),
                metadata={
                    'files_count': len(files_data),
                    'structure': 'hierarchical'
                }
            )
            
        except Exception as e:
            return ExportResult(
                format=self.format_type,
                success=False,
                file_path="",
                errors=[str(e)]
            )


class CSVExporter(BaseExporter):
    """CSV format exporter for spreadsheet analysis and reporting."""
    
    def __init__(self):
        super().__init__(ExportFormat.CSV)
    
    def export(self, requirements: List[Requirement], 
              config: ExportConfig, 
              context_data: Dict[str, Any] = None) -> ExportResult:
        """Export requirements to CSV format."""
        
        try:
            filtered_requirements = self._filter_requirements(requirements, config)
            
            output_path = Path(config.output_directory) / "requirements.csv"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                headers = [
                    'ID', 'Requirement Text', 'File Path', 'Code Symbol', 
                    'Status', 'Confidence', 'Created At'
                ]
                
                if config.include_metadata:
                    headers.extend(['Commit Hash', 'Metadata'])
                
                writer.writerow(headers)
                
                # Write requirements
                for req in filtered_requirements:
                    row = [
                        req.id,
                        req.requirement_text,
                        req.file_path,
                        req.code_symbol,
                        req.status,
                        req.confidence,
                        req.created_at
                    ]
                    
                    if config.include_metadata:
                        row.extend([
                            req.commit_hash or '',
                            json.dumps(req.metadata) if req.metadata else ''
                        ])
                    
                    writer.writerow(row)
            
            return ExportResult(
                format=self.format_type,
                success=True,
                file_path=str(output_path),
                size_bytes=output_path.stat().st_size,
                record_count=len(filtered_requirements),
                metadata={
                    'columns': len(headers),
                    'format': 'tabular'
                }
            )
            
        except Exception as e:
            return ExportResult(
                format=self.format_type,
                success=False,
                file_path="",
                errors=[str(e)]
            )


class ExportManager:
    """Manages all export operations with tier-based access control."""
    
    def __init__(self):
        """Initialize the export manager."""
        self.exporters = {
            ExportFormat.GHERKIN: GherkinExporter(),
            ExportFormat.MARKDOWN: MarkdownExporter(),
            ExportFormat.JSON: JSONExporter(),
            ExportFormat.YAML: YAMLExporter(),
            ExportFormat.CSV: CSVExporter(),
            # XML and PDF exporters would be added here
        }
    
    def export_requirements(self, requirements: List[Requirement], 
                          config: ExportConfig,
                          context_data: Dict[str, Any] = None) -> Dict[ExportFormat, ExportResult]:
        """Export requirements in multiple formats."""
        
        results = {}
        
        for export_format in config.formats:
            # Check tier access
            if not pricing_manager.check_export_format(export_format):
                results[export_format] = ExportResult(
                    format=export_format,
                    success=False,
                    file_path="",
                    errors=[f"Export format {export_format.value} not available in current tier"]
                )
                continue
            
            # Check if exporter exists
            if export_format not in self.exporters:
                results[export_format] = ExportResult(
                    format=export_format,
                    success=False,
                    file_path="",
                    errors=[f"Exporter for {export_format.value} not implemented"]
                )
                continue
            
            # Perform export
            try:
                exporter = self.exporters[export_format]
                exporter.setup_templates(config.template_directory)
                result = exporter.export(requirements, config, context_data)
                results[export_format] = result
            except Exception as e:
                results[export_format] = ExportResult(
                    format=export_format,
                    success=False,
                    file_path="",
                    errors=[str(e)]
                )
        
        return results
    
    def get_available_formats(self) -> List[ExportFormat]:
        """Get list of export formats available for current tier."""
        return pricing_manager.get_available_export_formats()
    
    def create_export_config(self, formats: List[str], **kwargs) -> ExportConfig:
        """Create export configuration with tier validation."""
        
        # Convert string formats to enums
        format_enums = set()
        for fmt in formats:
            try:
                format_enum = ExportFormat(fmt)
                if pricing_manager.check_export_format(format_enum):
                    format_enums.add(format_enum)
            except ValueError:
                pass  # Skip invalid formats
        
        return ExportConfig(
            formats=format_enums,
            **kwargs
        )
    
    def batch_export(self, requirements_list: List[List[Requirement]], 
                    configs: List[ExportConfig],
                    context_data_list: List[Dict[str, Any]] = None) -> List[Dict[ExportFormat, ExportResult]]:
        """Perform batch export operations."""
        
        results = []
        
        for i, (requirements, config) in enumerate(zip(requirements_list, configs)):
            context_data = context_data_list[i] if context_data_list and i < len(context_data_list) else None
            result = self.export_requirements(requirements, config, context_data)
            results.append(result)
        
        return results


# Global export manager instance
export_manager = ExportManager() 