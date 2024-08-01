from config import config
from .repositories import meme_repo_context
from services.FilesService import FilesService

from services.MemesService import MemesService


async def get_files_service() -> FilesService:
    return FilesService(
        host=config.files_api_host,
    )


async def get_memes_service() -> MemesService:
    yield MemesService(
        meme_repo_context=meme_repo_context,
        files_service=await get_files_service(),
    )
