from typing import Optional
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import Executable
from sqlalchemy.ext.asyncio import AsyncSession

from meme.exceptions import NotFoundException, InvalidSchemaError
from infrastructure.repositories.meme_repository import MemeRepo
from infrastructure.models import Meme
from public.meme.schemas import MemeCreate, MemeUpdate


# Моковая сессия для SQLAlchemy
@pytest.fixture
def mock_session():
    mock = AsyncMock(spec=AsyncSession)
    mock.execute.return_value.scalar_one = mock_scalar_one
    return mock


# Фикстура для создания репозитория
@pytest.fixture
def repo(mock_session):
    meme_repo = MemeRepo(session=mock_session)
    return meme_repo


mock_meme = Meme(id=1, name="test", description='lol')


def mock_scalar_one():
    if not mock_meme:
        raise NotFoundException

    return mock_meme


async def execute_updater(statement: Executable):
    global mock_meme

    class MockObject:
        def scalar_one(self):
            if mock_meme:
                return mock_meme

            raise NotFoundException

    if statement.is_update:
        init_values = mock_meme.to_dict()
        print(statement.__dict__)
        values = {x.name: y.value for x, y in statement.__dict__.get('_values').items()}
        for key in values:
            init_values[key] = values[key]
        mock_meme = Meme(**values)
        if 'id' in init_values:
            mock_meme.id = init_values['id']
    if statement.is_select:
        return MockObject()
    if statement.is_delete:
        mock_meme = None
        print('deleted')


# Тесты
@pytest.mark.asyncio
async def test_get(repo, mock_session):
    result = await repo.get(1)

    assert result.id == 1
    assert result.name == "test"
    mock_session.execute.assert_called_once()


class MemeCreateWithId(MemeCreate):
    id: int


@pytest.mark.asyncio
async def test_create(repo, mock_session):
    schema = MemeCreateWithId(id=1, name="test", description='lol')

    result = await repo.create(schema=schema)

    assert result.id == 1
    assert result.name == "test"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_create_invalid_schema(repo):
    with pytest.raises(InvalidSchemaError):
        await repo.create(None)


class MemeUpdateWithId(MemeUpdate):
    id: Optional[int] = None


@pytest.mark.asyncio
async def test_update(repo, mock_session):
    schema = MemeUpdate(name="updated_test", description='lol')
    mock_session.execute = execute_updater

    result = await repo.update(1, schema)

    assert result.id == 1
    assert result.name == "updated_test"


@pytest.mark.asyncio
async def test_update_invalid_schema(repo):
    with pytest.raises(InvalidSchemaError):
        await repo.update(1, None)


@pytest.mark.asyncio
async def test_delete(repo, mock_session):
    mock_session.execute = execute_updater

    await repo.get(1)

    await repo.delete(1)

    with pytest.raises(NotFoundException):
        await repo.get(1)
