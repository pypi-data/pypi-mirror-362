"""
DataFlow Migrations Module

Advanced database migration system with automatic schema comparison,
visual confirmation, rollback capabilities, and visual migration builder.
"""

from .auto_migration_system import (
    AutoMigrationSystem,
    ColumnDefinition,
    Migration,
    MigrationGenerator,
    MigrationOperation,
    MigrationStatus,
    MigrationType,
    SchemaDiff,
    SchemaInspector,
    TableDefinition,
)
from .visual_migration_builder import (
    ColumnBuilder,
    ColumnType,
    ConstraintType,
    IndexBuilder,
    IndexType,
    MigrationScript,
    TableBuilder,
    VisualMigrationBuilder,
)

__all__ = [
    # Auto Migration System
    "AutoMigrationSystem",
    "SchemaInspector",
    "MigrationGenerator",
    "Migration",
    "MigrationOperation",
    "SchemaDiff",
    "TableDefinition",
    "ColumnDefinition",
    "MigrationType",
    "MigrationStatus",
    # Visual Migration Builder
    "VisualMigrationBuilder",
    "MigrationScript",
    "ColumnBuilder",
    "TableBuilder",
    "IndexBuilder",
    "ColumnType",
    "IndexType",
    "ConstraintType",
]
