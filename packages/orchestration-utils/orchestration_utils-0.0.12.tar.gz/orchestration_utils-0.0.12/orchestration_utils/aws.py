import io
import pandas

from prefect_aws.s3 import S3Bucket
from prefect_aws import AwsCredentials


class S3Storage:
    def __init__(self, bucket: str, block=None) -> None:
        self.bucket = bucket
        if block == None:
            self.aws_cred = AwsCredentials.load("prefect-aws-credentials")
        else:
            self.aws_cred = block

    def bucket(self) -> str:
        return self.bucket

    def upload_df_as_csv(self, df: pandas.DataFrame, key: str) -> None:
        """
        This function uploads a DataFrame to S3 as a CSV file.
        Args:
            - df (pandas.DataFrame): the DataFrame to upload
            - key (str): the S3 key to upload the DataFrame to
        """
        # Convert the DataFrame to a CSV string
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)

        # Create a bytes object from the CSV string
        csv_bytes = csv_buf.getvalue().encode("utf-8")

        # Upload the bytes object to S3
        store = S3Bucket(bucket_name=self.bucket, credentials=self.aws_cred)
        store.write_path(path=key, content=csv_bytes)

        print(f"DataFrame uploaded to s3://{self.bucket}/{key}")
