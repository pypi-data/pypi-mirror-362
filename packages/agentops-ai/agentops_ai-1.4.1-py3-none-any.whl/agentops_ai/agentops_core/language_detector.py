"""Language Detection and Project Structure Analysis for AgentOps.

This module provides automatic detection of programming languages and project
structures to enable multi-language support.
"""

from pathlib import Path
from typing import List, Optional, Set
from enum import Enum
from dataclasses import dataclass


class LanguageType(Enum):
    """Supported programming languages."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    GO = "go"
    RUST = "rust"
    PHP = "php"
    RUBY = "ruby"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    SCALA = "scala"
    CPP = "cpp"
    C = "c"
    UNKNOWN = "unknown"


@dataclass
class ProjectStructure:
    """Project structure information."""

    root_path: Path
    detected_languages: Set[LanguageType]
    primary_language: LanguageType
    test_frameworks: List[str]
    build_tools: List[str]
    package_managers: List[str]
    config_files: List[str]
    source_directories: List[str]
    test_directories: List[str]
    documentation_files: List[str]


class LanguageDetector:
    """Detects programming languages and project structures."""

    # File extensions for each language
    LANGUAGE_EXTENSIONS = {
        LanguageType.PYTHON: {".py", ".pyw", ".pyx", ".pyi"},
        LanguageType.JAVASCRIPT: {".js", ".mjs", ".cjs"},
        LanguageType.TYPESCRIPT: {".ts", ".tsx"},
        LanguageType.JAVA: {".java"},
        LanguageType.CSHARP: {".cs"},
        LanguageType.GO: {".go"},
        LanguageType.RUST: {".rs"},
        LanguageType.PHP: {".php"},
        LanguageType.RUBY: {".rb"},
        LanguageType.SWIFT: {".swift"},
        LanguageType.KOTLIN: {".kt", ".kts"},
        LanguageType.SCALA: {".scala"},
        LanguageType.CPP: {".cpp", ".cc", ".cxx", ".hpp", ".hxx"},
        LanguageType.C: {".c", ".h"},
    }

    # Common test framework patterns
    TEST_FRAMEWORKS = {
        LanguageType.PYTHON: ["pytest", "unittest", "nose", "behave"],
        LanguageType.JAVASCRIPT: ["jest", "mocha", "jasmine", "cypress", "playwright"],
        LanguageType.TYPESCRIPT: ["jest", "mocha", "jasmine", "cypress", "playwright"],
        LanguageType.JAVA: ["junit", "testng", "spock", "cucumber"],
        LanguageType.CSHARP: ["nunit", "xunit", "mstest", "specflow"],
        LanguageType.GO: ["testing", "testify", "ginkgo"],
        LanguageType.RUST: ["cargo test", "criterion"],
        LanguageType.PHP: ["phpunit", "codeception"],
        LanguageType.RUBY: ["rspec", "minitest", "cucumber"],
        LanguageType.SWIFT: ["xctest"],
        LanguageType.KOTLIN: ["junit", "kotlin.test", "spek"],
        LanguageType.SCALA: ["scalatest", "specs2", "junit"],
        LanguageType.CPP: ["gtest", "catch2", "boost.test"],
        LanguageType.C: ["unity", "cmocka", "cunit"],
    }

    # Common build tool patterns
    BUILD_TOOLS = {
        LanguageType.PYTHON: [
            "setup.py",
            "pyproject.toml",
            "requirements.txt",
            "Pipfile",
            "poetry.lock",
        ],
        LanguageType.JAVASCRIPT: ["package.json", "yarn.lock", "pnpm-lock.yaml"],
        LanguageType.TYPESCRIPT: [
            "package.json",
            "tsconfig.json",
            "yarn.lock",
            "pnpm-lock.yaml",
        ],
        LanguageType.JAVA: ["pom.xml", "build.gradle", "gradle.properties"],
        LanguageType.CSHARP: ["*.csproj", "*.sln", "packages.config"],
        LanguageType.GO: ["go.mod", "go.sum"],
        LanguageType.RUST: ["Cargo.toml", "Cargo.lock"],
        LanguageType.PHP: ["composer.json", "composer.lock"],
        LanguageType.RUBY: ["Gemfile", "Gemfile.lock", "Rakefile"],
        LanguageType.SWIFT: ["Package.swift", "*.xcodeproj", "*.xcworkspace"],
        LanguageType.KOTLIN: ["build.gradle.kts", "pom.xml"],
        LanguageType.SCALA: ["build.sbt", "pom.xml"],
        LanguageType.CPP: ["CMakeLists.txt", "Makefile", "*.vcxproj"],
        LanguageType.C: ["Makefile", "CMakeLists.txt", "*.vcxproj"],
    }

    # Common package manager patterns
    PACKAGE_MANAGERS = {
        LanguageType.PYTHON: ["pip", "poetry", "pipenv", "conda"],
        LanguageType.JAVASCRIPT: ["npm", "yarn", "pnpm"],
        LanguageType.TYPESCRIPT: ["npm", "yarn", "pnpm"],
        LanguageType.JAVA: ["maven", "gradle"],
        LanguageType.CSHARP: ["nuget", "dotnet"],
        LanguageType.GO: ["go mod"],
        LanguageType.RUST: ["cargo"],
        LanguageType.PHP: ["composer"],
        LanguageType.RUBY: ["bundler", "gem"],
        LanguageType.SWIFT: ["swift package manager", "cocoapods"],
        LanguageType.KOTLIN: ["gradle", "maven"],
        LanguageType.SCALA: ["sbt", "maven"],
        LanguageType.CPP: ["cmake", "make", "vcpkg", "conan"],
        LanguageType.C: ["make", "cmake"],
    }

    def __init__(self, root_path: Optional[Path] = None):
        """Initialize the language detector."""
        self.root_path = root_path or Path.cwd()

    def detect_language_from_file(self, file_path: Path) -> LanguageType:
        """Detect language from a single file."""
        extension = file_path.suffix.lower()

        for language, extensions in self.LANGUAGE_EXTENSIONS.items():
            if extension in extensions:
                return language

        # Try to detect from file content for files without extensions
        if not extension:
            return self._detect_from_content(file_path)

        return LanguageType.UNKNOWN

    def _detect_from_content(self, file_path: Path) -> LanguageType:
        """Detect language from file content."""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(1024)  # Read first 1KB

            # Simple heuristics based on content
            if "#!/usr/bin/env python" in content or "#!/usr/bin/python" in content:
                return LanguageType.PYTHON
            elif "#!/usr/bin/env node" in content or "#!/usr/bin/node" in content:
                return LanguageType.JAVASCRIPT
            elif "#!/usr/bin/env ruby" in content or "#!/usr/bin/ruby" in content:
                return LanguageType.RUBY
            elif "#!/usr/bin/env php" in content or "#!/usr/bin/php" in content:
                return LanguageType.PHP
            elif "package main" in content and "import" in content:
                return LanguageType.GO
            elif "fn main" in content:
                return LanguageType.RUST
            elif "public class" in content or "public interface" in content:
                return LanguageType.JAVA
            elif "using System;" in content or "namespace" in content:
                return LanguageType.CSHARP
            elif "#include" in content and (
                "int main" in content or "void main" in content
            ):
                return LanguageType.C
            elif "#include" in content and (
                "class" in content or "namespace" in content
            ):
                return LanguageType.CPP

        except Exception:
            pass

        return LanguageType.UNKNOWN

    def analyze_project_structure(self) -> ProjectStructure:
        """Analyze the entire project structure."""
        detected_languages = set()
        test_frameworks = []
        build_tools = []
        package_managers = []
        config_files = []
        source_directories = []
        test_directories = []
        documentation_files = []

        # Scan all files in the project
        for file_path in self.root_path.rglob("*"):
            if file_path.is_file():
                # Detect language from file
                language = self.detect_language_from_file(file_path)
                if language != LanguageType.UNKNOWN:
                    detected_languages.add(language)

                # Check for test frameworks
                if self._is_test_file(file_path):
                    test_frameworks.extend(
                        self._detect_test_frameworks(file_path, language)
                    )

                # Check for build tools
                if self._is_build_file(file_path):
                    build_tools.extend(self._detect_build_tools(file_path, language))

                # Check for package managers
                if self._is_package_file(file_path):
                    package_managers.extend(
                        self._detect_package_managers(file_path, language)
                    )

                # Check for config files
                if self._is_config_file(file_path):
                    config_files.append(str(file_path.relative_to(self.root_path)))

                # Check for documentation
                if self._is_documentation_file(file_path):
                    documentation_files.append(
                        str(file_path.relative_to(self.root_path))
                    )

            elif file_path.is_dir():
                # Check for source and test directories
                dir_name = file_path.name.lower()
                if self._is_source_directory(dir_name):
                    source_directories.append(
                        str(file_path.relative_to(self.root_path))
                    )
                elif self._is_test_directory(dir_name):
                    test_directories.append(str(file_path.relative_to(self.root_path)))

        # Determine primary language
        primary_language = self._determine_primary_language(detected_languages)

        return ProjectStructure(
            root_path=self.root_path,
            detected_languages=detected_languages,
            primary_language=primary_language,
            test_frameworks=list(set(test_frameworks)),
            build_tools=list(set(build_tools)),
            package_managers=list(set(package_managers)),
            config_files=config_files,
            source_directories=source_directories,
            test_directories=test_directories,
            documentation_files=documentation_files,
        )

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file."""
        name = file_path.name.lower()
        return (
            "test" in name
            or "spec" in name
            or name.startswith("test_")
            or name.endswith("_test")
            or name.endswith(".test.")
            or name.endswith(".spec.")
        )

    def _is_build_file(self, file_path: Path) -> bool:
        """Check if file is a build configuration file."""
        name = file_path.name.lower()
        return name in {
            "setup.py",
            "pyproject.toml",
            "requirements.txt",
            "package.json",
            "pom.xml",
            "build.gradle",
            "cargo.toml",
            "go.mod",
            "composer.json",
            "gemfile",
            "cmakelists.txt",
            "makefile",
        }

    def _is_package_file(self, file_path: Path) -> bool:
        """Check if file is a package management file."""
        name = file_path.name.lower()
        return name in {
            "package.json",
            "requirements.txt",
            "pom.xml",
            "build.gradle",
            "cargo.toml",
            "go.mod",
            "composer.json",
            "gemfile",
        }

    def _is_config_file(self, file_path: Path) -> bool:
        """Check if file is a configuration file."""
        name = file_path.name.lower()
        return name in {
            ".gitignore",
            ".env",
            "config.json",
            "tsconfig.json",
            "webpack.config.js",
            "jest.config.js",
            "pytest.ini",
            "tox.ini",
            ".eslintrc",
            ".prettierrc",
        }

    def _is_documentation_file(self, file_path: Path) -> bool:
        """Check if file is a documentation file."""
        name = file_path.name.lower()
        return name in {
            "readme.md",
            "readme.txt",
            "readme.rst",
            "docs.md",
            "documentation.md",
            "changelog.md",
            "license",
            "license.txt",
            "license.md",
        }

    def _is_source_directory(self, dir_name: str) -> bool:
        """Check if directory is a source directory."""
        return dir_name in {
            "src",
            "source",
            "sources",
            "app",
            "lib",
            "libs",
            "main",
            "core",
        }

    def _is_test_directory(self, dir_name: str) -> bool:
        """Check if directory is a test directory."""
        return dir_name in {
            "test",
            "tests",
            "testing",
            "spec",
            "specs",
            "unit",
            "integration",
        }

    def _detect_test_frameworks(
        self, file_path: Path, language: LanguageType
    ) -> List[str]:
        """Detect test frameworks from file content."""
        frameworks = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for framework in self.TEST_FRAMEWORKS.get(language, []):
                if framework.lower() in content.lower():
                    frameworks.append(framework)
        except Exception:
            pass

        return frameworks

    def _detect_build_tools(self, file_path: Path, language: LanguageType) -> List[str]:
        """Detect build tools from file content."""
        tools = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for tool in self.BUILD_TOOLS.get(language, []):
                if tool.lower() in content.lower():
                    tools.append(tool)
        except Exception:
            pass

        return tools

    def _detect_package_managers(
        self, file_path: Path, language: LanguageType
    ) -> List[str]:
        """Detect package managers from file content."""
        managers = []
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()

            for manager in self.PACKAGE_MANAGERS.get(language, []):
                if manager.lower() in content.lower():
                    managers.append(manager)
        except Exception:
            pass

        return managers

    def _determine_primary_language(self, languages: Set[LanguageType]) -> LanguageType:
        """Determine the primary language of the project."""
        if not languages:
            return LanguageType.UNKNOWN

        # Priority order for primary language
        priority_order = [
            LanguageType.PYTHON,
            LanguageType.JAVASCRIPT,
            LanguageType.TYPESCRIPT,
            LanguageType.JAVA,
            LanguageType.CSHARP,
            LanguageType.GO,
            LanguageType.RUST,
            LanguageType.PHP,
            LanguageType.RUBY,
            LanguageType.SWIFT,
            LanguageType.KOTLIN,
            LanguageType.SCALA,
            LanguageType.CPP,
            LanguageType.C,
        ]

        for language in priority_order:
            if language in languages:
                return language

        return list(languages)[0]  # Return first if none in priority order
