"""
DataFlow Auto-Migration System

Advanced database migration system that automatically detects schema changes,
provides visual confirmation, and supports rollback capabilities.

Features:
- Automatic schema comparison and diff generation
- Visual confirmation before applying changes
- Rollback and versioning support
- Multi-database compatibility (PostgreSQL, MySQL, SQLite)
- Zero SQL knowledge required for users
"""

import json
import logging
import os
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union

logger = logging.getLogger(__name__)


class MigrationType(Enum):
    """Types of database migrations."""

    CREATE_TABLE = "create_table"
    DROP_TABLE = "drop_table"
    ADD_COLUMN = "add_column"
    DROP_COLUMN = "drop_column"
    MODIFY_COLUMN = "modify_column"
    ADD_INDEX = "add_index"
    DROP_INDEX = "drop_index"
    ADD_CONSTRAINT = "add_constraint"
    DROP_CONSTRAINT = "drop_constraint"
    RENAME_TABLE = "rename_table"
    RENAME_COLUMN = "rename_column"


class MigrationStatus(Enum):
    """Status of migration operations."""

    PENDING = "pending"
    APPLIED = "applied"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"


@dataclass
class ColumnDefinition:
    """Definition of a database column."""

    name: str
    type: str
    nullable: bool = True
    default: Optional[Any] = None
    primary_key: bool = False
    foreign_key: Optional[str] = None
    unique: bool = False
    auto_increment: bool = False
    max_length: Optional[int] = None


@dataclass
class TableDefinition:
    """Definition of a database table."""

    name: str
    columns: List[ColumnDefinition] = field(default_factory=list)
    indexes: List[Dict[str, Any]] = field(default_factory=list)
    constraints: List[Dict[str, Any]] = field(default_factory=list)

    def get_column(self, name: str) -> Optional[ColumnDefinition]:
        """Get column by name."""
        for column in self.columns:
            if column.name == name:
                return column
        return None


@dataclass
class MigrationOperation:
    """A single migration operation."""

    operation_type: MigrationType
    table_name: str
    description: str
    sql_up: str
    sql_down: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"{self.operation_type.value}: {self.description}"


@dataclass
class Migration:
    """A complete migration with multiple operations."""

    version: str
    name: str
    operations: List[MigrationOperation] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    applied_at: Optional[datetime] = None
    status: MigrationStatus = MigrationStatus.PENDING
    checksum: Optional[str] = None

    def add_operation(self, operation: MigrationOperation):
        """Add an operation to this migration."""
        self.operations.append(operation)

    def generate_checksum(self) -> str:
        """Generate checksum for migration integrity."""
        import hashlib

        content = f"{self.version}:{self.name}:" + "".join(
            op.sql_up for op in self.operations
        )
        return hashlib.sha256(content.encode()).hexdigest()[:16]


@dataclass
class SchemaDiff:
    """Difference between current and target schemas."""

    tables_to_create: List[TableDefinition] = field(default_factory=list)
    tables_to_drop: List[str] = field(default_factory=list)
    tables_to_modify: List[Tuple[str, TableDefinition, TableDefinition]] = field(
        default_factory=list
    )

    def has_changes(self) -> bool:
        """Check if there are any schema changes."""
        return bool(
            self.tables_to_create or self.tables_to_drop or self.tables_to_modify
        )

    def change_count(self) -> int:
        """Count total number of changes."""
        count = len(self.tables_to_create) + len(self.tables_to_drop)
        for _, _, _ in self.tables_to_modify:
            count += 1  # Each modified table counts as one change
        return count


class SchemaInspector:
    """Inspects database schema and compares with model definitions."""

    def __init__(self, connection, dialect: str = "postgresql"):
        self.connection = connection
        self.dialect = dialect.lower()

    async def get_current_schema(self) -> Dict[str, TableDefinition]:
        """Get current database schema."""
        if self.dialect == "postgresql":
            return await self._get_postgresql_schema()
        elif self.dialect == "mysql":
            return await self._get_mysql_schema()
        elif self.dialect == "sqlite":
            return await self._get_sqlite_schema()
        else:
            raise ValueError(f"Unsupported database dialect: {self.dialect}")

    async def _get_postgresql_schema(self) -> Dict[str, TableDefinition]:
        """Get PostgreSQL schema information."""
        tables = {}

        # Get tables and columns
        query = """
        SELECT
            t.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default,
            c.character_maximum_length,
            CASE WHEN pk.column_name IS NOT NULL THEN true ELSE false END as is_primary_key
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c ON t.table_name = c.table_name
        LEFT JOIN (
            SELECT ku.column_name, ku.table_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
        ) pk ON c.table_name = pk.table_name AND c.column_name = pk.column_name
        WHERE t.table_schema = 'public'
          AND t.table_type = 'BASE TABLE'
          AND t.table_name NOT LIKE 'dataflow_%'
        ORDER BY t.table_name, c.ordinal_position
        """

        async with self.connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()

            current_table = None
            for row in rows:
                table_name = row[0]
                if table_name != current_table:
                    tables[table_name] = TableDefinition(name=table_name)
                    current_table = table_name

                if row[1]:  # column_name exists
                    column = ColumnDefinition(
                        name=row[1],
                        type=row[2],
                        nullable=row[3] == "YES",
                        default=row[4],
                        max_length=row[5],
                        primary_key=row[6],
                    )
                    tables[table_name].columns.append(column)

        # Get indexes for each table
        for table_name in tables:
            await self._get_postgresql_indexes(table_name, tables[table_name])

        return tables

    async def _get_postgresql_indexes(
        self, table_name: str, table_def: TableDefinition
    ):
        """Get PostgreSQL indexes for a table."""
        query = """
        SELECT
            i.relname as index_name,
            array_agg(a.attname ORDER BY c.ordinality) as column_names,
            ix.indisunique as is_unique
        FROM pg_index ix
        JOIN pg_class i ON i.oid = ix.indexrelid
        JOIN pg_class t ON t.oid = ix.indrelid
        JOIN unnest(ix.indkey) WITH ORDINALITY AS c(attnum, ordinality) ON true
        JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = c.attnum
        WHERE t.relname = %s
          AND i.relname NOT LIKE '%_pkey'
        GROUP BY i.relname, ix.indisunique
        """

        async with self.connection.cursor() as cursor:
            await cursor.execute(query, (table_name,))
            rows = await cursor.fetchall()

            for row in rows:
                index_info = {"name": row[0], "columns": row[1], "unique": row[2]}
                table_def.indexes.append(index_info)

    async def _get_mysql_schema(self) -> Dict[str, TableDefinition]:
        """Get MySQL schema information."""
        tables = {}

        query = """
        SELECT
            t.TABLE_NAME,
            c.COLUMN_NAME,
            c.DATA_TYPE,
            c.IS_NULLABLE,
            c.COLUMN_DEFAULT,
            c.CHARACTER_MAXIMUM_LENGTH,
            CASE WHEN c.COLUMN_KEY = 'PRI' THEN 1 ELSE 0 END as IS_PRIMARY_KEY
        FROM information_schema.TABLES t
        LEFT JOIN information_schema.COLUMNS c ON t.TABLE_NAME = c.TABLE_NAME
        WHERE t.TABLE_SCHEMA = DATABASE()
          AND t.TABLE_TYPE = 'BASE TABLE'
          AND t.TABLE_NAME NOT LIKE 'dataflow_%'
        ORDER BY t.TABLE_NAME, c.ORDINAL_POSITION
        """

        async with self.connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()

            current_table = None
            for row in rows:
                table_name = row[0]
                if table_name != current_table:
                    tables[table_name] = TableDefinition(name=table_name)
                    current_table = table_name

                if row[1]:  # column_name exists
                    column = ColumnDefinition(
                        name=row[1],
                        type=row[2],
                        nullable=row[3] == "YES",
                        default=row[4],
                        max_length=row[5],
                        primary_key=bool(row[6]),
                    )
                    tables[table_name].columns.append(column)

        return tables

    async def _get_sqlite_schema(self) -> Dict[str, TableDefinition]:
        """Get SQLite schema information."""
        tables = {}

        # Get table names
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'dataflow_%'"

        async with self.connection.cursor() as cursor:
            await cursor.execute(query)
            table_rows = await cursor.fetchall()

            for table_row in table_rows:
                table_name = table_row[0]
                tables[table_name] = TableDefinition(name=table_name)

                # Get column information
                pragma_query = f"PRAGMA table_info({table_name})"
                await cursor.execute(pragma_query)
                column_rows = await cursor.fetchall()

                for col_row in column_rows:
                    column = ColumnDefinition(
                        name=col_row[1],
                        type=col_row[2],
                        nullable=not col_row[3],  # notnull is inverted
                        default=col_row[4],
                        primary_key=bool(col_row[5]),
                    )
                    tables[table_name].columns.append(column)

        return tables

    def compare_schemas(
        self,
        current_schema: Dict[str, TableDefinition],
        target_schema: Dict[str, TableDefinition],
    ) -> SchemaDiff:
        """Compare current and target schemas to generate diff."""
        diff = SchemaDiff()

        current_tables = set(current_schema.keys())
        target_tables = set(target_schema.keys())

        # Tables to create
        for table_name in target_tables - current_tables:
            diff.tables_to_create.append(target_schema[table_name])

        # Tables to drop
        for table_name in current_tables - target_tables:
            diff.tables_to_drop.append(table_name)

        # Tables to modify
        for table_name in current_tables & target_tables:
            current_table = current_schema[table_name]
            target_table = target_schema[table_name]

            if self._tables_differ(current_table, target_table):
                diff.tables_to_modify.append((table_name, current_table, target_table))

        return diff

    def _tables_differ(self, current: TableDefinition, target: TableDefinition) -> bool:
        """Check if two table definitions differ."""
        # Compare columns
        current_cols = {col.name: col for col in current.columns}
        target_cols = {col.name: col for col in target.columns}

        if set(current_cols.keys()) != set(target_cols.keys()):
            return True

        # Compare column definitions
        for col_name in current_cols:
            current_col = current_cols[col_name]
            target_col = target_cols[col_name]

            if (
                current_col.type != target_col.type
                or current_col.nullable != target_col.nullable
                or current_col.primary_key != target_col.primary_key
                or current_col.default != target_col.default
            ):
                return True

        return False


class MigrationGenerator:
    """Generates migration operations from schema differences."""

    def __init__(self, dialect: str = "postgresql"):
        self.dialect = dialect.lower()

    def generate_migration(self, diff: SchemaDiff, name: str = None) -> Migration:
        """Generate migration from schema diff."""
        if not name:
            name = f"auto_migration_{int(time.time())}"

        version = datetime.now().strftime("%Y%m%d_%H%M%S")
        migration = Migration(version=version, name=name)

        # Generate operations for new tables
        for table in diff.tables_to_create:
            operation = self._generate_create_table_operation(table)
            migration.add_operation(operation)

        # Generate operations for dropped tables
        for table_name in diff.tables_to_drop:
            operation = self._generate_drop_table_operation(table_name)
            migration.add_operation(operation)

        # Generate operations for modified tables
        for table_name, current_table, target_table in diff.tables_to_modify:
            operations = self._generate_modify_table_operations(
                table_name, current_table, target_table
            )
            for operation in operations:
                migration.add_operation(operation)

        migration.checksum = migration.generate_checksum()
        return migration

    def _generate_create_table_operation(
        self, table: TableDefinition
    ) -> MigrationOperation:
        """Generate CREATE TABLE operation."""
        sql_up = self._create_table_sql(table)
        sql_down = f"DROP TABLE IF EXISTS {table.name};"

        return MigrationOperation(
            operation_type=MigrationType.CREATE_TABLE,
            table_name=table.name,
            description=f"Create table '{table.name}' with {len(table.columns)} columns",
            sql_up=sql_up,
            sql_down=sql_down,
            metadata={"columns": len(table.columns)},
        )

    def _generate_drop_table_operation(self, table_name: str) -> MigrationOperation:
        """Generate DROP TABLE operation."""
        sql_up = f"DROP TABLE IF EXISTS {table_name};"
        sql_down = f"-- Cannot automatically recreate dropped table: {table_name}"

        return MigrationOperation(
            operation_type=MigrationType.DROP_TABLE,
            table_name=table_name,
            description=f"Drop table '{table_name}'",
            sql_up=sql_up,
            sql_down=sql_down,
            metadata={"warning": "Cannot automatically rollback table drops"},
        )

    def _generate_modify_table_operations(
        self,
        table_name: str,
        current_table: TableDefinition,
        target_table: TableDefinition,
    ) -> List[MigrationOperation]:
        """Generate operations for table modifications."""
        operations = []

        current_cols = {col.name: col for col in current_table.columns}
        target_cols = {col.name: col for col in target_table.columns}

        # Add new columns
        for col_name in set(target_cols.keys()) - set(current_cols.keys()):
            column = target_cols[col_name]
            operation = self._generate_add_column_operation(table_name, column)
            operations.append(operation)

        # Drop columns
        for col_name in set(current_cols.keys()) - set(target_cols.keys()):
            operation = self._generate_drop_column_operation(table_name, col_name)
            operations.append(operation)

        # Modify existing columns
        for col_name in set(current_cols.keys()) & set(target_cols.keys()):
            current_col = current_cols[col_name]
            target_col = target_cols[col_name]

            if self._columns_differ(current_col, target_col):
                operation = self._generate_modify_column_operation(
                    table_name, current_col, target_col
                )
                operations.append(operation)

        return operations

    def _generate_add_column_operation(
        self, table_name: str, column: ColumnDefinition
    ) -> MigrationOperation:
        """Generate ADD COLUMN operation."""
        column_sql = self._column_definition_sql(column)
        sql_up = f"ALTER TABLE {table_name} ADD COLUMN {column_sql};"
        sql_down = f"ALTER TABLE {table_name} DROP COLUMN {column.name};"

        return MigrationOperation(
            operation_type=MigrationType.ADD_COLUMN,
            table_name=table_name,
            description=f"Add column '{column.name}' to table '{table_name}'",
            sql_up=sql_up,
            sql_down=sql_down,
            metadata={"column_name": column.name, "column_type": column.type},
        )

    def _generate_drop_column_operation(
        self, table_name: str, column_name: str
    ) -> MigrationOperation:
        """Generate DROP COLUMN operation."""
        sql_up = f"ALTER TABLE {table_name} DROP COLUMN {column_name};"
        sql_down = f"-- Cannot automatically recreate dropped column: {column_name}"

        return MigrationOperation(
            operation_type=MigrationType.DROP_COLUMN,
            table_name=table_name,
            description=f"Drop column '{column_name}' from table '{table_name}'",
            sql_up=sql_up,
            sql_down=sql_down,
            metadata={
                "column_name": column_name,
                "warning": "Cannot automatically rollback",
            },
        )

    def _generate_modify_column_operation(
        self,
        table_name: str,
        current_col: ColumnDefinition,
        target_col: ColumnDefinition,
    ) -> MigrationOperation:
        """Generate MODIFY COLUMN operation."""
        if self.dialect == "postgresql":
            sql_up = self._postgresql_modify_column_sql(
                table_name, current_col, target_col
            )
            sql_down = self._postgresql_modify_column_sql(
                table_name, target_col, current_col
            )
        elif self.dialect == "mysql":
            sql_up = f"ALTER TABLE {table_name} MODIFY COLUMN {self._column_definition_sql(target_col)};"
            sql_down = f"ALTER TABLE {table_name} MODIFY COLUMN {self._column_definition_sql(current_col)};"
        else:  # SQLite
            sql_up = "-- SQLite does not support MODIFY COLUMN directly"
            sql_down = "-- SQLite does not support MODIFY COLUMN directly"

        return MigrationOperation(
            operation_type=MigrationType.MODIFY_COLUMN,
            table_name=table_name,
            description=f"Modify column '{current_col.name}' in table '{table_name}'",
            sql_up=sql_up,
            sql_down=sql_down,
            metadata={
                "column_name": current_col.name,
                "old_type": current_col.type,
                "new_type": target_col.type,
            },
        )

    def _create_table_sql(self, table: TableDefinition) -> str:
        """Generate CREATE TABLE SQL."""
        columns_sql = []
        for column in table.columns:
            columns_sql.append(self._column_definition_sql(column))

        sql = f"CREATE TABLE {table.name} (\n"
        sql += ",\n".join(f"    {col_sql}" for col_sql in columns_sql)
        sql += "\n);"

        return sql

    def _column_definition_sql(self, column: ColumnDefinition) -> str:
        """Generate column definition SQL."""
        parts = [column.name, column.type]

        if column.max_length and column.type.upper() in ("VARCHAR", "CHAR"):
            parts[1] = f"{column.type}({column.max_length})"

        if not column.nullable:
            parts.append("NOT NULL")

        if column.default is not None:
            if isinstance(column.default, str):
                parts.append(f"DEFAULT '{column.default}'")
            else:
                parts.append(f"DEFAULT {column.default}")

        if column.primary_key:
            parts.append("PRIMARY KEY")

        if column.unique:
            parts.append("UNIQUE")

        if column.auto_increment:
            if self.dialect == "postgresql":
                parts[1] = "SERIAL"
            elif self.dialect == "mysql":
                parts.append("AUTO_INCREMENT")

        return " ".join(parts)

    def _postgresql_modify_column_sql(
        self,
        table_name: str,
        current_col: ColumnDefinition,
        target_col: ColumnDefinition,
    ) -> str:
        """Generate PostgreSQL-specific ALTER COLUMN SQL."""
        statements = []

        # Change data type
        if current_col.type != target_col.type:
            statements.append(
                f"ALTER TABLE {table_name} ALTER COLUMN {current_col.name} TYPE {target_col.type};"
            )

        # Change nullable
        if current_col.nullable != target_col.nullable:
            if target_col.nullable:
                statements.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {current_col.name} DROP NOT NULL;"
                )
            else:
                statements.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {current_col.name} SET NOT NULL;"
                )

        # Change default
        if current_col.default != target_col.default:
            if target_col.default is not None:
                default_val = (
                    f"'{target_col.default}'"
                    if isinstance(target_col.default, str)
                    else target_col.default
                )
                statements.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {current_col.name} SET DEFAULT {default_val};"
                )
            else:
                statements.append(
                    f"ALTER TABLE {table_name} ALTER COLUMN {current_col.name} DROP DEFAULT;"
                )

        return "\n".join(statements)

    def _columns_differ(
        self, current: ColumnDefinition, target: ColumnDefinition
    ) -> bool:
        """Check if column definitions differ."""
        return (
            current.type != target.type
            or current.nullable != target.nullable
            or current.default != target.default
            or current.primary_key != target.primary_key
            or current.unique != target.unique
        )


class AutoMigrationSystem:
    """
    Main auto-migration system that orchestrates schema comparison,
    migration generation, and execution with visual confirmation.
    """

    def __init__(
        self,
        connection,
        dialect: str = "postgresql",
        migrations_dir: str = "migrations",
    ):
        self.connection = connection
        self.dialect = dialect.lower()
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)

        self.inspector = SchemaInspector(connection, dialect)
        self.generator = MigrationGenerator(dialect)

        # Migration history
        self.applied_migrations: List[Migration] = []
        self.pending_migrations: List[Migration] = []

    async def auto_migrate(
        self,
        target_schema: Dict[str, TableDefinition],
        dry_run: bool = False,
        interactive: bool = True,
        auto_confirm: bool = False,
    ) -> Tuple[bool, List[Migration]]:
        """
        Automatically generate and apply migrations to match target schema.

        Args:
            target_schema: Target schema to migrate to
            dry_run: If True, only show what would be done
            interactive: If True, prompt user for confirmation
            auto_confirm: If True, automatically confirm all changes

        Returns:
            Tuple of (success, list of applied migrations)
        """
        logger.info("Starting auto-migration process")

        try:
            # Ensure migration tracking table exists
            await self._ensure_migration_table()

            # Load migration history
            await self._load_migration_history()

            # Get current schema
            current_schema = await self.inspector.get_current_schema()
            logger.info(f"Current schema has {len(current_schema)} tables")

            # Compare schemas
            diff = self.inspector.compare_schemas(current_schema, target_schema)

            if not diff.has_changes():
                logger.info("No schema changes detected")
                return True, []

            # Generate migration
            migration = self.generator.generate_migration(diff, "auto_generated")
            logger.info(
                f"Generated migration with {len(migration.operations)} operations"
            )

            # Show visual confirmation
            if interactive and not auto_confirm:
                confirmed = await self._show_visual_confirmation(migration, diff)
                if not confirmed:
                    logger.info("Migration cancelled by user")
                    return False, []

            if dry_run:
                logger.info("Dry run mode - no changes applied")
                self._print_migration_preview(migration)
                return True, [migration]

            # Apply migration
            success = await self._apply_migration(migration)

            if success:
                logger.info(f"Migration {migration.version} applied successfully")
                return True, [migration]
            else:
                logger.error(f"Migration {migration.version} failed")
                return False, []

        except Exception as e:
            logger.error(f"Auto-migration failed: {e}")
            return False, []

    async def rollback_migration(self, migration_version: str = None) -> bool:
        """
        Rollback a migration.

        Args:
            migration_version: Version to rollback to. If None, rollback last migration.

        Returns:
            True if rollback successful
        """
        logger.info(f"Starting rollback process for version: {migration_version}")

        try:
            await self._load_migration_history()

            if not migration_version:
                # Rollback last migration
                applied_migrations = [
                    m
                    for m in self.applied_migrations
                    if m.status == MigrationStatus.APPLIED
                ]
                if not applied_migrations:
                    logger.warning("No migrations to rollback")
                    return False

                migration_to_rollback = max(
                    applied_migrations, key=lambda m: m.created_at
                )
            else:
                # Find specific migration
                migration_to_rollback = None
                for migration in self.applied_migrations:
                    if migration.version == migration_version:
                        migration_to_rollback = migration
                        break

                if not migration_to_rollback:
                    logger.error(f"Migration {migration_version} not found")
                    return False

            # Execute rollback operations in reverse order
            logger.info(f"Rolling back migration {migration_to_rollback.version}")

            async with self.connection.transaction():
                for operation in reversed(migration_to_rollback.operations):
                    if operation.sql_down.startswith("-- Cannot"):
                        logger.warning(
                            f"Cannot rollback operation: {operation.description}"
                        )
                        continue

                    try:
                        async with self.connection.cursor() as cursor:
                            await cursor.execute(operation.sql_down)
                        logger.info(f"Rolled back: {operation.description}")
                    except Exception as e:
                        logger.error(
                            f"Failed to rollback operation {operation.description}: {e}"
                        )
                        raise

                # Update migration status
                await self._update_migration_status(
                    migration_to_rollback.version, MigrationStatus.ROLLED_BACK
                )

            logger.info(
                f"Migration {migration_to_rollback.version} rolled back successfully"
            )
            return True

        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False

    async def get_migration_status(self) -> Dict[str, Any]:
        """Get current migration status and history."""
        await self._load_migration_history()

        applied_count = sum(
            1 for m in self.applied_migrations if m.status == MigrationStatus.APPLIED
        )
        failed_count = sum(
            1 for m in self.applied_migrations if m.status == MigrationStatus.FAILED
        )
        rolled_back_count = sum(
            1
            for m in self.applied_migrations
            if m.status == MigrationStatus.ROLLED_BACK
        )

        return {
            "total_migrations": len(self.applied_migrations),
            "applied_migrations": applied_count,
            "failed_migrations": failed_count,
            "rolled_back_migrations": rolled_back_count,
            "pending_migrations": len(self.pending_migrations),
            "last_migration": (
                max(self.applied_migrations, key=lambda m: m.created_at)
                if self.applied_migrations
                else None
            ),
        }

    async def _ensure_migration_table(self):
        """Ensure migration tracking table exists."""
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS dataflow_migrations (
            version VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            checksum VARCHAR(32) NOT NULL,
            applied_at TIMESTAMP,
            status VARCHAR(50) NOT NULL DEFAULT 'pending',
            operations TEXT,
            created_at TIMESTAMP DEFAULT {'CURRENT_TIMESTAMP' if self.dialect != 'sqlite' else "datetime('now')"}
        )
        """

        async with self.connection.cursor() as cursor:
            await cursor.execute(create_sql)

    async def _load_migration_history(self):
        """Load migration history from database."""
        query = "SELECT version, name, checksum, applied_at, status, operations, created_at FROM dataflow_migrations ORDER BY created_at"

        async with self.connection.cursor() as cursor:
            await cursor.execute(query)
            rows = await cursor.fetchall()

            self.applied_migrations = []
            for row in rows:
                operations_data = json.loads(row[5]) if row[5] else []
                operations = [
                    MigrationOperation(
                        operation_type=MigrationType(op["operation_type"]),
                        table_name=op["table_name"],
                        description=op["description"],
                        sql_up=op["sql_up"],
                        sql_down=op["sql_down"],
                        metadata=op.get("metadata", {}),
                    )
                    for op in operations_data
                ]

                migration = Migration(
                    version=row[0],
                    name=row[1],
                    checksum=row[2],
                    applied_at=row[3],
                    status=MigrationStatus(row[4]),
                    operations=operations,
                    created_at=row[6],
                )
                self.applied_migrations.append(migration)

    async def _apply_migration(self, migration: Migration) -> bool:
        """Apply a migration to the database."""
        try:
            async with self.connection.transaction():
                # Execute migration operations
                for operation in migration.operations:
                    async with self.connection.cursor() as cursor:
                        await cursor.execute(operation.sql_up)
                    logger.info(f"Applied: {operation.description}")

                # Record migration in history
                await self._record_migration(migration)

            migration.status = MigrationStatus.APPLIED
            migration.applied_at = datetime.now()
            return True

        except Exception as e:
            logger.error(f"Failed to apply migration: {e}")
            migration.status = MigrationStatus.FAILED

            # Record failed migration
            try:
                await self._record_migration(migration)
            except:
                pass  # Don't fail if we can't record the failure

            return False

    async def _record_migration(self, migration: Migration):
        """Record migration in the database."""
        operations_json = json.dumps(
            [
                {
                    "operation_type": op.operation_type.value,
                    "table_name": op.table_name,
                    "description": op.description,
                    "sql_up": op.sql_up,
                    "sql_down": op.sql_down,
                    "metadata": op.metadata,
                }
                for op in migration.operations
            ]
        )

        insert_sql = """
        INSERT INTO dataflow_migrations (version, name, checksum, applied_at, status, operations)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (version) DO UPDATE SET
            applied_at = EXCLUDED.applied_at,
            status = EXCLUDED.status
        """

        if self.dialect == "sqlite":
            insert_sql = """
            INSERT OR REPLACE INTO dataflow_migrations (version, name, checksum, applied_at, status, operations)
            VALUES (?, ?, ?, ?, ?, ?)
            """

        async with self.connection.cursor() as cursor:
            if self.dialect == "sqlite":
                await cursor.execute(
                    insert_sql,
                    (
                        migration.version,
                        migration.name,
                        migration.checksum,
                        migration.applied_at,
                        migration.status.value,
                        operations_json,
                    ),
                )
            else:
                await cursor.execute(
                    insert_sql,
                    (
                        migration.version,
                        migration.name,
                        migration.checksum,
                        migration.applied_at,
                        migration.status.value,
                        operations_json,
                    ),
                )

    async def _update_migration_status(self, version: str, status: MigrationStatus):
        """Update migration status in database."""
        update_sql = "UPDATE dataflow_migrations SET status = %s WHERE version = %s"
        if self.dialect == "sqlite":
            update_sql = "UPDATE dataflow_migrations SET status = ? WHERE version = ?"

        async with self.connection.cursor() as cursor:
            await cursor.execute(update_sql, (status.value, version))

    async def _show_visual_confirmation(
        self, migration: Migration, diff: SchemaDiff
    ) -> bool:
        """Show visual confirmation of migration changes."""
        print("\n" + "=" * 60)
        print("🔄 DataFlow Auto-Migration Preview")
        print("=" * 60)

        print("\n📊 Migration Summary:")
        print(f"  Version: {migration.version}")
        print(f"  Name: {migration.name}")
        print(f"  Operations: {len(migration.operations)}")
        print(f"  Total changes: {diff.change_count()}")

        # Show detailed changes
        if diff.tables_to_create:
            print(f"\n✅ Tables to CREATE ({len(diff.tables_to_create)}):")
            for table in diff.tables_to_create:
                print(f"  📋 {table.name} ({len(table.columns)} columns)")
                for col in table.columns[:3]:  # Show first 3 columns
                    print(f"    - {col.name}: {col.type}")
                if len(table.columns) > 3:
                    print(f"    ... and {len(table.columns) - 3} more columns")

        if diff.tables_to_drop:
            print(f"\n❌ Tables to DROP ({len(diff.tables_to_drop)}):")
            for table_name in diff.tables_to_drop:
                print(f"  🗑️ {table_name} (⚠️ Data will be lost!)")

        if diff.tables_to_modify:
            print(f"\n🔄 Tables to MODIFY ({len(diff.tables_to_modify)}):")
            for table_name, current, target in diff.tables_to_modify:
                print(f"  📝 {table_name}")
                # Show specific changes
                current_cols = {col.name: col for col in current.columns}
                target_cols = {col.name: col for col in target.columns}

                new_cols = set(target_cols.keys()) - set(current_cols.keys())
                dropped_cols = set(current_cols.keys()) - set(target_cols.keys())

                if new_cols:
                    print(f"    ➕ Adding columns: {', '.join(new_cols)}")
                if dropped_cols:
                    print(
                        f"    ➖ Dropping columns: {', '.join(dropped_cols)} (⚠️ Data will be lost!)"
                    )

        # Show SQL preview
        print("\n📜 SQL Operations Preview:")
        for i, operation in enumerate(migration.operations[:5], 1):
            print(f"  {i}. {operation.description}")
            # Show first line of SQL
            first_line = operation.sql_up.split("\n")[0]
            print(f"     SQL: {first_line[:60]}{'...' if len(first_line) > 60 else ''}")

        if len(migration.operations) > 5:
            print(f"     ... and {len(migration.operations) - 5} more operations")

        # Warnings
        has_data_loss = any(
            op.operation_type in [MigrationType.DROP_TABLE, MigrationType.DROP_COLUMN]
            for op in migration.operations
        )

        if has_data_loss:
            print("\n⚠️ WARNING: This migration will result in DATA LOSS!")
            print("   Please ensure you have backups before proceeding.")

        print(
            f"\n🔄 This migration can be rolled back: {self._can_rollback(migration)}"
        )

        # Confirmation prompt
        print("\n" + "-" * 60)
        while True:
            response = (
                input("Do you want to apply this migration? [y/N/details]: ")
                .lower()
                .strip()
            )

            if response in ["y", "yes"]:
                return True
            elif response in ["n", "no", ""]:
                return False
            elif response in ["d", "details"]:
                self._print_migration_details(migration)
            else:
                print(
                    "Please enter 'y' for yes, 'n' for no, or 'details' for more information."
                )

    def _can_rollback(self, migration: Migration) -> bool:
        """Check if migration can be rolled back."""
        for operation in migration.operations:
            if operation.sql_down.startswith("-- Cannot"):
                return False
        return True

    def _print_migration_preview(self, migration: Migration):
        """Print migration preview for dry run."""
        print("\n📋 Migration Preview (Dry Run)")
        print(f"Version: {migration.version}")
        print(f"Operations: {len(migration.operations)}")

        for operation in migration.operations:
            print(
                f"\n{operation.operation_type.value.upper()}: {operation.description}"
            )
            print(f"SQL: {operation.sql_up}")

    def _print_migration_details(self, migration: Migration):
        """Print detailed migration information."""
        print("\n" + "=" * 60)
        print("📋 Detailed Migration Information")
        print("=" * 60)

        for i, operation in enumerate(migration.operations, 1):
            print(f"\n{i}. {operation.operation_type.value.upper()}")
            print(f"   Table: {operation.table_name}")
            print(f"   Description: {operation.description}")
            print("   Forward SQL:")
            for line in operation.sql_up.split("\n"):
                print(f"     {line}")
            print("   Rollback SQL:")
            for line in operation.sql_down.split("\n"):
                print(f"     {line}")

            if operation.metadata:
                print(f"   Metadata: {operation.metadata}")

        print("\n" + "=" * 60)
