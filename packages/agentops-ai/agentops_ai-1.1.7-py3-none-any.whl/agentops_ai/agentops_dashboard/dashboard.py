"""
AgentOps Web Dashboard System

This module implements a comprehensive web dashboard with:
- Real-time project monitoring
- Test generation progress tracking
- Requirements management interface
- Analytics and reporting
- User management and permissions
- Modular feature system with switch on/off capabilities
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Union
from pathlib import Path
import json
import asyncio
from datetime import datetime, timedelta
import logging
from fastapi import FastAPI, HTTPException, Depends, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn

from ..agentops_core.features import get_feature_manager, is_feature_enabled
from ..agentops_core.pricing import PricingTier, pricing_manager


class DashboardFeature(Enum):
    """Dashboard features that can be enabled/disabled."""
    
    # Core Dashboard Features
    PROJECT_OVERVIEW = "project_overview"
    REAL_TIME_MONITORING = "real_time_monitoring"
    PROGRESS_TRACKING = "progress_tracking"
    
    # Analysis Features
    CODE_ANALYSIS_VIEW = "code_analysis_view"
    REQUIREMENTS_MANAGEMENT = "requirements_management"
    TEST_GENERATION_STATUS = "test_generation_status"
    
    # Advanced Features
    ANALYTICS_DASHBOARD = "analytics_dashboard"
    TEAM_COLLABORATION = "team_collaboration"
    AUDIT_TRAILS = "audit_trails"
    
    # Integration Features
    CI_CD_INTEGRATION = "ci_cd_integration"
    API_MANAGEMENT = "api_management"
    EXPORT_CAPABILITIES = "export_capabilities"


@dataclass
class DashboardConfig:
    """Configuration for the web dashboard."""
    
    # Server settings
    host: str = "localhost"
    port: int = 3000
    debug: bool = False
    
    # Feature settings
    enabled_features: Set[DashboardFeature] = field(default_factory=set)
    auth_enabled: bool = True
    analytics_enabled: bool = False
    
    # UI settings
    theme: str = "light"
    language: str = "en"
    auto_refresh: bool = True
    refresh_interval: int = 30  # seconds
    
    # Security settings
    cors_origins: List[str] = field(default_factory=lambda: ["http://localhost:3000"])
    session_timeout: int = 3600  # seconds
    
    # Data settings
    data_retention_days: int = 90
    max_file_size_mb: int = 10


class DashboardData:
    """Data structures for dashboard information."""
    
    def __init__(self):
        """Initialize dashboard data."""
        self.projects: Dict[str, Dict[str, Any]] = {}
        self.users: Dict[str, Dict[str, Any]] = {}
        self.analytics: Dict[str, Any] = {}
        self.audit_logs: List[Dict[str, Any]] = []
        self.real_time_events: List[Dict[str, Any]] = []
    
    def add_project(self, project_id: str, project_data: Dict[str, Any]):
        """Add or update project data."""
        self.projects[project_id] = {
            **project_data,
            "last_updated": datetime.now().isoformat()
        }
    
    def add_user(self, user_id: str, user_data: Dict[str, Any]):
        """Add or update user data."""
        self.users[user_id] = {
            **user_data,
            "last_updated": datetime.now().isoformat()
        }
    
    def add_audit_log(self, event: Dict[str, Any]):
        """Add audit log entry."""
        self.audit_logs.append({
            **event,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent logs
        cutoff_date = datetime.now() - timedelta(days=90)
        self.audit_logs = [
            log for log in self.audit_logs
            if datetime.fromisoformat(log["timestamp"]) > cutoff_date
        ]
    
    def add_real_time_event(self, event: Dict[str, Any]):
        """Add real-time event."""
        self.real_time_events.append({
            **event,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent events
        cutoff_date = datetime.now() - timedelta(hours=24)
        self.real_time_events = [
            event for event in self.real_time_events
            if datetime.fromisoformat(event["timestamp"]) > cutoff_date
        ]


class DashboardManager:
    """Manages the web dashboard system."""
    
    def __init__(self, config: DashboardConfig):
        """Initialize the dashboard manager.
        
        Args:
            config: Dashboard configuration
        """
        self.config = config
        self.data = DashboardData()
        self.feature_manager = get_feature_manager()
        self.app = FastAPI(title="AgentOps Dashboard", version="1.0.0")
        
        # Initialize dashboard features
        self._initialize_features()
        self._setup_routes()
        self._setup_middleware()
    
    def _initialize_features(self):
        """Initialize dashboard features based on feature flags."""
        self.enabled_features = set()
        
        # Check feature flags for dashboard capabilities
        if is_feature_enabled("web_dashboard"):
            # Core features always available when dashboard is enabled
            self.enabled_features.update([
                DashboardFeature.PROJECT_OVERVIEW,
                DashboardFeature.REAL_TIME_MONITORING,
                DashboardFeature.PROGRESS_TRACKING
            ])
            
            # Check tier-specific features
            current_tier = pricing_manager.current_tier
            
            if current_tier in [PricingTier.PROFESSIONAL, PricingTier.TEAM, PricingTier.ENTERPRISE]:
                self.enabled_features.update([
                    DashboardFeature.CODE_ANALYSIS_VIEW,
                    DashboardFeature.REQUIREMENTS_MANAGEMENT,
                    DashboardFeature.TEST_GENERATION_STATUS
                ])
            
            if current_tier in [PricingTier.TEAM, PricingTier.ENTERPRISE]:
                self.enabled_features.update([
                    DashboardFeature.ANALYTICS_DASHBOARD,
                    DashboardFeature.TEAM_COLLABORATION
                ])
            
            if current_tier == PricingTier.ENTERPRISE:
                self.enabled_features.update([
                    DashboardFeature.AUDIT_TRAILS,
                    DashboardFeature.CI_CD_INTEGRATION,
                    DashboardFeature.API_MANAGEMENT,
                    DashboardFeature.EXPORT_CAPABILITIES
                ])
    
    def _setup_middleware(self):
        """Setup FastAPI middleware."""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=self.config.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def _setup_routes(self):
        """Setup dashboard API routes."""
        
        # Health check
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "features": list(self.enabled_features)}
        
        # Dashboard overview
        @self.app.get("/api/dashboard/overview")
        async def get_dashboard_overview():
            if DashboardFeature.PROJECT_OVERVIEW not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Project overview not available")
            
            return {
                "total_projects": len(self.data.projects),
                "total_users": len(self.data.users),
                "recent_events": len(self.data.real_time_events),
                "enabled_features": list(self.enabled_features)
            }
        
        # Projects list
        @self.app.get("/api/projects")
        async def get_projects():
            if DashboardFeature.PROJECT_OVERVIEW not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Projects view not available")
            
            return {
                "projects": list(self.data.projects.values()),
                "total": len(self.data.projects)
            }
        
        # Project details
        @self.app.get("/api/projects/{project_id}")
        async def get_project(project_id: str):
            if DashboardFeature.PROJECT_OVERVIEW not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Project details not available")
            
            if project_id not in self.data.projects:
                raise HTTPException(status_code=404, detail="Project not found")
            
            return self.data.projects[project_id]
        
        # Real-time monitoring
        @self.app.get("/api/monitoring/events")
        async def get_monitoring_events():
            if DashboardFeature.REAL_TIME_MONITORING not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Real-time monitoring not available")
            
            return {
                "events": self.data.real_time_events[-50:],  # Last 50 events
                "total": len(self.data.real_time_events)
            }
        
        # Progress tracking
        @self.app.get("/api/progress/{project_id}")
        async def get_project_progress(project_id: str):
            if DashboardFeature.PROGRESS_TRACKING not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Progress tracking not available")
            
            if project_id not in self.data.projects:
                raise HTTPException(status_code=404, detail="Project not found")
            
            project = self.data.projects[project_id]
            return {
                "project_id": project_id,
                "status": project.get("status", "unknown"),
                "progress": project.get("progress", 0),
                "last_updated": project.get("last_updated")
            }
        
        # Code analysis view
        @self.app.get("/api/analysis/{project_id}")
        async def get_code_analysis(project_id: str):
            if DashboardFeature.CODE_ANALYSIS_VIEW not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Code analysis view not available")
            
            if project_id not in self.data.projects:
                raise HTTPException(status_code=404, detail="Project not found")
            
            project = self.data.projects[project_id]
            return {
                "project_id": project_id,
                "analysis": project.get("analysis", {}),
                "files_analyzed": project.get("files_analyzed", 0),
                "issues_found": project.get("issues_found", 0)
            }
        
        # Requirements management
        @self.app.get("/api/requirements/{project_id}")
        async def get_requirements(project_id: str):
            if DashboardFeature.REQUIREMENTS_MANAGEMENT not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Requirements management not available")
            
            if project_id not in self.data.projects:
                raise HTTPException(status_code=404, detail="Project not found")
            
            project = self.data.projects[project_id]
            return {
                "project_id": project_id,
                "requirements": project.get("requirements", []),
                "total_requirements": len(project.get("requirements", [])),
                "approved_requirements": len([
                    req for req in project.get("requirements", [])
                    if req.get("status") == "approved"
                ])
            }
        
        # Test generation status
        @self.app.get("/api/tests/{project_id}")
        async def get_test_status(project_id: str):
            if DashboardFeature.TEST_GENERATION_STATUS not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Test generation status not available")
            
            if project_id not in self.data.projects:
                raise HTTPException(status_code=404, detail="Project not found")
            
            project = self.data.projects[project_id]
            return {
                "project_id": project_id,
                "tests": project.get("tests", []),
                "total_tests": len(project.get("tests", [])),
                "test_coverage": project.get("test_coverage", 0),
                "test_status": project.get("test_status", "unknown")
            }
        
        # Analytics dashboard
        @self.app.get("/api/analytics")
        async def get_analytics():
            if DashboardFeature.ANALYTICS_DASHBOARD not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Analytics dashboard not available")
            
            return {
                "analytics": self.data.analytics,
                "generated_at": datetime.now().isoformat()
            }
        
        # Team collaboration
        @self.app.get("/api/team")
        async def get_team_info():
            if DashboardFeature.TEAM_COLLABORATION not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Team collaboration not available")
            
            return {
                "users": list(self.data.users.values()),
                "total_users": len(self.data.users),
                "active_users": len([
                    user for user in self.data.users.values()
                    if user.get("status") == "active"
                ])
            }
        
        # Audit trails
        @self.app.get("/api/audit")
        async def get_audit_trails():
            if DashboardFeature.AUDIT_TRAILS not in self.enabled_features:
                raise HTTPException(status_code=403, detail="Audit trails not available")
            
            return {
                "audit_logs": self.data.audit_logs[-100:],  # Last 100 logs
                "total_logs": len(self.data.audit_logs)
            }
        
        # WebSocket for real-time updates
        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            if DashboardFeature.REAL_TIME_MONITORING not in self.enabled_features:
                await websocket.close(code=1008, reason="Real-time monitoring not available")
                return
            
            await websocket.accept()
            try:
                while True:
                    # Send real-time updates
                    await websocket.send_json({
                        "type": "update",
                        "timestamp": datetime.now().isoformat(),
                        "events_count": len(self.data.real_time_events),
                        "projects_count": len(self.data.projects)
                    })
                    await asyncio.sleep(5)  # Update every 5 seconds
            except WebSocketDisconnect:
                pass
    
    def start(self):
        """Start the dashboard server."""
        uvicorn.run(
            self.app,
            host=self.config.host,
            port=self.config.port,
            debug=self.config.debug
        )
    
    def add_project_data(self, project_id: str, data: Dict[str, Any]):
        """Add or update project data.
        
        Args:
            project_id: Unique project identifier
            data: Project data dictionary
        """
        self.data.add_project(project_id, data)
        
        # Add audit log
        self.data.add_audit_log({
            "event": "project_updated",
            "project_id": project_id,
            "user_id": data.get("user_id", "unknown"),
            "changes": list(data.keys())
        })
    
    def add_user_data(self, user_id: str, data: Dict[str, Any]):
        """Add or update user data.
        
        Args:
            user_id: Unique user identifier
            data: User data dictionary
        """
        self.data.add_user(user_id, data)
    
    def add_real_time_event(self, event: Dict[str, Any]):
        """Add real-time event.
        
        Args:
            event: Event data dictionary
        """
        self.data.add_real_time_event(event)
    
    def get_enabled_features(self) -> Set[DashboardFeature]:
        """Get enabled dashboard features.
        
        Returns:
            Set of enabled dashboard features
        """
        return self.enabled_features
    
    def is_feature_enabled(self, feature: DashboardFeature) -> bool:
        """Check if a dashboard feature is enabled.
        
        Args:
            feature: Dashboard feature to check
            
        Returns:
            True if feature is enabled, False otherwise
        """
        return feature in self.enabled_features


# Global dashboard manager instance
_dashboard_manager: Optional[DashboardManager] = None


def get_dashboard_manager() -> DashboardManager:
    """Get the global dashboard manager instance.
    
    Returns:
        DashboardManager instance
    """
    global _dashboard_manager
    if _dashboard_manager is None:
        config = DashboardConfig()
        _dashboard_manager = DashboardManager(config)
    return _dashboard_manager


def start_dashboard(host: str = "localhost", port: int = 3000, debug: bool = False):
    """Start the AgentOps web dashboard.
    
    Args:
        host: Dashboard host address
        port: Dashboard port number
        debug: Enable debug mode
    """
    if not is_feature_enabled("web_dashboard"):
        raise RuntimeError("Web dashboard feature is not enabled")
    
    manager = get_dashboard_manager()
    manager.config.host = host
    manager.config.port = port
    manager.config.debug = debug
    
    print(f"🚀 Starting AgentOps Dashboard at http://{host}:{port}")
    print(f"📊 Enabled features: {list(manager.get_enabled_features())}")
    
    manager.start()


def add_project_to_dashboard(project_id: str, data: Dict[str, Any]):
    """Add project data to the dashboard.
    
    Args:
        project_id: Unique project identifier
        data: Project data dictionary
    """
    if is_feature_enabled("web_dashboard"):
        manager = get_dashboard_manager()
        manager.add_project_data(project_id, data)


def add_user_to_dashboard(user_id: str, data: Dict[str, Any]):
    """Add user data to the dashboard.
    
    Args:
        user_id: Unique user identifier
        data: User data dictionary
    """
    if is_feature_enabled("web_dashboard"):
        manager = get_dashboard_manager()
        manager.add_user_data(user_id, data)


def add_dashboard_event(event: Dict[str, Any]):
    """Add real-time event to the dashboard.
    
    Args:
        event: Event data dictionary
    """
    if is_feature_enabled("web_dashboard"):
        manager = get_dashboard_manager()
        manager.add_real_time_event(event)
