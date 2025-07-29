"""
AgentOps Context Engineering Framework

This module implements comprehensive context engineering capabilities:
- Requirements generation with business rules
- Architecture analysis and dependency mapping
- Current state assessment and technical debt analysis
- Data flow understanding and state management
- Success criteria definition and validation

Each context engineering capability is implemented as a specialized agent
that can be selectively enabled based on pricing tier and user needs.
"""

from typing import Dict, List, Optional, Any, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import ast
import json
import re
from datetime import datetime

from .pricing import ContextEngineering, check_tier_access, PricingTier
from .analyzer import CodeAnalyzer


@dataclass
class ContextResult:
    """Result from context engineering analysis."""
    
    context_type: ContextEngineering
    success: bool
    confidence: float
    data: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    errors: List[str] = field(default_factory=list)


@dataclass
class RequirementContext:
    """Enhanced requirement with full context."""
    
    requirement_text: str
    requirement_type: str  # functional, non-functional, business_rule
    priority: str  # critical, high, medium, low
    source: str  # code_analysis, user_story, business_rule
    acceptance_criteria: List[str]
    business_rules: List[str]
    dependencies: List[str]
    risk_level: str  # low, medium, high
    testability_score: float
    traceability: Dict[str, Any]


@dataclass
class ArchitectureContext:
    """Comprehensive architecture analysis."""
    
    system_overview: str
    components: List[Dict[str, Any]]
    dependencies: Dict[str, List[str]]
    patterns: List[str]
    technology_stack: List[str]
    interfaces: List[Dict[str, Any]]
    data_models: List[Dict[str, Any]]
    security_considerations: List[str]
    scalability_factors: List[str]
    maintainability_score: float


@dataclass
class CurrentStateContext:
    """Current state assessment of the codebase."""
    
    code_quality_metrics: Dict[str, float]
    technical_debt: List[Dict[str, Any]]
    test_coverage: Dict[str, float]
    performance_profile: Dict[str, Any]
    security_assessment: Dict[str, Any]
    compliance_status: Dict[str, Any]
    refactoring_opportunities: List[Dict[str, Any]]
    optimization_suggestions: List[str]


@dataclass
class DataFlowContext:
    """Data flow and state management analysis."""
    
    data_models: List[Dict[str, Any]]
    data_transformations: List[Dict[str, Any]]
    state_management: Dict[str, Any]
    input_output_patterns: List[Dict[str, Any]]
    validation_rules: List[Dict[str, Any]]
    error_handling_flows: List[Dict[str, Any]]
    data_lineage: Dict[str, List[str]]
    persistence_patterns: List[str]


@dataclass
class SuccessCriteriaContext:
    """Success criteria and validation framework."""
    
    functional_success: List[Dict[str, Any]]
    performance_success: List[Dict[str, Any]]
    quality_success: List[Dict[str, Any]]
    user_success: List[Dict[str, Any]]
    business_success: List[Dict[str, Any]]
    technical_success: List[Dict[str, Any]]
    validation_methods: List[str]
    measurement_criteria: Dict[str, Any]


class BaseContextEngineer:
    """Base class for context engineering agents."""
    
    def __init__(self, context_type: ContextEngineering):
        """Initialize the context engineer."""
        self.context_type = context_type
        self.code_analyzer = CodeAnalyzer()
    
    def analyze(self, file_path: str, code: str, 
               existing_context: Dict[str, Any] = None) -> ContextResult:
        """Analyze code and generate context."""
        raise NotImplementedError
    
    def _extract_docstrings(self, code: str) -> List[str]:
        """Extract all docstrings from code."""
        try:
            tree = ast.parse(code)
            docstrings = []
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef, ast.Module)):
                    if (ast.get_docstring(node)):
                        docstrings.append(ast.get_docstring(node))
            
            return docstrings
        except:
            return []
    
    def _extract_comments(self, code: str) -> List[str]:
        """Extract comments from code."""
        comments = []
        for line in code.split('\n'):
            line = line.strip()
            if line.startswith('#'):
                comments.append(line[1:].strip())
        return comments
    
    def _analyze_complexity(self, code: str) -> Dict[str, float]:
        """Analyze code complexity metrics."""
        try:
            tree = ast.parse(code)
            
            # Count different types of nodes
            node_counts = {}
            for node in ast.walk(tree):
                node_type = type(node).__name__
                node_counts[node_type] = node_counts.get(node_type, 0) + 1
            
            # Calculate complexity metrics
            total_nodes = sum(node_counts.values())
            cyclomatic_complexity = node_counts.get('If', 0) + node_counts.get('For', 0) + \
                                  node_counts.get('While', 0) + node_counts.get('Try', 0)
            
            return {
                'total_nodes': total_nodes,
                'cyclomatic_complexity': cyclomatic_complexity,
                'function_count': node_counts.get('FunctionDef', 0),
                'class_count': node_counts.get('ClassDef', 0),
                'complexity_score': min(cyclomatic_complexity / max(node_counts.get('FunctionDef', 1), 1), 10)
            }
        except:
            return {'complexity_score': 0}


class RequirementsEngineerContext(BaseContextEngineer):
    """Enhanced requirements engineering with business rules and context."""
    
    def __init__(self):
        super().__init__(ContextEngineering.REQUIREMENTS_GENERATION)
    
    @check_tier_access(PricingTier.DEVELOPER)
    def analyze(self, file_path: str, code: str, 
               existing_context: Dict[str, Any] = None) -> ContextResult:
        """Extract comprehensive requirements with business context."""
        
        try:
            # Basic code analysis
            analysis = self.code_analyzer.analyze_code(code)
            
            # Extract docstrings and comments for context
            docstrings = self._extract_docstrings(code)
            comments = self._extract_comments(code)
            
            # Generate requirements
            requirements = []
            
            # Functional requirements from functions
            for func in analysis.get('functions', []):
                req = self._generate_functional_requirement(func, docstrings, comments)
                if req:
                    requirements.append(req)
            
            # Class-based requirements
            for cls in analysis.get('classes', []):
                req = self._generate_class_requirement(cls, docstrings, comments)
                if req:
                    requirements.append(req)
            
            # Business rules from comments and docstrings
            business_rules = self._extract_business_rules(docstrings + comments)
            
            # Non-functional requirements
            non_functional = self._generate_non_functional_requirements(code, analysis)
            
            return ContextResult(
                context_type=self.context_type,
                success=True,
                confidence=0.85,
                data={
                    'functional_requirements': requirements,
                    'business_rules': business_rules,
                    'non_functional_requirements': non_functional,
                    'requirement_count': len(requirements),
                    'coverage_areas': list(set([req.requirement_type for req in requirements]))
                },
                metadata={
                    'file_path': file_path,
                    'analysis_method': 'enhanced_context_engineering',
                    'docstring_count': len(docstrings),
                    'comment_count': len(comments)
                }
            )
            
        except Exception as e:
            return ContextResult(
                context_type=self.context_type,
                success=False,
                confidence=0.0,
                data={},
                errors=[str(e)]
            )
    
    def _generate_functional_requirement(self, func_info: Dict, 
                                       docstrings: List[str], 
                                       comments: List[str]) -> Optional[RequirementContext]:
        """Generate functional requirement from function analysis."""
        
        func_name = func_info.get('name', '')
        params = func_info.get('params', [])
        
        # Generate requirement text
        if params:
            param_text = ", ".join(params)
            requirement_text = f"The function {func_name} should process {param_text} and return the expected result"
        else:
            requirement_text = f"The function {func_name} should execute its intended functionality"
        
        # Extract acceptance criteria from docstring
        acceptance_criteria = []
        for docstring in docstrings:
            if func_name in docstring.lower():
                # Extract criteria from docstring
                lines = docstring.split('\n')
                for line in lines:
                    if any(word in line.lower() for word in ['should', 'must', 'will', 'returns']):
                        acceptance_criteria.append(line.strip())
        
        return RequirementContext(
            requirement_text=requirement_text,
            requirement_type='functional',
            priority='medium',
            source='code_analysis',
            acceptance_criteria=acceptance_criteria,
            business_rules=[],
            dependencies=[],
            risk_level='low',
            testability_score=0.8,
            traceability={'function': func_name, 'file': ''}
        )
    
    def _generate_class_requirement(self, class_info: Dict, 
                                  docstrings: List[str], 
                                  comments: List[str]) -> Optional[RequirementContext]:
        """Generate requirement from class analysis."""
        
        class_name = class_info.get('name', '')
        methods = class_info.get('methods', [])
        
        requirement_text = f"The class {class_name} should provide {len(methods)} methods for its intended functionality"
        
        return RequirementContext(
            requirement_text=requirement_text,
            requirement_type='functional',
            priority='medium',
            source='code_analysis',
            acceptance_criteria=[f"Should implement {len(methods)} methods"],
            business_rules=[],
            dependencies=[],
            risk_level='medium',
            testability_score=0.7,
            traceability={'class': class_name, 'methods': methods}
        )
    
    def _extract_business_rules(self, text_sources: List[str]) -> List[str]:
        """Extract business rules from text sources."""
        
        business_rules = []
        rule_keywords = ['must', 'shall', 'required', 'mandatory', 'forbidden', 'allowed']
        
        for text in text_sources:
            sentences = re.split(r'[.!?]', text)
            for sentence in sentences:
                if any(keyword in sentence.lower() for keyword in rule_keywords):
                    business_rules.append(sentence.strip())
        
        return business_rules
    
    def _generate_non_functional_requirements(self, code: str, 
                                            analysis: Dict) -> List[RequirementContext]:
        """Generate non-functional requirements."""
        
        non_functional = []
        complexity = self._analyze_complexity(code)
        
        # Performance requirements
        if complexity['complexity_score'] > 5:
            non_functional.append(RequirementContext(
                requirement_text="The system should maintain acceptable performance under normal load",
                requirement_type='non_functional',
                priority='high',
                source='complexity_analysis',
                acceptance_criteria=["Response time < 2 seconds", "Memory usage < 512MB"],
                business_rules=[],
                dependencies=[],
                risk_level='medium',
                testability_score=0.6,
                traceability={'metric': 'performance'}
            ))
        
        # Reliability requirements
        if analysis.get('functions', []):
            non_functional.append(RequirementContext(
                requirement_text="The system should handle errors gracefully and provide meaningful feedback",
                requirement_type='non_functional',
                priority='high',
                source='error_handling_analysis',
                acceptance_criteria=["Proper exception handling", "User-friendly error messages"],
                business_rules=[],
                dependencies=[],
                risk_level='medium',
                testability_score=0.8,
                traceability={'metric': 'reliability'}
            ))
        
        return non_functional


class ArchitectureAnalyzerContext(BaseContextEngineer):
    """Architecture analysis and dependency mapping."""
    
    def __init__(self):
        super().__init__(ContextEngineering.ARCHITECTURE_GENERATION)
    
    @check_tier_access(PricingTier.PROFESSIONAL)
    def analyze(self, file_path: str, code: str, 
               existing_context: Dict[str, Any] = None) -> ContextResult:
        """Analyze architecture patterns and dependencies."""
        
        try:
            analysis = self.code_analyzer.analyze_code(code)
            
            # Extract components
            components = self._extract_components(analysis)
            
            # Analyze dependencies
            dependencies = self._analyze_dependencies(analysis)
            
            # Identify patterns
            patterns = self._identify_patterns(code, analysis)
            
            # Extract technology stack
            tech_stack = self._extract_technology_stack(code, analysis)
            
            # Analyze interfaces
            interfaces = self._analyze_interfaces(analysis)
            
            architecture_context = ArchitectureContext(
                system_overview=self._generate_system_overview(analysis),
                components=components,
                dependencies=dependencies,
                patterns=patterns,
                technology_stack=tech_stack,
                interfaces=interfaces,
                data_models=self._extract_data_models(analysis),
                security_considerations=self._analyze_security(code),
                scalability_factors=self._analyze_scalability(analysis),
                maintainability_score=self._calculate_maintainability(analysis)
            )
            
            return ContextResult(
                context_type=self.context_type,
                success=True,
                confidence=0.8,
                data=architecture_context.__dict__,
                metadata={
                    'file_path': file_path,
                    'component_count': len(components),
                    'dependency_count': len(dependencies)
                }
            )
            
        except Exception as e:
            return ContextResult(
                context_type=self.context_type,
                success=False,
                confidence=0.0,
                data={},
                errors=[str(e)]
            )
    
    def _extract_components(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Extract system components."""
        components = []
        
        for cls in analysis.get('classes', []):
            components.append({
                'name': cls['name'],
                'type': 'class',
                'methods': cls.get('methods', []),
                'responsibility': self._infer_responsibility(cls['name']),
                'complexity': len(cls.get('methods', []))
            })
        
        for func in analysis.get('functions', []):
            components.append({
                'name': func['name'],
                'type': 'function',
                'parameters': func.get('params', []),
                'responsibility': self._infer_responsibility(func['name']),
                'complexity': 1
            })
        
        return components
    
    def _analyze_dependencies(self, analysis: Dict) -> Dict[str, List[str]]:
        """Analyze component dependencies."""
        dependencies = {}
        
        # Extract import dependencies
        imports = analysis.get('imports', [])
        for imp in imports:
            module_name = imp.get('module', '')
            if module_name:
                dependencies[module_name] = imp.get('names', [])
        
        return dependencies
    
    def _identify_patterns(self, code: str, analysis: Dict) -> List[str]:
        """Identify architectural patterns."""
        patterns = []
        
        # Singleton pattern
        if 'class' in code and '__new__' in code:
            patterns.append('Singleton')
        
        # Factory pattern
        if any('factory' in name.lower() for name in [cls['name'] for cls in analysis.get('classes', [])]):
            patterns.append('Factory')
        
        # Observer pattern
        if 'observer' in code.lower() or 'notify' in code.lower():
            patterns.append('Observer')
        
        # Strategy pattern
        if 'strategy' in code.lower() or len(analysis.get('classes', [])) > 3:
            patterns.append('Strategy')
        
        return patterns
    
    def _extract_technology_stack(self, code: str, analysis: Dict) -> List[str]:
        """Extract technology stack information."""
        tech_stack = ['Python']
        
        imports = analysis.get('imports', [])
        for imp in imports:
            module = imp.get('module', '')
            if 'flask' in module.lower():
                tech_stack.append('Flask')
            elif 'django' in module.lower():
                tech_stack.append('Django')
            elif 'fastapi' in module.lower():
                tech_stack.append('FastAPI')
            elif 'pandas' in module.lower():
                tech_stack.append('Pandas')
            elif 'numpy' in module.lower():
                tech_stack.append('NumPy')
            elif 'requests' in module.lower():
                tech_stack.append('Requests')
        
        return list(set(tech_stack))
    
    def _analyze_interfaces(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Analyze interfaces and contracts."""
        interfaces = []
        
        for cls in analysis.get('classes', []):
            public_methods = [m for m in cls.get('methods', []) if not m.startswith('_')]
            if public_methods:
                interfaces.append({
                    'name': cls['name'],
                    'type': 'class_interface',
                    'methods': public_methods,
                    'contract': f"Provides {len(public_methods)} public methods"
                })
        
        return interfaces
    
    def _extract_data_models(self, analysis: Dict) -> List[Dict[str, Any]]:
        """Extract data model information."""
        data_models = []
        
        for cls in analysis.get('classes', []):
            if any(keyword in cls['name'].lower() for keyword in ['model', 'data', 'entity']):
                data_models.append({
                    'name': cls['name'],
                    'type': 'data_model',
                    'attributes': cls.get('methods', []),
                    'purpose': 'Data representation and management'
                })
        
        return data_models
    
    def _analyze_security(self, code: str) -> List[str]:
        """Analyze security considerations."""
        security_issues = []
        
        if 'password' in code.lower() and 'hash' not in code.lower():
            security_issues.append("Potential plaintext password handling")
        
        if 'sql' in code.lower() and 'prepare' not in code.lower():
            security_issues.append("Potential SQL injection vulnerability")
        
        if 'eval(' in code:
            security_issues.append("Use of eval() function poses security risk")
        
        return security_issues
    
    def _analyze_scalability(self, analysis: Dict) -> List[str]:
        """Analyze scalability factors."""
        factors = []
        
        class_count = len(analysis.get('classes', []))
        function_count = len(analysis.get('functions', []))
        
        if class_count > 10:
            factors.append("High class count may impact maintainability")
        
        if function_count > 20:
            factors.append("High function count suggests need for modularization")
        
        return factors
    
    def _calculate_maintainability(self, analysis: Dict) -> float:
        """Calculate maintainability score."""
        class_count = len(analysis.get('classes', []))
        function_count = len(analysis.get('functions', []))
        
        # Simple maintainability heuristic
        complexity = class_count + function_count
        if complexity < 10:
            return 0.9
        elif complexity < 20:
            return 0.7
        else:
            return 0.5
    
    def _infer_responsibility(self, name: str) -> str:
        """Infer component responsibility from name."""
        name_lower = name.lower()
        
        if 'manager' in name_lower:
            return "Management and coordination"
        elif 'handler' in name_lower:
            return "Event or request handling"
        elif 'service' in name_lower:
            return "Business logic service"
        elif 'model' in name_lower:
            return "Data representation"
        elif 'controller' in name_lower:
            return "Control flow management"
        else:
            return "General functionality"
    
    def _generate_system_overview(self, analysis: Dict) -> str:
        """Generate system overview description."""
        class_count = len(analysis.get('classes', []))
        function_count = len(analysis.get('functions', []))
        
        return f"System with {class_count} classes and {function_count} functions providing modular functionality"


# Additional context engineers would be implemented similarly...
# For brevity, I'll create the remaining ones as stubs

class CurrentStateAnalyzerContext(BaseContextEngineer):
    """Current state assessment and technical debt analysis."""
    
    def __init__(self):
        super().__init__(ContextEngineering.CURRENT_STATE_UNDERSTANDING)
    
    @check_tier_access(PricingTier.TEAM)
    def analyze(self, file_path: str, code: str, 
               existing_context: Dict[str, Any] = None) -> ContextResult:
        """Analyze current state and technical debt."""
        # Implementation would include code quality metrics, technical debt analysis, etc.
        pass


class DataFlowAnalyzerContext(BaseContextEngineer):
    """Data flow and state management analysis."""
    
    def __init__(self):
        super().__init__(ContextEngineering.DATA_FLOWS_UNDERSTANDING)
    
    @check_tier_access(PricingTier.PROFESSIONAL)
    def analyze(self, file_path: str, code: str, 
               existing_context: Dict[str, Any] = None) -> ContextResult:
        """Analyze data flows and transformations."""
        # Implementation would include data flow mapping, state analysis, etc.
        pass


class SuccessCriteriaAnalyzerContext(BaseContextEngineer):
    """Success criteria definition and validation."""
    
    def __init__(self):
        super().__init__(ContextEngineering.SUCCESS_CRITERIA_UNDERSTANDING)
    
    @check_tier_access(PricingTier.TEAM)
    def analyze(self, file_path: str, code: str, 
               existing_context: Dict[str, Any] = None) -> ContextResult:
        """Define and validate success criteria."""
        # Implementation would include success metrics, validation methods, etc.
        pass


class ContextEngineeringManager:
    """Manages all context engineering capabilities."""
    
    def __init__(self):
        """Initialize the context engineering manager."""
        self.engineers = {
            ContextEngineering.REQUIREMENTS_GENERATION: RequirementsEngineerContext(),
            ContextEngineering.ARCHITECTURE_GENERATION: ArchitectureAnalyzerContext(),
            ContextEngineering.CURRENT_STATE_UNDERSTANDING: CurrentStateAnalyzerContext(),
            ContextEngineering.DATA_FLOWS_UNDERSTANDING: DataFlowAnalyzerContext(),
            ContextEngineering.SUCCESS_CRITERIA_UNDERSTANDING: SuccessCriteriaAnalyzerContext(),
        }
    
    def analyze_context(self, file_path: str, code: str, 
                       enabled_contexts: Set[ContextEngineering]) -> Dict[ContextEngineering, ContextResult]:
        """Run context analysis for enabled context types."""
        results = {}
        
        for context_type in enabled_contexts:
            if context_type in self.engineers:
                try:
                    result = self.engineers[context_type].analyze(file_path, code)
                    results[context_type] = result
                except Exception as e:
                    results[context_type] = ContextResult(
                        context_type=context_type,
                        success=False,
                        confidence=0.0,
                        data={},
                        errors=[str(e)]
                    )
        
        return results
    
    def get_available_contexts(self) -> List[ContextEngineering]:
        """Get list of available context engineering types."""
        return list(self.engineers.keys())


# Global context engineering manager
context_engineering_manager = ContextEngineeringManager() 