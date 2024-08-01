from contextlib import asynccontextmanager

from infrastructure.db import get_async_session
from infrastructure.repositories.meme_repository import MemeRepo


async def get_meme_repo() -> MemeRepo:
    async with get_async_session() as session:
        yield MemeRepo(session=session)


@asynccontextmanager
async def meme_repo_context() -> MemeRepo:
    async with get_async_session() as session:
        yield MemeRepo(session=session)
