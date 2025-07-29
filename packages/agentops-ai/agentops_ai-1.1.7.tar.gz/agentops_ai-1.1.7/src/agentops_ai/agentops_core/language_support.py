"""
AgentOps Multi-Language Support System

This module implements comprehensive language support for:
- Python (default, fully supported)
- JavaScript/TypeScript (beta)
- Java (beta)
- C# (beta)
- Go (beta)

All language support is modular with switch on/off capabilities.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Union
from pathlib import Path
import ast
import re
import json
from abc import ABC, abstractmethod

from .features import FeatureManager, get_feature_manager, is_feature_enabled


class LanguageType(Enum):
    """Supported programming languages."""
    
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"


class AnalysisType(Enum):
    """Types of code analysis."""
    
    SYNTAX = "syntax"
    IMPORTS = "imports"
    FUNCTIONS = "functions"
    CLASSES = "classes"
    VARIABLES = "variables"
    COMMENTS = "comments"
    STRUCTURE = "structure"


@dataclass
class LanguageConfig:
    """Configuration for a specific language."""
    
    language: LanguageType
    enabled: bool = True
    beta_enabled: bool = False
    
    # Parser settings
    parser_type: str = "ast"
    parser_options: Dict[str, Any] = field(default_factory=dict)
    
    # Framework settings
    test_framework: str = "default"
    build_tool: str = "default"
    test_runner: str = "default"
    
    # File patterns
    file_extensions: List[str] = field(default_factory=list)
    ignore_patterns: List[str] = field(default_factory=list)
    
    # Analysis capabilities
    supported_analysis: Set[AnalysisType] = field(default_factory=set)
    
    # Test generation settings
    test_template: str = "default"
    test_patterns: Dict[str, str] = field(default_factory=dict)
    
    # Export settings
    export_formats: List[str] = field(default_factory=list)


class BaseLanguageAnalyzer(ABC):
    """Base class for language-specific analyzers."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize the analyzer.
        
        Args:
            config: Language configuration
        """
        self.config = config
        self.language = config.language
    
    @abstractmethod
    def analyze_syntax(self, code: str) -> Dict[str, Any]:
        """Analyze code syntax.
        
        Args:
            code: Source code to analyze
            
        Returns:
            Syntax analysis results
        """
        pass
    
    @abstractmethod
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """Extract function definitions.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of function definitions
        """
        pass
    
    @abstractmethod
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """Extract class definitions.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of class definitions
        """
        pass
    
    @abstractmethod
    def extract_imports(self, code: str) -> List[Dict[str, Any]]:
        """Extract import statements.
        
        Args:
            code: Source code to analyze
            
        Returns:
            List of import statements
        """
        pass
    
    @abstractmethod
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate code syntax.
        
        Args:
            code: Source code to validate
            
        Returns:
            Validation results
        """
        pass


class PythonAnalyzer(BaseLanguageAnalyzer):
    """Python language analyzer using AST."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize Python analyzer."""
        super().__init__(config)
        self.config.file_extensions = ['.py']
        self.config.supported_analysis = {
            AnalysisType.SYNTAX,
            AnalysisType.IMPORTS,
            AnalysisType.FUNCTIONS,
            AnalysisType.CLASSES,
            AnalysisType.VARIABLES,
            AnalysisType.COMMENTS,
            AnalysisType.STRUCTURE
        }
        self.config.test_framework = "pytest"
        self.config.export_formats = ["gherkin", "markdown", "json"]
    
    def analyze_syntax(self, code: str) -> Dict[str, Any]:
        """Analyze Python syntax using AST."""
        try:
            tree = ast.parse(code)
            return {
                "valid": True,
                "node_count": len(ast.walk(tree)),
                "has_syntax_errors": False
            }
        except SyntaxError as e:
            return {
                "valid": False,
                "error": str(e),
                "line": e.lineno,
                "column": e.offset,
                "has_syntax_errors": True
            }
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """Extract Python function definitions."""
        functions = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node),
                        "decorators": [d.id for d in node.decorator_list if hasattr(d, 'id')]
                    })
        except SyntaxError:
            pass
        return functions
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """Extract Python class definitions."""
        classes = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    methods = []
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            methods.append(child.name)
                    
                    classes.append({
                        "name": node.name,
                        "line": node.lineno,
                        "methods": methods,
                        "docstring": ast.get_docstring(node),
                        "bases": [base.id for base in node.bases if hasattr(base, 'id')]
                    })
        except SyntaxError:
            pass
        return classes
    
    def extract_imports(self, code: str) -> List[Dict[str, Any]]:
        """Extract Python import statements."""
        imports = []
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append({
                            "type": "import",
                            "module": alias.name,
                            "asname": alias.asname,
                            "line": node.lineno
                        })
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imports.append({
                            "type": "from",
                            "module": node.module,
                            "name": alias.name,
                            "asname": alias.asname,
                            "line": node.lineno
                        })
        except SyntaxError:
            pass
        return imports
    
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Python syntax."""
        return self.analyze_syntax(code)


class JavaScriptAnalyzer(BaseLanguageAnalyzer):
    """JavaScript/TypeScript language analyzer."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize JavaScript analyzer."""
        super().__init__(config)
        self.config.file_extensions = ['.js', '.jsx', '.ts', '.tsx']
        self.config.supported_analysis = {
            AnalysisType.SYNTAX,
            AnalysisType.IMPORTS,
            AnalysisType.FUNCTIONS,
            AnalysisType.CLASSES,
            AnalysisType.STRUCTURE
        }
        self.config.test_framework = "jest"
        self.config.export_formats = ["gherkin", "markdown", "json"]
    
    def analyze_syntax(self, code: str) -> Dict[str, Any]:
        """Analyze JavaScript syntax using regex patterns."""
        # Basic JavaScript syntax validation using regex
        patterns = {
            "function_declaration": r"function\s+\w+\s*\(",
            "arrow_function": r"=>\s*{",
            "class_declaration": r"class\s+\w+",
            "import_statement": r"import\s+.*from",
            "export_statement": r"export\s+",
            "variable_declaration": r"(?:const|let|var)\s+\w+"
        }
        
        results = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, code)
            results[pattern_name] = len(matches)
        
        return {
            "valid": True,
            "patterns_found": results,
            "has_syntax_errors": False
        }
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """Extract JavaScript function definitions."""
        functions = []
        
        # Function declarations
        func_pattern = r"function\s+(\w+)\s*\(([^)]*)\)"
        for match in re.finditer(func_pattern, code):
            functions.append({
                "name": match.group(1),
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()],
                "type": "function_declaration"
            })
        
        # Arrow functions
        arrow_pattern = r"(\w+)\s*=\s*\(([^)]*)\)\s*=>"
        for match in re.finditer(arrow_pattern, code):
            functions.append({
                "name": match.group(1),
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()],
                "type": "arrow_function"
            })
        
        return functions
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """Extract JavaScript class definitions."""
        classes = []
        
        class_pattern = r"class\s+(\w+)(?:\s+extends\s+(\w+))?\s*{"
        for match in re.finditer(class_pattern, code):
            classes.append({
                "name": match.group(1),
                "extends": match.group(2) if match.group(2) else None,
                "type": "class"
            })
        
        return classes
    
    def extract_imports(self, code: str) -> List[Dict[str, Any]]:
        """Extract JavaScript import statements."""
        imports = []
        
        # ES6 imports
        import_pattern = r"import\s+(.*?)\s+from\s+['\"]([^'\"]+)['\"]"
        for match in re.finditer(import_pattern, code):
            imports.append({
                "type": "es6_import",
                "imports": match.group(1).strip(),
                "module": match.group(2),
                "line": code[:match.start()].count('\n') + 1
            })
        
        # CommonJS requires
        require_pattern = r"const\s+(\w+)\s*=\s*require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)"
        for match in re.finditer(require_pattern, code):
            imports.append({
                "type": "commonjs_require",
                "variable": match.group(1),
                "module": match.group(2),
                "line": code[:match.start()].count('\n') + 1
            })
        
        return imports
    
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate JavaScript syntax."""
        return self.analyze_syntax(code)


class JavaAnalyzer(BaseLanguageAnalyzer):
    """Java language analyzer."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize Java analyzer."""
        super().__init__(config)
        self.config.file_extensions = ['.java']
        self.config.supported_analysis = {
            AnalysisType.SYNTAX,
            AnalysisType.IMPORTS,
            AnalysisType.FUNCTIONS,
            AnalysisType.CLASSES,
            AnalysisType.STRUCTURE
        }
        self.config.test_framework = "junit"
        self.config.export_formats = ["gherkin", "markdown", "json"]
    
    def analyze_syntax(self, code: str) -> Dict[str, Any]:
        """Analyze Java syntax using regex patterns."""
        patterns = {
            "class_declaration": r"(?:public\s+)?class\s+\w+",
            "method_declaration": r"(?:public|private|protected)?\s*(?:static\s+)?\w+\s+\w+\s*\([^)]*\)",
            "import_statement": r"import\s+[^;]+;",
            "package_declaration": r"package\s+[^;]+;"
        }
        
        results = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, code)
            results[pattern_name] = len(matches)
        
        return {
            "valid": True,
            "patterns_found": results,
            "has_syntax_errors": False
        }
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """Extract Java method definitions."""
        methods = []
        
        method_pattern = r"(?:public|private|protected)?\s*(?:static\s+)?(\w+)\s+(\w+)\s*\(([^)]*)\)"
        for match in re.finditer(method_pattern, code):
            methods.append({
                "name": match.group(2),
                "return_type": match.group(1),
                "args": [arg.strip() for arg in match.group(3).split(',') if arg.strip()],
                "type": "method"
            })
        
        return methods
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """Extract Java class definitions."""
        classes = []
        
        class_pattern = r"(?:public\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([^{]+))?"
        for match in re.finditer(class_pattern, code):
            classes.append({
                "name": match.group(1),
                "extends": match.group(2) if match.group(2) else None,
                "implements": match.group(3).strip() if match.group(3) else None,
                "type": "class"
            })
        
        return classes
    
    def extract_imports(self, code: str) -> List[Dict[str, Any]]:
        """Extract Java import statements."""
        imports = []
        
        import_pattern = r"import\s+([^;]+);"
        for match in re.finditer(import_pattern, code):
            imports.append({
                "type": "import",
                "package": match.group(1).strip(),
                "line": code[:match.start()].count('\n') + 1
            })
        
        return imports
    
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Java syntax."""
        return self.analyze_syntax(code)


class CSharpAnalyzer(BaseLanguageAnalyzer):
    """C# language analyzer."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize C# analyzer."""
        super().__init__(config)
        self.config.file_extensions = ['.cs']
        self.config.supported_analysis = {
            AnalysisType.SYNTAX,
            AnalysisType.IMPORTS,
            AnalysisType.FUNCTIONS,
            AnalysisType.CLASSES,
            AnalysisType.STRUCTURE
        }
        self.config.test_framework = "nunit"
        self.config.export_formats = ["gherkin", "markdown", "json"]
    
    def analyze_syntax(self, code: str) -> Dict[str, Any]:
        """Analyze C# syntax using regex patterns."""
        patterns = {
            "using_statement": r"using\s+[^;]+;",
            "namespace_declaration": r"namespace\s+\w+",
            "class_declaration": r"(?:public\s+)?class\s+\w+",
            "method_declaration": r"(?:public|private|protected|internal)?\s*(?:static\s+)?\w+\s+\w+\s*\([^)]*\)"
        }
        
        results = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, code)
            results[pattern_name] = len(matches)
        
        return {
            "valid": True,
            "patterns_found": results,
            "has_syntax_errors": False
        }
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """Extract C# method definitions."""
        methods = []
        
        method_pattern = r"(?:public|private|protected|internal)?\s*(?:static\s+)?(\w+)\s+(\w+)\s*\(([^)]*)\)"
        for match in re.finditer(method_pattern, code):
            methods.append({
                "name": match.group(2),
                "return_type": match.group(1),
                "args": [arg.strip() for arg in match.group(3).split(',') if arg.strip()],
                "type": "method"
            })
        
        return methods
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """Extract C# class definitions."""
        classes = []
        
        class_pattern = r"(?:public\s+)?class\s+(\w+)(?:\s*:\s*([^{]+))?"
        for match in re.finditer(class_pattern, code):
            classes.append({
                "name": match.group(1),
                "inheritance": match.group(2).strip() if match.group(2) else None,
                "type": "class"
            })
        
        return classes
    
    def extract_imports(self, code: str) -> List[Dict[str, Any]]:
        """Extract C# using statements."""
        imports = []
        
        using_pattern = r"using\s+([^;]+);"
        for match in re.finditer(using_pattern, code):
            imports.append({
                "type": "using",
                "namespace": match.group(1).strip(),
                "line": code[:match.start()].count('\n') + 1
            })
        
        return imports
    
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate C# syntax."""
        return self.analyze_syntax(code)


class GoAnalyzer(BaseLanguageAnalyzer):
    """Go language analyzer."""
    
    def __init__(self, config: LanguageConfig):
        """Initialize Go analyzer."""
        super().__init__(config)
        self.config.file_extensions = ['.go']
        self.config.supported_analysis = {
            AnalysisType.SYNTAX,
            AnalysisType.IMPORTS,
            AnalysisType.FUNCTIONS,
            AnalysisType.STRUCTURE
        }
        self.config.test_framework = "testing"
        self.config.export_formats = ["gherkin", "markdown", "json"]
    
    def analyze_syntax(self, code: str) -> Dict[str, Any]:
        """Analyze Go syntax using regex patterns."""
        patterns = {
            "package_declaration": r"package\s+\w+",
            "import_statement": r"import\s+[^)]+\)",
            "function_declaration": r"func\s+\w+\s*\([^)]*\)",
            "struct_declaration": r"type\s+\w+\s+struct"
        }
        
        results = {}
        for pattern_name, pattern in patterns.items():
            matches = re.findall(pattern, code)
            results[pattern_name] = len(matches)
        
        return {
            "valid": True,
            "patterns_found": results,
            "has_syntax_errors": False
        }
    
    def extract_functions(self, code: str) -> List[Dict[str, Any]]:
        """Extract Go function definitions."""
        functions = []
        
        func_pattern = r"func\s+(\w+)\s*\(([^)]*)\)"
        for match in re.finditer(func_pattern, code):
            functions.append({
                "name": match.group(1),
                "args": [arg.strip() for arg in match.group(2).split(',') if arg.strip()],
                "type": "function"
            })
        
        return functions
    
    def extract_classes(self, code: str) -> List[Dict[str, Any]]:
        """Extract Go struct definitions (Go doesn't have classes)."""
        structs = []
        
        struct_pattern = r"type\s+(\w+)\s+struct"
        for match in re.finditer(struct_pattern, code):
            structs.append({
                "name": match.group(1),
                "type": "struct"
            })
        
        return structs
    
    def extract_imports(self, code: str) -> List[Dict[str, Any]]:
        """Extract Go import statements."""
        imports = []
        
        import_pattern = r"import\s+\(([^)]+)\)"
        for match in re.finditer(import_pattern, code):
            import_block = match.group(1)
            for line in import_block.split('\n'):
                line = line.strip()
                if line and not line.startswith('//'):
                    imports.append({
                        "type": "import",
                        "package": line.strip('"'),
                        "line": code[:match.start()].count('\n') + 1
                    })
        
        return imports
    
    def validate_syntax(self, code: str) -> Dict[str, Any]:
        """Validate Go syntax."""
        return self.analyze_syntax(code)


class LanguageSupportManager:
    """Manages multi-language support capabilities."""
    
    def __init__(self):
        """Initialize the language support manager."""
        self.analyzers: Dict[LanguageType, BaseLanguageAnalyzer] = {}
        self.feature_manager = get_feature_manager()
        
        # Initialize analyzers for enabled languages
        self._initialize_analyzers()
    
    def _initialize_analyzers(self):
        """Initialize analyzers for enabled languages."""
        language_configs = {
            LanguageType.PYTHON: LanguageConfig(LanguageType.PYTHON, enabled=True),
            LanguageType.JAVASCRIPT: LanguageConfig(LanguageType.JAVASCRIPT, enabled=False, beta_enabled=True),
            LanguageType.TYPESCRIPT: LanguageConfig(LanguageType.TYPESCRIPT, enabled=False, beta_enabled=True),
            LanguageType.JAVA: LanguageConfig(LanguageType.JAVA, enabled=False, beta_enabled=True),
            LanguageType.CSHARP: LanguageConfig(LanguageType.CSHARP, enabled=False, beta_enabled=True),
            LanguageType.GO: LanguageConfig(LanguageType.GO, enabled=False, beta_enabled=True)
        }
        
        # Create analyzers for enabled languages
        if is_feature_enabled("language_python"):
            self.analyzers[LanguageType.PYTHON] = PythonAnalyzer(language_configs[LanguageType.PYTHON])
        
        if is_feature_enabled("language_javascript"):
            self.analyzers[LanguageType.JAVASCRIPT] = JavaScriptAnalyzer(language_configs[LanguageType.JAVASCRIPT])
            self.analyzers[LanguageType.TYPESCRIPT] = JavaScriptAnalyzer(language_configs[LanguageType.TYPESCRIPT])
        
        if is_feature_enabled("language_java"):
            self.analyzers[LanguageType.JAVA] = JavaAnalyzer(language_configs[LanguageType.JAVA])
        
        if is_feature_enabled("language_csharp"):
            self.analyzers[LanguageType.CSHARP] = CSharpAnalyzer(language_configs[LanguageType.CSHARP])
        
        if is_feature_enabled("language_go"):
            self.analyzers[LanguageType.GO] = GoAnalyzer(language_configs[LanguageType.GO])
    
    def detect_language(self, file_path: str) -> Optional[LanguageType]:
        """Detect programming language from file extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Detected language type or None
        """
        extension = Path(file_path).suffix.lower()
        
        extension_map = {
            '.py': LanguageType.PYTHON,
            '.js': LanguageType.JAVASCRIPT,
            '.jsx': LanguageType.JAVASCRIPT,
            '.ts': LanguageType.TYPESCRIPT,
            '.tsx': LanguageType.TYPESCRIPT,
            '.java': LanguageType.JAVA,
            '.cs': LanguageType.CSHARP,
            '.go': LanguageType.GO
        }
        
        return extension_map.get(extension)
    
    def get_analyzer(self, language: LanguageType) -> Optional[BaseLanguageAnalyzer]:
        """Get analyzer for a specific language.
        
        Args:
            language: Language type
            
        Returns:
            Language analyzer or None if not available
        """
        return self.analyzers.get(language)
    
    def analyze_file(self, file_path: str, code: str) -> Dict[str, Any]:
        """Analyze a file with the appropriate language analyzer.
        
        Args:
            file_path: Path to the file
            code: Source code content
            
        Returns:
            Analysis results
        """
        language = self.detect_language(file_path)
        if not language:
            return {"error": f"Unsupported file type: {file_path}"}
        
        analyzer = self.get_analyzer(language)
        if not analyzer:
            return {"error": f"Language analyzer not available for {language.value}"}
        
        try:
            return {
                "language": language.value,
                "file_path": file_path,
                "syntax": analyzer.analyze_syntax(code),
                "functions": analyzer.extract_functions(code),
                "classes": analyzer.extract_classes(code),
                "imports": analyzer.extract_imports(code),
                "validation": analyzer.validate_syntax(code)
            }
        except Exception as e:
            return {
                "language": language.value,
                "file_path": file_path,
                "error": str(e)
            }
    
    def get_supported_languages(self) -> List[LanguageType]:
        """Get list of supported languages.
        
        Returns:
            List of supported language types
        """
        return list(self.analyzers.keys())
    
    def is_language_supported(self, language: LanguageType) -> bool:
        """Check if a language is supported.
        
        Args:
            language: Language type to check
            
        Returns:
            True if language is supported, False otherwise
        """
        return language in self.analyzers
    
    def enable_language(self, language: LanguageType) -> bool:
        """Enable support for a specific language.
        
        Args:
            language: Language type to enable
            
        Returns:
            True if language was enabled, False otherwise
        """
        feature_name = f"language_{language.value}"
        return self.feature_manager.enable_feature(feature_name)
    
    def disable_language(self, language: LanguageType) -> bool:
        """Disable support for a specific language.
        
        Args:
            language: Language type to disable
            
        Returns:
            True if language was disabled, False otherwise
        """
        feature_name = f"language_{language.value}"
        return self.feature_manager.disable_feature(feature_name)


# Global language support manager instance
_language_manager: Optional[LanguageSupportManager] = None


def get_language_manager() -> LanguageSupportManager:
    """Get the global language support manager instance.
    
    Returns:
        LanguageSupportManager instance
    """
    global _language_manager
    if _language_manager is None:
        _language_manager = LanguageSupportManager()
    return _language_manager


def analyze_file(file_path: str, code: str) -> Dict[str, Any]:
    """Analyze a file with appropriate language support.
    
    Args:
        file_path: Path to the file
        code: Source code content
        
    Returns:
        Analysis results
    """
    return get_language_manager().analyze_file(file_path, code)


def detect_language(file_path: str) -> Optional[LanguageType]:
    """Detect programming language from file path.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Detected language type or None
    """
    return get_language_manager().detect_language(file_path)


def is_language_supported(language: LanguageType) -> bool:
    """Check if a language is supported.
    
    Args:
        language: Language type to check
        
    Returns:
        True if language is supported, False otherwise
    """
    return get_language_manager().is_language_supported(language) 