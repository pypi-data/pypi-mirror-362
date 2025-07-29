# orchestration-utilities
This repository holds the utilities modules that are essential for ETL operations. This repository will be used as a package and serve the ETL flows.<br> This package will be used in the `PREFECT` flows and `SNOWFLAKE` as part of the ETL operations.


## Installation
Install the package using PYPI
```bash
pip install orchestration-utils
```

## Inside this package

### 1. aws.py
This module contains the functions that are used to interact with the AWS services.<br> Example: S3
___

### 2. copy_into_s3
This module contains the functions that can be used to copy the data from the Snowflake Stage(S3 Bucket) to the Snowflake Table.
This module leverages the `etl_operations` module to perform the `Schema Drift Handeling` and `Query Execution`.<br>
This module works best with the Stages that are partitioned well. Example: The data in the S3 bucket is partitioned by date, year, month, etc.<br>
This module does not perform well if the data is not partitioned well in the S3 bucket.
Example: If the data in the S3 bucket is dropped under a single folder without any partitioning, then the copy operation will take a lot of time to complete. Given the folder is heavy with files.

#### Class/Groups:
- `CopyIntoTable`: This class contains the functions that are used to copy the data from the Snowflake Stage(S3 Bucket) to the Snowflake Table.
- `copy_into_snowflake_table`: This function is the main function that is used to copy the data from the Snowflake Stage(S3 Bucket) to the Snowflake Table. It accepts the parameter `force` which is used to force the copy operation to be performed even if the data is already present in the table. The default value of the `force` parameter is `False`. 
___

### 3. etl_contol.py
This module contains the functions that interact with Snowflake and stores the states of the flows in the database.
- This module accepts the connection(connection_creds) paramater where the default value is `snowflake-prefect-user`, pipeline name and environment name.
- The pipeline name and environment name are used to store the states of the flows in the database. Example when the flow is started, completed, failed, etc.
___

### 4. etl_operations.py
This module contains the functions that are used to perform the ETL operations either in the Destination table or in the Source table.<br>

#### Class/Groups:
- `CreateConnections`: This class is used to create the connections to the databases. The connections are created using the connection credentials and warehouse name.
- `SnowflakeDestination`: This class contains all the load types and the functions that are used to load the data into the Snowflake tables.<br>This class accepts the connection credentials (by default the value is `snowflake-prefect-user`), warehouse name(by default the value is `loading`), database name, and environment name(by default the value is `dev`).
- `DataFrameHadler`: This class contains the functions that converts the dataframes columns to the relevant data types.
- `SchemaDriftHandler`: This class contains the functions that are used to handle the schema drifts in the destination table.
- `SnowflakeSource`: This class contains the functions that are used to extract the data from the Snowflake tables.
___

### 5. notifications.py
This module contains the functions that are used to send the notifications to Slack. The Webhook blocks need to be created in `Prefect` first to send the notifications to Slack.

#### Class/Groups:
- `SlackWebhooksNotification`: This class is used to send the notifications to Slack. The Class accepts the webhook name and the message that needs to be sent to Slack.
___
### 6. queries.py
This module contains the queries that are used to perform the ETL operations in the Snowflake tables. This module is referred by the `etl_control` and `etl_operations` modules.


## How to locally build package

Install the dependencies in your virtual environment.
```bash
pip install -r requirements-dev.txt
```

Build `dist` floder where `.whl` and `.tar.gz` files are created
```sh
make build
```
This will create the `dist` folder where two files are created.

- `orchestration_utils-0.0.0.tar.gz`
- `orchestration_utils-0.0.0-py3-none-any.whl`

The `.whl` is the installation file that can be installed using the `pip install dist/orchestration_utils-0.0.0-py3-none-any.whl` command.<br>

## How to deploy

Deploy the package to the PYPI using Github Actions. There are two workflows one to deploy in dev and the other to deploy in production.

#### 1. Dev/Manual Release to TestPyPI
- Click on Run workflow
- Select the branch that you have made the changes
- The changes will be refelcted in [TestPyPI](https://test.pypi.org/project/orchestration-utils/)
#### 2. Prod Release to PyPI
- Click on Run workflow
- Select the `main` branch only
- The changes will be refelcted in [PyPI](https://pypi.org/project/orchestration-utils/)
