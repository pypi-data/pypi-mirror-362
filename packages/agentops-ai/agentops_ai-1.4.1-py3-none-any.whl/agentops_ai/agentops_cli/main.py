"""AgentOps CLI - Business-Focused Requirements Generation.

Addresses critical issues identified in requirements generation analysis:
- Generates actual business requirements, not code summaries
- Includes ambiguity detection and business context
- Validates requirement quality and provides stakeholder perspective
- Focuses on test generation as primary value proposition

Commands:
- init: Initialize AgentOps project structure
- runner: Complete workflow from business analysis to traceability
- analyze: Deep business requirements analysis
- tests: Generate comprehensive test suites
- status: Check project status
- version: Show version information
"""

import os
import subprocess
import sys
import time
import json
import sqlite3
import re
from pathlib import Path
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import glob

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from rich.syntax import Syntax


# Import the package version dynamically
try:
    from agentops_ai import __version__ as agentops_version
except ImportError:
    agentops_version = "0.2.0"

console = Console()

class RequirementType(Enum):
    FUNCTIONAL = "functional"
    NON_FUNCTIONAL = "non_functional"
    BUSINESS_RULE = "business_rule"
    CONSTRAINT = "constraint"
    AMBIGUITY = "ambiguity"
    QUESTION = "question"

@dataclass
class BusinessRequirement:
    """Represents a proper business requirement."""
    id: str
    type: RequirementType
    title: str
    description: str
    acceptance_criteria: List[str]
    business_value: str
    stakeholders: List[str]
    assumptions: List[str]
    questions: List[str]
    confidence: float
    source_code: Optional[str] = None
    rationale: Optional[str] = None

@dataclass
class CodeAnalysis:
    """Deep analysis of code for business understanding."""
    file_path: str
    functions: List[Dict[str, Any]]
    classes: List[Dict[str, Any]]
    business_logic: List[str]
    potential_issues: List[str]
    ambiguities: List[str]
    missing_validations: List[str]
    domain_hints: List[str]
    complexity_score: float

def get_project_root() -> Path:
    """Get the project root directory."""
    return Path.cwd()

def get_agentops_dir() -> Path:
    """Get the .agentops directory."""
    return get_project_root() / ".agentops"

def ensure_agentops_dir():
    """Ensure .agentops directory exists."""
    agentops_dir = get_agentops_dir()
    agentops_dir.mkdir(exist_ok=True)
    (agentops_dir / "requirements").mkdir(exist_ok=True)
    (agentops_dir / "tests").mkdir(exist_ok=True)
    (agentops_dir / "reports").mkdir(exist_ok=True)
    (agentops_dir / "traceability").mkdir(exist_ok=True)
    (agentops_dir / "analysis").mkdir(exist_ok=True)

def analyze_code_for_business_context(file_path: str) -> CodeAnalysis:
    """Perform deep business-focused analysis of code."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract functions with detailed analysis
        functions = []
        function_matches = re.finditer(r'def\s+(\w+)\s*\([^)]*\):\s*(?:"""([^"]*?)""")?', content, re.DOTALL)
        for match in function_matches:
            func_name = match.group(1)
            docstring = match.group(2) or ""
            
            # Analyze function for business logic
            func_content = _extract_function_body(content, match.start())
            business_indicators = _identify_business_logic(func_content)
            
            functions.append({
                'name': func_name,
                'docstring': docstring.strip(),
                'business_indicators': business_indicators,
                'validation_logic': _extract_validation_patterns(func_content),
                'error_handling': _extract_error_handling(func_content),
                'external_dependencies': _extract_dependencies(func_content)
            })
        
        # Extract classes with business context
        classes = []
        class_matches = re.finditer(r'class\s+(\w+)(?:\([^)]*\))?:\s*(?:"""([^"]*?)""")?', content, re.DOTALL)
        for match in class_matches:
            class_name = match.group(1)
            docstring = match.group(2) or ""
            
            # Analyze class methods for business patterns
            class_content = _extract_class_body(content, match.start())
            business_methods = _identify_business_methods(class_content)
            
            classes.append({
                'name': class_name,
                'docstring': docstring.strip(),
                'business_methods': business_methods,
                'state_management': _analyze_state_management(class_content),
                'domain_model': _infer_domain_model(class_name, class_content)
            })
        
        # Identify business logic patterns
        business_logic = _identify_business_logic_patterns(content)
        
        # Detect potential issues and ambiguities
        potential_issues = _detect_potential_issues(content)
        ambiguities = _detect_ambiguities(content)
        missing_validations = _detect_missing_validations(content)
        
        # Extract domain hints
        domain_hints = _extract_domain_hints(content, file_path)
        
        # Calculate complexity score
        complexity_score = _calculate_business_complexity(content)
        
        return CodeAnalysis(
            file_path=file_path,
            functions=functions,
            classes=classes,
            business_logic=business_logic,
            potential_issues=potential_issues,
            ambiguities=ambiguities,
            missing_validations=missing_validations,
            domain_hints=domain_hints,
            complexity_score=complexity_score
        )
        
    except Exception as e:
        console.print(f"[red]Error analyzing {file_path}: {e}[/red]")
        return CodeAnalysis(
            file_path=file_path,
            functions=[],
            classes=[],
            business_logic=[],
            potential_issues=[f"Analysis failed: {e}"],
            ambiguities=[],
            missing_validations=[],
            domain_hints=[],
            complexity_score=0.0
        )

def _extract_function_body(content: str, start_pos: int) -> str:
    """Extract the body of a function from code."""
    lines = content[start_pos:].split('\n')
    body_lines = []
    indent_level = None
    
    for line in lines[1:]:  # Skip function definition line
        if line.strip() == "":
            continue
        
        current_indent = len(line) - len(line.lstrip())
        
        if indent_level is None:
            indent_level = current_indent
        
        if current_indent < indent_level and line.strip():
            break
            
        body_lines.append(line)
    
    return '\n'.join(body_lines)

def _extract_class_body(content: str, start_pos: int) -> str:
    """Extract the body of a class from code."""
    lines = content[start_pos:].split('\n')
    body_lines = []
    indent_level = None
    
    for line in lines[1:]:  # Skip class definition line
        if line.strip() == "":
            continue
        
        current_indent = len(line) - len(line.lstrip())
        
        if indent_level is None:
            indent_level = current_indent
        
        if current_indent <= indent_level and line.strip() and not line.lstrip().startswith(('def ', 'class ', '@')):
            if 'class ' in line:
                break
            
        body_lines.append(line)
    
    return '\n'.join(body_lines)

def _identify_business_logic(code: str) -> List[str]:
    """Identify business logic patterns in code."""
    patterns = []
    
    # Look for validation patterns
    if re.search(r'if.*(?:valid|check|verify)', code, re.IGNORECASE):
        patterns.append("Input validation logic")
    
    # Look for calculation patterns
    if re.search(r'(?:calculate|compute|total|sum|rate|fee|price)', code, re.IGNORECASE):
        patterns.append("Business calculations")
    
    # Look for workflow patterns
    if re.search(r'(?:process|workflow|step|stage|approve)', code, re.IGNORECASE):
        patterns.append("Business workflow")
    
    # Look for business rules
    if re.search(r'(?:rule|policy|limit|threshold|maximum|minimum)', code, re.IGNORECASE):
        patterns.append("Business rules")
    
    # Look for state changes
    if re.search(r'(?:status|state|active|pending|completed)', code, re.IGNORECASE):
        patterns.append("State management")
    
    return patterns

def _identify_business_logic_patterns(content: str) -> List[str]:
    """Identify high-level business logic patterns."""
    patterns = []
    
    # Domain-specific patterns
    domain_keywords = {
        'financial': ['payment', 'transaction', 'balance', 'account', 'currency', 'rate'],
        'user_management': ['user', 'login', 'authentication', 'permission', 'role'],
        'inventory': ['stock', 'product', 'quantity', 'warehouse', 'order'],
        'workflow': ['approval', 'review', 'submit', 'process', 'status'],
        'analytics': ['report', 'metric', 'analysis', 'data', 'statistics']
    }
    
    content_lower = content.lower()
    for domain, keywords in domain_keywords.items():
        if any(keyword in content_lower for keyword in keywords):
            patterns.append(f"Contains {domain} business logic")
    
    return patterns

def _extract_validation_patterns(code: str) -> List[str]:
    """Extract validation patterns from code."""
    validations = []
    
    # Look for explicit validations
    if re.search(r'if.*(?:len|length|size)', code):
        validations.append("Length/size validation")
    
    if re.search(r'if.*(?:is.*None|== None|!= None)', code):
        validations.append("Null/None validation")
    
    if re.search(r'if.*(?:>=|<=|>|<)', code):
        validations.append("Range validation")
    
    if re.search(r'(?:raise|throw).*(?:Error|Exception)', code):
        validations.append("Error handling")
    
    return validations

def _extract_error_handling(code: str) -> List[str]:
    """Extract error handling patterns."""
    patterns = []
    
    if 'try:' in code:
        patterns.append("Exception handling")
    
    if re.search(r'(?:raise|throw)', code):
        patterns.append("Error raising")
    
    if re.search(r'(?:log|logger)', code):
        patterns.append("Error logging")
    
    return patterns

def _extract_dependencies(code: str) -> List[str]:
    """Extract external dependencies."""
    dependencies = []
    
    # Look for database operations
    if re.search(r'(?:db|database|sql|query|session)', code, re.IGNORECASE):
        dependencies.append("Database operations")
    
    # Look for API calls
    if re.search(r'(?:request|http|api|url)', code, re.IGNORECASE):
        dependencies.append("External API calls")
    
    # Look for file operations
    if re.search(r'(?:file|open|read|write)', code, re.IGNORECASE):
        dependencies.append("File system operations")
    
    return dependencies

def _identify_business_methods(code: str) -> List[str]:
    """Identify business-relevant methods in a class."""
    methods = []
    
    method_matches = re.finditer(r'def\s+(\w+)', code)
    for match in method_matches:
        method_name = match.group(1)
        
        # Skip private and magic methods for business analysis
        if not method_name.startswith('_'):
            methods.append(method_name)
    
    return methods

def _analyze_state_management(code: str) -> List[str]:
    """Analyze state management patterns."""
    patterns = []
    
    if re.search(r'self\.\w+\s*=', code):
        patterns.append("Instance state modification")
    
    if re.search(r'(?:status|state)', code, re.IGNORECASE):
        patterns.append("Status/state tracking")
    
    return patterns

def _infer_domain_model(class_name: str, code: str) -> str:
    """Infer the domain model from class name and content."""
    name_lower = class_name.lower()
    
    if any(keyword in name_lower for keyword in ['user', 'account', 'person']):
        return "User/Account Management"
    elif any(keyword in name_lower for keyword in ['order', 'product', 'inventory']):
        return "Commerce/Inventory"
    elif any(keyword in name_lower for keyword in ['payment', 'transaction', 'billing']):
        return "Financial/Payment"
    elif any(keyword in name_lower for keyword in ['report', 'analytics', 'data']):
        return "Analytics/Reporting"
    else:
        return "General Business Logic"

def _detect_potential_issues(content: str) -> List[str]:
    """Detect potential business logic issues."""
    issues = []
    
    # Look for hardcoded values that might be business rules
    if re.search(r'(?:==|!=)\s*(?:\d+|"[^"]*")', content):
        issues.append("Hardcoded values detected - should these be configurable business rules?")
    
    # Look for magic numbers
    magic_numbers = re.findall(r'\b(?<![\w.])\d{2,}\b(?![\w.])', content)
    if magic_numbers:
        issues.append(f"Magic numbers found: {', '.join(set(magic_numbers))} - business significance unclear")
    
    # Look for TODO/FIXME comments
    if re.search(r'(?:TODO|FIXME|HACK)', content, re.IGNORECASE):
        issues.append("Incomplete implementation detected - business requirements may be unclear")
    
    # Look for complex boolean logic
    if re.search(r'(?:and|or).*(?:and|or)', content):
        issues.append("Complex boolean logic - business rules may need clarification")
    
    return issues

def _detect_ambiguities(content: str) -> List[str]:
    """Detect ambiguous business logic."""
    ambiguities = []
    
    # Look for random operations
    if re.search(r'random|choice|shuffle', content, re.IGNORECASE):
        ambiguities.append("Random behavior detected - is this intentional business logic?")
    
    # Look for unclear variable names
    unclear_vars = re.findall(r'\b(?:temp|tmp|data|info|stuff|thing)\w*\b', content)
    if unclear_vars:
        ambiguities.append(f"Unclear variable names: {', '.join(set(unclear_vars))} - business purpose unclear")
    
    # Look for empty catch blocks
    if re.search(r'except.*:\s*pass', content):
        ambiguities.append("Silent error handling - business impact of failures unclear")
    
    return ambiguities

def _detect_missing_validations(content: str) -> List[str]:
    """Detect potentially missing business validations."""
    missing = []
    
    # Look for direct attribute access without validation
    if re.search(r'self\.\w+\s*=.*(?:input|request|param)', content, re.IGNORECASE):
        missing.append("Direct assignment from external input - validation may be missing")
    
    # Look for database operations without error handling
    if re.search(r'(?:insert|update|delete|save)', content, re.IGNORECASE) and 'try:' not in content:
        missing.append("Database operations without error handling")
    
    # Look for calculations without bounds checking
    if re.search(r'[*/]', content) and not re.search(r'if.*(?:>|<|==)', content):
        missing.append("Mathematical operations without bounds checking")
    
    return missing

def _extract_domain_hints(content: str, file_path: str) -> List[str]:
    """Extract domain context hints."""
    hints = []
    
    # From file path
    path_parts = Path(file_path).parts
    if 'models' in path_parts:
        hints.append("Data model/entity")
    if 'services' in path_parts:
        hints.append("Business service layer")
    if 'controllers' in path_parts:
        hints.append("API/interface layer")
    if 'utils' in path_parts:
        hints.append("Utility/helper functions")
    
    # From imports
    imports = re.findall(r'(?:from|import)\s+([\w.]+)', content)
    for imp in imports:
        if 'django' in imp or 'flask' in imp:
            hints.append("Web application framework")
        elif 'sqlalchemy' in imp or 'django.db' in imp:
            hints.append("Database ORM usage")
        elif 'requests' in imp:
            hints.append("External API integration")
    
    return hints

def _calculate_business_complexity(content: str) -> float:
    """Calculate business logic complexity score."""
    score = 0.0
    
    # Base complexity from lines of code
    lines = len([line for line in content.split('\n') if line.strip()])
    score += lines * 0.1
    
    # Add complexity for business logic patterns
    if re.search(r'if.*(?:and|or)', content):
        score += 10.0  # Complex conditions
    
    # Add complexity for loops
    score += len(re.findall(r'(?:for|while)', content)) * 5.0
    
    # Add complexity for function calls
    score += len(re.findall(r'\w+\(', content)) * 2.0
    
    # Add complexity for classes
    score += len(re.findall(r'class\s+\w+', content)) * 15.0
    
    return min(score, 100.0)  # Cap at 100

def generate_business_requirements(analysis: CodeAnalysis) -> List[BusinessRequirement]:
    """Generate proper business requirements from code analysis."""
    requirements = []
    req_id = 1
    
    # Generate functional requirements
    for func in analysis.functions:
        if func['business_indicators']:
            req = BusinessRequirement(
                id=f"FR-{req_id:03d}",
                type=RequirementType.FUNCTIONAL,
                title=f"Business function: {func['name']}",
                description=_generate_functional_description(func),
                acceptance_criteria=_generate_acceptance_criteria(func),
                business_value=_infer_business_value(func),
                stakeholders=_identify_stakeholders(func),
                assumptions=_extract_assumptions(func),
                questions=_generate_questions(func),
                confidence=_calculate_requirement_confidence(func),
                source_code=func['name']
            )
            requirements.append(req)
            req_id += 1
    
    # Generate business rule requirements
    for issue in analysis.potential_issues:
        if 'business rule' in issue.lower() or 'configurable' in issue.lower():
            req = BusinessRequirement(
                id=f"BR-{req_id:03d}",
                type=RequirementType.BUSINESS_RULE,
                title="Business rule configuration",
                description=issue,
                acceptance_criteria=["Business rules must be externally configurable", "Changes should not require code deployment"],
                business_value="Enables business agility and reduces deployment risk",
                stakeholders=["Business Analysts", "Operations Team"],
                assumptions=["Current hardcoded values represent business rules"],
                questions=["Who has authority to change these rules?", "How often do these rules change?"],
                confidence=0.7,
                source_code=analysis.file_path
            )
            requirements.append(req)
            req_id += 1
    
    # Generate ambiguity/question requirements
    for ambiguity in analysis.ambiguities:
        req = BusinessRequirement(
            id=f"AMB-{req_id:03d}",
            type=RequirementType.AMBIGUITY,
            title="Business logic clarification needed",
            description=ambiguity,
            acceptance_criteria=["Business logic must be clearly documented", "Implementation must match business intent"],
            business_value="Reduces risk of incorrect business behavior",
            stakeholders=["Product Owner", "Business Analysts", "Development Team"],
            assumptions=["Current implementation may not reflect business intent"],
            questions=["What is the intended business behavior?", "Are there specific business rules governing this?"],
            confidence=0.3,
            source_code=analysis.file_path
        )
        requirements.append(req)
        req_id += 1
    
    # Generate non-functional requirements
    if analysis.complexity_score > 50:
        req = BusinessRequirement(
            id=f"NFR-{req_id:03d}",
            type=RequirementType.NON_FUNCTIONAL,
            title="Performance and maintainability",
            description=f"High complexity code (score: {analysis.complexity_score:.1f}) requires performance and maintainability considerations",
            acceptance_criteria=[
                "Response time must be under 2 seconds for typical operations",
                "Code must be maintainable by team members",
                "Performance must not degrade with normal data volumes"
            ],
            business_value="Ensures system scalability and team productivity",
            stakeholders=["Technical Lead", "Operations Team", "End Users"],
            assumptions=["Complex code may have performance implications"],
            questions=["What are the expected data volumes?", "What are acceptable response times?"],
            confidence=0.8,
            source_code=analysis.file_path
        )
        requirements.append(req)
    
    return requirements

def _generate_functional_description(func: Dict[str, Any]) -> str:
    """Generate proper functional requirement description."""
    name = func['name']
    indicators = func['business_indicators']
    
    if 'Business calculations' in indicators:
        return f"The system must provide accurate business calculations through the {name} function, ensuring all financial/business rules are properly applied and results are auditable."
    elif 'Input validation logic' in indicators:
        return f"The system must validate all input data according to business rules before processing, with clear error messages for invalid data."
    elif 'Business workflow' in indicators:
        return f"The system must support the business workflow implemented in {name}, ensuring proper state transitions and business rule compliance."
    elif 'State management' in indicators:
        return f"The system must maintain consistent business state through {name}, ensuring data integrity and business rule compliance."
    else:
        return f"The system must provide the business functionality implemented in {name}, meeting all relevant business requirements and constraints."

def _generate_acceptance_criteria(func: Dict[str, Any]) -> List[str]:
    """Generate meaningful acceptance criteria."""
    criteria = []
    
    if func['validation_logic']:
        criteria.append("All input validation rules must be enforced")
        criteria.append("Invalid input must be rejected with clear error messages")
    
    if func['error_handling']:
        criteria.append("All error conditions must be handled gracefully")
        criteria.append("Error messages must be user-friendly and actionable")
    
    if func['business_indicators']:
        criteria.append("Business logic must produce consistent and auditable results")
        criteria.append("Function must handle all identified business scenarios")
    
    if not criteria:
        criteria.append("Function must operate according to business requirements")
        criteria.append("Results must be consistent and predictable")
    
    return criteria

def _infer_business_value(func: Dict[str, Any]) -> str:
    """Infer business value from function analysis."""
    if 'Business calculations' in func['business_indicators']:
        return "Enables accurate business operations and financial reporting"
    elif 'Input validation logic' in func['business_indicators']:
        return "Prevents data corruption and ensures data quality"
    elif 'Business workflow' in func['business_indicators']:
        return "Supports critical business processes and operations"
    else:
        return "Contributes to overall business functionality and user experience"

def _identify_stakeholders(func: Dict[str, Any]) -> List[str]:
    """Identify relevant stakeholders."""
    stakeholders = ["Development Team"]
    
    if func['business_indicators']:
        stakeholders.extend(["Business Analysts", "Product Owner"])
    
    if func['validation_logic']:
        stakeholders.append("Data Quality Team")
    
    if func['external_dependencies']:
        stakeholders.append("Operations Team")
    
    return list(set(stakeholders))

def _extract_assumptions(func: Dict[str, Any]) -> List[str]:
    """Extract assumptions from function analysis."""
    assumptions = []
    
    if func['validation_logic']:
        assumptions.append("Current validation rules reflect all business requirements")
    
    if func['external_dependencies']:
        assumptions.append("External dependencies are reliable and available")
    
    if not func['error_handling']:
        assumptions.append("Function operates in controlled environment with valid inputs")
    
    return assumptions

def _generate_questions(func: Dict[str, Any]) -> List[str]:
    """Generate clarifying questions."""
    questions = []
    
    if not func['validation_logic']:
        questions.append("What validation rules should be applied to inputs?")
    
    if not func['error_handling']:
        questions.append("How should error conditions be handled?")
    
    if func['business_indicators']:
        questions.append("Are there any business rules or constraints not captured in the code?")
    
    questions.append("Who are the primary users of this functionality?")
    
    return questions

def _calculate_requirement_confidence(func: Dict[str, Any]) -> float:
    """Calculate confidence in requirement extraction."""
    confidence = 0.5  # Base confidence
    
    if func['docstring']:
        confidence += 0.2
    
    if func['validation_logic']:
        confidence += 0.1
    
    if func['error_handling']:
        confidence += 0.1
    
    if func['business_indicators']:
        confidence += 0.1
    
    return min(confidence, 1.0)

def export_requirements_gherkin(requirements: List[BusinessRequirement], file_path: str) -> str:
    """Export requirements in proper Gherkin format."""
    filename = Path(file_path).stem
    content = f"""# Business Requirements for {filename}
# Generated by AgentOps - Business-Focused Requirements Analysis

Feature: {filename.replace('_', ' ').title()} Business Functionality
  As a stakeholder
  I want the {filename} functionality to meet business requirements
  So that business objectives are achieved and risks are minimized

"""
    
    for req in requirements:
        if req.type == RequirementType.FUNCTIONAL:
            content += f"""
  Scenario: {req.title}
    Given the system is properly configured
    And all business rules are in place
    When the functionality is executed
    Then {req.description.lower()}
    And all acceptance criteria are met:
"""
            for criteria in req.acceptance_criteria:
                content += f"      * {criteria}\n"
        
        elif req.type == RequirementType.AMBIGUITY:
            content += f"""
  # REQUIRES CLARIFICATION: {req.title}
  # Question: {req.description}
  # Stakeholders needed: {', '.join(req.stakeholders)}
  # Business Impact: {req.business_value}
  
"""
    
    # Add business questions section
    content += """
  # BUSINESS CLARIFICATION NEEDED
  # The following questions require stakeholder input:
  
"""
    
    for req in requirements:
        if req.questions:
            content += f"  # {req.id} - {req.title}:\n"
            for question in req.questions:
                content += f"  #   - {question}\n"
    
    return content

def export_requirements_markdown(requirements: List[BusinessRequirement], file_path: str) -> str:
    """Export requirements in comprehensive markdown format."""
    filename = Path(file_path).stem
    
    content = f"""# Business Requirements Analysis: {filename}

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Source**: {file_path}  
**Analysis Type**: Business-Focused Requirements Extraction  

## Executive Summary

This document contains business requirements extracted from code analysis, focusing on actual business needs rather than technical implementation details. Requirements are categorized by type and include stakeholder perspectives, business value, and clarification needs.

## Requirements Overview

"""
    
    # Create summary table
    req_types = {}
    for req in requirements:
        req_types[req.type.value] = req_types.get(req.type.value, 0) + 1
    
    content += "| Requirement Type | Count | Focus |\n"
    content += "|-----------------|-------|-------|\n"
    
    for req_type, count in req_types.items():
        focus_map = {
            'functional': 'Business functionality and user needs',
            'business_rule': 'Configurable business logic',
            'ambiguity': 'Clarification required from stakeholders',
            'non_functional': 'Performance, security, maintainability'
        }
        content += f"| {req_type.replace('_', ' ').title()} | {count} | {focus_map.get(req_type, 'General requirements')} |\n"
    
    content += "\n## Detailed Requirements\n\n"
    
    # Group requirements by type
    by_type = {}
    for req in requirements:
        if req.type not in by_type:
            by_type[req.type] = []
        by_type[req.type].append(req)
    
    for req_type, reqs in by_type.items():
        content += f"### {req_type.value.replace('_', ' ').title()} Requirements\n\n"
        
        for req in reqs:
            content += f"#### {req.id}: {req.title}\n\n"
            content += f"**Description**: {req.description}\n\n"
            content += f"**Business Value**: {req.business_value}\n\n"
            
            content += "**Acceptance Criteria**:\n"
            for criteria in req.acceptance_criteria:
                content += f"- {criteria}\n"
            content += "\n"
            
            content += f"**Stakeholders**: {', '.join(req.stakeholders)}\n\n"
            
            if req.assumptions:
                content += "**Assumptions**:\n"
                for assumption in req.assumptions:
                    content += f"- {assumption}\n"
                content += "\n"
            
            if req.questions:
                content += "**❓ Questions for Stakeholders**:\n"
                for question in req.questions:
                    content += f"- {question}\n"
                content += "\n"
            
            content += f"**Confidence Level**: {req.confidence:.1%}\n\n"
            content += "---\n\n"
    
    # Add clarification section
    clarification_needed = [req for req in requirements if req.type == RequirementType.AMBIGUITY or req.questions]
    
    if clarification_needed:
        content += "## 🚨 Stakeholder Input Required\n\n"
        content += "The following requirements need stakeholder clarification before implementation:\n\n"
        
        for req in clarification_needed:
            content += f"### {req.id}: {req.title}\n"
            content += f"**Issue**: {req.description}\n"
            content += f"**Required Stakeholders**: {', '.join(req.stakeholders)}\n"
            if req.questions:
                content += "**Questions**:\n"
                for question in req.questions:
                    content += f"- {question}\n"
            content += "\n"
    
    # Add recommendations
    content += "## 📋 Recommendations\n\n"
    
    if any(req.type == RequirementType.AMBIGUITY for req in requirements):
        content += "1. **Schedule stakeholder review session** to clarify ambiguous business logic\n"
    
    if any(req.confidence < 0.7 for req in requirements):
        content += "2. **Gather additional business context** for low-confidence requirements\n"
    
    content += "3. **Prioritize requirements** based on business value and risk\n"
    content += "4. **Create acceptance tests** for all functional requirements\n"
    content += "5. **Establish traceability** between requirements and implementation\n\n"
    
    content += "## Next Steps\n\n"
    content += "1. Review requirements with stakeholders\n"
    content += "2. Clarify ambiguous business logic\n"
    content += "3. Prioritize implementation based on business value\n"
    content += "4. Generate comprehensive test suites\n"
    content += "5. Establish ongoing requirements traceability\n"
    
    return content

def generate_comprehensive_tests(requirements: List[BusinessRequirement], analysis: CodeAnalysis) -> str:
    """Generate comprehensive tests focusing on business requirements."""
    
    test_code = f"""\"\"\"Comprehensive tests for {analysis.file_path}
Generated by AgentOps - Business-Focused Test Generation

This test suite focuses on:
1. Business requirement validation
2. Edge case handling
3. Error condition testing
4. Integration scenarios
5. Business rule compliance
\"\"\"

import pytest
import unittest.mock as mock
from unittest.mock import patch, MagicMock
import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import the module under test
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("test_module", "{analysis.file_path}")
    test_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_module)
except Exception as e:
    pytest.skip(f"Could not import module: {{e}}")

class TestBusinessRequirements:
    \"\"\"Test business requirements compliance.\"\"\"
    
    def setup_method(self):
        \"\"\"Set up test fixtures.\"\"\"
        self.test_data = {{
            'valid_input': {{'example': 'data'}},
            'invalid_input': {{'bad': 'data'}},
            'edge_cases': [None, '', 0, -1, float('inf')]
        }}
    
"""
    
    # Generate tests for each functional requirement
    functional_reqs = [req for req in requirements if req.type == RequirementType.FUNCTIONAL]
    
    for req in functional_reqs:
        if req.source_code:
            test_code += f"""
    def test_{req.id.lower()}_{req.source_code}_business_compliance(self):
        \"\"\"Test {req.title} - Business Requirement: {req.id}
        
        Requirement: {req.description}
        
        Acceptance Criteria:
        {chr(10).join(f'        - {criteria}' for criteria in req.acceptance_criteria)}
        \"\"\"
        # Test basic functionality
        assert hasattr(test_module, '{req.source_code}'), f"Function {req.source_code} must exist"
        func = getattr(test_module, '{req.source_code}')
        assert callable(func), f"{req.source_code} must be callable"
        
        # TODO: Implement specific business logic tests based on requirements
        # This requires stakeholder input for specific test data and expected results
        
    def test_{req.id.lower()}_{req.source_code}_error_handling(self):
        \"\"\"Test error handling for {req.title}\"\"\"
        func = getattr(test_module, '{req.source_code}', None)
        if func is None:
            pytest.skip(f"Function {req.source_code} not found")
        
        # Test with invalid inputs
        for invalid_input in self.test_data['edge_cases']:
            try:
                # This will need customization based on function signature
                # result = func(invalid_input)
                pass  # TODO: Implement based on actual function signature
            except Exception as e:
                # Verify that exceptions are business-appropriate
                assert isinstance(e, (ValueError, TypeError, RuntimeError)), f"Unexpected exception type: {{type(e)}}"
    
    def test_{req.id.lower()}_{req.source_code}_acceptance_criteria(self):
        \"\"\"Test acceptance criteria for {req.title}\"\"\"
        # Test each acceptance criterion
        {chr(10).join(f'        # Criterion: {criteria}' for criteria in req.acceptance_criteria)}
        
        # TODO: Implement specific tests for each acceptance criterion
        # This requires business stakeholder input
        pass
"""
    
    # Generate tests for business rules
    business_rules = [req for req in requirements if req.type == RequirementType.BUSINESS_RULE]
    
    if business_rules:
        test_code += """
class TestBusinessRules:
    \"\"\"Test business rule compliance and configuration.\"\"\"
    
"""
        
        for req in business_rules:
            test_code += f"""
    def test_{req.id.lower()}_business_rule_compliance(self):
        \"\"\"Test {req.title} - Business Rule: {req.id}
        
        Rule: {req.description}
        \"\"\"
        # TODO: Test that business rules are externally configurable
        # TODO: Test that rule changes don't require code deployment
        # TODO: Validate business rule logic
        
        # This test requires:
        # 1. Configuration system for business rules
        # 2. Stakeholder definition of valid rule ranges
        # 3. Integration with business rule engine
        
        pytest.skip("Business rule testing requires stakeholder input and configuration system")
"""
    
    # Generate tests for ambiguity detection
    ambiguities = [req for req in requirements if req.type == RequirementType.AMBIGUITY]
    
    if ambiguities:
        test_code += """
class TestBusinessLogicClarification:
    \"\"\"Tests that highlight ambiguous business logic requiring clarification.\"\"\"
    
"""
        
        for req in ambiguities:
            test_code += f"""
    def test_{req.id.lower()}_ambiguity_clarification(self):
        \"\"\"Highlight ambiguity: {req.title}
        
        Issue: {req.description}
        
        Questions for stakeholders:
        {chr(10).join(f'        - {question}' for question in req.questions)}
        \"\"\"
        # This test documents ambiguous business logic
        # Implementation requires stakeholder clarification
        
        pytest.skip(f"BUSINESS CLARIFICATION NEEDED: {req.description}")
"""
    
    # Add performance and integration tests
    test_code += """
class TestIntegrationAndPerformance:
    \"\"\"Test integration scenarios and performance requirements.\"\"\"
    
    def test_integration_with_external_dependencies(self):
        \"\"\"Test integration with external systems.\"\"\"
        # TODO: Mock external dependencies
        # TODO: Test error handling for external failures
        # TODO: Test timeout scenarios
        pass
    
    def test_performance_requirements(self):
        \"\"\"Test performance requirements.\"\"\"
        import time
        
        # TODO: Define performance benchmarks with stakeholders
        # TODO: Test with realistic data volumes
        # TODO: Measure response times
        
        # Example performance test structure:
        # start_time = time.time()
        # result = function_under_test(large_dataset)
        # elapsed = time.time() - start_time
        # assert elapsed < 2.0, f"Performance requirement violated: {elapsed}s > 2.0s"
        
        pass
    
    def test_data_integrity_and_consistency(self):
        \"\"\"Test data integrity across business operations.\"\"\"
        # TODO: Test that business operations maintain data consistency
        # TODO: Test transaction rollback scenarios
        # TODO: Validate business invariants
        pass

class TestBusinessValueValidation:
    \"\"\"Validate that implementation delivers expected business value.\"\"\"
    
    def test_business_value_metrics(self):
        \"\"\"Test that business value is measurable and achieved.\"\"\"
        # TODO: Define business value metrics with stakeholders
        # TODO: Implement measurement mechanisms
        # TODO: Validate against business objectives
        
        pytest.skip("Business value testing requires stakeholder-defined metrics")
"""
    
    return test_code

def run_tests(test_file: str) -> Dict[str, Any]:
    """Run the generated tests and return results."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v", "--tb=short", "-x"],
            capture_output=True,
            text=True,
            cwd=get_project_root()
        )
        
        return {
            'success': result.returncode == 0,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'stdout': '',
            'stderr': str(e),
            'returncode': 1
        }

def generate_traceability_matrix(requirements: List[BusinessRequirement], analysis: CodeAnalysis, test_results: Dict[str, Any]) -> str:
    """Generate comprehensive traceability matrix."""
    
    content = f"""# Business Requirements Traceability Matrix

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Source**: {analysis.file_path}  
**Analysis Type**: Business-Focused Requirements Traceability  

## Overview

This traceability matrix links business requirements to implementation and test coverage, ensuring complete accountability for business value delivery.

## Traceability Summary

| Requirement Type | Total | Implemented | Tested | Clarification Needed |
|------------------|-------|-------------|--------|---------------------|
"""
    
    # Calculate traceability metrics
    by_type = {}
    for req in requirements:
        if req.type not in by_type:
            by_type[req.type] = []
        by_type[req.type].append(req)
    
    for req_type, reqs in by_type.items():
        total = len(reqs)
        implemented = len([r for r in reqs if r.source_code])
        tested = len([r for r in reqs if r.source_code and test_results.get('success', False)])
        needs_clarification = len([r for r in reqs if r.type == RequirementType.AMBIGUITY or r.confidence < 0.7])
        
        content += f"| {req_type.value.replace('_', ' ').title()} | {total} | {implemented} | {tested} | {needs_clarification} |\n"
    
    content += "\n## Detailed Traceability\n\n"
    
    for req in requirements:
        content += f"### {req.id}: {req.title}\n\n"
        content += f"**Type**: {req.type.value.replace('_', ' ').title()}\n"
        content += f"**Business Value**: {req.business_value}\n"
        content += f"**Confidence**: {req.confidence:.1%}\n\n"
        
        # Implementation traceability
        if req.source_code:
            content += f"**Implementation**: ✅ `{req.source_code}` in `{analysis.file_path}`\n"
        else:
            content += "**Implementation**: ❌ Not implemented or not traceable\n"
        
        # Test coverage
        test_name = f"test_{req.id.lower()}_{req.source_code if req.source_code else 'unknown'}"
        if test_results.get('success', False):
            content += f"**Test Coverage**: ✅ `{test_name}` (PASSED)\n"
        else:
            content += f"**Test Coverage**: ⚠️ `{test_name}` (Tests require stakeholder input)\n"
        
        # Stakeholder accountability
        content += f"**Stakeholders**: {', '.join(req.stakeholders)}\n"
        
        # Risk assessment
        if req.type == RequirementType.AMBIGUITY:
            content += "**Risk Level**: 🔴 HIGH - Requires immediate stakeholder clarification\n"
        elif req.confidence < 0.7:
            content += "**Risk Level**: 🟡 MEDIUM - Low confidence in requirement accuracy\n"
        else:
            content += "**Risk Level**: 🟢 LOW - Well-defined requirement\n"
        
        # Outstanding questions
        if req.questions:
            content += "\n**Outstanding Questions**:\n"
            for question in req.questions:
                content += f"- ❓ {question}\n"
        
        content += "\n---\n\n"
    
    # Risk analysis section
    high_risk = [req for req in requirements if req.type == RequirementType.AMBIGUITY]
    medium_risk = [req for req in requirements if req.confidence < 0.7 and req.type != RequirementType.AMBIGUITY]
    
    content += "## Risk Analysis\n\n"
    
    if high_risk:
        content += "### 🔴 High Risk Requirements (Immediate Action Needed)\n\n"
        for req in high_risk:
            content += f"- **{req.id}**: {req.title} - {req.description}\n"
        content += "\n"
    
    if medium_risk:
        content += "### 🟡 Medium Risk Requirements (Review Recommended)\n\n"
        for req in medium_risk:
            content += f"- **{req.id}**: {req.title} - Confidence: {req.confidence:.1%}\n"
        content += "\n"
    
    # Business value analysis
    content += "## Business Value Analysis\n\n"
    
    total_reqs = len(requirements)
    implemented_reqs = len([req for req in requirements if req.source_code])
    coverage_percentage = (implemented_reqs / total_reqs * 100) if total_reqs > 0 else 0
    
    content += f"**Requirements Coverage**: {coverage_percentage:.1f}% ({implemented_reqs}/{total_reqs})\n"
    content += f"**Business Risk Level**: {'HIGH' if high_risk else 'MEDIUM' if medium_risk else 'LOW'}\n"
    content += f"**Stakeholder Review Required**: {'YES' if high_risk or medium_risk else 'NO'}\n\n"
    
    # Recommendations
    content += "## 📋 Recommendations\n\n"
    
    if high_risk:
        content += "1. **URGENT**: Schedule stakeholder review for high-risk requirements\n"
    
    if medium_risk:
        content += "2. **Priority**: Clarify medium-risk requirements with business stakeholders\n"
    
    content += "3. **Quality**: Implement comprehensive test coverage for all functional requirements\n"
    content += "4. **Process**: Establish regular requirement review cycles\n"
    content += "5. **Measurement**: Define business value metrics for ongoing validation\n\n"
    
    content += "## Next Actions\n\n"
    content += "1. **Stakeholder Review Session**: Schedule with business stakeholders for requirement clarification\n"
    content += "2. **Test Implementation**: Complete business-focused test suites\n"
    content += "3. **Requirement Prioritization**: Rank requirements by business value and risk\n"
    content += "4. **Continuous Monitoring**: Establish ongoing traceability and validation processes\n"
    
    return content

@click.group()
@click.version_option(version=agentops_version, prog_name="AgentOps")
def cli():
    """AgentOps - Business-Focused Requirements and Test Generation."""
    pass

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def init(verbose):
    """Initialize AgentOps project structure."""
    console.print(Panel.fit("🚀 Initializing AgentOps Business Analysis Project", style="bold blue"))
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Creating project structure...", total=None)
        
        try:
            ensure_agentops_dir()
            progress.update(task, description="✅ Project structure created")
            
            # Create initial configuration with business focus
            config = {
                'version': agentops_version,
                'created': datetime.now().isoformat(),
                'project_root': str(get_project_root()),
                'analysis_type': 'business_focused',
                'focus': 'Business requirements extraction over code documentation'
            }
            
            config_file = get_agentops_dir() / 'config.json'
            with open(config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            progress.update(task, description="✅ Business-focused configuration initialized")
            
            if verbose:
                console.print(f"📁 Project root: {get_project_root()}")
                console.print(f"📁 AgentOps directory: {get_agentops_dir()}")
                console.print(f"📄 Configuration: {config_file}")
                console.print("🎯 Focus: Business requirements over code summaries")
            
            console.print(Panel.fit("✅ AgentOps business analysis project initialized!", style="bold green"))
            console.print("\n[cyan]💡 Next steps:[/cyan]")
            console.print("1. Run: [bold]agentops runner <file_path>[/bold] for complete analysis")
            console.print("2. Run: [bold]agentops analyze <file_path>[/bold] for requirements only")
            
        except Exception as e:
            console.print(f"[red]❌ Error initializing project: {e}[/red]")
            sys.exit(1)

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def analyze(file_path, verbose):
    """Deep business requirements analysis (requirements only)."""
    console.print(Panel.fit("🔍 Deep Business Requirements Analysis", style="bold blue"))
    
    if verbose:
        console.print(f"📄 Analyzing file: {file_path}")
    
    # Initialize project if needed
    ensure_agentops_dir()
    
    # Perform deep business analysis
    console.print("\n[bold cyan]Analyzing code for business context...[/bold cyan]")
    analysis = analyze_code_for_business_context(file_path)
    
    if verbose:
        console.print(f"✅ Found {len(analysis.functions)} functions with business logic")
        console.print(f"✅ Found {len(analysis.classes)} classes")
        console.print(f"✅ Identified {len(analysis.potential_issues)} potential issues")
        console.print(f"✅ Detected {len(analysis.ambiguities)} ambiguities")
        console.print(f"📊 Business complexity score: {analysis.complexity_score:.1f}")
    
    # Generate business requirements
    console.print("\n[bold cyan]Generating business requirements...[/bold cyan]")
    requirements = generate_business_requirements(analysis)
    
    if not requirements:
        console.print("[yellow]⚠️ No clear business requirements could be extracted from this code.[/yellow]")
        console.print("This may indicate:")
        console.print("• Code is purely technical/utility focused")
        console.print("• Business logic is not clearly expressed")
        console.print("• Additional stakeholder input is needed")
        return
    
    # Export requirements
    gherkin_content = export_requirements_gherkin(requirements, file_path)
    gherkin_file = get_agentops_dir() / "requirements" / f"{Path(file_path).stem}_business_requirements.feature"
    with open(gherkin_file, 'w') as f:
        f.write(gherkin_content)
    
    markdown_content = export_requirements_markdown(requirements, file_path)
    markdown_file = get_agentops_dir() / "requirements" / f"{Path(file_path).stem}_business_requirements.md"
    with open(markdown_file, 'w') as f:
        f.write(markdown_content)
    
    # Save analysis results
    analysis_file = get_agentops_dir() / "analysis" / f"{Path(file_path).stem}_analysis.json"
    analysis_data = {
        'file_path': file_path,
        'analysis_timestamp': datetime.now().isoformat(),
        'complexity_score': analysis.complexity_score,
        'business_logic_patterns': analysis.business_logic,
        'potential_issues': analysis.potential_issues,
        'ambiguities': analysis.ambiguities,
        'requirements_count': len(requirements),
        'high_risk_count': len([r for r in requirements if r.type == RequirementType.AMBIGUITY]),
        'stakeholder_input_needed': any(r.questions for r in requirements)
    }
    
    with open(analysis_file, 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    # Display results
    console.print(Panel.fit("📋 Business Requirements Analysis Complete", style="bold green"))
    
    # Requirements summary
    summary_table = Table(title="Requirements Analysis Summary")
    summary_table.add_column("Metric", style="cyan")
    summary_table.add_column("Value", style="green")
    summary_table.add_column("Assessment", style="yellow")
    
    total_reqs = len(requirements)
    high_risk = len([r for r in requirements if r.type == RequirementType.AMBIGUITY])
    needs_input = len([r for r in requirements if r.questions])
    
    summary_table.add_row("Total Requirements", str(total_reqs), "✅ Good" if total_reqs > 0 else "⚠️ Limited")
    summary_table.add_row("High Risk (Ambiguous)", str(high_risk), "🔴 Review Needed" if high_risk > 0 else "✅ Clear")
    summary_table.add_row("Stakeholder Input Needed", str(needs_input), "📝 Required" if needs_input > 0 else "✅ Complete")
    summary_table.add_row("Business Complexity", f"{analysis.complexity_score:.1f}", "🔴 High" if analysis.complexity_score > 70 else "🟡 Medium" if analysis.complexity_score > 30 else "✅ Low")
    
    console.print(summary_table)
    
    # Show critical issues
    if high_risk > 0:
        console.print("\n[bold red]🚨 Critical: Stakeholder Input Required[/bold red]")
        ambiguous_reqs = [r for r in requirements if r.type == RequirementType.AMBIGUITY]
        for req in ambiguous_reqs[:3]:  # Show first 3
            console.print(f"• {req.id}: {req.description}")
    
    if verbose:
        console.print(f"\n📁 Files created:")
        console.print(f"✅ Business requirements (Gherkin): {gherkin_file}")
        console.print(f"✅ Business requirements (Markdown): {markdown_file}")
        console.print(f"✅ Analysis data: {analysis_file}")
    
    console.print(f"\n[cyan]💡 Next steps:[/cyan]")
    if high_risk > 0:
        console.print("1. [bold red]URGENT[/bold red]: Review ambiguous requirements with stakeholders")
    console.print("2. Run: [bold]agentops runner <file_path>[/bold] for complete workflow with tests")
    console.print("3. Run: [bold]agentops status[/bold] to see project overview")

@cli.command()
@click.argument('file_path', required=False, type=click.Path(exists=True))
@click.option('--all', is_flag=True, help='Run on all Python files in the current directory (recursively)')
@click.option('--auto-approve', is_flag=True, help='Automatically approve all requirements/tests (no manual review)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def runner(file_path, all, auto_approve, verbose):
    """Complete business-focused workflow: analysis → requirements → tests → traceability.

    Examples:
      agentops runner myfile.py --auto-approve
      agentops runner --all -v
    """
    console.print(Panel.fit("🏃‍♂️ AgentOps Business-Focused Runner", style="bold blue"))
    
    # Handle --all
    if all:
        py_files = [f for f in glob.glob('**/*.py', recursive=True) if not f.startswith('.venv/') and not f.startswith('venv/')]
        if not py_files:
            console.print("[red]No Python files found in the current directory.[/red]")
            return
        for f in py_files:
            console.print(f"\n[bold yellow]Processing:[/bold yellow] {f}")
            # Call the runner logic directly instead of callback
            _run_runner_workflow(f, auto_approve, verbose)
        return
    if not file_path:
        console.print("[red]Please provide a file path or use --all.[/red]")
        return
    
    _run_runner_workflow(file_path, auto_approve, verbose)

def _run_runner_workflow(file_path, auto_approve, verbose):
    """Internal function to run the runner workflow."""
    if verbose:
        console.print(f"📄 Analyzing file: {file_path}")
        console.print("🎯 Focus: Business requirements and comprehensive testing")
    
    # Step 1: Initialize project
    console.print("\n[bold cyan]Step 1: Initializing project...[/bold cyan]")
    ensure_agentops_dir()
    
    # Step 2: Deep business analysis
    console.print("\n[bold cyan]Step 2: Performing deep business analysis...[/bold cyan]")
    analysis = analyze_code_for_business_context(file_path)
    
    if verbose:
        console.print(f"✅ Business complexity: {analysis.complexity_score:.1f}")
        console.print(f"✅ Potential issues: {len(analysis.potential_issues)}")
        console.print(f"✅ Ambiguities detected: {len(analysis.ambiguities)}")
    
    # Step 3: Generate business requirements
    console.print("\n[bold cyan]Step 3: Generating business requirements...[/bold cyan]")
    requirements = generate_business_requirements(analysis)
    
    if not requirements:
        console.print("[yellow]⚠️ No business requirements extracted. Generating basic test structure only.[/yellow]")
    else:
        # Export requirements
        gherkin_content = export_requirements_gherkin(requirements, file_path)
        gherkin_file = get_agentops_dir() / "requirements" / f"{Path(file_path).stem}_business_requirements.feature"
        with open(gherkin_file, 'w') as f:
            f.write(gherkin_content)
        
        markdown_content = export_requirements_markdown(requirements, file_path)
        markdown_file = get_agentops_dir() / "requirements" / f"{Path(file_path).stem}_business_requirements.md"
        with open(markdown_file, 'w') as f:
            f.write(markdown_content)
        
        if verbose:
            console.print(f"✅ Generated {len(requirements)} business requirements")
            console.print(f"✅ Exported to: {gherkin_file}")
    
    # Step 4: Generate comprehensive tests
    console.print("\n[bold cyan]Step 4: Generating comprehensive test suite...[/bold cyan]")
    test_code = generate_comprehensive_tests(requirements, analysis)
    test_file = get_agentops_dir() / "tests" / f"test_{Path(file_path).stem}_business.py"
    with open(test_file, 'w') as f:
        f.write(test_code)
    
    if verbose:
        console.print(f"✅ Test file: {test_file}")
    
    # Step 5: Run tests
    console.print("\n[bold cyan]Step 5: Running test suite...[/bold cyan]")
    test_results = run_tests(str(test_file))
    
    if test_results['success']:
        console.print("✅ All tests passed!")
    else:
        console.print("⚠️ Tests require stakeholder input (this is expected for business-focused tests)")
        if verbose and test_results['stdout']:
            console.print(f"Test output: {test_results['stdout']}")
    
    # Step 6: Generate traceability matrix
    console.print("\n[bold cyan]Step 6: Generating business traceability matrix...[/bold cyan]")
    traceability = generate_traceability_matrix(requirements, analysis, test_results)
    traceability_file = get_agentops_dir() / "traceability" / f"{Path(file_path).stem}_business_traceability.md"
    with open(traceability_file, 'w') as f:
        f.write(traceability)
    
    # Step 7: Save comprehensive analysis
    analysis_file = get_agentops_dir() / "analysis" / f"{Path(file_path).stem}_complete_analysis.json"
    complete_analysis = {
        'file_path': file_path,
        'timestamp': datetime.now().isoformat(),
        'analysis': {
            'complexity_score': analysis.complexity_score,
            'business_logic_patterns': analysis.business_logic,
            'potential_issues': analysis.potential_issues,
            'ambiguities': analysis.ambiguities,
            'domain_hints': analysis.domain_hints
        },
        'requirements': {
            'total_count': len(requirements),
            'by_type': {req_type.value: len([r for r in requirements if r.type == req_type]) for req_type in RequirementType},
            'high_risk_count': len([r for r in requirements if r.type == RequirementType.AMBIGUITY]),
            'stakeholder_input_needed': any(r.questions for r in requirements)
        },
        'testing': {
            'test_file': str(test_file),
            'test_success': test_results['success'],
            'requires_stakeholder_input': True  # Business tests always need stakeholder input
        }
    }
    
    with open(analysis_file, 'w') as f:
        json.dump(complete_analysis, f, indent=2)
    
    # Summary
    console.print(Panel.fit("🎉 Business-Focused Analysis Complete!", style="bold green"))
    
    summary_table = Table(title="Generated Business Artifacts")
    summary_table.add_column("Type", style="cyan")
    summary_table.add_column("File", style="green")
    summary_table.add_column("Focus", style="yellow")
    
    if requirements:
        summary_table.add_row("Business Requirements (Gherkin)", str(gherkin_file), "Stakeholder communication")
        summary_table.add_row("Business Requirements (Markdown)", str(markdown_file), "Detailed business analysis")
    summary_table.add_row("Comprehensive Tests", str(test_file), "Business requirement validation")
    summary_table.add_row("Business Traceability", str(traceability_file), "Requirements accountability")
    summary_table.add_row("Complete Analysis", str(analysis_file), "Technical + business insights")
    
    console.print(summary_table)
    
    # Risk assessment
    if requirements:
        high_risk = len([r for r in requirements if r.type == RequirementType.AMBIGUITY])
        if high_risk > 0:
            console.print(f"\n[bold red]🚨 ATTENTION: {high_risk} requirements need stakeholder clarification![/bold red]")
            console.print("Schedule a stakeholder review session before proceeding with implementation.")
    
    console.print(f"\n📁 All artifacts saved in: {get_agentops_dir()}")

@cli.command()
@click.argument('file_path', required=False, type=click.Path(exists=True))
@click.option('--all', is_flag=True, help='Run tests on all Python files in the current directory (recursively)')
@click.option('--auto-approve', is_flag=True, help='Automatically approve all generated tests')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def tests(file_path, all, auto_approve, verbose):
    """Generate comprehensive test suites (test generation focus).

    Examples:
      agentops tests myfile.py --auto-approve
      agentops tests --all -v
    """
    console.print(Panel.fit("🧪 Comprehensive Test Generation", style="bold blue"))
    
    # Handle --all
    if all:
        py_files = [f for f in glob.glob('**/*.py', recursive=True) if not f.startswith('.venv/') and not f.startswith('venv/')]
        if not py_files:
            console.print("[red]No Python files found in the current directory.[/red]")
            return
        for f in py_files:
            console.print(f"\n[bold yellow]Processing:[/bold yellow] {f}")
            # Call the tests logic directly instead of callback
            _run_tests_workflow(f, auto_approve, verbose)
        return
    if not file_path:
        console.print("[red]Please provide a file path or use --all.[/red]")
        return
    
    _run_tests_workflow(file_path, auto_approve, verbose)

def _run_tests_workflow(file_path, auto_approve, verbose):
    """Internal function to run the tests workflow."""
    if verbose:
        console.print(f"📄 Target file: {file_path}")
        console.print("🎯 Focus: High-quality test generation with business validation")
    
    ensure_agentops_dir()
    
    # Quick analysis for test generation
    console.print("\n[bold cyan]Analyzing code for test generation...[/bold cyan]")
    analysis = analyze_code_for_business_context(file_path)
    
    # Generate lightweight requirements for test structure
    requirements = generate_business_requirements(analysis)
    
    # Generate comprehensive tests
    console.print("\n[bold cyan]Generating comprehensive test suite...[/bold cyan]")
    test_code = generate_comprehensive_tests(requirements, analysis)
    test_file = get_agentops_dir() / "tests" / f"test_{Path(file_path).stem}_comprehensive.py"
    with open(test_file, 'w') as f:
        f.write(test_code)
    
    # Run tests
    console.print("\n[bold cyan]Running generated tests...[/bold cyan]")
    test_results = run_tests(str(test_file))
    
    if test_results['success']:
        console.print("✅ All generated tests passed!")
    else:
        console.print("⚠️ Some tests require customization with business data")
    
    console.print(Panel.fit("✅ Comprehensive Test Suite Generated!", style="bold green"))
    
    test_table = Table(title="Test Generation Results")
    test_table.add_column("Metric", style="cyan")
    test_table.add_column("Value", style="green")
    
    test_table.add_row("Test File", str(test_file))
    test_table.add_row("Functions Covered", str(len(analysis.functions)))
    test_table.add_row("Classes Covered", str(len(analysis.classes)))
    test_table.add_row("Business Requirements", str(len(requirements)))
    test_table.add_row("Test Execution", "✅ Passed" if test_results['success'] else "⚠️ Needs customization")
    
    console.print(test_table)
    
    if verbose:
        console.print(f"\n📄 Generated test file: {test_file}")
        console.print("💡 Next steps:")
        console.print("1. Customize tests with actual business data")
        console.print("2. Add integration test scenarios")
        console.print("3. Define performance benchmarks")

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def status(verbose):
    """Check AgentOps business analysis project status."""
    console.print(Panel.fit("📊 AgentOps Business Analysis Status", style="bold blue"))
    
    agentops_dir = get_agentops_dir()
    
    if not agentops_dir.exists():
        console.print("[red]❌ AgentOps project not initialized[/red]")
        console.print("Run: [bold]agentops init[/bold] to get started")
        return
    
    # Check configuration
    config_file = agentops_dir / 'config.json'
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
        console.print(f"✅ Version: {config.get('version', 'Unknown')}")
        console.print(f"✅ Focus: {config.get('focus', 'Business requirements over code summaries')}")
        console.print(f"✅ Created: {config.get('created', 'Unknown')}")
    else:
        console.print("[yellow]⚠️ Configuration file missing[/yellow]")
    
    # Count artifacts with business focus
    requirements_count = len(list(agentops_dir.glob("requirements/*business*.md"))) + len(list(agentops_dir.glob("requirements/*business*.feature")))
    tests_count = len(list(agentops_dir.glob("tests/*business*.py"))) + len(list(agentops_dir.glob("tests/*comprehensive*.py")))
    analysis_count = len(list(agentops_dir.glob("analysis/*.json")))
    traceability_count = len(list(agentops_dir.glob("traceability/*business*.md")))
    
    status_table = Table(title="Business Analysis Artifacts")
    status_table.add_column("Type", style="cyan")
    status_table.add_column("Count", style="green")
    status_table.add_column("Status", style="yellow")
    status_table.add_column("Focus", style="blue")
    
    status_table.add_row("Business Requirements", str(requirements_count), "✅" if requirements_count > 0 else "❌", "Stakeholder value")
    status_table.add_row("Comprehensive Tests", str(tests_count), "✅" if tests_count > 0 else "❌", "Quality assurance")
    status_table.add_row("Business Analysis", str(analysis_count), "✅" if analysis_count > 0 else "❌", "Deep insights")
    status_table.add_row("Business Traceability", str(traceability_count), "✅" if traceability_count > 0 else "❌", "Accountability")
    
    console.print(status_table)
    
    # Risk assessment
    if analysis_count > 0:
        latest_analysis = max(agentops_dir.glob("analysis/*.json"), key=os.path.getctime)
        with open(latest_analysis, 'r') as f:
            analysis_data = json.load(f)
        
        high_risk = analysis_data.get('requirements', {}).get('high_risk_count', 0)
        needs_input = analysis_data.get('requirements', {}).get('stakeholder_input_needed', False)
        
        console.print("\n[bold]Risk Assessment:[/bold]")
        if high_risk > 0:
            console.print(f"🔴 HIGH RISK: {high_risk} requirements need stakeholder clarification")
        elif needs_input:
            console.print("🟡 MEDIUM RISK: Some requirements need stakeholder input")
        else:
            console.print("🟢 LOW RISK: Requirements are well-defined")
    
    if verbose:
        console.print(f"\n📁 Project directory: {agentops_dir}")
        console.print(f"📁 Business requirements: {agentops_dir / 'requirements'}")
        console.print(f"📁 Comprehensive tests: {agentops_dir / 'tests'}")
        console.print(f"📁 Business analysis: {agentops_dir / 'analysis'}")
        console.print(f"📁 Traceability: {agentops_dir / 'traceability'}")

@cli.command()
def version():
    """Show AgentOps version information."""
    console.print(Panel.fit(f"AgentOps v{agentops_version}", style="bold blue"))
    console.print(f"📦 Version: {agentops_version}")
    console.print(f"🎯 Focus: Business-focused requirements generation")
    console.print(f"🐍 Python: {sys.version}")
    console.print(f"📁 Working Directory: {get_project_root()}")

@cli.command()
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def onboarding(verbose):
    """Interactive onboarding guide for new users."""
    console.print(Panel.fit(
        "[bold blue]🚀 Welcome to AgentOps![/bold blue]\n\n"
        "This interactive guide will help you get started with AgentOps.\n"
        "It will check your setup, create sample files, and run a demo.",
        title="AgentOps Onboarding",
        border_style="blue"
    ))
    
    # Check installation
    with console.status("[bold green]Checking installation...") as status:
        try:
            result = subprocess.run(
                ["agentops", "version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                console.print("✅ [green]AgentOps is installed and working![/green]")
                console.print(f"   Version: {result.stdout.strip()}")
            else:
                console.print("❌ [red]AgentOps installation check failed[/red]")
                return
        except (subprocess.TimeoutExpired, FileNotFoundError):
            console.print("❌ [red]AgentOps not found. Please install with: pip install agentops-ai[/red]")
            return
    
    # Check API key
    with console.status("[bold green]Checking API key...") as status:
        api_key = os.getenv("OPENAI_API_KEY")
        env_file = Path.cwd() / ".env"
        
        if api_key:
            console.print("✅ [green]OpenAI API key found in environment[/green]")
        elif env_file.exists():
            with open(env_file, 'r') as f:
                content = f.read()
                if "OPENAI_API_KEY" in content:
                    console.print("✅ [green]OpenAI API key found in .env file[/green]")
                else:
                    console.print("⚠️ [yellow]OpenAI API key not found[/yellow]")
                    console.print("   Please set your API key:")
                    console.print("   export OPENAI_API_KEY='your-key-here'")
        else:
            console.print("⚠️ [yellow]OpenAI API key not found[/yellow]")
            console.print("   Please set your API key:")
            console.print("   export OPENAI_API_KEY='your-key-here'")
    
    # Initialize project
    with console.status("[bold green]Initializing project...") as status:
        try:
            result = subprocess.run(
                ["agentops", "init"], 
                capture_output=True, 
                text=True, 
                timeout=30
            )
            if result.returncode == 0:
                console.print("✅ [green]Project initialized successfully![/green]")
            else:
                console.print(f"❌ [red]Project initialization failed: {result.stderr}[/red]")
                return
        except subprocess.TimeoutExpired:
            console.print("❌ [red]Project initialization timed out[/red]")
            return
    
    # Create sample files
    with console.status("[bold green]Creating sample files...") as status:
        sample_dir = Path.cwd() / "sample_files"
        sample_dir.mkdir(exist_ok=True)
        
        # Create calculator.py
        calculator_content = '''def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def calculate_total(items, tax_rate=0.1):
    """Calculate total with tax for a list of items."""
    subtotal = sum(items)
    tax = subtotal * tax_rate
    return subtotal + tax'''
        
        with open(sample_dir / "calculator.py", 'w') as f:
            f.write(calculator_content)
        
        console.print("✅ [green]Created sample files[/green]")
        console.print("   📄 sample_files/calculator.py")
    
    # Run demo
    with console.status("[bold green]Running AgentOps demo...") as status:
        sample_file = sample_dir / "calculator.py"
        try:
            result = subprocess.run(
                ["agentops", "runner", str(sample_file)], 
                capture_output=True, 
                text=True, 
                timeout=120
            )
            
            if result.returncode == 0:
                console.print("✅ [green]Demo completed successfully![/green]")
            else:
                console.print(f"⚠️ [yellow]Demo failed: {result.stderr}[/yellow]")
                console.print("   You can still try with your own files")
                
        except subprocess.TimeoutExpired:
            console.print("⚠️ [yellow]Demo timed out[/yellow]")
            console.print("   You can still try with your own files")
    
    # Show results
    console.print("\n[bold blue]📊 Demo Results:[/bold blue]")
    try:
        result = subprocess.run(
            ["agentops", "status"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        if result.returncode == 0:
            console.print(result.stdout)
    except:
        pass
    
    # Show next steps
    console.print(Panel.fit(
        "[bold green]🎯 Next Steps:[/bold green]\n\n"
        "1. Try AgentOps on your own code:\n"
        "   [blue]agentops runner your_file.py[/blue]\n\n"
        "2. Check project status:\n"
        "   [blue]agentops status[/blue]\n\n"
        "3. View traceability matrix:\n"
        "   [blue]agentops traceability[/blue]\n\n"
        "4. Get help:\n"
        "   [blue]agentops help[/blue]\n\n"
        "5. Read documentation:\n"
        "   [blue]docs/04_user_guides/01_getting_started.md[/blue]\n\n"
        "[bold green]🚀 You're ready to use AgentOps![/bold green]",
        title="Next Steps",
        border_style="green"
    ))
    console.print(f"🔧 Addresses: Code summary → Business requirements transformation")
    
    # After demo, prompt about --all and --auto-approve:
    console.print("\n[bold cyan]💡 Power User Shortcuts:[/bold cyan]")
    console.print("- [green]--all[/green]: Run on all Python files in your project (e.g., agentops runner --all)")
    console.print("- [green]--auto-approve[/green]: Automatically approve all requirements/tests (e.g., agentops runner myfile.py --auto-approve)")
    console.print("- [green]-v[/green]: Verbose output for detailed logs")
    
    # Offer to run a command interactively:
    try:
        import questionary
        if questionary.confirm("Would you like to see AgentOps run on all files with --all?", default=False).ask():
            subprocess.run(["agentops", "runner", "--all", "--auto-approve"])
    except ImportError:
        console.print("\n💡 Tip: Install 'questionary' for interactive prompts: pip install questionary")
        console.print("   You can manually try: agentops runner --all --auto-approve")
    
    # Print summary table:
    table = Table(title="AgentOps Command Shortcuts")
    table.add_column("Command", style="cyan")
    table.add_column("Option/Flag", style="green")
    table.add_column("Description", style="yellow")
    table.add_column("Example", style="blue")
    table.add_row("runner", "--all", "Run on all files", "agentops runner --all")
    table.add_row("runner", "--auto-approve", "Auto-approve all", "agentops runner myfile.py --auto-approve")
    table.add_row("runner", "-v", "Verbose output", "agentops runner myfile.py -v")
    table.add_row("tests", "--all", "Test all files", "agentops tests --all")
    table.add_row("tests", "--auto-approve", "Auto-approve tests", "agentops tests myfile.py --auto-approve")
    table.add_row("analyze", "--all", "Analyze all files", "agentops analyze --all")
    table.add_row("init", "-v", "Verbose output", "agentops init -v")
    table.add_row("status", "-v", "Verbose output", "agentops status -v")
    console.print(table)

@cli.command()
def help():
    """Show help and usage examples."""
    console.print(Panel.fit(
        "[bold blue]AgentOps CLI Help & Examples[/bold blue]\n\n"
        "Essential Commands:\n\n"
        "onboarding - Interactive setup guide for new users\n"
        "  Usage: agentops onboarding\n"
        "  Checks setup, creates samples, runs demo\n\n"
        "init - Initialize AgentOps project structure\n"
        "  Usage: agentops init\n"
        "  Creates .agentops directory and initial configuration\n\n"
        "runner - Complete workflow execution\n"
        "  Usage: agentops runner <file_path>\n"
        "  Performs: requirements → tests → execution → traceability\n"
        "  Example: agentops runner myfile.py\n\n"
        "traceability - Generate traceability matrix\n"
        "  Usage: agentops traceability\n"
        "  Shows requirements-to-tests mapping\n\n"
        "status - Check project status\n"
        "  Usage: agentops status\n"
        "  Shows project artifacts and configuration\n\n"
        "version - Show version information\n"
        "  Usage: agentops version\n"
        "  Shows AgentOps and Python versions\n\n"
        "Workflow Example:\n"
        "1. agentops onboarding              # New user setup (recommended)\n"
        "2. agentops init                    # Initialize project\n"
        "3. agentops runner myfile.py        # Complete analysis\n"
        "4. agentops status                  # Check results\n"
        "5. agentops traceability            # View traceability\n\n"
        "Generated Artifacts:\n"
        "- .agentops/requirements/           # Gherkin & Markdown requirements\n"
        "- .agentops/tests/                  # Generated test cases\n"
        "- .agentops/traceability/           # Traceability matrices\n"
        "- .agentops/reports/                # Analysis reports",
        title="AgentOps CLI Help",
        border_style="blue"
    ))

if __name__ == '__main__':
    cli()
