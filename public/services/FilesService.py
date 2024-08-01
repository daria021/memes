import httpx
from fastapi import UploadFile

from .exceptions import ServerNotAvailableException
from services.exceptions import WrongKeyException


class FilesService:
    def __init__(self, host: str):
        self.host = host

    @staticmethod
    def _get_filepath(key: str) -> str:
        return f"temp/{key}"

    def _get_url(self, key: str) -> str:
        return f"http://{self.host}/files/{key}"

    async def post_file(self, key: str, image: UploadFile):
        async with httpx.AsyncClient() as client:
            data = await client.post(
                url=self._get_url(key=key),
                files={'file': (image.filename, image.file, image.content_type)},
            )

        if data.status_code == 200:
            return

        raise ServerNotAvailableException()

    async def get_file(self, key: str):
        async with httpx.AsyncClient() as client:
            data = await client.get(
                url=self._get_url(key=key),
            )

        if data.status_code == 404:
            raise WrongKeyException()

        if data.status_code != 200:
            raise ServerNotAvailableException()

        filepath = f"temp/{key}"
        with open(filepath, 'wb') as file:
            file.write(data.content)

        return filepath

    async def delete_file(self, key: str):
        async with httpx.AsyncClient() as client:
            data = await client.delete(
                url=self._get_url(key=key),
            )

        if data.status_code == 200:
            return

        if data.status_code == 404:
            raise WrongKeyException()
        else:
            raise ServerNotAvailableException()
