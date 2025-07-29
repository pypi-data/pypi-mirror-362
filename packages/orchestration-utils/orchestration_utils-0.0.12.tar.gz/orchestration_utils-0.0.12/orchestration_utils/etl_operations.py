import json
import time

import pandas as pd
import numpy as np

from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass

from prefect import get_run_logger
from snowflake.connector import cursor, DictCursor
from snowflake.connector.pandas_tools import write_pandas
from prefect_snowflake.database import SnowflakeCredentials

from .queries import QUERIES
from .notifications import SlackWebhooksNotification

class Destination:
    pass

class Source:
    pass

class CreateConnection:
    def __init__(self, connection_creds, warehouse):
        self._creds = SnowflakeCredentials.load(connection_creds)
        self._warehouse = warehouse
    def get_connection(self):
        return self._creds.get_client(warehouse=self._warehouse)


class SnowflakeDestination(Destination):
    def __init__(
            self, database,
            schema="scratch",
            environment="dev",
            warehouse="loading",
            connection_creds="snowflake-prefect-user"
    ):
        self._creds = CreateConnection(
            connection_creds=connection_creds,
            warehouse=warehouse
        ).get_connection()
        self._environment = environment
        self._db_suffix = "" if self._environment == "prod" else "_" + self._environment
        self._db = database + self._db_suffix
        self._warehouse = warehouse
        self._conn = self._creds

    def get_warehouse(self):
        return self._warehouse

    def _check_if_table_exists(self, details) -> bool:
        """
        This function will check if a table exists in Snowflake.
        Args:
        details (dict): A dictionary containing details about the table to check.
        Returns:
        bool: True if the table exists, False otherwise.
        """
        logger = get_run_logger()

        schema = details["schema"]
        table = details["table_name"]
        sql = f"{QUERIES['check_if_table_exists']}".format(
            db=self._db, schema_name=schema, table_name=table
        )

        logger.info("Checking if the table exists in Snowflake...")
        response = self.query(sql)

        if response.fetchone()[0] is True:
            logger.info(f"Table '{table}' exists in Snowflake")
            return True
        else:
            logger.info(f"Table '{table}' does not exist in Snowflake")
            return False

    def _create_schema(self, schema) -> cursor:
        """
        This function will create a schema in Snowflake if not exists.
        """
        sql = "create schema if not exists " + schema + ";"
        response = self.query(sql)
        return response
    
    def _create_table_like(self, new_table, source_table) -> cursor:
        """
        This function will create a new table in Snowflake based on an existing table.
        Only the columns and data types will be copied. The values inside the table wont be copied.        
        """
        sql = f"create table {new_table} if not exists like {source_table};"
        response = self.query(sql)
        return response
    
    def query(self, sql) -> cursor:
        logger = get_run_logger()
        logger.info(sql)
        return self._conn.cursor().execute(sql)
    
    def query_to_df(self, sql: str) -> pd.DataFrame:
        """
        Executes the given SQL query and returns the result as a pandas DataFrame.

        Args:
            sql (str): The SQL query to execute.

        Returns:
            pd.DataFrame: The result of the query as a pandas DataFrame.
        """
        cursor = self._conn.cursor(DictCursor)
        try:
            cursor.execute(sql)
            df = cursor.fetch_pandas_all()
        finally:
            cursor.close()
        return df

    # _create_pk_merge_condition and _create_merge_sql are adapted from https://github.com/transferwise/pipelinewise-target-snowflake/
    def _create_pk_merge_condition(self, pk: str) -> str:
        """
            Accepts a primary key column and converts it into a join condition.
            Future adaptations should account for composite keys.

        Usage exmaples:
        >>> SnowflakeDestination._create_pk_merge_condition(SnowflakeDestination, 'account_email')
        's.account_email = t.account_email'

        """
        return f"s.{pk} = t.{pk}"

    def _create_merge_sql(
        self, temp_table_name: str, table_name: str, columns: List, pk: str
    ) -> str:
        """Generate a snowflake MERGE INTO command from table names and columns."""
        logger = get_run_logger()
        p_source_columns = ", ".join([f"\n\t\t{c}" for i, c in enumerate(columns)])
        p_update_condition = " or ".join(
            [
                (
                    f"\n\tt.{c} != s.{c} or (t.{c} is null and s.{c} is not null) or (t.{c} is not null and s.{c} is null)"
                    if c != "_record_loaded_at"
                    else ""
                )
                for c in columns
            ]
        )

        p_update_condition = (
            p_update_condition[:-4]
            if p_update_condition[-4:] == " or "
            else p_update_condition
        )

        p_update = ", ".join([f"\n\tt.{c} = s.{c}" for c in columns])
        # remove trailing comma
        if p_update[-2:] == ", ":
            p_update = p_update[:-2]
        else:
            p_update

        p_insert_cols = ", ".join([f"\n\tt.{c}" for c in columns])
        p_insert_values = ", ".join([f"\n\ts.{c}" for c in columns])
        pk_merge_condition = self._create_pk_merge_condition(pk)

        merge_sql = (
            f"MERGE INTO {table_name} t USING (\n"
            f"\tSELECT {p_source_columns} \n"
            f"\tFROM {temp_table_name}\n) s\n"
            f"ON {pk_merge_condition}\n"
            f"WHEN MATCHED AND ({p_update_condition}\n)\n"
            f"THEN UPDATE SET {p_update}\n"
            "WHEN NOT MATCHED THEN "
            f"INSERT ({p_insert_cols}\n) \n"
            f"VALUES ({p_insert_values}\n)"
        )
        return merge_sql

    def _write_df(self, df, details):
        """
        Writes a DataFrame to a database connection.

        Args:
            df (pandas.DataFrame): The DataFrame to be written.
            details (dict): Additional details for the write operation.

        Returns:
            tuple: A tuple containing the response from the write operation and a list of column names created from the DataFrame.
        """
        handler = DataFrameHandler()
        df = handler.infer_string_column_types(df=df)
        df = handler.replace_nan_values(df=df)
        create_schema_response = self._create_schema(
            f"{details['database']}.{details['schema']}"
        )
        response = write_pandas(
            conn=self._conn, df=df, use_logical_type=True, **details
        )
        return response, list(df.columns.values)

    def write_df(self, df, details):
        """
        Args:
        This function will take a dataframe to COPY INTO a table in Snowflake and
        it take details to create the Schemas and Tables if they don't exist.

        Returns:
        This function will return the function write_pandas to COPY INTO a table in Snowflake.

        Use:
        Use this function if you want to insert a dataframe into a table in Snowflake and
        if your dataset doesn't have a primary key to check if the data can be merged or not.
        This function have the ability to handle the Schema Drift in the destination table.
        """
        current_time = datetime.now(tz=None)
        df["_record_loaded_at"] = current_time

        database = details["database"] + self._db_suffix
        schema = details["schema"]
        table = details["table_name"]

        new_details = {
            "database": database,
            "schema": schema,
            "table_name": table,
            "quote_identifiers": False,
            "auto_create_table": True,
        }

        temp_details = {
            "database": database,
            "schema": schema,
            "table_name": "temp_" + table + "_" + str(int(time.time())),
            "quote_identifiers": False,
            "auto_create_table": True,
        }

        try:
            response_bool = self._check_if_table_exists(new_details)
            if response_bool is False:
                response, created_table_columns_list = self._write_df(df, new_details)
                return response, created_table_columns_list

            schema_handler = SchemaDriftHandler(environment=self._environment)

            dest_columns = schema_handler._get_columns_and_data_types_from_dest_table(new_details)

            source_columns = schema_handler._get_columns_and_data_types_from_source_temp_table(df, temp_details)

            col_to_add, col_to_modify = schema_handler._compare_columns_and_data_type(dest_columns, source_columns)

            if not (col_to_add or col_to_modify):
                response, created_table_columns_list = self._write_df(df, new_details)
                return response, created_table_columns_list

            else:
                added_cols, modified_cols = schema_handler._add_or_modify_columns(
                    new_details, col_to_add, col_to_modify, dest_columns
                )
                if (added_cols and modified_cols) or modified_cols:
                    modified_df = schema_handler._rename_columns_in_df(df, modified_cols)
                    response, created_table_columns_list = self._write_df(modified_df, new_details)
                else:
                    response, created_table_columns_list = self._write_df(df, new_details)
                return response, created_table_columns_list

        finally:
            self.close()

    def merge_df(self, df, details):
        """
        Merges a DataFrame with an existing table in the database.

        Args:
            df (pandas.DataFrame): The DataFrame to be merged.
            details (dict): A dictionary containing details about the merge operation,
                            including the primary key, database, schema, and table name.

        Returns:
            tuple: The result of the merge operation.

        Use:
            Use this function if you want to merge a dataframe into a table in Snowflake and
            your dataset has a primary key.
            This function have the ability to handle the Schema Drift in the destination table.
        """
        current_time = datetime.now(tz=None)
        df["_record_loaded_at"] = current_time

        pk = details.pop("primary_key")
        database = details["database"] + self._db_suffix
        schema = details["schema"]
        table_name = details["table_name"]

        temp_table_name = "temp_" + table_name + "_" + str(int(time.time()))
        database_schema = database + "." + schema
        table_full_name = database_schema + "." + table_name
        temp_table_full_name = database_schema + "." + temp_table_name

        new_details = {
            "database": database,
            "schema": schema,
            "table_name": table_name,
            "quote_identifiers": False,
            "auto_create_table": True,
        }

        temp_details = {
            "table_name": temp_table_name,
            "schema": schema,
            "database": database,
            "quote_identifiers": False,
            "auto_create_table": True,
        }

        def _merge_dataframe(df=df, temp_details=temp_details):
            temp_table_response, columns_list = self._write_df(df, temp_details)
            perm_table_create_response = self._create_table_like(
                table_full_name, temp_table_full_name
            )
            sql = self._create_merge_sql(
                temp_table_full_name, table_full_name, columns_list, pk
            )
            merge_response = self.query(sql)
            self.query("drop table if exists " + temp_table_full_name + ";")

            return merge_response.fetchall()[0]

        try:
            response_bool = self._check_if_table_exists(details=details)
            if response_bool is False:
                return _merge_dataframe(df=df, temp_details=temp_details)

            schema_handler = SchemaDriftHandler(environment=self._environment)

            dest_columns = schema_handler._get_columns_and_data_types_from_dest_table(new_details)

            source_columns = schema_handler._get_columns_and_data_types_from_source_temp_table(df, temp_details)

            col_to_add, col_to_modify = schema_handler._compare_columns_and_data_type(dest_columns, source_columns)

            if not (col_to_add or col_to_modify):
                return _merge_dataframe(df=df, temp_details=temp_details)
            else:
                added_cols, modified_cols = schema_handler._add_or_modify_columns(
                    new_details, col_to_add, col_to_modify, dest_columns
                )
                if (added_cols and modified_cols) or modified_cols:
                    modified_df = schema_handler._rename_columns_in_df(df, modified_cols)
                    return _merge_dataframe(df=modified_df, temp_details=temp_details)
                else:
                    return _merge_dataframe(df=df, temp_details=temp_details)

        finally:
            self.close()

    def close(self):
        self._conn.close()


class DataFrameHandler:
    def __init__(self) -> None:
        pass

    def infer_string_column_types(self, df: pd.DataFrame):
        """
        Infers and converts string columns to their appropriate types in a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame to process.

        Returns:
            pd.DataFrame: The processed DataFrame with inferred column types.
        """
        for column in df.columns:
            if pd.api.types.is_string_dtype(df[column]):
                try:
                    df[column] = pd.to_numeric(df[column])
                except BaseException as e:
                    try:
                        df[column] = pd.to_datetime(
                            df[column], utc=True
                        )
                    except:
                        pass
        return df

    def replace_nan_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Replaces NaN values in a DataFrame with a specified value.

        Args:
            df (pd.DataFrame): The DataFrame to process.
            value (str, optional): The value to replace NaN values with. Defaults to "NULL".

        Returns:
            pd.DataFrame: The processed DataFrame with NaN values replaced.
        """
        return df.replace({np.nan: None})


class SchemaDriftHandler:
    def __init__(self, environment) -> None:
        self.environment = environment

    def _get_columns_and_data_types_from_dest_table(self, details) -> List[dict]:
        """
        Args:
            details (dict): A dictionary containing details about the table to check.

        Returns:
            List[dict]: A list of dictionaries containing the column names and data types of the table.

        Use:
            This function will get the columns and data types from a table in Snowflake when details is passed into it.
        """
        logger = get_run_logger()

        database = details["database"]
        schema = details["schema"]
        table = details["table_name"]

        snowflake_dest = SnowflakeDestination(database=database, schema=schema)

        sql = f"{QUERIES['get_columns_and_data_type']}".format(
            db=database, schema_name=schema, table_name=table
        )

        logger.info("Getting columns and data types from table...")

        try:
            response = snowflake_dest.query(sql)
            response_fetch = response.fetchall()
            column_properties = [json.loads(response[0]) for response in response_fetch]
        finally:
            snowflake_dest.close()

        return column_properties

    def _get_columns_and_data_types_from_source_temp_table(self, df, temp_details):
        """
        Args:
            df (pd.DataFrame): The DataFrame to process. This is the source DataFrame.
            temp_details (dict): A dictionary containing details about the temporary table or the source.

        Returns:
            List[dict]: A list of dictionaries containing the column names and data types of the source DataFrame.
        
        Uses:
            This function will get the columns and data types from a DataFrame
            when the source DataFrame and the details are passed into it.
            Also, this function will drop the temporary table after getting the columns and data types.
        """
        logger = get_run_logger()

        database = temp_details["database"]
        schema = temp_details["schema"]
        table = temp_details["table_name"]

        snowflake_dest = SnowflakeDestination(database=database, schema=schema)

        logger.info(f"Temp table details: {database}.{schema}.{table}")

        try:
            response, column_list = snowflake_dest._write_df(df, temp_details)
            column_properties = self._get_columns_and_data_types_from_dest_table(
                temp_details
            )
            snowflake_dest.query(f"drop table if exists {database}.{schema}.{table};")
            return column_properties
        finally:
            snowflake_dest.close()

    def _compare_columns_and_data_type(self, dest_columns, source_columns):
        """
        Args:
            dest_columns (List[dict]): A list of dictionaries containing
                the column names and data types of the destination table.
            source_columns (List[dict]): A list of dictionaries containing
                the column names and data types of the source DataFrame.
            
        Returns:
            List[dict]: A list of dictionaries containing the column names and data types
                of the columns to be added or columns to be modified in the destination table.
        
        Uses:
            To compare the columns and data types of the destination table and the source DataFrame.
        """
        logger = get_run_logger()
        logger.info("Comparing columns and data types...")

        dest_col_names = [col["column_name"] for col in dest_columns]

        add_columns = []
        modify_columns = []
        for values in source_columns:
            if values["column_name"] not in dest_col_names:
                add_columns.append(values)

            if values["column_name"] in dest_col_names:
                if values["data_type"] != dest_columns[dest_col_names.index(values["column_name"])]["data_type"]:
                    modify_columns.append(values)

        return add_columns, modify_columns

    def _add_or_modify_columns(self, dest_details, add_columns, modify_columns, dest_columns):
        """
        Args:
            dest_details (dict): A dictionary containing details about the destination table.
            add_columns (List[dict]): A list of dictionaries containing the column names and data types
                of the columns to be added in the destination table.
            modify_columns (List[dict]): A list of dictionaries containing the column names and data types
                of the columns to be modified in the destination table.
        
        Returns:
            This function will return the added_columns and modified_columns in the destination table.
        
        Uses:
            This function will add or modify the columns in the destination table when there is a schema drift.
            This function will also send a slack message to the slack channel when there is a schema drift.
        """
        logger = get_run_logger()

        database = dest_details["database"]
        schema = dest_details["schema"]
        table = dest_details["table_name"]

        snowflake_dest = SnowflakeDestination(database=database, schema=schema)
        try:
            if add_columns:
                for column in add_columns:
                    sql = f"alter table {database}.{schema}.{table} add column {column['column_name']} {column['data_type']};"
                    response = snowflake_dest.query(sql)
                    logger.info(
                        f"Added column: {column['column_name']} {column['data_type']}"
                    )

                slack_add_mesaage = f"ALERT!!! New columns {add_columns} detected in table {database.upper()}.{schema.upper()}.{table.upper()}"
                slack_alert = SlackWebhooksNotification(environment=self.environment, slack_message=slack_add_mesaage)
                slack_alert.send_slack_json_message()

            if modify_columns:
                for column in modify_columns:
                    sql = f"alter table {database}.{schema}.{table} add column if not exists {column['column_name']}_{column['data_type']} {column['data_type']};"
                    response = snowflake_dest.query(sql)
                    logger.info(
                        f"Added modified column: {column['column_name']} {column['data_type']}"
                    )

                _modified_columns = [f"{column['column_name']}_{column['data_type']}" for column in modify_columns]
                _dest_columns = [column["column_name"] for column in dest_columns]

                if not set(_modified_columns).issubset(_dest_columns):
                    slack_modify_mesaage = f"ALERT!!! Modified columns {list(set(_modified_columns) - set(_dest_columns))} detected in table {database.upper()}.{schema.upper()}.{table.upper()}"
                    slack_alert = SlackWebhooksNotification(environment=self.environment, slack_message=slack_modify_mesaage)
                    slack_alert.send_slack_json_message()

            return add_columns, modify_columns

        finally:
            snowflake_dest.close()

    def _rename_columns_in_df(self, df, modified_cols) -> pd.DataFrame:
        """
        Args:
            df (pd.DataFrame): The DataFrame to process.
            modified_cols (List[dict]): A list of dictionaries containing the column names and data types
                of the columns to be modified in the destination table.
        
        Returns:
            pd.DataFrame: The processed DataFrame with renamed columns.
        
        Uses:
            This function will rename the columns in the DataFrame when there is a columns to be modified.
            When a column data type changes in the source DataFrame for same column name in the destination table,
                this function will rename the column in the DataFrame to match the column name in the destination table.
            Example: If the column name is 'column_A' and the data type is 'float',
                then the column name will be renamed to 'column_A_float'.
        """
        logger = get_run_logger()
        logger.info("Renaming columns in DataFrame...")

        df.columns = [col.upper() for col in df.columns]

        for column in modified_cols:
            if column["column_name"] in df.columns:
                df = df.rename(
                    columns={
                        column["column_name"]: f"{column['column_name']}_{column['data_type']}"
                    }
                )
        return df

@dataclass
class SnowflakeSource(Source):
    database: Optional[str] = "raw"
    schema: Optional[str] = "public"
    environment: Optional[str] = "dev"
    connection_creds: str = "prefect-analyst-reader-credentials"
    warehouse: str = "analyst_xs"

    def __post_init__(self) -> None:
        self._creds = CreateConnection(connection_creds=self.connection_creds, warehouse=self.warehouse).get_connection()
        self._environment = self.environment
        self._db_suffix = "" if self._environment == "prod" else "_" + self._environment
        self._db = self.database + self._db_suffix
        self._conn = self._creds
        self.logger = get_run_logger()

    def query_to_dataframe(self, sql) -> pd.DataFrame:
        cursor = self._conn.cursor(DictCursor)

        try:
            cursor.execute(sql)
            df = cursor.fetch_pandas_all()
        finally:
            cursor.close()
        return df

    def execute_query(self, sql) -> cursor:
        cursor = self._conn.cursor(DictCursor)

        try:
            cursor.execute("use role ods_unloader;")
            cursor.execute(sql)
        except:
            self.logger.info("Error executing query")
        return cursor

    def close(self):
        self._conn.close()


@dataclass
class SnowflakeOperations:
    connection_creds: str = "snowflake-prefect-user"
    warehouse: str = "loading"

    def __post_init__(self):
        self.creds = CreateConnection(
            connection_creds=self.connection_creds, warehouse=self.warehouse
        ).get_connection()
        self.logger = get_run_logger()

    def execute_query(self, sql):
        """
        Executes a SQL query in Snowflake.
        
        Args:
            sql (str): The SQL query to execute.
        
        Returns:
            cursor: The cursor object after executing the query.
        """
        cursor = self.creds.cursor(DictCursor)
        try:
            cursor.execute(sql)
            return cursor
        except Exception as e:
            self.logger.error(f"Error executing query: {e}")
            raise


    def check_current_role(self):
        """
        Check the current role in Snowflake.
        """
        query = "select current_role();"
        cursor = self.creds.cursor(DictCursor)
        try:
            cursor.execute(query)
            current_role = cursor.fetchall()[0]['CURRENT_ROLE()']
            return current_role
        except Exception as e:
            self.logger.error(f"Error checking current role: {e}")
        finally:
            cursor.close()
