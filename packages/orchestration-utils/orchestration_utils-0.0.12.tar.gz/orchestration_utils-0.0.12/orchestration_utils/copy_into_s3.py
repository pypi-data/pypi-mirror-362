import time

from snowflake.connector.errors import Error
from . import etl_operations

from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, field

from prefect import get_run_logger


@dataclass
class CopyIntoResult:
    """
    Class to hold the result of a copy operation.
    Args:
        success (bool): Indicates if the copy operation was successful.
        message (str): Message detailing the result of the operation.
        file_name (Optional[str]): Name of the file being processed.
        status (Optional[str]): Status of the copy operation.
        rows_parsed (Optional[int]): Number of rows parsed from the file.
        rows_loaded (Optional[int]): Number of rows loaded into the table.
        data (Optional[List[Tuple]]): Optional data returned from the copy operation.
    """

    success: bool
    message: str
    file_name: Optional[str] = None
    status: Optional[str] = None
    rows_parsed: Optional[int] = 0
    rows_loaded: Optional[int] = 0
    data: Optional[List[Tuple]] = None


@dataclass
class CopyIntoTable:
    """
    Class to copy data from S3 into a Snowflake table.
    Args:
        db (str): Name of the database.
        schema_name (str): Name of the schema.
        table_name (str): Name of the table to copy data into.
        stage_name (str): Name of the Snowflake stage. This is equivalent to the s3 bucket name.
        pattern (str): Pattern to match files in the stage.
        file_format (str): Name of the file format in Snowflake.
        stage_suffix (Optional[str]): Suffix for the stage, defaults to an empty string. This is equivalent to the s3 prefix.
        on_error (Optional[str]): Error handling strategy for the copy operation, defaults to "ABORT_STATEMENT".
        environment (str): Environment name, defaults to "dev". Set to "prod" for production.
    """

    db: str
    schema_name: str
    table_name: str
    stage_name: str
    pattern: str
    file_format: str
    stage_suffix: Optional[str] = ""
    on_error: Optional[str] = "ABORT_STATEMENT"
    environment: str = "dev"

    # Computed fields
    db_name: str = field(init=False)
    snowflake_dest: object = field(init=False)
    schema_handler: object = field(init=False)
    logger: object = field(init=False)

    def __post_init__(self):
        self.db_name = (
            self.db if self.environment == "prod" else f"{self.db}_{self.environment}"
        )
        self.snowflake_dest = etl_operations.SnowflakeDestination(database=self.db, environment=self.environment)
        self.schema_handler = etl_operations.SchemaDriftHandler(environment=self.environment)
        self.snowflake_operations = etl_operations.SnowflakeOperations()
        self.logger = get_run_logger()
        self._check_if_stage_exists()

    def _check_if_stage_exists(self):
        """Check if the target stage exists."""
        stage_query = f"""
            show stages like '{self.stage_name}'
            in schema {self.db_name}.{self.schema_name}
            ;
        """
        stage_result = self.snowflake_operations.execute_query(sql=stage_query)
        stage_response = stage_result.fetchall()
        current_role = self.snowflake_operations.check_current_role()
        if stage_response:
            stage_name = stage_response[0]["name"]
            if stage_name.lower() == self.stage_name.lower():
                return
        raise Error(
            f"Stage '{self.stage_name}' does not exist in schema '{self.db_name}.{self.schema_name}' or Maybe the current role {current_role} does not have read access to the stage."
        )

    def check_if_table_exists(self) -> bool:
        """Check if the target table exists."""
        details = {
            "database": self.db_name,
            "schema": self.schema_name,
            "table_name": self.table_name,
        }
        return self.snowflake_dest._check_if_table_exists(details=details)

    def _build_infer_schema_query(self, query_type: str) -> str:
        """Build infer schema query based on type."""
        base_location = f"@{self.db_name}.{self.schema_name}.{self.stage_name}/{self.stage_suffix}"
        base_format = f"'{self.db_name}.{self.schema_name}.{self.file_format}'"

        query_templates = {
            "expressions": f"""\n
                with inferred_schema as (
                    select
                        column_name,
                        expression
                    from table(
                        infer_schema(
                            location=>'{base_location}',
                            file_format=>{base_format}
                        )
                    )
                ),
                list_agg as (
                    select
                        listagg(expression, ',\\n\\t\\t\\t') within group (order by column_name) as expressions
                    from inferred_schema
                )
                select
                    nullif(expressions, '') as expressions
                from list_agg
            ;
            """,
            "columns_and_types": f"""\n
                with inferred_schema as (
                    select
                        column_name,
                        upper(column_name) || ' ' || type as column_and_type
                    from table(
                        infer_schema(
                            location=>'{base_location}',
                            file_format=>{base_format}
                        )
                    )
                ),
                list_agg as (
                    select
                        listagg(column_and_type, ',\\n\\t\\t') within group (order by column_name) as columns_and_types
                    from inferred_schema
                )
                select
                    nullif(columns_and_types, '') as columns_and_types
                from list_agg
            ;
            """,
            "expressions_if_table_exists": f"""\n
                    with inferred_schema as (
                        select
                            column_name,
                            expression
                        from table(
                            infer_schema(
                                location=>'{base_location}',
                                file_format=>{base_format}
                            )
                        )
                    ),
                    column_and_datatypes as (
                        select
                            column_name,
                            ordinal_position
                        from {self.db_name}.information_schema.columns
                        where lower(table_schema) = '{self.schema_name}'
                        and lower(table_name) = '{self.table_name}'
                    ),
                    expressions as (
                        select 
                            case
                                when infer.expression is null and cnd.column_name = '_RECORD_ID'
                                    then 'uuid_string() as _record_id'
                                when infer.expression is null and cnd.column_name = '_FILE_NAME'
                                    then 'metadata$filename as _file_name'
                                when infer.expression is null and cnd.column_name = '_FILE_ROW_NUMBER'
                                    then 'metadata$file_row_number as _file_row_number'
                                when infer.expression is null and cnd.column_name = '_FILE_CONTENT_KEY'
                                    then 'metadata$file_content_key as _file_content_key'
                                when infer.expression is null and cnd.column_name = '_FILE_LAST_MODIFIED_AT'
                                    then 'metadata$file_last_modified as _file_last_modified'
                                when infer.expression is null and cnd.column_name = '_RECORD_LOADED_AT'
                                    then 'metadata$start_scan_time as _record_loaded_at'
                                when infer.expression is null and infer.column_name is null
                                    then 'null as ' || lower(cnd.column_name)
                                else infer.expression
                            end as expression,
                            ordinal_position
                        from column_and_datatypes as cnd
                        left join inferred_schema as infer
                            on upper(cnd.column_name) = upper(infer.column_name)
                        order by ordinal_position
                    )
                    select
                        listagg(expression, ',\\n\\t\\t\\t') within group (order by ordinal_position) as expressions
                    from expressions
                    ;
            """
        }
        return query_templates.get(query_type, "")

    def execute_query(self, query: str) -> List:
        """Execute a query and return results."""
        try:
            response = self.snowflake_dest.query(sql=query)
            return response.fetchall()
        except Exception as e:
            self.logger.error(f"Query execution failed: {e}")
            raise

    def execute_infer_schema(self, query: str) -> str:
        """Execute infer schema query and return the first result."""
        response = self.execute_query(query)
        return response[0][0] if response and len(response) > 0 else ""

    def get_schema_info(self) -> Tuple[str, str]:
        """Get column expressions and column definitions from inferred schema."""
        expressions_query = self._build_infer_schema_query("expressions")
        columns_types_query = self._build_infer_schema_query("columns_and_types")

        column_expressions = self.execute_infer_schema(expressions_query)
        columns_and_types = self.execute_infer_schema(columns_types_query)
        if not column_expressions or not columns_and_types:
            return (None, None)
        return column_expressions, columns_and_types

    def get_schema_info_if_table_exists(self) -> str:
        """Get column expressions for existing table."""
        expressions_query = self._build_infer_schema_query("expressions_if_table_exists")
        column_expressions = self.execute_infer_schema(expressions_query)
        return column_expressions

    def generate_create_table_statement(self, columns_and_data_types: str) -> str:
        """Generate CREATE TABLE statement."""
        return f"""
            create table if not exists {self.db_name}.{self.schema_name}.{self.table_name} (
                {columns_and_data_types},
                _record_id varchar comment 'Unique identifier for the record, uses uuid_string() while loading data',
                _file_name varchar comment 'Name of the staged data file the current row belongs to. Includes the full path to the data file.',
                _file_row_number integer comment 'Row number for each record in the staged data file.',
                _file_content_key varchar comment 'Checksum of the staged data file the current row belongs to.',
                _file_last_modified_at timestamp_ntz comment 'Last modified timestamp of the staged data file the current row belongs to. Returned as TIMESTAMP_NTZ.',
                _record_loaded_at timestamp_ltz comment 'Start timestamp of operation for each record in the staged data file. Returned as TIMESTAMP_LTZ. This is the time when the record was loaded into the table.'
            );
        """

    def generate_copy_into_statement(self, columns_expression: str, force: bool) -> str:
        """Generate COPY INTO statement."""
        return f"""
            copy into {self.db_name}.{self.schema_name}.{self.table_name}
                from (
                    select
                        {columns_expression},
                        -- metadata --
                        uuid_string() as _record_id,
                        metadata$filename as _file_name,
                        metadata$file_row_number as _file_row_number,
                        metadata$file_content_key as _file_content_key,
                        metadata$file_last_modified as _file_last_modified_at,
                        metadata$start_scan_time as _record_loaded_at
                    from @{self.db_name}.{self.schema_name}.{self.stage_name}/{self.stage_suffix}
                )
            pattern = '{self.pattern}'
            file_format = {self.db_name}.{self.schema_name}.{self.file_format}
            on_error = {self.on_error}
            force = {force};
        """

    def generate_copy_into_statement_if_table_exists(self, columns_expression: str, force: bool) -> str:
        """Generate COPY INTO statement for existing table."""
        return f"""
            copy into {self.db_name}.{self.schema_name}.{self.table_name}
                from (
                    select
                        {columns_expression}
                    from @{self.db_name}.{self.schema_name}.{self.stage_name}/{self.stage_suffix}
                )
            pattern = '{self.pattern}'
            file_format = {self.db_name}.{self.schema_name}.{self.file_format}
            on_error = {self.on_error}
            force = {force}
        ;
        """

    def _cleanup_failed_table(self):
        """Drop table if copy operation fails."""
        drop_query = f"DROP TABLE IF EXISTS {self.db_name}.{self.schema_name}.{self.table_name};"
        drop_resp = self.execute_query(drop_query)
        self.logger.info(f"Table dropped due to failure: {drop_resp}")

    def create_and_load_table(self, column_expressions: str, columns_and_types: str, force: bool) -> List[Tuple]:
        """Create table and load data."""
        create_query = self.generate_create_table_statement(columns_and_types)
        copy_query = self.generate_copy_into_statement(column_expressions, force=force)

        try:
            create_resp = self.execute_query(create_query)
            copy_resp = self.execute_query(copy_query)
            return copy_resp

        except Exception as e:
            self.logger.error(f"Copy into failed: {e}")
            self._cleanup_failed_table()
            raise e

    def get_table_columns(self) -> Dict:
        """Get columns and data types from existing table."""
        details = {
            "database": self.db_name,
            "schema": self.schema_name,
            "table_name": self.table_name,
        }
        return self.schema_handler._get_columns_and_data_types_from_dest_table(details=details)

    def compare_schemas(self, dest_columns: Dict, source_columns: Dict) -> Tuple[List, List]:
        """Compare source and destination schemas."""
        return self.schema_handler._compare_columns_and_data_type(
            dest_columns=dest_columns, source_columns=source_columns
        )

    def modify_table_schema(self, add_columns: List, modify_columns: List, dest_columns: Dict) -> Tuple[List, List]:
        """Add columns in the destination table."""
        dest_details = {
            "database": self.db_name,
            "schema": self.schema_name,
            "table_name": self.table_name
        }
        return self.schema_handler._add_or_modify_columns(
            dest_details=dest_details,
            add_columns=add_columns,
            modify_columns=modify_columns,
            dest_columns=dest_columns
        )

    def handle_existing_table_load(self, force) -> CopyIntoResult:
        """Handle data loading when table already exists."""

        # Get schema information from current stage
        column_expressions, columns_and_types = self.get_schema_info()
        if not column_expressions or not columns_and_types:
            return CopyIntoResult(
                success=False,
                message="No columns found in the stage or Maybe there is no file in the stage. Cannot proceed with copy operation."
            )
        # Create temporary table to validate schema
        temp_table_name = f"{self.table_name}_{int(time.time())}"
        original_table_name = self.table_name

        try:
            # Test with temporary table
            self.table_name = temp_table_name
            temp_create_query = self.generate_create_table_statement(columns_and_types)
            temp_copy_query = self.generate_copy_into_statement(column_expressions, force=force)

            self.execute_query(temp_create_query)
            self.execute_query(temp_copy_query)

            # Get schema from temporary table
            source_columns = self.get_table_columns()

            # Clean up temporary table
            self.execute_query(f"DROP TABLE IF EXISTS {self.db_name}.{self.schema_name}.{temp_table_name};")

        finally:
            # Restore original table name
            self.table_name = original_table_name

        # Compare schemas
        dest_columns = self.get_table_columns()
        add_columns, modify_columns = self.compare_schemas(dest_columns, source_columns)

        self.logger.info(f"Columns to add: {add_columns}, Columns to modify: {modify_columns}")

        if add_columns:
            self.modify_table_schema(add_columns=add_columns, modify_columns=[], dest_columns=dest_columns)

        # Execute final copy
        column_expression_if_table_exists = self.get_schema_info_if_table_exists()
        copy_query = self.generate_copy_into_statement_if_table_exists(column_expression_if_table_exists, force=force)
        response = self.execute_query(copy_query)

        if response[0][0] == "Copy executed with 0 files processed.":
            return CopyIntoResult(
                success=True,
                message="Copy operation completed successfully with no files processed. This may indicate that the file already exists/loaded in the table.",
                data=response
            )
        return CopyIntoResult(
            success=True,
            message="Copy operation completed successfully",
            file_name=response[0][0],
            status=response[0][1],
            rows_parsed=response[0][2],
            rows_loaded=response[0][3],
            data=response
        )

    def copy_into_snowflake_table(self, force: bool = False) -> CopyIntoResult:
        """
        Main function to copy data into Snowflake table.
        Args:
            force (bool): Whether to force the copy operation even if the table exists. Defaults to False.
        Returns:
            Class CopyIntoResult: Result of the copy operation.
        """
        if_table_exists = self.check_if_table_exists()

        try:
            if not if_table_exists:
                column_expressions, columns_and_types = self.get_schema_info()
                if not column_expressions or not columns_and_types:
                    return CopyIntoResult(
                        success=False,
                        message="No columns found in the stage or Maybe there is no file in the stage. Cannot proceed with copy operation."
                    )
                result = self.create_and_load_table(column_expressions, columns_and_types, force=force)
                return CopyIntoResult(
                    success=True,
                    message="Copy operation completed successfully.",
                    file_name=result[0][0],
                    status=result[0][1],
                    rows_parsed=result[0][2],
                    rows_loaded=result[0][3],
                    data=result
                )
            else:
                return self.handle_existing_table_load(force=force)
        except Exception as e:
            self.logger.error(f"Copy into snowflake failed: {e}")
            raise e
