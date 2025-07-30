"""
DataFlow Smart Nodes

Smart operations that use auto-detection and natural language.
"""

from .aggregate_operations import AggregateNode

# Bulk operation nodes
from .bulk_create import BulkCreateNode
from .bulk_delete import BulkDeleteNode
from .bulk_update import BulkUpdateNode
from .bulk_upsert import BulkUpsertNode
from .natural_language_filter import NaturalLanguageFilterNode
from .saga_coordinator import DataFlowSagaCoordinatorNode

# Security nodes
from .security_access_control import DataFlowAccessControlNode
from .security_mfa import DataFlowMFANode
from .security_threat_detection import DataFlowThreatDetectionNode
from .smart_operations import SmartMergeNode

# Transaction nodes
from .transaction_manager import DataFlowTransactionManagerNode
from .two_phase_commit_coordinator import DataFlowTwoPhaseCommitNode
from .workflow_connection_manager import DataFlowConnectionManager

__all__ = [
    "SmartMergeNode",
    "NaturalLanguageFilterNode",
    "AggregateNode",
    "DataFlowConnectionManager",
    "BulkCreateNode",
    "BulkUpdateNode",
    "BulkDeleteNode",
    "BulkUpsertNode",
    "DataFlowAccessControlNode",
    "DataFlowMFANode",
    "DataFlowThreatDetectionNode",
    "DataFlowTransactionManagerNode",
    "DataFlowSagaCoordinatorNode",
    "DataFlowTwoPhaseCommitNode",
]
