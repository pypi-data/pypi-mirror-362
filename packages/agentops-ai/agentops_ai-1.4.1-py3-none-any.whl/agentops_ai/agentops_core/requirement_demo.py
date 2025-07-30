"""Demonstration script for requirement validation system.

Shows how the system prevents hallucinated requirements and validates against actual code.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, List

# Add the parent directory to the path to import our modules
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    from agentops_ai.agentops_core.requirement_inference import (
        RequirementInferenceEngine,
    )
    from agentops_ai.agentops_core.requirement_validator import RequirementValidator
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent))
    from requirement_inference import RequirementInferenceEngine
    from requirement_validator import RequirementValidator


def create_test_file(file_path: str, content: str):
    """Create a test file with the given content."""
    # Fix: Handle files in current directory
    directory = os.path.dirname(file_path)
    if directory:  # Only create directory if there is one
        os.makedirs(directory, exist_ok=True)

    with open(file_path, "w") as f:
        f.write(content)


def demonstrate_validation():
    """Demonstrate the requirement validation system."""
    print("🔍 AgentOps Requirement Validation Demo")
    print("=" * 50)

    # Create test files
    test_dir = "test_validation"

    # Test file 1: Simple function
    simple_func_content = '''
def calculate_factorial(n):
    """Calculate the factorial of a number."""
    if n <= 1:
        return 1
    return n * calculate_factorial(n - 1)

def add_numbers(a, b):
    """Add two numbers together."""
    return a + b
'''

    # Test file 2: Class with methods
    class_content = '''
class UserManager:
    """Manage user operations."""
    
    def __init__(self):
        self.users = {}
    
    def add_user(self, user_id, name):
        """Add a new user."""
        self.users[user_id] = name
        return True
    
    def get_user(self, user_id):
        """Get user by ID."""
        return self.users.get(user_id)
    
    def delete_user(self, user_id):
        """Delete user by ID."""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
'''

    # Test file 3: Empty file (should generate no valid requirements)
    empty_content = """
# This is an empty file with no functions or classes
import os
import sys

# Just some imports and comments
"""

    # Create the test files
    create_test_file(f"{test_dir}/simple_func.py", simple_func_content)
    create_test_file(f"{test_dir}/user_manager.py", class_content)
    create_test_file(f"{test_dir}/empty_file.py", empty_content)

    # Initialize the inference engine and validator
    try:
        engine = RequirementInferenceEngine()
        validator = RequirementValidator()
        has_api_key = True
    except Exception as e:
        print(f"⚠️  API key issue: {str(e)}")
        print("Running validation-only demo without LLM generation...")
        validator = RequirementValidator()
        has_api_key = False

    # Test each file
    test_files = [
        f"{test_dir}/simple_func.py",
        f"{test_dir}/user_manager.py",
        f"{test_dir}/empty_file.py",
    ]

    for file_path in test_files:
        print(f"\n📁 Testing: {file_path}")
        print("-" * 30)

        try:
            if has_api_key:
                # Extract requirements using LLM
                requirements = engine.infer_requirements(file_path)
            else:
                # Create mock requirements for demonstration
                requirements = create_mock_requirements(file_path)

            print(f"Generated {len(requirements)} requirements:")

            for i, req in enumerate(requirements, 1):
                print(f"  {i}. {req.get('requirement_text', '')}")
                print(f"     Confidence: {req.get('confidence', 0):.2f}")
                print(
                    f"     Source: {req.get('metadata', {}).get('source', 'unknown')}"
                )
                print()

            # Validate requirements
            validation_results = validator.validate_requirements_batch(
                requirements, file_path
            )

            print("Validation Results:")
            print(f"  Valid: {validation_results['validation_summary']['valid_count']}")
            print(
                f"  Invalid: {validation_results['validation_summary']['invalid_count']}"
            )
            print(
                f"  Validity Rate: {validation_results['validation_summary']['validity_rate']:.2%}"
            )

            if validation_results["invalid_requirements"]:
                print("\n❌ Invalid Requirements:")
                for invalid_req in validation_results["invalid_requirements"]:
                    print(
                        f"  - {invalid_req['requirement'].get('requirement_text', '')[:80]}..."
                    )
                    print(f"    Issues: {', '.join(invalid_req['issues'])}")

            if validation_results["validation_summary"]["common_issues"]:
                print("\n🔍 Common Issues:")
                for issue, count in validation_results["validation_summary"][
                    "common_issues"
                ].items():
                    print(f"  - {issue}: {count} occurrences")

        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")

    # Cleanup
    import shutil

    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    print("\n✅ Demo completed!")


def create_mock_requirements(file_path: str) -> List[Dict[str, Any]]:
    """Create mock requirements for demonstration when API key is not available."""
    filename = os.path.basename(file_path)

    if "simple_func" in filename:
        return [
            {
                "requirement_text": "The calculate_factorial function should calculate the factorial of a positive integer and return the result.",
                "confidence": 0.9,
                "metadata": {
                    "file_path": file_path,
                    "element_type": "function",
                    "element_name": "calculate_factorial",
                    "line_number": 2,
                    "parameters": ["n"],
                    "source": "mock_demo",
                },
            },
            {
                "requirement_text": "The add_numbers function should add two numbers together and return the sum.",
                "confidence": 0.9,
                "metadata": {
                    "file_path": file_path,
                    "element_type": "function",
                    "element_name": "add_numbers",
                    "line_number": 7,
                    "parameters": ["a", "b"],
                    "source": "mock_demo",
                },
            },
        ]
    elif "user_manager" in filename:
        return [
            {
                "requirement_text": "The UserManager class should manage user operations and provide methods for adding, getting, and deleting users.",
                "confidence": 0.9,
                "metadata": {
                    "file_path": file_path,
                    "element_type": "class",
                    "element_name": "UserManager",
                    "line_number": 3,
                    "methods": ["__init__", "add_user", "get_user", "delete_user"],
                    "source": "mock_demo",
                },
            }
        ]
    elif "empty_file" in filename:
        return [
            {
                "requirement_text": "The system should process user data and generate reports.",
                "confidence": 0.8,
                "metadata": {
                    "file_path": file_path,
                    "element_type": "file",
                    "element_name": "empty_file.py",
                    "source": "mock_demo",
                },
            }
        ]
    else:
        return []


def demonstrate_hallucination_prevention():
    """Demonstrate how the system prevents hallucinated requirements."""
    print("\n🛡️ Hallucination Prevention Demo")
    print("=" * 50)

    # Create a file with minimal content
    minimal_content = """
# This file has very little content
x = 1
y = 2
"""

    test_file = "test_minimal.py"
    create_test_file(test_file, minimal_content)

    try:
        engine = RequirementInferenceEngine()
        validator = RequirementValidator()
        has_api_key = True
    except Exception:
        validator = RequirementValidator()
        has_api_key = False

    print(f"Testing minimal file: {test_file}")
    print("Content:")
    print(minimal_content)

    # Extract requirements
    if has_api_key:
        requirements = engine.infer_requirements(test_file)
    else:
        # Create a mock hallucinated requirement for demonstration
        requirements = [
            {
                "requirement_text": "The system should process user data and generate reports.",
                "confidence": 0.8,
                "metadata": {
                    "file_path": test_file,
                    "element_type": "file",
                    "element_name": "test_minimal.py",
                    "source": "mock_hallucination",
                },
            }
        ]

    print(f"\nGenerated {len(requirements)} requirements:")
    for i, req in enumerate(requirements, 1):
        print(f"  {i}. {req.get('requirement_text', '')}")

    # Validate requirements
    validation_results = validator.validate_requirements_batch(requirements, test_file)

    print("\nValidation Results:")
    print(f"  Valid: {validation_results['validation_summary']['valid_count']}")
    print(f"  Invalid: {validation_results['validation_summary']['invalid_count']}")

    if validation_results["invalid_requirements"]:
        print("\n❌ Rejected Hallucinated Requirements:")
        for invalid_req in validation_results["invalid_requirements"]:
            print(f"  - {invalid_req['requirement'].get('requirement_text', '')}")
            print(f"    Issues: {', '.join(invalid_req['issues'])}")

    # Cleanup
    if os.path.exists(test_file):
        os.remove(test_file)

    print("\n✅ Hallucination prevention demo completed!")


if __name__ == "__main__":
    demonstrate_validation()
    demonstrate_hallucination_prevention()
