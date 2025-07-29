"""
Requirements Clarification System for AgentOps.

This module provides generic functionality to:
1. Analyze test failures and identify requirements gaps
2. Suggest clarifications to make requirements more specific
3. Provide auto/manual update options with audit trails
4. Track all requirement changes for traceability
"""

import os
import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import sqlite3


@dataclass
class TestFailure:
    """Represents a test failure with context."""
    test_file: str
    test_function: str
    requirement_id: Optional[int]
    error_message: str
    expected_behavior: str
    actual_behavior: str
    failure_type: str  # 'assertion_error', 'exception_mismatch', 'logic_error', etc.
    timestamp: str


@dataclass
class RequirementsGap:
    """Represents a gap in requirements that caused a test failure."""
    requirement_id: Optional[int]
    original_requirement: str
    identified_gap: str
    suggested_clarification: str
    confidence_score: float
    failure_context: List[TestFailure]
    timestamp: str


@dataclass
class ClarificationAudit:
    """Audit trail for requirement clarifications."""
    audit_id: str
    requirement_id: Optional[int]
    original_requirement: str
    clarified_requirement: str
    clarification_reason: str
    update_method: str  # 'auto', 'manual', 'suggested'
    user_id: Optional[str]
    timestamp: str
    test_failures_triggered: List[str]


class RequirementsClarificationEngine:
    """Generic engine for analyzing test failures and suggesting requirement clarifications."""
    
    def __init__(self, db_path: str = ".agentops/requirements_clarification.db"):
        """Initialize the clarification engine."""
        self.db_path = db_path
        self._ensure_db_directory()
        self._init_database()
    
    def _ensure_db_directory(self):
        """Ensure the database directory exists."""
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
    
    def _init_database(self):
        """Initialize the SQLite database for audit trails."""
        with sqlite3.connect(self.db_path) as conn:
            # Test failures table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS test_failures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    test_file TEXT NOT NULL,
                    test_function TEXT NOT NULL,
                    requirement_id INTEGER,
                    error_message TEXT NOT NULL,
                    expected_behavior TEXT,
                    actual_behavior TEXT,
                    failure_type TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            # Requirements gaps table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS requirements_gaps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    requirement_id INTEGER,
                    original_requirement TEXT NOT NULL,
                    identified_gap TEXT NOT NULL,
                    suggested_clarification TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    failure_context TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            
            # Clarification audit table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS clarification_audit (
                    audit_id TEXT PRIMARY KEY,
                    requirement_id INTEGER,
                    original_requirement TEXT NOT NULL,
                    clarified_requirement TEXT NOT NULL,
                    clarification_reason TEXT NOT NULL,
                    update_method TEXT NOT NULL,
                    user_id TEXT,
                    timestamp TEXT NOT NULL,
                    test_failures_triggered TEXT NOT NULL
                )
            """)
            
            conn.commit()
    
    def analyze_test_failures(self, pytest_output: str) -> List[TestFailure]:
        """Analyze pytest output to extract test failures and their context.
        
        Args:
            pytest_output: Raw pytest output string
            
        Returns:
            List of TestFailure objects
        """
        failures = []
        
        # Parse pytest output to extract failure information
        lines = pytest_output.split('\n')
        current_failure = None
        
        for line in lines:
            # Detect test failure start
            if 'FAILED' in line and '::' in line:
                parts = line.split('::')
                if len(parts) >= 2:
                    test_file = parts[0].strip()
                    test_function = parts[1].strip()
                    
                    # Extract requirement ID from test file if available
                    requirement_id = self._extract_requirement_id_from_test(test_file, test_function)
                    
                    current_failure = TestFailure(
                        test_file=test_file,
                        test_function=test_function,
                        requirement_id=requirement_id,
                        error_message="",
                        expected_behavior="",
                        actual_behavior="",
                        failure_type="unknown",
                        timestamp=datetime.now().isoformat()
                    )
            
            # Extract error details
            elif current_failure and line.strip().startswith('E'):
                current_failure.error_message += line.strip()[1:] + "\n"
            
            # Detect failure type
            elif current_failure and 'AssertionError' in line:
                current_failure.failure_type = 'assertion_error'
            elif current_failure and 'ValueError' in line:
                current_failure.failure_type = 'exception_mismatch'
            elif current_failure and 'TypeError' in line:
                current_failure.failure_type = 'type_error'
            
            # Extract expected vs actual behavior
            elif current_failure and 'Expected' in line and 'Actual' in line:
                # Parse expected/actual from error message
                expected_match = re.search(r'Expected[^:]*:\s*([^,]+)', line)
                actual_match = re.search(r'Actual[^:]*:\s*([^,]+)', line)
                
                if expected_match:
                    current_failure.expected_behavior = expected_match.group(1).strip()
                if actual_match:
                    current_failure.actual_behavior = actual_match.group(1).strip()
        
        # Add the last failure if exists
        if current_failure:
            failures.append(current_failure)
        
        return failures
    
    def _extract_requirement_id_from_test(self, test_file: str, test_function: str) -> Optional[int]:
        """Extract requirement ID from test file comments."""
        try:
            with open(test_file, 'r') as f:
                content = f.read()
            
            # Look for AGENTOPS-REQ comment above the test function
            test_function_pattern = rf'def {test_function}'
            lines = content.split('\n')
            
            for i, line in enumerate(lines):
                if test_function_pattern in line:
                    # Check previous line for requirement ID
                    if i > 0 and 'AGENTOPS-REQ:' in lines[i-1]:
                        req_match = re.search(r'AGENTOPS-REQ:\s*(\w+)', lines[i-1])
                        if req_match:
                            return req_match.group(1)
            
            return None
        except Exception:
            return None
    
    def identify_requirements_gaps(self, failures: List[TestFailure]) -> List[RequirementsGap]:
        """Identify gaps in requirements based on test failures.
        
        Args:
            failures: List of test failures
            
        Returns:
            List of requirements gaps with suggested clarifications
        """
        gaps = []
        
        # Group failures by requirement ID
        failures_by_requirement = {}
        for failure in failures:
            req_id = failure.requirement_id
            if req_id not in failures_by_requirement:
                failures_by_requirement[req_id] = []
            failures_by_requirement[req_id].append(failure)
        
        # Analyze each group for patterns
        for req_id, req_failures in failures_by_requirement.items():
            gap = self._analyze_failure_patterns(req_id, req_failures)
            if gap:
                gaps.append(gap)
        
        return gaps
    
    def _analyze_failure_patterns(self, requirement_id: Optional[int], 
                                failures: List[TestFailure]) -> Optional[RequirementsGap]:
        """Analyze failure patterns to identify requirements gaps."""
        
        # Get original requirement text
        original_requirement = self._get_requirement_text(requirement_id)
        if not original_requirement:
            return None
        
        # Analyze failure types
        failure_types = [f.failure_type for f in failures]
        error_messages = [f.error_message for f in failures]
        
        # Pattern matching for common gaps
        gap_analysis = self._detect_gap_patterns(original_requirement, failure_types, error_messages)
        
        if gap_analysis:
            return RequirementsGap(
                requirement_id=requirement_id,
                original_requirement=original_requirement,
                identified_gap=gap_analysis['gap'],
                suggested_clarification=gap_analysis['clarification'],
                confidence_score=gap_analysis['confidence'],
                failure_context=failures,
                timestamp=datetime.now().isoformat()
            )
        
        return None
    
    def _detect_gap_patterns(self, requirement: str, failure_types: List[str], 
                           error_messages: List[str]) -> Optional[Dict[str, Any]]:
        """Detect common patterns in requirements gaps."""
        
        # Pattern 1: Exception message mismatch
        if 'exception_mismatch' in failure_types:
            return self._analyze_exception_mismatch(requirement, error_messages)
        
        # Pattern 2: Missing edge cases
        elif 'assertion_error' in failure_types:
            return self._analyze_missing_edge_cases(requirement, error_messages)
        
        # Pattern 3: Type handling issues
        elif 'type_error' in failure_types:
            return self._analyze_type_handling(requirement, error_messages)
        
        # Pattern 4: Logic errors
        else:
            return self._analyze_logic_errors(requirement, error_messages)
    
    def _analyze_exception_mismatch(self, requirement: str, error_messages: List[str]) -> Dict[str, Any]:
        """Analyze exception message mismatches."""
        for error in error_messages:
            if 'Regex pattern did not match' in error:
                return {
                    'gap': 'Exception message specification is ambiguous',
                    'clarification': f'{requirement}. The function should raise specific exceptions with exact error messages as specified in the test.',
                    'confidence': 0.9
                }
        return None
    
    def _analyze_missing_edge_cases(self, requirement: str, error_messages: List[str]) -> Dict[str, Any]:
        """Analyze missing edge cases in requirements."""
        return {
            'gap': 'Edge cases not explicitly covered in requirement',
            'clarification': f'{requirement}. The requirement should explicitly specify behavior for edge cases and boundary conditions.',
            'confidence': 0.8
        }
    
    def _analyze_type_handling(self, requirement: str, error_messages: List[str]) -> Dict[str, Any]:
        """Analyze type handling issues."""
        return {
            'gap': 'Input type handling not specified',
            'clarification': f'{requirement}. The requirement should specify how the function handles different input types (strings, numbers, None, etc.).',
            'confidence': 0.85
        }
    
    def _analyze_logic_errors(self, requirement: str, error_messages: List[str]) -> Dict[str, Any]:
        """Analyze logic errors in requirements."""
        return {
            'gap': 'Logic or algorithm specification is unclear',
            'clarification': f'{requirement}. The requirement should provide more specific details about the expected algorithm or logic.',
            'confidence': 0.7
        }
    
    def _get_requirement_text(self, requirement_id: Optional[int]) -> Optional[str]:
        """Get requirement text from the requirement store."""
        if not requirement_id:
            return None
        
        try:
            from .requirement_store import RequirementStore
            store = RequirementStore()
            requirement = store.get_requirement(requirement_id)
            return requirement.requirement_text if requirement else None
        except Exception:
            return None
    
    def suggest_clarifications(self, gaps: List[RequirementsGap]) -> List[Dict[str, Any]]:
        """Generate specific clarification suggestions for requirements gaps."""
        suggestions = []
        
        for gap in gaps:
            suggestion = {
                'requirement_id': gap.requirement_id,
                'original_requirement': gap.original_requirement,
                'suggested_clarification': gap.suggested_clarification,
                'confidence': gap.confidence_score,
                'failure_count': len(gap.failure_context),
                'failure_summary': [f.failure_type for f in gap.failure_context]
            }
            suggestions.append(suggestion)
        
        return suggestions
    
    def update_requirement(self, requirement_id: Optional[int], 
                         clarified_requirement: str, 
                         clarification_reason: str,
                         update_method: str = 'manual',
                         user_id: Optional[str] = None) -> bool:
        """Update a requirement with clarification and record audit trail."""
        try:
            # Update requirement in store
            if requirement_id:
                from .requirement_store import RequirementStore
                store = RequirementStore()
                store.update_requirement_text(requirement_id, clarified_requirement)
            
            # Record audit trail
            audit = ClarificationAudit(
                audit_id=f"clarification_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                requirement_id=requirement_id,
                original_requirement=self._get_requirement_text(requirement_id) or "Unknown",
                clarified_requirement=clarified_requirement,
                clarification_reason=clarification_reason,
                update_method=update_method,
                user_id=user_id,
                timestamp=datetime.now().isoformat(),
                test_failures_triggered=[]  # Will be populated from context
            )
            
            self._save_audit_trail(audit)
            return True
            
        except Exception as e:
            print(f"Error updating requirement: {e}")
            return False
    
    def _save_audit_trail(self, audit: ClarificationAudit):
        """Save audit trail to database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO clarification_audit 
                (audit_id, requirement_id, original_requirement, clarified_requirement, 
                 clarification_reason, update_method, user_id, timestamp, test_failures_triggered)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                audit.audit_id,
                audit.requirement_id,
                audit.original_requirement,
                audit.clarified_requirement,
                audit.clarification_reason,
                audit.update_method,
                audit.user_id,
                audit.timestamp,
                json.dumps(audit.test_failures_triggered)
            ))
            conn.commit()
    
    def get_audit_history(self, requirement_id: Optional[int] = None) -> List[ClarificationAudit]:
        """Get audit history for requirements clarifications."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            if requirement_id:
                cursor = conn.execute("""
                    SELECT * FROM clarification_audit 
                    WHERE requirement_id = ? 
                    ORDER BY timestamp DESC
                """, (requirement_id,))
            else:
                cursor = conn.execute("""
                    SELECT * FROM clarification_audit 
                    ORDER BY timestamp DESC
                """)
            
            audits = []
            for row in cursor.fetchall():
                audit = ClarificationAudit(
                    audit_id=row['audit_id'],
                    requirement_id=row['requirement_id'],
                    original_requirement=row['original_requirement'],
                    clarified_requirement=row['clarified_requirement'],
                    clarification_reason=row['clarification_reason'],
                    update_method=row['update_method'],
                    user_id=row['user_id'],
                    timestamp=row['timestamp'],
                    test_failures_triggered=json.loads(row['test_failures_triggered'])
                )
                audits.append(audit)
            
            return audits 