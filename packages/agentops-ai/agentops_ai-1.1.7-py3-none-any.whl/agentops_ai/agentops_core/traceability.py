"""
AgentOps Traceability Matrix System

This module implements a comprehensive bidirectional traceability matrix that:
- Links requirements to tests and code
- Tracks coverage and relationships
- Provides export capabilities
- Supports multiple formats (CSV, Excel, HTML)
- Features modular enable/disable capabilities
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Any, Union
from pathlib import Path
import json
import csv
import pandas as pd
from datetime import datetime
import logging

from .features import get_feature_manager, is_feature_enabled
from .pricing import pricing_manager, PricingTier


class TraceabilityType(Enum):
    """Types of traceability relationships."""
    
    REQUIREMENT_TO_TEST = "requirement_to_test"
    REQUIREMENT_TO_CODE = "requirement_to_code"
    TEST_TO_CODE = "test_to_code"
    CODE_TO_REQUIREMENT = "code_to_requirement"
    CODE_TO_TEST = "code_to_test"
    TEST_TO_REQUIREMENT = "test_to_requirement"


class CoverageStatus(Enum):
    """Coverage status for traceability."""
    
    FULLY_COVERED = "fully_covered"
    PARTIALLY_COVERED = "partially_covered"
    NOT_COVERED = "not_covered"
    PENDING = "pending"


@dataclass
class TraceabilityItem:
    """Individual item in the traceability matrix."""
    
    id: str
    type: str  # requirement, test, code
    name: str
    description: str
    status: str = "active"
    priority: str = "medium"
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Relationships
    relationships: Set[str] = field(default_factory=set)
    
    # Coverage information
    coverage_status: CoverageStatus = CoverageStatus.NOT_COVERED
    coverage_percentage: float = 0.0


@dataclass
class TraceabilityRelationship:
    """Relationship between traceability items."""
    
    source_id: str
    target_id: str
    relationship_type: TraceabilityType
    strength: float = 1.0  # 0.0 to 1.0
    confidence: float = 1.0  # 0.0 to 1.0
    created_at: datetime = field(default_factory=datetime.now)
    
    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Status
    status: str = "active"
    verified: bool = False


@dataclass
class TraceabilityMatrix:
    """Complete traceability matrix."""
    
    project_id: str
    items: Dict[str, TraceabilityItem] = field(default_factory=dict)
    relationships: List[TraceabilityRelationship] = field(default_factory=list)
    
    # Configuration
    auto_update: bool = True
    coverage_threshold: float = 0.8
    confidence_threshold: float = 0.7
    
    # Statistics
    total_items: int = 0
    total_relationships: int = 0
    coverage_percentage: float = 0.0
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


class TraceabilityManager:
    """Manages traceability matrix operations."""
    
    def __init__(self):
        """Initialize the traceability manager."""
        self.matrices: Dict[str, TraceabilityMatrix] = {}
        self.feature_manager = get_feature_manager()
        
        # Check if traceability matrix feature is enabled
        if not is_feature_enabled("traceability_matrix"):
            logging.warning("Traceability matrix feature is not enabled")
    
    def create_matrix(self, project_id: str) -> TraceabilityMatrix:
        """Create a new traceability matrix for a project.
        
        Args:
            project_id: Unique project identifier
            
        Returns:
            New traceability matrix
        """
        if not is_feature_enabled("traceability_matrix"):
            raise RuntimeError("Traceability matrix feature is not enabled")
        
        matrix = TraceabilityMatrix(project_id=project_id)
        self.matrices[project_id] = matrix
        return matrix
    
    def get_matrix(self, project_id: str) -> Optional[TraceabilityMatrix]:
        """Get traceability matrix for a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Traceability matrix or None if not found
        """
        return self.matrices.get(project_id)
    
    def add_item(self, project_id: str, item: TraceabilityItem) -> bool:
        """Add an item to the traceability matrix.
        
        Args:
            project_id: Project identifier
            item: Item to add
            
        Returns:
            True if item was added, False otherwise
        """
        if not is_feature_enabled("traceability_matrix"):
            return False
        
        matrix = self.get_matrix(project_id)
        if not matrix:
            matrix = self.create_matrix(project_id)
        
        matrix.items[item.id] = item
        matrix.total_items = len(matrix.items)
        matrix.updated_at = datetime.now()
        
        return True
    
    def add_relationship(self, project_id: str, relationship: TraceabilityRelationship) -> bool:
        """Add a relationship to the traceability matrix.
        
        Args:
            project_id: Project identifier
            relationship: Relationship to add
            
        Returns:
            True if relationship was added, False otherwise
        """
        if not is_feature_enabled("traceability_matrix"):
            return False
        
        matrix = self.get_matrix(project_id)
        if not matrix:
            matrix = self.create_matrix(project_id)
        
        # Validate relationship
        if not self._validate_relationship(matrix, relationship):
            return False
        
        matrix.relationships.append(relationship)
        matrix.total_relationships = len(matrix.relationships)
        matrix.updated_at = datetime.now()
        
        # Update item relationships
        if relationship.source_id in matrix.items:
            matrix.items[relationship.source_id].relationships.add(relationship.target_id)
        
        if relationship.target_id in matrix.items:
            matrix.items[relationship.target_id].relationships.add(relationship.source_id)
        
        return True
    
    def _validate_relationship(self, matrix: TraceabilityMatrix, 
                             relationship: TraceabilityRelationship) -> bool:
        """Validate a relationship.
        
        Args:
            matrix: Traceability matrix
            relationship: Relationship to validate
            
        Returns:
            True if relationship is valid, False otherwise
        """
        # Check if both items exist
        if relationship.source_id not in matrix.items:
            return False
        
        if relationship.target_id not in matrix.items:
            return False
        
        # Check for duplicate relationships
        for existing in matrix.relationships:
            if (existing.source_id == relationship.source_id and 
                existing.target_id == relationship.target_id and
                existing.relationship_type == relationship.relationship_type):
                return False
        
        return True
    
    def calculate_coverage(self, project_id: str) -> Dict[str, Any]:
        """Calculate coverage statistics for a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Coverage statistics
        """
        if not is_feature_enabled("traceability_matrix"):
            return {"error": "Traceability matrix feature not enabled"}
        
        matrix = self.get_matrix(project_id)
        if not matrix:
            return {"error": "Matrix not found"}
        
        # Calculate coverage for each item type
        requirements = [item for item in matrix.items.values() if item.type == "requirement"]
        tests = [item for item in matrix.items.values() if item.type == "test"]
        code_items = [item for item in matrix.items.values() if item.type == "code"]
        
        # Calculate coverage percentages
        req_coverage = self._calculate_item_coverage(matrix, requirements)
        test_coverage = self._calculate_item_coverage(matrix, tests)
        code_coverage = self._calculate_item_coverage(matrix, code_items)
        
        # Overall coverage
        total_items = len(matrix.items)
        covered_items = len([item for item in matrix.items.values() 
                           if item.coverage_status != CoverageStatus.NOT_COVERED])
        overall_coverage = (covered_items / total_items * 100) if total_items > 0 else 0
        
        return {
            "project_id": project_id,
            "overall_coverage": overall_coverage,
            "requirements": {
                "total": len(requirements),
                "covered": req_coverage["covered"],
                "coverage_percentage": req_coverage["coverage_percentage"]
            },
            "tests": {
                "total": len(tests),
                "covered": test_coverage["covered"],
                "coverage_percentage": test_coverage["coverage_percentage"]
            },
            "code_items": {
                "total": len(code_items),
                "covered": code_coverage["covered"],
                "coverage_percentage": code_coverage["coverage_percentage"]
            },
            "relationships": {
                "total": len(matrix.relationships),
                "verified": len([r for r in matrix.relationships if r.verified])
            }
        }
    
    def _calculate_item_coverage(self, matrix: TraceabilityMatrix, 
                                items: List[TraceabilityItem]) -> Dict[str, Any]:
        """Calculate coverage for a list of items.
        
        Args:
            matrix: Traceability matrix
            items: List of items to calculate coverage for
            
        Returns:
            Coverage statistics
        """
        if not items:
            return {"covered": 0, "coverage_percentage": 0.0}
        
        covered = len([item for item in items if item.coverage_status != CoverageStatus.NOT_COVERED])
        coverage_percentage = (covered / len(items) * 100) if items else 0
        
        return {
            "covered": covered,
            "coverage_percentage": coverage_percentage
        }
    
    def export_matrix(self, project_id: str, format_type: str = "csv", 
                     output_path: Optional[str] = None) -> str:
        """Export traceability matrix to various formats.
        
        Args:
            project_id: Project identifier
            format_type: Export format (csv, excel, html)
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        if not is_feature_enabled("traceability_matrix"):
            raise RuntimeError("Traceability matrix feature not enabled")
        
        matrix = self.get_matrix(project_id)
        if not matrix:
            raise ValueError(f"Matrix not found for project {project_id}")
        
        # Check tier access for export formats
        current_tier = pricing_manager.current_tier
        if format_type == "excel" and current_tier == PricingTier.DEVELOPER:
            raise RuntimeError("Excel export not available in developer tier")
        
        if format_type == "html" and current_tier in [PricingTier.DEVELOPER, PricingTier.PROFESSIONAL]:
            raise RuntimeError("HTML export not available in current tier")
        
        # Generate output path
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"traceability_matrix_{project_id}_{timestamp}.{format_type}"
        
        # Export based on format
        if format_type == "csv":
            return self._export_csv(matrix, output_path)
        elif format_type == "excel":
            return self._export_excel(matrix, output_path)
        elif format_type == "html":
            return self._export_html(matrix, output_path)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
    
    def _export_csv(self, matrix: TraceabilityMatrix, output_path: str) -> str:
        """Export matrix to CSV format.
        
        Args:
            matrix: Traceability matrix
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        # Create items CSV
        items_data = []
        for item in matrix.items.values():
            items_data.append({
                "id": item.id,
                "type": item.type,
                "name": item.name,
                "description": item.description,
                "status": item.status,
                "priority": item.priority,
                "coverage_status": item.coverage_status.value,
                "coverage_percentage": item.coverage_percentage,
                "created_at": item.created_at.isoformat(),
                "updated_at": item.updated_at.isoformat()
            })
        
        # Create relationships CSV
        relationships_data = []
        for rel in matrix.relationships:
            relationships_data.append({
                "source_id": rel.source_id,
                "target_id": rel.target_id,
                "relationship_type": rel.relationship_type.value,
                "strength": rel.strength,
                "confidence": rel.confidence,
                "status": rel.status,
                "verified": rel.verified,
                "created_at": rel.created_at.isoformat()
            })
        
        # Write CSV files
        items_path = output_path.replace('.csv', '_items.csv')
        relationships_path = output_path.replace('.csv', '_relationships.csv')
        
        with open(items_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=items_data[0].keys())
            writer.writeheader()
            writer.writerows(items_data)
        
        with open(relationships_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=relationships_data[0].keys())
            writer.writeheader()
            writer.writerows(relationships_data)
        
        return items_path
    
    def _export_excel(self, matrix: TraceabilityMatrix, output_path: str) -> str:
        """Export matrix to Excel format.
        
        Args:
            matrix: Traceability matrix
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        # Prepare data for Excel
        items_data = []
        for item in matrix.items.values():
            items_data.append({
                "ID": item.id,
                "Type": item.type,
                "Name": item.name,
                "Description": item.description,
                "Status": item.status,
                "Priority": item.priority,
                "Coverage Status": item.coverage_status.value,
                "Coverage %": item.coverage_percentage,
                "Created": item.created_at.isoformat(),
                "Updated": item.updated_at.isoformat()
            })
        
        relationships_data = []
        for rel in matrix.relationships:
            relationships_data.append({
                "Source ID": rel.source_id,
                "Target ID": rel.target_id,
                "Relationship Type": rel.relationship_type.value,
                "Strength": rel.strength,
                "Confidence": rel.confidence,
                "Status": rel.status,
                "Verified": rel.verified,
                "Created": rel.created_at.isoformat()
            })
        
        # Create Excel file with multiple sheets
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            pd.DataFrame(items_data).to_excel(writer, sheet_name='Items', index=False)
            pd.DataFrame(relationships_data).to_excel(writer, sheet_name='Relationships', index=False)
            
            # Add summary sheet
            coverage_stats = self.calculate_coverage(matrix.project_id)
            summary_data = [
                {"Metric": "Total Items", "Value": coverage_stats.get("requirements", {}).get("total", 0) + 
                                                   coverage_stats.get("tests", {}).get("total", 0) + 
                                                   coverage_stats.get("code_items", {}).get("total", 0)},
                {"Metric": "Total Relationships", "Value": coverage_stats.get("relationships", {}).get("total", 0)},
                {"Metric": "Overall Coverage %", "Value": coverage_stats.get("overall_coverage", 0)},
                {"Metric": "Requirements Coverage %", "Value": coverage_stats.get("requirements", {}).get("coverage_percentage", 0)},
                {"Metric": "Tests Coverage %", "Value": coverage_stats.get("tests", {}).get("coverage_percentage", 0)},
                {"Metric": "Code Coverage %", "Value": coverage_stats.get("code_items", {}).get("coverage_percentage", 0)}
            ]
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        return output_path
    
    def _export_html(self, matrix: TraceabilityMatrix, output_path: str) -> str:
        """Export matrix to HTML format.
        
        Args:
            matrix: Traceability matrix
            output_path: Output file path
            
        Returns:
            Path to exported file
        """
        # Calculate coverage statistics
        coverage_stats = self.calculate_coverage(matrix.project_id)
        
        # Generate HTML content
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Traceability Matrix - {matrix.project_id}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat {{ text-align: center; padding: 10px; background-color: #e8f4fd; border-radius: 5px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                .coverage-high {{ background-color: #d4edda; }}
                .coverage-medium {{ background-color: #fff3cd; }}
                .coverage-low {{ background-color: #f8d7da; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Traceability Matrix</h1>
                <p><strong>Project:</strong> {matrix.project_id}</p>
                <p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <div class="stats">
                <div class="stat">
                    <h3>Overall Coverage</h3>
                    <p>{coverage_stats.get('overall_coverage', 0):.1f}%</p>
                </div>
                <div class="stat">
                    <h3>Total Items</h3>
                    <p>{coverage_stats.get('requirements', {}).get('total', 0) + 
                        coverage_stats.get('tests', {}).get('total', 0) + 
                        coverage_stats.get('code_items', {}).get('total', 0)}</p>
                </div>
                <div class="stat">
                    <h3>Total Relationships</h3>
                    <p>{coverage_stats.get('relationships', {}).get('total', 0)}</p>
                </div>
            </div>
            
            <h2>Items</h2>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Type</th>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Coverage</th>
                </tr>
        """
        
        for item in matrix.items.values():
            coverage_class = "coverage-high" if item.coverage_percentage >= 80 else \
                           "coverage-medium" if item.coverage_percentage >= 50 else "coverage-low"
            
            html_content += f"""
                <tr class="{coverage_class}">
                    <td>{item.id}</td>
                    <td>{item.type}</td>
                    <td>{item.name}</td>
                    <td>{item.status}</td>
                    <td>{item.coverage_percentage:.1f}%</td>
                </tr>
            """
        
        html_content += """
            </table>
            
            <h2>Relationships</h2>
            <table>
                <tr>
                    <th>Source</th>
                    <th>Target</th>
                    <th>Type</th>
                    <th>Strength</th>
                    <th>Verified</th>
                </tr>
        """
        
        for rel in matrix.relationships:
            html_content += f"""
                <tr>
                    <td>{rel.source_id}</td>
                    <td>{rel.target_id}</td>
                    <td>{rel.relationship_type.value}</td>
                    <td>{rel.strength:.2f}</td>
                    <td>{'Yes' if rel.verified else 'No'}</td>
                </tr>
            """
        
        html_content += """
            </table>
        </body>
        </html>
        """
        
        with open(output_path, 'w') as f:
            f.write(html_content)
        
        return output_path
    
    def get_matrix_summary(self, project_id: str) -> Dict[str, Any]:
        """Get summary of traceability matrix.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Matrix summary
        """
        if not is_feature_enabled("traceability_matrix"):
            return {"error": "Traceability matrix feature not enabled"}
        
        matrix = self.get_matrix(project_id)
        if not matrix:
            return {"error": "Matrix not found"}
        
        coverage_stats = self.calculate_coverage(project_id)
        
        return {
            "project_id": project_id,
            "total_items": matrix.total_items,
            "total_relationships": matrix.total_relationships,
            "coverage_stats": coverage_stats,
            "created_at": matrix.created_at.isoformat(),
            "updated_at": matrix.updated_at.isoformat()
        }


# Global traceability manager instance
_traceability_manager: Optional[TraceabilityManager] = None


def get_traceability_manager() -> TraceabilityManager:
    """Get the global traceability manager instance.
    
    Returns:
        TraceabilityManager instance
    """
    global _traceability_manager
    if _traceability_manager is None:
        _traceability_manager = TraceabilityManager()
    return _traceability_manager


def create_traceability_matrix(project_id: str) -> TraceabilityMatrix:
    """Create a new traceability matrix.
    
    Args:
        project_id: Project identifier
        
    Returns:
        New traceability matrix
    """
    return get_traceability_manager().create_matrix(project_id)


def add_traceability_item(project_id: str, item: TraceabilityItem) -> bool:
    """Add an item to the traceability matrix.
    
    Args:
        project_id: Project identifier
        item: Item to add
        
    Returns:
        True if item was added, False otherwise
    """
    return get_traceability_manager().add_item(project_id, item)


def add_traceability_relationship(project_id: str, relationship: TraceabilityRelationship) -> bool:
    """Add a relationship to the traceability matrix.
    
    Args:
        project_id: Project identifier
        relationship: Relationship to add
        
    Returns:
        True if relationship was added, False otherwise
    """
    return get_traceability_manager().add_relationship(project_id, relationship)


def export_traceability_matrix(project_id: str, format_type: str = "csv", 
                             output_path: Optional[str] = None) -> str:
    """Export traceability matrix.
    
    Args:
        project_id: Project identifier
        format_type: Export format
        output_path: Output file path
        
    Returns:
        Path to exported file
    """
    return get_traceability_manager().export_matrix(project_id, format_type, output_path)


def get_traceability_summary(project_id: str) -> Dict[str, Any]:
    """Get traceability matrix summary.
    
    Args:
        project_id: Project identifier
        
    Returns:
        Matrix summary
    """
    return get_traceability_manager().get_matrix_summary(project_id) 