from typing import Callable

from s3.client import S3Client
from s3.schemas import FileResponse


class FilesService:
    def __init__(self, client_factory: Callable[[], S3Client]):
        self.client_factory = client_factory

    async def get_file(self,
                       key: str,
                       ):
        client = self.client_factory()
        filepath = f"temp/{key}"
        await client.get_meme(key=key, destination_path=filepath)
        return filepath

    async def upload_file(self,
                          key: str,
                          ):
        client = self.client_factory()

        filepath = f"temp/{key}"
        await client.upload_meme(key=key, file_path=filepath)
        schema = FileResponse(
            id=key,
            path=filepath,
        )
        return schema

    async def delete_file(self,
                          key: str,
                          ):
        client = self.client_factory()
        await client.delete_meme(key=key)
