from config import config
from s3.client import S3Client


def get_s3_client() -> S3Client:
    return S3Client(
        access_key=config.access_key.get_secret_value(),
        secret_key=config.secret_key.get_secret_value(),
        endpoint_url=config.endpoint_url,
        bucket_name=config.bucket_name,
    )