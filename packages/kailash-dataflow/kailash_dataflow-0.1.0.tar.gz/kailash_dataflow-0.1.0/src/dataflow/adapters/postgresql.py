"""
PostgreSQL Database Adapter

PostgreSQL-specific database adapter implementation.
"""

import logging
from typing import Any, Dict, List, Tuple

from .base import DatabaseAdapter
from .exceptions import AdapterError, ConnectionError, QueryError

logger = logging.getLogger(__name__)


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter."""

    @property
    def database_type(self) -> str:
        return "postgresql"

    @property
    def default_port(self) -> int:
        return 5432

    def __init__(self, connection_string: str, **kwargs):
        super().__init__(connection_string, **kwargs)

        # PostgreSQL-specific configuration
        self.ssl_mode = self.query_params.get("sslmode", "prefer")
        self.application_name = kwargs.get("application_name", "dataflow")

        # Use actual port or default
        if self.port is None:
            self.port = self.default_port

    async def connect(self) -> None:
        """Establish PostgreSQL connection."""
        try:
            # Mock connection for now
            self._connection = f"postgresql_connection_{id(self)}"
            self.is_connected = True
            logger.info(f"Connected to PostgreSQL at {self.host}:{self.port}")
        except Exception as e:
            raise ConnectionError(f"Failed to connect to PostgreSQL: {e}")

    async def disconnect(self) -> None:
        """Close PostgreSQL connection."""
        if self._connection:
            self._connection = None
            self.is_connected = False
            logger.info("Disconnected from PostgreSQL")

    async def execute_query(self, query: str, params: List[Any] = None) -> List[Dict]:
        """Execute PostgreSQL query."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        try:
            # Format query for PostgreSQL parameter style
            pg_query, pg_params = self.format_query(query, params)

            # Mock execution for now
            logger.debug(f"Executing query: {pg_query} with params: {pg_params}")

            # Return mock results
            return [{"result": "success", "rows_affected": 1}]
        except Exception as e:
            raise QueryError(f"Query execution failed: {e}")

    async def execute_transaction(
        self, queries: List[Tuple[str, List[Any]]]
    ) -> List[Any]:
        """Execute multiple queries in PostgreSQL transaction."""
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
        """Get PostgreSQL table schema."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        # Mock schema information
        return {
            "id": {"type": "integer", "nullable": False, "primary_key": True},
            "name": {"type": "varchar", "nullable": True, "max_length": 255},
            "created_at": {"type": "timestamp", "nullable": False, "default": "NOW()"},
        }

    async def create_table(self, table_name: str, schema: Dict[str, Dict]) -> None:
        """Create PostgreSQL table."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        # Mock table creation
        logger.info(f"Creating table: {table_name}")

    async def drop_table(self, table_name: str) -> None:
        """Drop PostgreSQL table."""
        if not self.is_connected:
            raise ConnectionError("Not connected to database")

        # Mock table drop
        logger.info(f"Dropping table: {table_name}")

    def get_dialect(self) -> str:
        """Get PostgreSQL dialect."""
        return "postgresql"

    def supports_feature(self, feature: str) -> bool:
        """Check PostgreSQL feature support."""
        postgresql_features = {
            "json": True,
            "arrays": True,
            "regex": True,
            "window_functions": True,
            "cte": True,
            "upsert": True,
            "hstore": True,
            "fulltext_search": True,
            "spatial_indexes": True,
            "mysql_specific": False,
            "sqlite_specific": False,
        }
        return postgresql_features.get(feature, False)

    def format_query(
        self, query: str, params: List[Any] = None
    ) -> Tuple[str, List[Any]]:
        """Format query for PostgreSQL parameter style ($1, $2, etc.)."""
        if params is None:
            params = []

        # Convert ? placeholders to $1, $2, etc.
        formatted_query = query
        param_count = 1

        while "?" in formatted_query:
            formatted_query = formatted_query.replace("?", f"${param_count}", 1)
            param_count += 1

        return formatted_query, params

    @property
    def supports_savepoints(self) -> bool:
        """PostgreSQL supports savepoints."""
        return True
