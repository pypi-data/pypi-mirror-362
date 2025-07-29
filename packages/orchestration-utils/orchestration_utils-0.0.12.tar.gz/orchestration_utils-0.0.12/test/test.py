import pandas as pd
from prefect import task, flow, get_run_logger, __version__

from orchestration_utils import etl_operations

@task
def create_data():
    logger = get_run_logger()
    df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "name": ["Tom", "Brad", "Kyle", "Jerry"],
            "address": ["123 Main St", "456 Elm St", "789 Oak St", "101 Pine St"],
            "created_at": ["2021-01-01 00:00:00+00:00", "2021-01-02 00:00:00+00:00", "2021-01-03 00:00:00+00:00", "2021-01-05 00:00:00+00:00"]
        }
    )

    logger.info(f"Created data:\n {df}")
    return df

@task
def load_data(df: pd.DataFrame):
    logger = get_run_logger()
    logger.info("Load dataframe directly to Snowflake")

    snowflake = etl_operations.SnowflakeDestination("raw", environment="dev")

    details = {
        "table_name": "ic_load_test",
        "schema": "scratch",
        "database": "raw",
        "primary_key": "id",
        "record_timestamp": "created_at"
    }

    # results = snowflake.write_df(df, details)
    snowflake.load_incremental(df=df, details=details)
    # logger.info(results)

def merge_dataframe_to_snowflake(
    df: pd.DataFrame,
):
    logger = get_run_logger()
    logger.info("Load dataframe directly to Snowflake")

    snowflake = etl_operations.SnowflakeDestination("raw", environment="dev")

    details = {
        "table_name": "ic_load_test",
        "schema": "scratch",
        "database": "raw",
        "primary_key": "id",
    }

    # insert_count, update_count = snowflake.merge_df(df, details)
    results = snowflake.merge_df(df, details)

    # count_metadata = {"inserts": insert_count, "updates": update_count}

    logger = get_run_logger()
    logger.info(results)

    # metadata.update(count_metadata)
    logger.info("Adding metadata...")


@flow
def main():
    logger = get_run_logger()
    logger.info("Prefect Version: {}".format(__version__))

    data = create_data()
    merge_dataframe_to_snowflake(data)

if __name__ == "__main__":
    main()
