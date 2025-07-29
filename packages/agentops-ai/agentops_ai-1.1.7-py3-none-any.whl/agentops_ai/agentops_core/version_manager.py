"""
Version Manager for AgentOps Documentation.

This module provides versioned documentation snapshots that include all documents
(requirements, tests, clarifications, etc.) for each version, enabling complete
traceability and compliance.
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3


@dataclass
class VersionInfo:
    """Information about a documentation version."""
    version_id: str
    timestamp: str
    description: str
    trigger: str  # 'manual', 'auto', 'clarification', 'test_generation'
    requirements_count: int
    tests_count: int
    clarifications_count: int
    files_included: List[str]
    metadata: Dict[str, Any]


class VersionManager:
    """Manages versioned documentation snapshots."""
    
    def __init__(self, versions_dir: str = ".agentops/versions"):
        """Initialize the version manager."""
        self.versions_dir = versions_dir
        self._ensure_versions_directory()
        self._init_version_database()
    
    def _ensure_versions_directory(self):
        """Ensure the versions directory exists."""
        os.makedirs(self.versions_dir, exist_ok=True)
    
    def _init_version_database(self):
        """Initialize the version database."""
        db_path = os.path.join(self.versions_dir, "versions.db")
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS versions (
                    version_id TEXT PRIMARY KEY,
                    timestamp TEXT NOT NULL,
                    description TEXT NOT NULL,
                    trigger TEXT NOT NULL,
                    requirements_count INTEGER NOT NULL,
                    tests_count INTEGER NOT NULL,
                    clarifications_count INTEGER NOT NULL,
                    files_included TEXT NOT NULL,
                    metadata TEXT NOT NULL
                )
            """)
            conn.commit()
    
    def create_version_snapshot(self, description: str, trigger: str = "manual") -> Optional[str]:
        """Create a complete documentation snapshot for the current state.
        
        Args:
            description: Human-readable description of this version
            trigger: What triggered this version (manual, auto, clarification, etc.)
            
        Returns:
            Version ID of the created snapshot
        """
        try:
            # Generate version ID
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            version_id = f"v1.0.0_{timestamp}"
            
            # Create version directory
            version_dir = os.path.join(self.versions_dir, version_id)
            os.makedirs(version_dir, exist_ok=True)
            
            # Collect all current documentation
            files_included = []
            
            # 1. Export requirements (Gherkin and Markdown)
            from .workflow import AgentOpsWorkflow
            workflow = AgentOpsWorkflow()
            
            # Temporarily disable version manager to prevent infinite recursion
            original_version_manager = workflow.version_manager
            workflow.version_manager = None  # type: ignore
            
            try:
                # Export requirements directly without triggering version creation
                export_result = workflow.export_requirements_automatically()
                if export_result["success"]:
                    for file_path in export_result["exported_files"]:
                        if os.path.exists(file_path):
                            dest_path = os.path.join(version_dir, os.path.basename(file_path))
                            shutil.copy2(file_path, dest_path)
                            files_included.append(os.path.basename(file_path))
            finally:
                # Restore version manager
                workflow.version_manager = original_version_manager
            
            # 2. Copy test files
            tests_dir = os.path.join(version_dir, "tests")
            if os.path.exists(".agentops/tests"):
                if os.path.exists(tests_dir):
                    shutil.rmtree(tests_dir)
                shutil.copytree(".agentops/tests", tests_dir)
                files_included.append("tests/")
            
            # 3. Generate and copy traceability matrix
            traceability_result = workflow.generate_traceability_matrix("markdown")
            if traceability_result["success"]:
                traceability_file = traceability_result["file_path"]
                if os.path.exists(traceability_file):
                    dest_path = os.path.join(version_dir, "traceability_matrix.md")
                    shutil.copy2(traceability_file, dest_path)
                    files_included.append("traceability_matrix.md")
            
            # 4. Export audit history
            from .requirements_clarification import RequirementsClarificationEngine
            engine = RequirementsClarificationEngine()
            audits = engine.get_audit_history()
            
            if audits:
                audit_file = os.path.join(version_dir, "audit_history.md")
                with open(audit_file, 'w') as f:
                    f.write("# Requirements Clarification Audit History\n\n")
                    for audit in audits:
                        f.write(f"## {audit.audit_id}\n")
                        f.write(f"- **Requirement ID:** {audit.requirement_id}\n")
                        f.write(f"- **Method:** {audit.update_method}\n")
                        f.write(f"- **Timestamp:** {audit.timestamp}\n")
                        f.write(f"- **Reason:** {audit.clarification_reason}\n")
                        f.write(f"- **Original:** {audit.original_requirement}\n")
                        f.write(f"- **Clarified:** {audit.clarified_requirement}\n\n")
                files_included.append("audit_history.md")
            
            # 5. Create version info
            version_info = VersionInfo(
                version_id=version_id,
                timestamp=datetime.now().isoformat(),
                description=description,
                trigger=trigger,
                requirements_count=len(workflow.requirement_store.get_all_requirements()),
                tests_count=len([f for f in os.listdir(".agentops/tests") if f.endswith('.py')]) if os.path.exists(".agentops/tests") else 0,
                clarifications_count=len(audits),
                files_included=files_included,
                metadata={
                    "agentops_version": "1.0.0",
                    "python_version": "3.13.3",
                    "total_test_functions": self._count_test_functions(),
                    "project_root": os.getcwd()
                }
            )
            
            # Save version info
            version_info_file = os.path.join(version_dir, "version_info.json")
            with open(version_info_file, 'w') as f:
                json.dump(asdict(version_info), f, indent=2)
            
            # Update database
            self._save_version_to_db(version_info)
            
            # Update latest symlink
            latest_link = os.path.join(self.versions_dir, "latest")
            if os.path.exists(latest_link):
                os.remove(latest_link)
            os.symlink(version_id, latest_link)
            
            return version_id
            
        except Exception as e:
            print(f"Error creating version snapshot: {e}")
            return None
    
    def _count_test_functions(self) -> int:
        """Count total test functions across all test files."""
        count = 0
        if os.path.exists(".agentops/tests"):
            for root, dirs, files in os.walk(".agentops/tests"):
                for file in files:
                    if file.endswith('.py'):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r') as f:
                                content = f.read()
                                count += len([line for line in content.split('\n') 
                                            if line.strip().startswith('def test_')])
                        except Exception:
                            pass
        return count
    
    def _save_version_to_db(self, version_info: VersionInfo):
        """Save version information to database."""
        db_path = os.path.join(self.versions_dir, "versions.db")
        with sqlite3.connect(db_path) as conn:
            conn.execute("""
                INSERT OR REPLACE INTO versions 
                (version_id, timestamp, description, trigger, requirements_count, 
                 tests_count, clarifications_count, files_included, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                version_info.version_id,
                version_info.timestamp,
                version_info.description,
                version_info.trigger,
                version_info.requirements_count,
                version_info.tests_count,
                version_info.clarifications_count,
                json.dumps(version_info.files_included),
                json.dumps(version_info.metadata)
            ))
            conn.commit()
    
    def list_versions(self) -> List[VersionInfo]:
        """List all available versions."""
        db_path = os.path.join(self.versions_dir, "versions.db")
        with sqlite3.connect(db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT * FROM versions ORDER BY timestamp DESC
            """)
            
            versions = []
            for row in cursor.fetchall():
                version_info = VersionInfo(
                    version_id=row['version_id'],
                    timestamp=row['timestamp'],
                    description=row['description'],
                    trigger=row['trigger'],
                    requirements_count=row['requirements_count'],
                    tests_count=row['tests_count'],
                    clarifications_count=row['clarifications_count'],
                    files_included=json.loads(row['files_included']),
                    metadata=json.loads(row['metadata'])
                )
                versions.append(version_info)
            
            return versions
    
    def get_version(self, version_id: str) -> Optional[VersionInfo]:
        """Get information about a specific version."""
        versions = self.list_versions()
        for version in versions:
            if version.version_id == version_id:
                return version
        return None
    
    def restore_version(self, version_id: str) -> bool:
        """Restore a specific version to the current state."""
        try:
            version_dir = os.path.join(self.versions_dir, version_id)
            if not os.path.exists(version_dir):
                return False
            
            # Restore requirements files
            for file_name in ["requirements.gherkin", "requirements.md"]:
                src_path = os.path.join(version_dir, file_name)
                if os.path.exists(src_path):
                    dest_path = os.path.join(".agentops", file_name)
                    shutil.copy2(src_path, dest_path)
            
            # Restore test files
            src_tests_dir = os.path.join(version_dir, "tests")
            if os.path.exists(src_tests_dir):
                dest_tests_dir = ".agentops/tests"
                if os.path.exists(dest_tests_dir):
                    shutil.rmtree(dest_tests_dir)
                shutil.copytree(src_tests_dir, dest_tests_dir)
            
            # Restore traceability matrix
            src_traceability = os.path.join(version_dir, "traceability_matrix.md")
            if os.path.exists(src_traceability):
                dest_traceability = ".agentops/traceability_matrix.md"
                shutil.copy2(src_traceability, dest_traceability)
            
            return True
            
        except Exception as e:
            print(f"Error restoring version {version_id}: {e}")
            return False
    
    def compare_versions(self, version1_id: str, version2_id: str) -> Dict[str, Any]:
        """Compare two versions and show differences."""
        version1 = self.get_version(version1_id)
        version2 = self.get_version(version2_id)
        
        if not version1 or not version2:
            return {"error": "One or both versions not found"}
        
        return {
            "version1": asdict(version1),
            "version2": asdict(version2),
            "differences": {
                "requirements_count": version2.requirements_count - version1.requirements_count,
                "tests_count": version2.tests_count - version1.tests_count,
                "clarifications_count": version2.clarifications_count - version1.clarifications_count,
                "new_files": list(set(version2.files_included) - set(version1.files_included)),
                "removed_files": list(set(version1.files_included) - set(version2.files_included))
            }
        }
    
    def auto_create_version(self, trigger: str, description: Optional[str] = None) -> Optional[str]:
        """Automatically create a version snapshot based on triggers."""
        if trigger == "clarification":
            # Create version when requirements are clarified
            return self.create_version_snapshot(
                description or "Requirements clarification applied",
                trigger="clarification"
            )
        elif trigger == "test_generation":
            # Create version when new tests are generated
            return self.create_version_snapshot(
                description or "New tests generated",
                trigger="test_generation"
            )
        elif trigger == "requirements_update":
            # Create version when requirements are updated
            return self.create_version_snapshot(
                description or "Requirements updated",
                trigger="requirements_update"
            )
        
        return None 