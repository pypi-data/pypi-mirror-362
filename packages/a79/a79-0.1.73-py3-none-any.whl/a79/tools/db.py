from typing import Any

from ..client import A79Client
from ..models.tools import DEFAULT
from ..models.tools.db_models import (
    DatabaseCredentials,
    DatabaseHierarchy,
    DatabaseSelection,
    DatabaseSourceInput,
    Enum,
    ExecuteSQLInput,
    ExecuteSQLOutput,
    ListDatabasesInput,
    ListDatabasesOutput,
    ListSchemasInput,
    ListSchemasOutput,
    ListTablesInput,
    ListTablesOutput,
    NLToSQLInput,
    NLToSQLOutput,
    SchemaSelection,
    SearchTablesInput,
    SearchTablesOutput,
    SourceSelectionInput,
    SourceSelectionOutput,
    SQADatabaseConfig,
    SqlDialect,
    SqlType,
)

__all__ = [
    "DatabaseCredentials",
    "DatabaseHierarchy",
    "DatabaseSelection",
    "DatabaseSourceInput",
    "Enum",
    "ExecuteSQLInput",
    "ExecuteSQLOutput",
    "ListDatabasesInput",
    "ListDatabasesOutput",
    "ListSchemasInput",
    "ListSchemasOutput",
    "ListTablesInput",
    "ListTablesOutput",
    "NLToSQLInput",
    "NLToSQLOutput",
    "SQADatabaseConfig",
    "SchemaSelection",
    "SearchTablesInput",
    "SearchTablesOutput",
    "SourceSelectionInput",
    "SourceSelectionOutput",
    "SqlDialect",
    "SqlType",
    "generate_sql",
    "execute_sql",
    "list_databases",
    "list_schemas",
    "list_tables",
    "search_tables",
]


def generate_sql(
    *,
    connector_name: str | None = DEFAULT,
    files: list[str] | None = DEFAULT,
    query: str,
    num_tables_to_filter_for_sql_generation: int = DEFAULT,
    sample_rows: dict[str, list[dict[str, Any]]] | None = DEFAULT,
) -> NLToSQLOutput:
    """
    Convert natural language queries to SQL with automatic table selection.

    This tool combines table selection and SQL generation into a single step:
    1. Analyzes your query to select the most relevant tables
    2. Generates optimized SQL using the selected tables
    3. Converts to the appropriate SQL dialect for your database
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = NLToSQLInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="db", name="generate_sql", input=input_model.model_dump()
    )
    return NLToSQLOutput.model_validate(output_model)


def execute_sql(
    *,
    connector_name: str | None = DEFAULT,
    files: list[str] | None = DEFAULT,
    sql_query: str,
    database_name: str | None = DEFAULT,
    page: int = DEFAULT,
    max_rows_per_page: int = DEFAULT,
) -> ExecuteSQLOutput:
    """
    Execute a SQL query with automatic result capping and pagination support.

    This tool executes raw SQL queries against your database and returns the results
    in a format that can be easily converted to a pandas DataFrame. It supports all
    standard SQL operations including SELECT, JOIN, GROUP BY, etc.

    The results are automatically capped to prevent accidentally loading huge datasets.
    Pagination is handled through page numbers, with each page containing up to
    max_rows_per_page results (default 100, max 1000).

    If your SQL query already contains LIMIT/OFFSET clauses, those will be respected
    and the pagination parameters will be ignored.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = ExecuteSQLInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="db", name="execute_sql", input=input_model.model_dump()
    )
    return ExecuteSQLOutput.model_validate(output_model)


def list_databases(
    *, connector_name: str | None = DEFAULT, files: list[str] | None = DEFAULT
) -> ListDatabasesOutput:
    """
    List all available databases from the specified connector.

    This tool returns a list of all databases accessible through the connector,
    useful for database discovery and exploration.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = ListDatabasesInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="db", name="list_databases", input=input_model.model_dump()
    )
    return ListDatabasesOutput.model_validate(output_model)


def list_schemas(
    *,
    connector_name: str | None = DEFAULT,
    files: list[str] | None = DEFAULT,
    database_name: str,
) -> ListSchemasOutput:
    """
    List all schemas in the specified database.

    This tool returns a list of all schemas within a database, helpful for
    understanding the database structure and organization.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = ListSchemasInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="db", name="list_schemas", input=input_model.model_dump()
    )
    return ListSchemasOutput.model_validate(output_model)


def list_tables(
    *,
    connector_name: str | None = DEFAULT,
    files: list[str] | None = DEFAULT,
    database_name: str,
    schema_name: str,
) -> ListTablesOutput:
    """
    List all tables in the specified schema of a database.

    This tool returns a list of all tables within a schema, useful for
    exploring the data structure and finding specific tables.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = ListTablesInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="db", name="list_tables", input=input_model.model_dump()
    )
    return ListTablesOutput.model_validate(output_model)


def search_tables(
    *,
    connector_name: str | None = DEFAULT,
    files: list[str] | None = DEFAULT,
    query: str,
    num_tables: int = DEFAULT,
) -> SearchTablesOutput:
    """
    Search for relevant tables using natural language queries.

    This tool uses semantic search to find tables that match your query,
    returning the most relevant tables with scores and explanations.
    It's particularly useful when you don't know the exact table names
    but know what kind of data you're looking for.
    """
    kwargs = locals()
    kwargs = {k: v for k, v in kwargs.items() if v is not DEFAULT}
    input_model = SearchTablesInput.model_validate(kwargs)

    client = A79Client()
    output_model = client.execute_tool(
        package="db", name="search_tables", input=input_model.model_dump()
    )
    return SearchTablesOutput.model_validate(output_model)
