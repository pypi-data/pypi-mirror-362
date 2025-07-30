"""
Connection String Parser

Utilities for parsing database connection strings.
"""

import logging
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from .exceptions import AdapterError

logger = logging.getLogger(__name__)


class ConnectionParser:
    """Parser for database connection strings."""

    @staticmethod
    def parse_connection_string(connection_string: str) -> Dict[str, Any]:
        """
        Parse database connection string into components.

        Args:
            connection_string: Database connection string

        Returns:
            Dictionary with connection components

        Raises:
            AdapterError: If connection string is invalid
        """
        try:
            parsed = urlparse(connection_string)

            # Basic components
            components = {
                "scheme": parsed.scheme,
                "host": parsed.hostname,
                "port": parsed.port,
                "database": parsed.path.lstrip("/") if parsed.path else None,
                "username": parsed.username,
                "password": parsed.password,
                "query_params": {},
            }

            # Parse query parameters
            if parsed.query:
                components["query_params"] = {
                    key: value[0] if len(value) == 1 else value
                    for key, value in parse_qs(parsed.query).items()
                }

            return components

        except Exception as e:
            raise AdapterError(f"Invalid connection string: {e}")

    @staticmethod
    def validate_postgresql_connection(components: Dict[str, Any]) -> None:
        """
        Validate PostgreSQL connection components.

        Args:
            components: Connection components from parse_connection_string

        Raises:
            AdapterError: If connection components are invalid
        """
        if not components.get("host"):
            raise AdapterError("PostgreSQL connection requires host")

        if not components.get("database"):
            raise AdapterError("PostgreSQL connection requires database name")

        # Validate SSL mode
        ssl_mode = components.get("query_params", {}).get("sslmode")
        if ssl_mode and ssl_mode not in [
            "disable",
            "allow",
            "prefer",
            "require",
            "verify-ca",
            "verify-full",
        ]:
            raise AdapterError(f"Invalid SSL mode: {ssl_mode}")

        # Validate port
        port = components.get("port")
        if port is not None and (port < 1 or port > 65535):
            raise AdapterError(f"Invalid port: {port}")

    @staticmethod
    def validate_mysql_connection(components: Dict[str, Any]) -> None:
        """
        Validate MySQL connection components.

        Args:
            components: Connection components from parse_connection_string

        Raises:
            AdapterError: If connection components are invalid
        """
        if not components.get("host"):
            raise AdapterError("MySQL connection requires host")

        if not components.get("database"):
            raise AdapterError("MySQL connection requires database name")

        # Validate charset
        charset = components.get("query_params", {}).get("charset")
        if charset and charset not in ["utf8", "utf8mb4", "latin1"]:
            logger.warning(f"Non-standard charset: {charset}")

        # Validate port
        port = components.get("port")
        if port is not None and (port < 1 or port > 65535):
            raise AdapterError(f"Invalid port: {port}")

    @staticmethod
    def validate_sqlite_connection(components: Dict[str, Any]) -> None:
        """
        Validate SQLite connection components.

        Args:
            components: Connection components from parse_connection_string

        Raises:
            AdapterError: If connection components are invalid
        """
        # For SQLite, the path is the database file
        if components.get("host") and components.get("host") != "":
            raise AdapterError("SQLite connection should not specify host")

        if components.get("port"):
            raise AdapterError("SQLite connection should not specify port")

        # Database path is required (can be :memory: for in-memory)
        if not components.get("database"):
            raise AdapterError("SQLite connection requires database path")

    @staticmethod
    def extract_connection_parameters(connection_string: str) -> Dict[str, Any]:
        """
        Extract connection parameters from connection string.

        Args:
            connection_string: Database connection string

        Returns:
            Dictionary with extracted parameters
        """
        components = ConnectionParser.parse_connection_string(connection_string)

        # Extract standard parameters
        params = {
            "host": components.get("host"),
            "port": components.get("port"),
            "database": components.get("database"),
            "username": components.get("username"),
            "password": components.get("password"),
        }

        # Add query parameters
        params.update(components.get("query_params", {}))

        # Remove None values
        return {k: v for k, v in params.items() if v is not None}

    @staticmethod
    def build_connection_string(
        scheme: str,
        host: str,
        database: str,
        username: str = None,
        password: str = None,
        port: int = None,
        **params,
    ) -> str:
        """
        Build connection string from components.

        Args:
            scheme: Database scheme (postgresql, mysql, sqlite)
            host: Database host
            database: Database name
            username: Username (optional)
            password: Password (optional)
            port: Port (optional)
            **params: Additional query parameters

        Returns:
            Connection string
        """
        # Build base URL
        if scheme == "sqlite":
            # SQLite format: sqlite:///path/to/db.sqlite
            return f"sqlite:///{database}"

        # Build authority part
        authority = ""
        if username:
            authority = username
            if password:
                authority += f":{password}"
            authority += "@"

        authority += host

        if port:
            authority += f":{port}"

        # Build full URL
        url = f"{scheme}://{authority}/{database}"

        # Add query parameters
        if params:
            query_parts = []
            for key, value in params.items():
                if isinstance(value, list):
                    for v in value:
                        query_parts.append(f"{key}={v}")
                else:
                    query_parts.append(f"{key}={value}")

            if query_parts:
                url += "?" + "&".join(query_parts)

        return url
