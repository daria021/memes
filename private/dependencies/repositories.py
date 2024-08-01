from dependencies.s3 import get_s3_client
from s3.service import FilesService


async def get_files_service() -> FilesService:
    yield FilesService(client_factory=get_s3_client)