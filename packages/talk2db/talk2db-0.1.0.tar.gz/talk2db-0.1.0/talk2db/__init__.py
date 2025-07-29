"""PyQL - Natural Language Query Interface for CQL and SQL."""

from .core import (
    PyQL,
    QueryResult,
    QueryType,
    LLMProvider,
    Neo4jConfig,
    DatabaseConfig,
    create_pyql_openai,
    create_pyql_google,
    PyQLError,
    ConfigurationError,
    QueryGenerationError,
    DatabaseConnectionError,
)


__version__ = "0.1.0"
__all__ = [
    "PyQL",
    "QueryResult",
    "QueryType",
    "LLMProvider",
    "Neo4jConfig",
    "DatabaseConfig",
    "create_pyql_openai",
    "create_pyql_google",
    "PyQLError",
    "ConfigurationError",
    "QueryGenerationError",
    "DatabaseConnectionError",
]
