import pandas as pd
import numpy as np

from prefect import task, flow, get_run_logger, __version__
from orchestration_utils import etl_operations


@task
def merge_dataframe_to_snowflake(
    df: pd.DataFrame,
):
    logger = get_run_logger()
    logger.info("Load dataframe directly to Snowflake")

    snowflake = etl_operations.SnowflakeDestination("raw", environment="dev")

    details = {
        "table_name": "new_util_data",
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



@flow()
def test_flow():
    prefect_version = __version__
    logger = get_run_logger()
    logger.info(f"Prefect version: {prefect_version}")
    logger.info("Starting flow...")

    data = {
        "id": [1, 2, 3, 4],
        "Name": ["Tom", "Brad", "Kyle", "Jerry"],
        "Age": [1, 30, 100, 15],
        "int_as_string": ["1", "2", "3", "4"],
        "float_as_string": ["1.1", "2.2", "3.3", "4.5"],
        "Height": [np.nan, 2.1, 6.0, 6.1],
        "Date": [
            "2021-01-01 00:00:00+00:00",
            "2021-01-02 00:00:00+00:00",
            "2021-01-03 00:00:00+5:45",
            # "02/06/2024, 08:12:37",
            "joseph",
        ],
        "Alt_Date": [
            "2021-01-01 00:00:00+00:00",
            "2021-01-02 00:00:00-06:00",
            "2021-01-03 00:00:00+5:45",
            "2021-01-05",
        ],
        # "variant_col": [
        #     "{'a': 1, 'b': 2}",
        #     "{'c': 3, 'd': 4}",
        #     "{'e': 5, 'f': 6}",
        #     "{'g': 7, 'h': 8}",
        # ],
        "variant_obj": [
            {"a": 1, "b": 2},
            {"a": 3, "b": 4},
            {"a": 5, "b": 6},
            {"a": 7, "b": 8},
        ],
        "json_str": [
            """{\"a\": 1, \"b\": 2}""",
            """{\"a\": 3, \"b\": 4}""",
            """{\"a\": 5, \"b\": 6}""",
            """{\"a\": 7, \"b\": 8}""",
        ],
        "variant_list": [
            ["a", "b", "c"],
            ["d", "e", "f"],
            ["g", "h", "i"],
            ["j", "k", "l"],
        ],
    }
    df = pd.DataFrame(data)
    print(df)
    merge_dataframe_to_snowflake(df)


if __name__ == "__main__":
    test_flow()
