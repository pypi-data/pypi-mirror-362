"""Database operations for AgentOps enhanced modules.

Handles database operations for Problem Discovery and Human-in-the-Loop Requirements.
"""

import sqlite3
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from .config import get_config


@dataclass
class ProblemSession:
    """Data class for problem discovery sessions."""

    session_id: str
    user_id: str = "default"
    created_at: datetime = None
    updated_at: datetime = None
    status: str = "active"  # active, completed, abandoned
    problem_statement: Optional[str] = None
    refined_problem: Optional[str] = None
    selected_solution: Optional[str] = None
    current_stage: str = (
        "problem_discovery"  # problem_discovery, solution_ideation, solution_selection
    )
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ConversationMessage:
    """Data class for conversation messages."""

    id: str
    session_id: str
    message_type: str  # user, assistant, system
    content: str
    timestamp: datetime = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class GeneratedSolution:
    """Data class for generated solutions."""

    id: str
    session_id: str
    solution_id: str
    title: str
    description: str
    technology_stack: List[str]
    complexity: str  # simple, medium, complex
    pros: List[str]
    cons: List[str]
    estimated_effort: str
    created_at: datetime = None
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.metadata is None:
            self.metadata = {}


@dataclass
class RequirementRecord:
    """Data class for enhanced requirements."""

    id: str
    project_id: str
    file_path: str
    requirement_text: str
    category: str
    priority: str
    status: str
    confidence_score: float
    business_value: str
    implementation_complexity: str
    created_by: str
    created_at: datetime = None
    updated_at: datetime = None
    version: int = 1
    acceptance_criteria: List[str] = None
    business_context: Dict[str, Any] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()
        if self.acceptance_criteria is None:
            self.acceptance_criteria = []
        if self.business_context is None:
            self.business_context = {}


@dataclass
class BusinessContext:
    """Data class for business context."""

    id: str
    project_id: str
    domain: str
    industry: str
    compliance_requirements: List[str]
    user_types: List[str]
    business_objectives: str
    constraints: str
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


@dataclass
class HumanFeedback:
    """Data class for human feedback."""

    id: str
    requirement_id: str
    feedback_type: str
    original_text: str
    corrected_text: str
    feedback_notes: str
    user_id: str
    timestamp: datetime = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class AgentOpsDatabase:
    """Enhanced database manager for AgentOps."""

    def __init__(self, db_path: Optional[str] = None):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        if db_path is None:
            config = get_config()
            db_path = Path(config.project.project_root) / ".agentops/agentops.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()

    def _init_database(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA foreign_keys = ON")

            # Problem discovery sessions
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS problem_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'active',
                    problem_statement TEXT,
                    refined_problem TEXT,
                    selected_solution TEXT,
                    current_stage TEXT DEFAULT 'problem_discovery',
                    metadata TEXT
                )
            """
            )

            # Conversation history
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS conversation_history (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    message_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES problem_sessions(session_id)
                )
            """
            )

            # Generated solutions
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS generated_solutions (
                    id TEXT PRIMARY KEY,
                    session_id TEXT NOT NULL,
                    solution_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    technology_stack TEXT,
                    complexity TEXT,
                    pros TEXT,
                    cons TEXT,
                    estimated_effort TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    metadata TEXT,
                    FOREIGN KEY (session_id) REFERENCES problem_sessions(session_id)
                )
            """
            )

            # Enhanced requirements
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS requirements (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    requirement_text TEXT NOT NULL,
                    category TEXT NOT NULL,
                    priority TEXT NOT NULL,
                    status TEXT NOT NULL,
                    confidence_score REAL,
                    business_value TEXT,
                    implementation_complexity TEXT,
                    created_by TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    version INTEGER DEFAULT 1,
                    acceptance_criteria TEXT,
                    business_context TEXT
                )
            """
            )

            # Business context
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS business_context (
                    id TEXT PRIMARY KEY,
                    project_id TEXT NOT NULL,
                    domain TEXT,
                    industry TEXT,
                    compliance_requirements TEXT,
                    user_types TEXT,
                    business_objectives TEXT,
                    constraints TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            # Human feedback
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS human_feedback (
                    id TEXT PRIMARY KEY,
                    requirement_id TEXT NOT NULL,
                    feedback_type TEXT,
                    original_text TEXT,
                    corrected_text TEXT,
                    feedback_notes TEXT,
                    user_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (requirement_id) REFERENCES requirements(id)
                )
            """
            )

            # Code analysis cache
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS code_analysis (
                    id TEXT PRIMARY KEY,
                    file_path TEXT NOT NULL,
                    project_id TEXT NOT NULL,
                    patterns_detected TEXT,
                    business_logic_identified TEXT,
                    complexity_score INTEGER,
                    risk_factors TEXT,
                    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()

    # Problem Discovery Methods
    def create_problem_session(self, user_id: str = "default") -> str:
        """Create a new problem discovery session."""
        session_id = str(uuid.uuid4())
        session = ProblemSession(session_id=session_id, user_id=user_id)

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO problem_sessions 
                (session_id, user_id, created_at, updated_at, status, current_stage, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    session.session_id,
                    session.user_id,
                    session.created_at,
                    session.updated_at,
                    session.status,
                    session.current_stage,
                    json.dumps(session.metadata),
                ),
            )
            conn.commit()

        return session_id

    def get_problem_session(self, session_id: str) -> Optional[ProblemSession]:
        """Get problem session by ID."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT session_id, user_id, created_at, updated_at, status,
                       problem_statement, refined_problem, selected_solution,
                       current_stage, metadata
                FROM problem_sessions WHERE session_id = ?
            """,
                (session_id,),
            )

            row = cursor.fetchone()
            if row:
                return ProblemSession(
                    session_id=row[0],
                    user_id=row[1],
                    created_at=datetime.fromisoformat(row[2]) if row[2] else None,
                    updated_at=datetime.fromisoformat(row[3]) if row[3] else None,
                    status=row[4],
                    problem_statement=row[5],
                    refined_problem=row[6],
                    selected_solution=row[7],
                    current_stage=row[8],
                    metadata=json.loads(row[9]) if row[9] else {},
                )
        return None

    def update_problem_session(self, session: ProblemSession):
        """Update problem session."""
        session.updated_at = datetime.now()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                UPDATE problem_sessions 
                SET updated_at = ?, status = ?, problem_statement = ?,
                    refined_problem = ?, selected_solution = ?, current_stage = ?,
                    metadata = ?
                WHERE session_id = ?
            """,
                (
                    session.updated_at,
                    session.status,
                    session.problem_statement,
                    session.refined_problem,
                    session.selected_solution,
                    session.current_stage,
                    json.dumps(session.metadata),
                    session.session_id,
                ),
            )
            conn.commit()

    def add_conversation_message(self, message: ConversationMessage):
        """Add conversation message."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO conversation_history 
                (id, session_id, message_type, content, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    message.id,
                    message.session_id,
                    message.message_type,
                    message.content,
                    message.timestamp,
                    json.dumps(message.metadata),
                ),
            )
            conn.commit()

    def get_conversation_history(self, session_id: str) -> List[ConversationMessage]:
        """Get conversation history for session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT id, session_id, message_type, content, timestamp, metadata
                FROM conversation_history 
                WHERE session_id = ? 
                ORDER BY timestamp
            """,
                (session_id,),
            )

            messages = []
            for row in cursor.fetchall():
                messages.append(
                    ConversationMessage(
                        id=row[0],
                        session_id=row[1],
                        message_type=row[2],
                        content=row[3],
                        timestamp=datetime.fromisoformat(row[4]) if row[4] else None,
                        metadata=json.loads(row[5]) if row[5] else {},
                    )
                )

            return messages

    def add_generated_solution(self, solution: GeneratedSolution):
        """Add generated solution."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO generated_solutions 
                (id, session_id, solution_id, title, description, technology_stack,
                 complexity, pros, cons, estimated_effort, created_at, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    solution.id,
                    solution.session_id,
                    solution.solution_id,
                    solution.title,
                    solution.description,
                    json.dumps(solution.technology_stack),
                    solution.complexity,
                    json.dumps(solution.pros),
                    json.dumps(solution.cons),
                    solution.estimated_effort,
                    solution.created_at,
                    json.dumps(solution.metadata),
                ),
            )
            conn.commit()

    def get_generated_solutions(self, session_id: str) -> List[GeneratedSolution]:
        """Get generated solutions for session."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT id, session_id, solution_id, title, description, technology_stack,
                       complexity, pros, cons, estimated_effort, created_at, metadata
                FROM generated_solutions 
                WHERE session_id = ?
                ORDER BY created_at
            """,
                (session_id,),
            )

            solutions = []
            for row in cursor.fetchall():
                solutions.append(
                    GeneratedSolution(
                        id=row[0],
                        session_id=row[1],
                        solution_id=row[2],
                        title=row[3],
                        description=row[4],
                        technology_stack=json.loads(row[5]) if row[5] else [],
                        complexity=row[6],
                        pros=json.loads(row[7]) if row[7] else [],
                        cons=json.loads(row[8]) if row[8] else [],
                        estimated_effort=row[9],
                        created_at=datetime.fromisoformat(row[10]) if row[10] else None,
                        metadata=json.loads(row[11]) if row[11] else {},
                    )
                )

            return solutions

    # Requirements Methods
    def add_requirement(self, requirement: RequirementRecord):
        """Add a new requirement."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO requirements 
                (id, project_id, file_path, requirement_text, category, priority, status,
                 confidence_score, business_value, implementation_complexity, created_by,
                 created_at, updated_at, version, acceptance_criteria, business_context)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    requirement.id,
                    requirement.project_id,
                    requirement.file_path,
                    requirement.requirement_text,
                    requirement.category,
                    requirement.priority,
                    requirement.status,
                    requirement.confidence_score,
                    requirement.business_value,
                    requirement.implementation_complexity,
                    requirement.created_by,
                    requirement.created_at,
                    requirement.updated_at,
                    requirement.version,
                    json.dumps(requirement.acceptance_criteria),
                    json.dumps(requirement.business_context),
                ),
            )
            conn.commit()

    def get_requirements_for_file(self, file_path: str) -> List[RequirementRecord]:
        """Get all requirements for a specific file."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT id, project_id, file_path, requirement_text, category, priority, status,
                       confidence_score, business_value, implementation_complexity, created_by,
                       created_at, updated_at, version, acceptance_criteria, business_context
                FROM requirements 
                WHERE file_path = ?
                ORDER BY created_at DESC
            """,
                (file_path,),
            )

            requirements = []
            for row in cursor.fetchall():
                requirements.append(
                    RequirementRecord(
                        id=row[0],
                        project_id=row[1],
                        file_path=row[2],
                        requirement_text=row[3],
                        category=row[4],
                        priority=row[5],
                        status=row[6],
                        confidence_score=row[7],
                        business_value=row[8],
                        implementation_complexity=row[9],
                        created_by=row[10],
                        created_at=datetime.fromisoformat(row[11]) if row[11] else None,
                        updated_at=datetime.fromisoformat(row[12]) if row[12] else None,
                        version=row[13],
                        acceptance_criteria=json.loads(row[14]) if row[14] else [],
                        business_context=json.loads(row[15]) if row[15] else {},
                    )
                )

            return requirements

    def add_human_feedback(self, feedback: HumanFeedback):
        """Add human feedback for a requirement."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO human_feedback 
                (id, requirement_id, feedback_type, original_text, corrected_text,
                 feedback_notes, user_id, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    feedback.id,
                    feedback.requirement_id,
                    feedback.feedback_type,
                    feedback.original_text,
                    feedback.corrected_text,
                    feedback.feedback_notes,
                    feedback.user_id,
                    feedback.timestamp,
                ),
            )
            conn.commit()

    def get_business_context(self, project_id: str) -> Optional[BusinessContext]:
        """Get business context for project."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT id, project_id, domain, industry, compliance_requirements,
                       user_types, business_objectives, constraints, created_at
                FROM business_context 
                WHERE project_id = ?
                ORDER BY created_at DESC
                LIMIT 1
            """,
                (project_id,),
            )

            row = cursor.fetchone()
            if row:
                return BusinessContext(
                    id=row[0],
                    project_id=row[1],
                    domain=row[2],
                    industry=row[3],
                    compliance_requirements=json.loads(row[4]) if row[4] else [],
                    user_types=json.loads(row[5]) if row[5] else [],
                    business_objectives=row[6],
                    constraints=row[7],
                    created_at=datetime.fromisoformat(row[8]) if row[8] else None,
                )
        return None

    def save_business_context(self, context: BusinessContext):
        """Save business context."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO business_context 
                (id, project_id, domain, industry, compliance_requirements,
                 user_types, business_objectives, constraints, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    context.id,
                    context.project_id,
                    context.domain,
                    context.industry,
                    json.dumps(context.compliance_requirements),
                    json.dumps(context.user_types),
                    context.business_objectives,
                    context.constraints,
                    context.created_at,
                ),
            )
            conn.commit()

    def cleanup_old_sessions(self, days: int = 7):
        """Clean up old problem sessions."""
        cutoff_date = datetime.now() - timedelta(days=days)

        with sqlite3.connect(self.db_path) as conn:
            # Delete old sessions and related data
            cursor = conn.execute(
                """
                SELECT session_id FROM problem_sessions 
                WHERE updated_at < ? AND status = 'abandoned'
            """,
                (cutoff_date,),
            )

            old_sessions = [row[0] for row in cursor.fetchall()]

            for session_id in old_sessions:
                conn.execute(
                    "DELETE FROM conversation_history WHERE session_id = ?",
                    (session_id,),
                )
                conn.execute(
                    "DELETE FROM generated_solutions WHERE session_id = ?",
                    (session_id,),
                )
                conn.execute(
                    "DELETE FROM problem_sessions WHERE session_id = ?", (session_id,)
                )

            conn.commit()

        return len(old_sessions)
