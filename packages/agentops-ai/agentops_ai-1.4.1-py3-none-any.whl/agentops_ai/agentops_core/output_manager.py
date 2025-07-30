"""Automatic Output Organization for AgentOps.

This module provides intelligent organization of generated outputs based on
project structure, language, and user preferences.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from .language_detector import LanguageType, ProjectStructure


@dataclass
class OutputConfig:
    """Configuration for output organization."""

    base_dir: Path
    language: LanguageType
    project_structure: ProjectStructure
    organize_by_language: bool = True
    organize_by_date: bool = True
    organize_by_type: bool = True
    preserve_structure: bool = True
    create_backups: bool = True


class OutputManager:
    """Manages automatic organization of AgentOps outputs."""

    # Output type mappings
    OUTPUT_TYPES = {
        "requirements": {
            "extensions": [".gherkin", ".md", ".txt", ".json"],
            "subdir": "requirements",
            "description": "Requirements and specifications",
        },
        "tests": {
            "extensions": [
                ".py",
                ".js",
                ".ts",
                ".java",
                ".cs",
                ".go",
                ".rs",
                ".php",
                ".rb",
            ],
            "subdir": "tests",
            "description": "Generated test files",
        },
        "traceability": {
            "extensions": [".md", ".csv", ".json", ".html"],
            "subdir": "traceability",
            "description": "Traceability matrices and reports",
        },
        "reports": {
            "extensions": [".md", ".html", ".pdf", ".json"],
            "subdir": "reports",
            "description": "Analysis reports and summaries",
        },
        "documentation": {
            "extensions": [".md", ".rst", ".txt", ".html"],
            "subdir": "docs",
            "description": "Generated documentation",
        },
        "config": {
            "extensions": [".json", ".yaml", ".yml", ".toml", ".ini"],
            "subdir": "config",
            "description": "Configuration files",
        },
    }

    # Language-specific output patterns
    LANGUAGE_PATTERNS = {
        LanguageType.PYTHON: {
            "test_prefix": "test_",
            "test_suffix": "_test.py",
            "test_dir": "tests",
            "source_dir": "src",
            "config_files": ["pytest.ini", "tox.ini", "setup.cfg"],
        },
        LanguageType.JAVASCRIPT: {
            "test_prefix": "",
            "test_suffix": ".test.js",
            "test_dir": "tests",
            "source_dir": "src",
            "config_files": ["jest.config.js", "webpack.config.js", ".eslintrc"],
        },
        LanguageType.TYPESCRIPT: {
            "test_prefix": "",
            "test_suffix": ".test.ts",
            "test_dir": "tests",
            "source_dir": "src",
            "config_files": ["jest.config.js", "tsconfig.json", ".eslintrc"],
        },
        LanguageType.JAVA: {
            "test_prefix": "",
            "test_suffix": "Test.java",
            "test_dir": "src/test/java",
            "source_dir": "src/main/java",
            "config_files": ["pom.xml", "build.gradle"],
        },
        LanguageType.CSHARP: {
            "test_prefix": "",
            "test_suffix": "Tests.cs",
            "test_dir": "Tests",
            "source_dir": "src",
            "config_files": ["*.csproj", "*.sln"],
        },
        LanguageType.GO: {
            "test_prefix": "",
            "test_suffix": "_test.go",
            "test_dir": "",
            "source_dir": "",
            "config_files": ["go.mod", "go.sum"],
        },
        LanguageType.RUST: {
            "test_prefix": "",
            "test_suffix": "_test.rs",
            "test_dir": "tests",
            "source_dir": "src",
            "config_files": ["Cargo.toml", "Cargo.lock"],
        },
    }

    def __init__(self, config: OutputConfig):
        """Initialize the output manager."""
        self.config = config
        self.output_dir = self._create_output_directory()
        self._setup_directory_structure()

    def _create_output_directory(self) -> Path:
        """Create the main output directory with timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if self.config.organize_by_date:
            base_name = f"agentops_output_{timestamp}"
        else:
            base_name = "agentops_output"

        output_dir = self.config.base_dir / base_name

        # Create directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)

        return output_dir

    def _setup_directory_structure(self):
        """Set up the organized directory structure."""
        # Create main subdirectories
        for output_type, info in self.OUTPUT_TYPES.items():
            if self.config.organize_by_type:
                subdir = self.output_dir / info["subdir"]
                subdir.mkdir(exist_ok=True)

        # Create language-specific directories
        if self.config.organize_by_language:
            lang_dir = self.output_dir / self.config.language.value
            lang_dir.mkdir(exist_ok=True)

            # Create language-specific subdirectories
            for output_type, info in self.OUTPUT_TYPES.items():
                if self.config.organize_by_type:
                    lang_subdir = lang_dir / info["subdir"]
                    lang_subdir.mkdir(exist_ok=True)

    def organize_file(
        self, file_path: Path, output_type: str, source_file: Optional[Path] = None
    ) -> Path:
        """Organize a single file into the appropriate directory structure."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Determine target directory
        target_dir = self._get_target_directory(output_type, source_file)

        # Create target directory if it doesn't exist
        target_dir.mkdir(parents=True, exist_ok=True)

        # Generate target filename
        target_filename = self._generate_target_filename(
            file_path, output_type, source_file
        )
        target_path = target_dir / target_filename

        # Copy file to target location
        shutil.copy2(file_path, target_path)

        return target_path

    def organize_directory(self, source_dir: Path, output_type: str) -> Dict[str, Path]:
        """Organize all files in a directory."""
        organized_files = {}

        if not source_dir.exists():
            return organized_files

        for file_path in source_dir.rglob("*"):
            if file_path.is_file():
                try:
                    target_path = self.organize_file(file_path, output_type, source_dir)
                    organized_files[str(file_path)] = target_path
                except Exception as e:
                    print(f"Warning: Failed to organize {file_path}: {e}")

        return organized_files

    def _get_target_directory(
        self, output_type: str, source_file: Optional[Path] = None
    ) -> Path:
        """Get the target directory for a specific output type."""
        if output_type not in self.OUTPUT_TYPES:
            raise ValueError(f"Unknown output type: {output_type}")

        base_dir = self.output_dir

        # Add language-specific directory
        if self.config.organize_by_language:
            base_dir = base_dir / self.config.language.value

        # Add type-specific directory
        if self.config.organize_by_type:
            base_dir = base_dir / self.OUTPUT_TYPES[output_type]["subdir"]

        # Add source file structure if preserving structure
        if self.config.preserve_structure and source_file:
            relative_path = source_file.parent.relative_to(
                self.config.project_structure.root_path
            )
            if str(relative_path) != ".":
                base_dir = base_dir / relative_path

        return base_dir

    def _generate_target_filename(
        self, file_path: Path, output_type: str, source_file: Optional[Path] = None
    ) -> str:
        """Generate an appropriate filename for the target file."""
        original_name = file_path.name

        # If we have a source file, try to create a related name
        if source_file:
            source_name = source_file.stem
            extension = file_path.suffix

            # Generate test filename based on language patterns
            if output_type == "tests":
                lang_patterns = self.LANGUAGE_PATTERNS.get(self.config.language, {})
                test_prefix = lang_patterns.get("test_prefix", "test_")
                test_suffix = lang_patterns.get("test_suffix", "_test")

                if extension == ".py":
                    return f"{test_prefix}{source_name}{test_suffix}.py"
                elif extension == ".js":
                    return f"{source_name}{test_suffix}.js"
                elif extension == ".ts":
                    return f"{source_name}{test_suffix}.ts"
                elif extension == ".java":
                    return f"{source_name}{test_suffix}.java"
                elif extension == ".cs":
                    return f"{source_name}{test_suffix}.cs"
                elif extension == ".go":
                    return f"{source_name}{test_suffix}.go"
                elif extension == ".rs":
                    return f"{source_name}{test_suffix}.rs"

            # For other types, add a prefix
            type_prefix = output_type.upper()
            return f"{type_prefix}_{source_name}{extension}"

        return original_name

    def create_backup(self, file_path: Path) -> Optional[Path]:
        """Create a backup of a file if backup is enabled."""
        if not self.config.create_backups:
            return None

        backup_dir = self.output_dir / "backups"
        backup_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = backup_dir / backup_name

        shutil.copy2(file_path, backup_path)
        return backup_path

    def get_output_summary(self) -> Dict[str, Any]:
        """Get a summary of the organized outputs."""
        summary = {
            "output_directory": str(self.output_dir),
            "language": self.config.language.value,
            "organization_config": {
                "by_language": self.config.organize_by_language,
                "by_date": self.config.organize_by_date,
                "by_type": self.config.organize_by_type,
                "preserve_structure": self.config.preserve_structure,
                "create_backups": self.config.create_backups,
            },
            "directory_structure": self._get_directory_structure(),
            "file_counts": self._count_files_by_type(),
        }

        return summary

    def _get_directory_structure(self) -> Dict[str, Any]:
        """Get the current directory structure."""
        structure = {}

        def scan_directory(path: Path, level: int = 0):
            if level > 3:  # Limit depth for readability
                return

            items = []
            for item in path.iterdir():
                if item.is_dir():
                    items.append(
                        {
                            "name": item.name,
                            "type": "directory",
                            "contents": scan_directory(item, level + 1),
                        }
                    )
                else:
                    items.append(
                        {"name": item.name, "type": "file", "size": item.stat().st_size}
                    )

            return items

        structure["contents"] = scan_directory(self.output_dir)
        return structure

    def _count_files_by_type(self) -> Dict[str, int]:
        """Count files by output type."""
        counts = {}

        for output_type, info in self.OUTPUT_TYPES.items():
            type_dir = self.output_dir / info["subdir"]
            if type_dir.exists():
                count = len(list(type_dir.rglob("*")))
                counts[output_type] = count
            else:
                counts[output_type] = 0

        return counts

    def cleanup_old_outputs(self, max_age_days: int = 30):
        """Clean up old output directories."""
        import time

        current_time = time.time()
        max_age_seconds = max_age_days * 24 * 60 * 60

        for item in self.config.base_dir.iterdir():
            if item.is_dir() and item.name.startswith("agentops_output"):
                try:
                    # Check if directory is old enough
                    dir_age = current_time - item.stat().st_mtime
                    if dir_age > max_age_seconds:
                        shutil.rmtree(item)
                        print(f"Cleaned up old output directory: {item}")
                except Exception as e:
                    print(f"Warning: Failed to clean up {item}: {e}")

    def export_organization_report(self, output_path: Path):
        """Export a report of the organization structure."""
        summary = self.get_output_summary()

        report_content = f"""# AgentOps Output Organization Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Configuration
- Output Directory: {summary['output_directory']}
- Language: {summary['language']}
- Organization Settings: {summary['organization_config']}

## File Counts by Type
"""

        for output_type, count in summary["file_counts"].items():
            report_content += f"- {output_type}: {count} files\n"

        report_content += "\n## Directory Structure\n"
        report_content += self._format_directory_structure(
            summary["directory_structure"]["contents"]
        )

        # Write report
        with open(output_path, "w") as f:
            f.write(report_content)

    def _format_directory_structure(self, contents: List[Dict], indent: int = 0) -> str:
        """Format directory structure for display."""
        result = ""
        indent_str = "  " * indent

        for item in contents:
            if item["type"] == "directory":
                result += f"{indent_str}📁 {item['name']}/\n"
                if item["contents"]:
                    result += self._format_directory_structure(
                        item["contents"], indent + 1
                    )
            else:
                size = item["size"]
                size_str = f"({size} bytes)" if size < 1024 else f"({size/1024:.1f} KB)"
                result += f"{indent_str}📄 {item['name']} {size_str}\n"

        return result
