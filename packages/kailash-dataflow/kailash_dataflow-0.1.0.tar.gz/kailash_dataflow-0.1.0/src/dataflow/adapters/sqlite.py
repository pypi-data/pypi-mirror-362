"""
SQLite Database Adapter

SQLite-specific database adapter implementation.
"""

import logging
from typing import Any, Dict, List, Tuple

from .base import DatabaseAdapter
from .exceptions import AdapterError, ConnectionError, QueryError, TransactionError

logger = logging.getLogger(__name__)


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter."""

    @property
    def database_type(self) -> str:
        return "sqlite"

    @property
    def default_port(self) -> int:
        return 0  # SQLite doesn't use ports

    def __init__(self, connection_string: str, **kwargs):
        super().__init__(connection_string, **kwargs)

        # SQLite-specific configuration
        if self.connection_string.startswith("sqlite:///"):
            path_part = self.connection_string.replace("sqlite:///", "")
            if path_part == ":memory:":
                self.database_path = ":memory:"
            else:
                self.database_path = "/" + path_part
        elif self.connection_string.startswith("sqlite://"):
            self.database_path = self.connection_string.replace("sqlite://", "")
        self.is_memory_database = self.database_path == ":memory:"

        # SQLite-specific settings
        self.enable_wal = kwargs.get("enable_wal", False)
        self.timeout = kwargs.get("timeout", 5.0)
        self.journal_mode = "WAL" if self.enable_wal else "DELETE"

        # PRAGMA settings
        self.pragmas = kwargs.get(
            "pragmas",
            {
                "foreign_keys": "ON",
                "journal_mode": self.journal_mode,
                "synchronous": "NORMAL",
            },
        )

    async def connect(self) -> None:
        """Establish SQLite connection."""
        try:
            # Mock connection for now
            self._connection = f"sqlite_connection_{id(self)}"
            self.is_connected = True

            # Apply PRAGMA settings
            for pragma, value in self.pragmas.items():
                logger.debug(f"Setting PRAGMA {pragma} = {value}")

            logger.info(f"Connected to SQLite database: {self.database_path}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to SQLite: {e}")

    async def disconnect(self) -> None:
        """Close SQLite connection."""
        if self._connection:
            self._connection = None
            self.is_connected = False
            logger.info("Disconnected from SQLite")

    async def execute_query(self, query: str, params: List[Any] = None) -> List[Dict]:
        """Execute SQLite query."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        try:
            # SQLite uses ? parameters (no conversion needed)
            sqlite_query, sqlite_params = self.format_query(query, params)

            # Mock execution for now
            logger.debug(
                f"Executing query: {sqlite_query} with params: {sqlite_params}"
            )

            # Return mock results
            return [{"result": "success", "rows_affected": 1}]
        except Exception as e:
            raise QueryError(f"Query execution failed: {e}")

    async def execute_transaction(
        self, queries: List[Tuple[str, List[Any]]]
    ) -> List[Any]:
        """Execute multiple queries in SQLite transaction."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        try:
            results = []
            logger.debug(f"Starting transaction with {len(queries)} queries")

            for query, params in queries:
                result = await self.execute_query(query, params)
                results.append(result)

            logger.debug("Transaction completed successfully")
            return results
        except Exception as e:
            logger.error(f"Transaction failed: {e}")
            raise TransactionError(f"Transaction failed: {e}")

    async def get_table_schema(self, table_name: str) -> Dict[str, Dict]:
        """Get SQLite table schema."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        # Mock schema information
        return {
            "id": {"type": "integer", "nullable": False, "primary_key": True},
            "name": {"type": "text", "nullable": True},
            "created_at": {
                "type": "timestamp",
                "nullable": False,
                "default": "CURRENT_TIMESTAMP",
            },
        }

    async def create_table(self, table_name: str, schema: Dict[str, Dict]) -> None:
        """Create SQLite table."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        # Mock table creation
        logger.info(f"Creating table: {table_name}")

    async def drop_table(self, table_name: str) -> None:
        """Drop SQLite table."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        # Mock table drop
        logger.info(f"Dropping table: {table_name}")

    def get_dialect(self) -> str:
        """Get SQLite dialect."""
        return "sqlite"

    def supports_feature(self, feature: str) -> bool:
        """Check SQLite feature support."""
        sqlite_features = {
            "json": True,  # SQLite 3.38+
            "arrays": False,
            "regex": False,  # Requires extension
            "window_functions": True,  # SQLite 3.25+
            "cte": True,
            "upsert": True,  # INSERT ... ON CONFLICT
            "fts": True,  # Full-text search
            "fulltext_search": True,
            "spatial_indexes": False,  # Requires extension
            "hstore": False,  # PostgreSQL-specific
            "mysql_specific": False,
            "sqlite_specific": True,
        }
        return sqlite_features.get(feature, False)

    def format_query(
        self, query: str, params: List[Any] = None
    ) -> Tuple[str, List[Any]]:
        """Format query for SQLite parameter style (? - no conversion needed)."""
        if params is None:
            params = []

        # SQLite uses ? parameters, so no conversion needed
        return query, params

    def get_affinity(self, column_type: str) -> str:
        """Get SQLite type affinity for column type."""
        column_type = column_type.upper()

        # SQLite type affinity rules
        if "INT" in column_type:
            return "integer"
        elif any(text_type in column_type for text_type in ["CHAR", "TEXT", "CLOB"]):
            return "text"
        elif "BLOB" in column_type:
            return "blob"
        elif any(real_type in column_type for real_type in ["REAL", "FLOA", "DOUB"]):
            return "real"
        else:
            return "numeric"

    @property
    def supports_concurrent_reads(self) -> bool:
        """SQLite supports concurrent reads better with WAL mode."""
        return self.journal_mode == "WAL"

    @property
    def supports_savepoints(self) -> bool:
        """SQLite supports savepoints."""
        return True
