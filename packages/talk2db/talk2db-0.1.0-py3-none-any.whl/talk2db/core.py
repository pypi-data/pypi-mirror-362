"""
PyQL - Natural Language Query Interface for CQL and SQL
A Python library that converts natural language queries to Cypher (CQL) and SQL
"""

import os
import json
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
from enum import Enum
import logging

try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_openai import ChatOpenAI
    from langchain.schema import BaseMessage, HumanMessage, SystemMessage

    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

try:
    import neo4j

    NEO4J_AVAILABLE = True
except ImportError:
    NEO4J_AVAILABLE = False

try:
    import psycopg2

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class QueryType(Enum):
    CYPHER = "cypher"
    SQL = "sql"


class LLMProvider(Enum):
    OPENAI = "openai"
    GOOGLE = "google"


@dataclass
class DatabaseConfig:
    """Configuration for database connections"""

    host: str
    port: int
    database: str
    username: str
    password: str

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> "DatabaseConfig":
        return cls(**config)


@dataclass
class Neo4jConfig(DatabaseConfig):
    """Neo4j specific configuration"""

    uri: str = None

    def __post_init__(self):
        if not self.uri:
            self.uri = f"bolt://{self.host}:{self.port}"


@dataclass
class QueryResult:
    """Result of a query execution"""

    query: str
    natural_language: str
    query_type: QueryType
    results: List[Dict[str, Any]]
    execution_time: float
    error: Optional[str] = None


class PyQLError(Exception):
    """Base exception for PyQL library"""

    def __init__(self, message: str):
        super().__init__(message)
        logging.error(f"PyQLError: {message}")


class QueryExecutionError(PyQLError):
    """Raised when query execution fails"""

    def __init__(self, message: str):
        super().__init__(message)
        logging.error(f"QueryExecutionError: {message}")


class ConfigurationError(PyQLError):
    """Raised when configuration is invalid"""

    def __init__(self, message: str):
        super().__init__(message)
        logging.error(f"ConfigurationError: {message}")


class QueryGenerationError(PyQLError):
    """Raised when query generation fails"""

    def __init__(self, message: str):
        super().__init__(message)
        logging.error(f"QueryGenerationError: {message}")


class DatabaseConnectionError(PyQLError):
    """Raised when database connection fails"""

    def __init__(self, message: str):
        super().__init__(message)
        logging.error(f"DatabaseConnectionError: {message}")


class QueryExecutor:
    """Base class for query executors"""

    def __init__(self, config: DatabaseConfig):
        self.config = config
        self.connection = None

    def connect(self):
        """Establish database connection"""
        raise NotImplementedError

    def execute(self, query: str) -> List[Dict[str, Any]]:
        """Execute query and return results"""
        raise NotImplementedError

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()


class Neo4jExecutor(QueryExecutor):
    """Neo4j query executor"""

    def __init__(self, config: Neo4jConfig):
        if not NEO4J_AVAILABLE:
            raise ImportError("neo4j package is required for Neo4j support")
        super().__init__(config)

    def connect(self):
        """Connect to Neo4j database"""
        try:
            self.driver = neo4j.GraphDatabase.driver(
                self.config.uri, auth=(self.config.username, self.config.password)
            )
            # Test connection
            with self.driver.session() as session:
                session.run("RETURN 1")
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to connect to Neo4j: {e}")

    def execute(self, query: str) -> List[Dict[str, Any]]:
        """Execute Cypher query"""
        if not self.driver:
            self.connect()

        try:
            with self.driver.session() as session:
                result = session.run(query)
                return [record.data() for record in result]
        except Exception as e:
            raise QueryExecutionError(f"Query execution failed: {e}")

    def close(self):
        """Close Neo4j connection"""
        if hasattr(self, "driver") and self.driver:
            self.driver.close()


class PostgresExecutor(QueryExecutor):
    """PostgreSQL query executor"""

    def __init__(self, config: DatabaseConfig):
        if not POSTGRES_AVAILABLE:
            raise ImportError("psycopg2 package is required for PostgreSQL support")
        super().__init__(config)

    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.username,
                password=self.config.password,
            )
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to connect to PostgreSQL: {e}")

    def execute(self, query: str) -> List[Dict[str, Any]]:
        """Execute SQL query"""
        if not self.connection:
            self.connect()

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                return [dict(zip(columns, row)) for row in results]
        except Exception as e:
            raise QueryExecutionError(f"Query execution failed: {e}")


class QueryGenerator:
    """Generates database queries from natural language"""

    def __init__(self, provider: LLMProvider, api_key: str, model: str = None):
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("langchain packages are required")

        self.provider = provider
        self.api_key = api_key

        if provider == LLMProvider.OPENAI:
            self.llm = ChatOpenAI(api_key=api_key, model=model or "gpt-3.5-turbo")
        elif provider == LLMProvider.GOOGLE:
            self.llm = ChatGoogleGenerativeAI(
                google_api_key=api_key, model=model or "gemini-pro"
            )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def generate_cypher(self, natural_query: str, schema_info: str = "") -> str:
        """Generate Cypher query from natural language"""
        system_prompt = f"""
        You are an expert Neo4j Cypher query generator. Convert natural language queries to Cypher.
        
        Schema Information:
        {schema_info}
        
        Rules:
        1. Only return the Cypher query, no explanations
        2. Use proper Cypher syntax
        3. Handle relationships and properties correctly
        4. Use MATCH, WHERE, RETURN appropriately
        5. For time-based queries, use datetime functions
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Convert this to Cypher: {natural_query}"),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            raise QueryGenerationError(f"Failed to generate Cypher query: {e}")

    def generate_sql(self, natural_query: str, schema_info: str = "") -> str:
        """Generate SQL query from natural language"""
        system_prompt = f"""
        You are an expert SQL query generator. Convert natural language queries to SQL.
        
        Schema Information:
        {schema_info}
        
        Rules:
        1. Only return the SQL query, no explanations
        2. Use proper SQL syntax
        3. Handle JOINs, WHERE clauses, and aggregations correctly
        4. Use appropriate date/time functions
        5. Consider PostgreSQL-specific functions if needed
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Convert this to SQL: {natural_query}"),
        ]

        try:
            response = self.llm.invoke(messages)
            return response.content.strip()
        except Exception as e:
            raise QueryGenerationError(f"Failed to generate SQL query: {e}")


class PyQL:
    """Main PyQL interface"""

    def __init__(self, llm_provider: LLMProvider, api_key: str, model: str = None):
        """
        Initialize PyQL with LLM configuration

        Args:
            llm_provider: LLM provider (openai or google)
            api_key: API key for the LLM provider
            model: Model name (optional)
        """
        self.query_generator = QueryGenerator(llm_provider, api_key, model)
        self.executors = {}
        self.schemas = {}

    def add_neo4j(self, name: str, config: Neo4jConfig, schema: str = ""):
        """Add Neo4j database connection"""
        self.executors[name] = Neo4jExecutor(config)
        self.schemas[name] = schema

    def add_postgres(self, name: str, config: DatabaseConfig, schema: str = ""):
        """Add PostgreSQL database connection"""
        self.executors[name] = PostgresExecutor(config)
        self.schemas[name] = schema

    def query(
        self, natural_query: str, database: str, query_type: QueryType = None
    ) -> QueryResult:
        """
        Execute natural language query

        Args:
            natural_query: Natural language query
            database: Database name (as added to PyQL)
            query_type: Force query type (optional)

        Returns:
            QueryResult with query and results
        """
        if database not in self.executors:
            raise ValueError(f"Database '{database}' not configured")

        executor = self.executors[database]
        schema_info = self.schemas.get(database, "")

        # Auto-detect query type if not specified
        if query_type is None:
            if isinstance(executor, Neo4jExecutor):
                query_type = QueryType.CYPHER
            else:
                query_type = QueryType.SQL

        # Generate query
        if query_type == QueryType.CYPHER:
            generated_query = self.query_generator.generate_cypher(
                natural_query, schema_info
            )
        else:
            generated_query = self.query_generator.generate_sql(
                natural_query, schema_info
            )

        # Execute query
        import time

        start_time = time.time()

        try:
            results = executor.execute(generated_query)
            execution_time = time.time() - start_time

            return QueryResult(
                query=generated_query,
                natural_language=natural_query,
                query_type=query_type,
                results=results,
                execution_time=execution_time,
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return QueryResult(
                query=generated_query,
                natural_language=natural_query,
                query_type=query_type,
                results=[],
                execution_time=execution_time,
                error=str(e),
            )

    def close_all(self):
        """Close all database connections"""
        for executor in self.executors.values():
            executor.close()


# Convenience functions for quick setup
def create_pyql_openai(api_key: str = None, model: str = "gpt-3.5-turbo") -> PyQL:
    """Create PyQL instance with OpenAI"""
    if not api_key:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ConfigurationError("OpenAI API key required")

    return PyQL(LLMProvider.OPENAI, api_key, model)


def create_pyql_google(api_key: str = None, model: str = "gemini-pro") -> PyQL:
    """Create PyQL instance with Google Generative AI"""
    if not api_key:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ConfigurationError("Google API key required")

    return PyQL(LLMProvider.GOOGLE, api_key, model)


# # Example usage
# if __name__ == "__main__":
#     # Example configuration
#     pyql = create_pyql_openai()

#     # Add Neo4j database
#     neo4j_config = Neo4jConfig(
#         host="localhost",
#         port=7687,
#         database="neo4j",
#         username="neo4j",
#         password="password",
#     )

#     pyql.add_neo4j(
#         "social_network",
#         neo4j_config,
#         schema="Nodes: User(name, email, created_at), Post(title, content, created_at)",
#     )

#     # Add PostgreSQL database
#     postgres_config = DatabaseConfig(
#         host="localhost",
#         port=5432,
#         database="ecommerce",
#         username="postgres",
#         password="password",
#     )

#     pyql.add_postgres(
#         "ecommerce",
#         postgres_config,
#         schema="Tables: users(id, name, email, created_at), orders(id, user_id, total, created_at)",
#     )

#     # Execute queries
#     try:
#         # Neo4j query
#         result = pyql.query(
#             "Show me all users who created posts last month", "social_network"
#         )
#         print(f"Generated Cypher: {result.query}")
#         print(f"Results: {result.results}")

#         # PostgreSQL query
#         result = pyql.query(
#             "Show me all users who signed up last month and have premium accounts",
#             "ecommerce",
#         )
#         print(f"Generated SQL: {result.query}")
#         print(f"Results: {result.results}")

#     finally:
#         pyql.close_all()
