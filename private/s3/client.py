import asyncio
from contextlib import asynccontextmanager

from aiobotocore.session import get_session
from botocore.exceptions import ClientError


class S3Client:
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }
        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_meme(
            self,
            file_path: str,
            key: str,
    ):
        try:
            async with self.get_client() as client:
                with open(file_path, "rb") as file:
                    await client.put_object(
                        Bucket=self.bucket_name,
                        Key=key,
                        Body=file,
                    )
                print(f"File {key} uploaded to {self.bucket_name}")
        except ClientError as e:
            print(f"Error uploading file: {e}")

    async def delete_meme(self, key: str):
        try:

            async with self.get_client() as client:
                await client.delete_object(Bucket=self.bucket_name, Key=key)
                print(f"File {key} deleted from {self.bucket_name}")
        except ClientError as e:
            print(f"Error deleting file: {e}")

    async def get_meme(self, key: str, destination_path: str):
        try:
            async with self.get_client() as client:
                response = await client.get_object(Bucket=self.bucket_name, Key=key)
                data = await response["Body"].read()
                with open(destination_path, "wb") as file:
                    file.write(data)
                print(f"File {key} downloaded to {destination_path}")
        except ClientError as e:
            print(f"Error downloading file: {e}")


async def main():
    s3_client = S3Client(
        access_key="",
        secret_key="",
        endpoint_url="",
        bucket_name="",
    )


if __name__ == "__main__":
    asyncio.run(main())
