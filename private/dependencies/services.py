from dependencies.s3 import get_s3_client
from s3.service import FilesService


def get_s3_service() -> FilesService:
    return FilesService(client_factory=get_s3_client)
