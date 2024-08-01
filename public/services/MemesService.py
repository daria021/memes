from typing import Annotated

from fastapi import UploadFile

from meme.schemas import MemeCreate, MemeResponse
from services.FilesService import FilesService


class MemesService:
    def __init__(
            self,
            meme_repo_context,
            files_service: FilesService,
    ):
        self.memes = meme_repo_context
        self.files_service = files_service

    async def upload_meme(
            self,
            image: UploadFile,
            meme: MemeCreate,
    ):
        async with self.memes() as memes:
            meme = await memes.create(schema=meme)

        try:
            await self.files_service.post_file(
                key=str(meme.id),
                image=image,
            )
        except Exception as e:
            async with self.memes() as memes:
                await memes.delete(record_id=meme.id)
            raise e

        return meme

    async def get_meme(
            self,
            key: str,
    ):
        filepath = await self._get_meme_image(key=key)

        meme = await self._get_meme_info(key=key)

        return filepath, meme

    async def get_meme_image(
            self,
            key: str,
    ) -> tuple[
        Annotated[str, "Path there the file is saved"],
        Annotated[str, "Name of the meme, which is associated with this file"]
    ]:
        filepath = await self._get_meme_image(key=key)
        filename = (await self._get_meme_info(key=key)).name
        return filepath, filename

    async def get_meme_info(
            self,
            key: str,
    ) -> MemeResponse:
        meme = await self._get_meme_info(key=key)

        return meme

    async def _get_meme_image(
            self,
            key: str,
    ) -> Annotated[str, "Path there the file is saved"]:
        filepath = await self.files_service.get_file(key=key)

        return filepath

    async def _get_meme_info(
            self,
            key: str,
    ) -> MemeResponse:
        async with self.memes() as memes:
            meme = await memes.get(int(key))

        return meme

    async def delete_meme(
            self,
            key: str
    ):
        await self.files_service.delete_file(key=key)

        async with self.memes() as memes:
            await memes.delete(record_id=int(key))
