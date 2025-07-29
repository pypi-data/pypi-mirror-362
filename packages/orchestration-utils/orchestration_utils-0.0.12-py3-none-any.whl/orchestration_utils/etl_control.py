import json

from datetime import datetime, timedelta

from prefect_snowflake.database import SnowflakeCredentials
from snowflake.connector import DictCursor

from .queries import QUERIES


def date_range_to_chunks(start_date, end_date, interval_days):
    """Converts a date range into a list of smaller ranges of the same duration.  Duration is defined by interval_days.

    Usage exmaples:
    >>> date_range_to_chunks(date(2022,11,1), date(2022,11,10), 14)
    [{'start': datetime.date(2022, 11, 1), 'end': datetime.date(2022, 11, 10)}]

    >>> date_range_to_chunks(date(2022,11,1), date(2022,11,6), 2)
    [{'start': datetime.date(2022, 11, 1), 'end': datetime.date(2022, 11, 2)}, {'start': datetime.date(2022, 11, 3), 'end': datetime.date(2022, 11, 4)}, {'start': datetime.date(2022, 11, 5), 'end': datetime.date(2022, 11, 6)}]

    """
    interval = timedelta(days=interval_days)
    periods = []
    position_date = start_date

    while position_date <= end_date:
        next_position_date = position_date + interval
        interval_end_date = next_position_date - timedelta(days=1)
        period_start = position_date
        period_end = end_date if interval_end_date > end_date else interval_end_date
        periods.append({"start": period_start, "end": period_end})
        position_date = next_position_date
    return periods


def timestamp_range_to_chunks(start_at, end_at, interval_days):
    # returns Tuple of parallel lists
    interval = timedelta(days=interval_days)
    periods = []
    position_at = start_at
    while position_at < end_at:
        next_position_at = position_at + interval
        interval_end_at = next_position_at - timedelta(milliseconds=1)
        period_start = position_at
        period_end = end_at if interval_end_at > end_at else interval_end_at
        periods.append({"start": period_start, "end": period_end})
        position_at = next_position_at

    return periods

class CreateConnection:
    def __init__(self, connection_creds):
        self._creds = SnowflakeCredentials.load(connection_creds)
    def get_connection(self):
        return self._creds.get_client()

class ETLController:
    def __init__(self, pipeline_name, environment="dev", connection_creds="snowflake-prefect-user"):
        self._creds = CreateConnection(connection_creds=connection_creds).get_connection()
        self._pipeline_name = pipeline_name
        self._environment = environment
        self._db_prefix = "" if self._environment == "prod" else "_" + self._environment


    def _execute_operation(self, operation_name, **kwargs):
        sql = QUERIES[operation_name].format(
            operation_name, pipeline=self._pipeline_name, env=self._db_prefix, **kwargs
        )
        conn = self._creds
        cur = conn.cursor(DictCursor)
        return cur.execute(sql).fetchall()

    def _process_watermark(self, watermark_result):
        """Returns a watermark object using the valid, appropriate data type

        Usage examples:
        >>> ETLController._process_watermark(ETLController, json.dumps({'type': 'integer', 'val': 1669089890}))
        1669089890

        >>> ETLController._process_watermark(ETLController, json.dumps({'type': 'date', 'val': '2022-11-22'}))
        datetime.date(2022, 11, 22)

        >>> ETLController._process_watermark(ETLController, json.dumps({'type': 'datetime', 'val': '2022-11-22T05:04:06.123Z'}))
        '2022-11-22T05:04:06.123Z'

        """
        watermark = json.loads(watermark_result)
        result = watermark["val"]

        if watermark["type"] == "integer":
            result = int(watermark["val"])
        elif watermark["type"] == "date":
            result = datetime.strptime(watermark["val"], "%Y-%m-%d").date()
        elif watermark["type"] == "timestamp":
            result = datetime.strptime(watermark["val"], "%Y-%m-%dT%H:%M:%S.%f%z")
        return result

    def _initialize_pipeline(self):
        new_pipeline_operation_name = "new_pipeline"
        self._execute_operation(new_pipeline_operation_name)
        return self.get_pipeline()

    def _create_run(self, metadata):
        insert_run_operation_name = "insert_run_metadata"
        self._execute_operation(insert_run_operation_name, **metadata)
        return self.get_last_run()

    def _create_entity(self, metadata):
        entity_params = {}

        insert_entity_operation_name = "insert_entity_metadata"
        # get_entity_id_operation_name ='get_entity_id'

        entity_param_list = [
            "pipeline_id",
            "run_id",
            "entity_name",
            "starting_watermark",
            "high_watermark",
            "starting_row_count",
            "ending_row_count",
            "extract_row_count",
            "update_count",
            "insert_count",
            "delete_count",
            "error_count",
        ]

        for item in entity_param_list:
            if item == "starting_watermark" or item == "high_watermark":
                watermark_val = metadata[item]
                if metadata["watermark_type"] == "integer":
                    watermark_val = int(watermark_val)
                elif metadata["watermark_type"] == "date":
                    watermark_val = datetime.strftime(watermark_val, "%Y-%m-%d")
                elif metadata["watermark_type"] == "timestamp":
                    watermark_val = watermark_val.isoformat(timespec="milliseconds")

                entity_params[item] = json.dumps({"type": metadata["watermark_type"], "val": watermark_val})
            else:
                entity_params[item] = metadata.get(item, "NULL")
        self._execute_operation(insert_entity_operation_name, **entity_params)
        # return self._execute_operation(get_entity_id_operation_name, **metadata)

    def get_pipeline(self):
        get_pipeline_id_operation_name = "get_pipeline_id"
        results = self._execute_operation(get_pipeline_id_operation_name)
        if results:
            result = results[0]
            response = {"pipeline_id": result["PIPELINE_ID"]}
            return response

    def get_pipeline_name(self):
        return self._pipeline_name

    def get_last_run(self):
        get_last_run_operation_name = "get_run_id"
        pipeline = self.get_pipeline()
        if pipeline:
            results = self._execute_operation(get_last_run_operation_name, pipeline_id=pipeline["pipeline_id"])
            if results:
                result = results[0]
                response = {"run_id": result["RUN_ID"]}
                return response

    def get_last_run_metadata(self):
        get_last_run_metadata_operation_name = "get_last_run_metadata"

        results = self._execute_operation(get_last_run_metadata_operation_name)

        if results:
            metadata = {}
            result = results[0]
            metadata["pipeline_id"] = result["PIPELINE_ID"]
            if "RUN_ID" in result and result["RUN_ID"]:
                metadata["last_run_id"] = result["RUN_ID"]
                if result.get("HIGH_WATERMARK"):
                    metadata["last_run_start_at"] = result["RUN_START_AT"]
                    metadata["last_run_end_at"] = result["RUN_END_AT"]
                    metadata["watermark_type"] = json.loads(result["HIGH_WATERMARK"])["type"]
                    metadata["last_run_starting_watermark"] = self._process_watermark(result["STARTING_WATERMARK"])
                    metadata["last_run_high_watermark"] = self._process_watermark(result["HIGH_WATERMARK"])
        else:
            metadata = self._initialize_pipeline()
        return metadata

    def update_run_metadata(self, metadata):
        result = self._create_run(metadata)
        metadata["run_id"] = result["run_id"]

        self._create_entity(metadata)

    def date_range_to_chunks(self, start_date, end_date, interval_days):
        """Converts a date range into a list of smaller ranges of the same duration.  Duration is defined by interval_days.

        Usage exmaples:
        >>> date_range_to_chunks(date(2022,11,1), date(2022,11,10), 14)
        [{'start': datetime.date(2022, 11, 1), 'end': datetime.date(2022, 11, 10)}]

        >>> date_range_to_chunks(date(2022,11,1), date(2022,11,6), 2)
        [{'start': datetime.date(2022, 11, 1), 'end': datetime.date(2022, 11, 2)}, {'start': datetime.date(2022, 11, 3), 'end': datetime.date(2022, 11, 4)}, {'start': datetime.date(2022, 11, 5), 'end': datetime.date(2022, 11, 6)}]

        """
        interval = timedelta(days=interval_days)
        periods = []
        position_date = start_date

        while position_date <= end_date:
            next_position_date = position_date + interval
            interval_end_date = next_position_date - timedelta(days=1)
            period_start = position_date
            period_end = end_date if interval_end_date > end_date else interval_end_date
            periods.append({"start": period_start, "end": period_end})
            position_date = next_position_date
        return periods

    def timestamp_range_to_chunks(self, start_at, end_at, interval_days):
        # returns Tuple of parallel lists
        interval = timedelta(days=interval_days)
        periods = []
        position_at = start_at
        while position_at < end_at:
            next_position_at = position_at + interval
            interval_end_at = next_position_at - timedelta(milliseconds=1)
            period_start = position_at
            period_end = end_at if interval_end_at > end_at else interval_end_at
            periods.append({"start": period_start, "end": period_end})
            position_at = next_position_at

        return periods
