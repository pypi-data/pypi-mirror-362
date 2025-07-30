"""Requirement inference module for AgentOps.

Uses LLMs to infer requirements from code changes.
"""

import subprocess
import ast
from typing import Dict, Any, Optional, List
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from .config import get_config

load_dotenv()


class RequirementInferenceEngine:
    """Infers functional requirements from code diffs using LLM."""

    def __init__(self, api_key: Optional[str] = None, model: str = None):
        """Initialize the requirement inference engine.

        Args:
            api_key: OpenAI API key (defaults to config)
            model: OpenAI model to use (defaults to config)
        """
        config = get_config()
        self.api_key = api_key or config.llm.api_key
        self.model = model or config.llm.model
        self.client = OpenAI(api_key=self.api_key)

    def infer_requirements(self, code_files: List[str]) -> Dict[str, Any]:
        """Infer requirements from multiple code files using AST analysis.

        This is the main method that was missing and causing the hallucination issue.

        Args:
            code_files: List of file paths to analyze

        Returns:
            Dict containing inferred requirements with validation
        """
        if not code_files:
            return {"success": False, "error": "No code files provided"}

        all_requirements = []
        analysis_results = {}

        for file_path in code_files:
            try:
                # Read and parse the file
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Parse with AST to get actual code structure
                try:
                    tree = ast.parse(content)
                    code_elements = self._extract_code_elements(tree)
                except SyntaxError as e:
                    analysis_results[file_path] = {
                        "success": False,
                        "error": f"Syntax error in file: {str(e)}",
                    }
                    continue

                # Generate requirements based on actual code elements
                if code_elements["functions"] or code_elements["classes"]:
                    requirements = self._generate_requirements_from_elements(
                        code_elements, file_path, content
                    )

                    # Validate each requirement against the actual code
                    validated_requirements = []
                    for req in requirements:
                        if self._validate_requirement_against_code(
                            req, code_elements, content
                        ):
                            validated_requirements.append(req)

                    all_requirements.extend(validated_requirements)
                    analysis_results[file_path] = {
                        "success": True,
                        "requirements_count": len(validated_requirements),
                        "code_elements": code_elements,
                    }
                else:
                    analysis_results[file_path] = {
                        "success": True,
                        "requirements_count": 0,
                        "note": "No significant code elements found",
                    }

            except Exception as e:
                analysis_results[file_path] = {
                    "success": False,
                    "error": f"Failed to process file: {str(e)}",
                }

        return {
            "success": True,
            "requirements": all_requirements,
            "total_requirements": len(all_requirements),
            "analysis_results": analysis_results,
        }

    def _extract_code_elements(self, tree: ast.AST) -> Dict[str, List[Dict]]:
        """Extract functions, classes, and other code elements from AST."""
        functions = []
        classes = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(
                    {
                        "name": node.name,
                        "args": [arg.arg for arg in node.args.args],
                        "docstring": ast.get_docstring(node),
                        "line_number": node.lineno,
                    }
                )
            elif isinstance(node, ast.ClassDef):
                class_methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        class_methods.append(item.name)

                classes.append(
                    {
                        "name": node.name,
                        "methods": class_methods,
                        "docstring": ast.get_docstring(node),
                        "line_number": node.lineno,
                    }
                )

        return {"functions": functions, "classes": classes}

    def _generate_requirements_from_elements(
        self, code_elements: Dict, file_path: str, content: str
    ) -> List[str]:
        """Generate requirements based on actual code elements."""
        requirements = []

        # Generate requirements for functions
        for func in code_elements["functions"]:
            if func["docstring"]:
                # Use existing docstring as a base for requirement
                requirement = f"Function '{func['name']}' should {func['docstring'].split('.')[0].lower()}."
            else:
                # Generate based on function name and arguments
                args_desc = (
                    f" with parameters {', '.join(func['args'])}"
                    if func["args"]
                    else ""
                )
                requirement = f"Function '{func['name']}' should perform its intended operation{args_desc}."

            requirements.append(requirement)

        # Generate requirements for classes
        for cls in code_elements["classes"]:
            if cls["docstring"]:
                requirement = f"Class '{cls['name']}' should {cls['docstring'].split('.')[0].lower()}."
            else:
                methods_desc = (
                    f" with methods: {', '.join(cls['methods'])}"
                    if cls["methods"]
                    else ""
                )
                requirement = f"Class '{cls['name']}' should provide the required functionality{methods_desc}."

            requirements.append(requirement)

        return requirements

    def _validate_requirement_against_code(
        self, requirement: str, code_elements: Dict, content: str
    ) -> bool:
        """Validate that the requirement references actual code elements."""
        requirement_lower = requirement.lower()

        # Check for generic requirements that should be rejected first
        generic_terms = [
            "should work",
            "should function",
            "should operate",
            "perform its intended operation",
        ]
        if any(term in requirement_lower for term in generic_terms):
            return False

        # Extract function/class names mentioned in the requirement
        import re

        function_matches = re.findall(r"function\s+'([^']+)'", requirement_lower)
        class_matches = re.findall(r"class\s+'([^']+)'", requirement_lower)

        # If specific function/class names are mentioned, they must exist
        if function_matches:
            actual_function_names = [
                func["name"].lower() for func in code_elements["functions"]
            ]
            for mentioned_func in function_matches:
                if mentioned_func not in actual_function_names:
                    return False

        if class_matches:
            actual_class_names = [
                cls["name"].lower() for cls in code_elements["classes"]
            ]
            for mentioned_cls in class_matches:
                if mentioned_cls not in actual_class_names:
                    return False

        # Check if requirement references actual functions (for general references)
        for func in code_elements["functions"]:
            if func["name"].lower() in requirement_lower:
                return True

        # Check if requirement references actual classes (for general references)
        for cls in code_elements["classes"]:
            if cls["name"].lower() in requirement_lower:
                return True

        # If no specific code elements mentioned, require at least some validation
        if not function_matches and not class_matches:
            # Must reference at least one actual code element
            referenced_elements = []
            for func in code_elements["functions"]:
                if func["name"].lower() in requirement_lower:
                    referenced_elements.append(func["name"])
            for cls in code_elements["classes"]:
                if cls["name"].lower() in requirement_lower:
                    referenced_elements.append(cls["name"])

            return len(referenced_elements) > 0

        return True

    def get_git_diff(self, file_path: str) -> Optional[str]:
        """Get git diff for a specific file.

        Args:
            file_path: Path to the file to get diff for

        Returns:
            Git diff as string or None if no diff/error
        """
        try:
            result = subprocess.run(
                ["git", "diff", "HEAD", file_path],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout if result.stdout.strip() else None
        except subprocess.CalledProcessError:
            # Try unstaged changes if no staged changes
            try:
                result = subprocess.run(
                    ["git", "diff", file_path],
                    capture_output=True,
                    text=True,
                    check=True,
                )
                return result.stdout if result.stdout.strip() else None
            except subprocess.CalledProcessError:
                return None

    def get_file_changes(self, file_path: str) -> Optional[str]:
        """Get recent changes for a file using git or file modification.

        Args:
            file_path: Path to the file

        Returns:
            Code diff or None if no changes detected
        """
        # First try git diff
        diff = self.get_git_diff(file_path)
        if diff:
            return diff

        # If no git diff available, read the whole file as "new"
        # This handles new files or non-git projects
        try:
            with open(file_path, "r") as f:
                content = f.read()
            return f"New file: {file_path}\n\n{content}"
        except Exception:
            return None

    def infer_requirement_from_diff(self, diff: str, file_path: str) -> Dict[str, Any]:
        """Infer a functional requirement from a code diff.

        Args:
            diff: Git diff or code changes
            file_path: Path to the file being analyzed

        Returns:
            Dict with requirement, confidence, and metadata
        """
        if not diff or not diff.strip():
            return {"success": False, "error": "No code changes detected"}

        prompt = self._create_inference_prompt(diff, file_path)

        try:
            # Load system prompt from file
            system_prompt = self._load_prompt("requirement_inference.txt")

            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.0,
                max_tokens=200,
            )

            requirement_text = response.choices[0].message.content.strip()

            # Parse the response to extract requirement and confidence
            return self._parse_inference_response(requirement_text, diff, file_path)

        except Exception as e:
            return {"success": False, "error": f"Failed to infer requirement: {str(e)}"}

    def _load_prompt(self, prompt_file: str) -> str:
        """Load a prompt from the prompts directory.

        Args:
            prompt_file: Name of the prompt file

        Returns:
            Prompt content as string
        """
        prompt_path = Path(__file__).parent.parent / "prompts" / prompt_file
        try:
            with open(prompt_path, "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            # Fallback to hardcoded prompt if file not found
            return "You are an expert software analyst. Your job is to infer a single, clear functional requirement from code changes."

    def _create_inference_prompt(self, diff: str, file_path: str) -> str:
        """Create a prompt for requirement inference.

        Args:
            diff: Code diff
            file_path: Path to the file

        Returns:
            Formatted prompt for LLM
        """
        # Load the base prompt template
        base_prompt = self._load_prompt("requirement_inference.txt")

        # Format the prompt with the specific diff and file path
        return base_prompt.format(file_path=file_path, diff=diff)

    def _parse_inference_response(
        self, response: str, diff: str, file_path: str
    ) -> Dict[str, Any]:
        """Parse the LLM response and extract requirement details.

        Args:
            response: Raw LLM response
            diff: Original diff
            file_path: File path

        Returns:
            Parsed requirement data
        """
        # Clean up the response
        requirement = response.strip()

        # Remove any markdown formatting
        if requirement.startswith("```"):
            lines = requirement.split("\n")
            requirement = "\n".join(
                line for line in lines if not line.startswith("```")
            )

        # Extract just the requirement statement
        if "\n" in requirement:
            requirement = requirement.split("\n")[0]

        # Basic validation
        if len(requirement) < 10:
            return {
                "success": False,
                "error": "Generated requirement too short or unclear",
            }

        if len(requirement) > 200:
            return {"success": False, "error": "Generated requirement too long"}

        # Calculate confidence based on diff complexity and requirement clarity
        confidence = self._calculate_confidence(diff, requirement)

        return {
            "success": True,
            "requirement": requirement,
            "confidence": confidence,
            "metadata": {
                "file_path": file_path,
                "diff_lines": len(diff.split("\n")),
                "requirement_length": len(requirement),
            },
        }

    def _calculate_confidence(self, diff: str, requirement: str) -> float:
        """Calculate confidence score for the inferred requirement.

        Args:
            diff: Code diff
            requirement: Inferred requirement

        Returns:
            Confidence score between 0.0 and 1.0
        """
        confidence = 0.8  # Base confidence

        # Adjust based on diff complexity
        diff_lines = len(
            [line for line in diff.split("\n") if line.startswith(("+", "-"))]
        )
        if diff_lines > 20:
            confidence -= 0.1  # Complex changes are harder to infer
        elif diff_lines < 5:
            confidence += 0.1  # Simple changes are easier to infer

        # Adjust based on requirement clarity
        if any(
            keyword in requirement.lower() for keyword in ["should", "must", "will"]
        ):
            confidence += 0.05

        if any(
            keyword in requirement.lower()
            for keyword in ["function", "method", "class"]
        ):
            confidence += 0.05

        # Ensure confidence is within bounds
        return max(0.1, min(1.0, confidence))

    def infer_requirement_from_file(self, file_path: str) -> Dict[str, Any]:
        """Infer requirement from a file by getting its changes and analyzing them.

        Args:
            file_path: Path to the Python file

        Returns:
            Requirement inference result
        """
        # Get file changes
        diff = self.get_file_changes(file_path)
        if not diff:
            return {"success": False, "error": "No changes detected in file"}

        # Infer requirement from diff
        return self.infer_requirement_from_diff(diff, file_path)

    def infer_requirements(self, file_path: str) -> List[Dict[str, Any]]:
        """Infer requirements from a Python file using AST analysis.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            List of requirement dictionaries
        """
        import ast

        try:
            # Read and parse the file
            with open(file_path, "r") as f:
                content = f.read()

            tree = ast.parse(content)
            requirements = []

            # Extract code elements
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    req = {
                        "requirement": f"The function '{node.name}' should perform its intended functionality correctly",
                        "element_type": "function",
                        "element_name": node.name,
                        "confidence": 0.8,
                        "metadata": {
                            "file_path": file_path,
                            "line_number": node.lineno,
                            "element_type": "function",
                        },
                    }
                    requirements.append(req)

                elif isinstance(node, ast.ClassDef):
                    req = {
                        "requirement": f"The class '{node.name}' should implement its defined interface correctly",
                        "element_type": "class",
                        "element_name": node.name,
                        "confidence": 0.8,
                        "metadata": {
                            "file_path": file_path,
                            "line_number": node.lineno,
                            "element_type": "class",
                        },
                    }
                    requirements.append(req)

            # Validate requirements using RequirementValidator
            try:
                from .requirement_validator import RequirementValidator

                validator = RequirementValidator()

                validated_requirements = []
                for req in requirements:
                    if validator.validate_requirement(req, file_path):
                        validated_requirements.append(req)
                    else:
                        print(f"⚠️  Requirement rejected: {req['requirement']}")

                return validated_requirements

            except ImportError:
                # If validator not available, return all requirements
                return requirements

        except Exception as e:
            print(f"❌ Error analyzing file {file_path}: {str(e)}")
            return []
