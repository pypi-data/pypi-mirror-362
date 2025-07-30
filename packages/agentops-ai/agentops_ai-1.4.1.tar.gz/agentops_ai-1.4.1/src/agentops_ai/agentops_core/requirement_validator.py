"""Requirement validation module for AgentOps.

Validates that generated requirements are actually based on real code.
"""

import ast
import re
from typing import Dict, Any, List, Tuple


class RequirementValidator:
    """Validates requirements against actual code to prevent hallucinations."""

    def __init__(self):
        """Initialize the requirement validator."""
        self.validation_rules = [
            self._validate_code_existence,
            self._validate_element_references,
            self._validate_requirement_specificity,
            self._validate_requirement_clarity,
            self._validate_requirement_testability,
        ]

    def validate_requirement(
        self, requirement: Dict[str, Any], file_path: str
    ) -> Tuple[bool, List[str]]:
        """Validate a single requirement against the actual code.

        Args:
            requirement: The requirement dictionary to validate
            file_path: Path to the source file

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        try:
            # Read and parse the source code
            with open(file_path, "r") as f:
                code = f.read()

            code_analysis = self._analyze_code(code)

            # Run all validation rules
            for rule in self.validation_rules:
                is_valid, rule_issues = rule(requirement, code_analysis, file_path)
                if not is_valid:
                    issues.extend(rule_issues)

            return len(issues) == 0, issues

        except Exception as e:
            return False, [f"Validation error: {str(e)}"]

    def validate_requirements_batch(
        self, requirements: List[Dict[str, Any]], file_path: str
    ) -> Dict[str, Any]:
        """Validate multiple requirements and return detailed results.

        Args:
            requirements: List of requirement dictionaries
            file_path: Path to the source file

        Returns:
            Dictionary with validation results
        """
        results = {
            "total_requirements": len(requirements),
            "valid_requirements": [],
            "invalid_requirements": [],
            "validation_summary": {},
        }

        for i, requirement in enumerate(requirements):
            is_valid, issues = self.validate_requirement(requirement, file_path)

            requirement_result = {
                "requirement": requirement,
                "index": i,
                "is_valid": is_valid,
                "issues": issues,
            }

            if is_valid:
                results["valid_requirements"].append(requirement_result)
            else:
                results["invalid_requirements"].append(requirement_result)

        # Generate summary
        results["validation_summary"] = {
            "valid_count": len(results["valid_requirements"]),
            "invalid_count": len(results["invalid_requirements"]),
            "validity_rate": (
                len(results["valid_requirements"]) / len(requirements)
                if requirements
                else 0
            ),
            "common_issues": self._get_common_issues(results["invalid_requirements"]),
        }

        return results

    def _analyze_code(self, code: str) -> Dict[str, Any]:
        """Analyze code structure to extract elements for validation."""
        try:
            tree = ast.parse(code)

            functions = []
            classes = []
            imports = []
            variables = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(
                        {
                            "name": node.name,
                            "lineno": node.lineno,
                            "args": [arg.arg for arg in node.args.args],
                            "docstring": ast.get_docstring(node) or "",
                            "decorators": [
                                d.id
                                for d in node.decorator_list
                                if isinstance(d, ast.Name)
                            ],
                        }
                    )
                elif isinstance(node, ast.ClassDef):
                    methods = []
                    for child in node.body:
                        if isinstance(child, ast.FunctionDef):
                            methods.append(child.name)

                    classes.append(
                        {
                            "name": node.name,
                            "lineno": node.lineno,
                            "methods": methods,
                            "docstring": ast.get_docstring(node) or "",
                            "bases": [
                                base.id
                                for base in node.bases
                                if isinstance(base, ast.Name)
                            ],
                        }
                    )
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    for alias in node.names:
                        imports.append(f"{module}.{alias.name}")
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variables.append(target.id)

            return {
                "functions": functions,
                "classes": classes,
                "imports": imports,
                "variables": variables,
                "total_functions": len(functions),
                "total_classes": len(classes),
            }

        except Exception as e:
            return {
                "functions": [],
                "classes": [],
                "imports": [],
                "variables": [],
                "total_functions": 0,
                "total_classes": 0,
                "parse_error": str(e),
            }

    def _validate_code_existence(
        self, requirement: Dict[str, Any], code_analysis: Dict[str, Any], file_path: str
    ) -> Tuple[bool, List[str]]:
        """Validate that the requirement references actually existing code elements."""
        issues = []
        requirement_text = requirement.get("requirement_text", "").lower()

        # Check if requirement mentions specific functions
        for func in code_analysis["functions"]:
            if func["name"].lower() in requirement_text:
                # Function exists, this is good
                return True, []

        # Check if requirement mentions specific classes
        for cls in code_analysis["classes"]:
            if cls["name"].lower() in requirement_text:
                # Class exists, this is good
                return True, []

        # Check if requirement mentions specific variables
        for var in code_analysis["variables"]:
            if var.lower() in requirement_text:
                # Variable exists, this is good
                return True, []

        # If no specific elements are mentioned, check for generic but valid patterns
        if any(
            word in requirement_text
            for word in ["function", "method", "class", "module", "file"]
        ):
            # Generic but acceptable
            return True, []

        issues.append("Requirement does not reference any existing code elements")
        return False, issues

    def _validate_element_references(
        self, requirement: Dict[str, Any], code_analysis: Dict[str, Any], file_path: str
    ) -> Tuple[bool, List[str]]:
        """Validate that element references in metadata match actual code."""
        issues = []
        metadata = requirement.get("metadata", {})

        # Check element name reference
        element_name = metadata.get("element_name", "")
        element_type = metadata.get("element_type", "")

        if element_name and element_type:
            if element_type == "function":
                func_names = [f["name"] for f in code_analysis["functions"]]
                if element_name not in func_names:
                    issues.append(
                        f"Function '{element_name}' referenced in requirement does not exist in code"
                    )

            elif element_type == "class":
                class_names = [c["name"] for c in code_analysis["classes"]]
                if element_name not in class_names:
                    issues.append(
                        f"Class '{element_name}' referenced in requirement does not exist in code"
                    )

        return len(issues) == 0, issues

    def _validate_requirement_specificity(
        self, requirement: Dict[str, Any], code_analysis: Dict[str, Any], file_path: str
    ) -> Tuple[bool, List[str]]:
        """Validate that requirements are specific enough to be testable."""
        issues = []
        requirement_text = requirement.get("requirement_text", "")

        # Check for overly generic requirements
        generic_patterns = [
            r"should work",
            r"should function",
            r"should operate",
            r"should run",
            r"should execute",
            r"should process",
            r"should handle",
            r"should manage",
        ]

        for pattern in generic_patterns:
            if re.search(pattern, requirement_text.lower()):
                # Check if there's enough additional context
                words = requirement_text.split()
                if len(words) < 10:
                    issues.append("Requirement is too generic and lacks specificity")
                    break

        # Check for requirements that are too short
        if len(requirement_text.split()) < 5:
            issues.append("Requirement is too short to be meaningful")

        # Check for requirements that are too long
        if len(requirement_text.split()) > 50:
            issues.append("Requirement is too long and may be unclear")

        return len(issues) == 0, issues

    def _validate_requirement_clarity(
        self, requirement: Dict[str, Any], code_analysis: Dict[str, Any], file_path: str
    ) -> Tuple[bool, List[str]]:
        """Validate that requirements are clear and understandable."""
        issues = []
        requirement_text = requirement.get("requirement_text", "")

        # Check for unclear or ambiguous language
        unclear_patterns = [
            r"should somehow",
            r"should maybe",
            r"should possibly",
            r"should try to",
            r"should attempt to",
            r"should ideally",
            r"should preferably",
        ]

        for pattern in unclear_patterns:
            if re.search(pattern, requirement_text.lower()):
                issues.append("Requirement uses unclear or ambiguous language")
                break

        # Check for requirements that don't start with clear action words
        action_words = [
            "should",
            "must",
            "will",
            "shall",
            "needs to",
            "has to",
            "the function should",
            "the class should",
            "the system should",
        ]

        if not any(requirement_text.lower().startswith(word) for word in action_words):
            issues.append("Requirement does not start with a clear action statement")

        return len(issues) == 0, issues

    def _validate_requirement_testability(
        self, requirement: Dict[str, Any], code_analysis: Dict[str, Any], file_path: str
    ) -> Tuple[bool, List[str]]:
        """Validate that requirements can be converted into testable assertions."""
        issues = []
        requirement_text = requirement.get("requirement_text", "")

        # Check for requirements that mention specific inputs/outputs
        has_inputs = any(
            word in requirement_text.lower()
            for word in ["input", "parameter", "argument", "data"]
        )
        has_outputs = any(
            word in requirement_text.lower()
            for word in ["output", "return", "result", "response"]
        )

        if not (has_inputs or has_outputs):
            # Check if it's a class requirement that mentions methods
            if (
                "class" in requirement_text.lower()
                and "method" in requirement_text.lower()
            ):
                pass  # Class requirements can be testable without explicit inputs/outputs
            else:
                issues.append(
                    "Requirement does not specify inputs or outputs, making it difficult to test"
                )

        # Check for requirements that mention specific conditions
        has_conditions = any(
            word in requirement_text.lower()
            for word in ["when", "if", "given", "provided"]
        )

        if not has_conditions and not has_inputs:
            issues.append(
                "Requirement does not specify conditions or inputs for testing"
            )

        return len(issues) == 0, issues

    def _get_common_issues(
        self, invalid_requirements: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        """Get a summary of common validation issues."""
        issue_counts = {}

        for req_result in invalid_requirements:
            for issue in req_result["issues"]:
                issue_counts[issue] = issue_counts.get(issue, 0) + 1

        return dict(sorted(issue_counts.items(), key=lambda x: x[1], reverse=True))
