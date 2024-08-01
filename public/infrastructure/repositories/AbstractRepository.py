import logging
from typing import TypeVar, Type

from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from sqlalchemy.orm import DeclarativeBase

from meme.exceptions import NotFoundException, InvalidSchemaError

Schema = TypeVar("Schema", bound=BaseModel, covariant=True)
SQLModel = TypeVar("SQLModel", bound=DeclarativeBase, covariant=True)


class AbstractRepo:
    model: Type[SQLModel] = SQLModel
    update_schema: Type[Schema] = Schema
    create_schema: Type[Schema] = Schema
    get_schema: Type[Schema] = Schema

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, record_id: int) -> get_schema:
        try:
            res = await self.session.execute(select(self.model).where(self.model.id == record_id))
            obj = res.scalar_one()
            return await self.validate(obj) if obj else None
        except NoResultFound:
            raise NotFoundException()

    async def get_all(self, *filters, offset: int = 0, limit: int = 100) -> list[get_schema]:
        res = await self.session.execute(select(self.model).offset(offset).limit(limit).where(*filters))
        objects = res.scalars().all()
        return [await self.validate(obj) for obj in objects]

    async def get_filtered_by(self, **kwargs) -> list[get_schema]:
        res = await self.session.execute(select(self.model).filter_by(**kwargs))
        objects = res.scalars().all()
        return [await self.validate(obj) for obj in objects]

    async def create(self, schema: create_schema) -> get_schema:
        if not schema:
            raise InvalidSchemaError("schema is required")
        instance = self.model(**schema.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        logging.getLogger(__name__).info(instance.__dict__)
        return await self.validate(instance)

    async def update(self, record_id: int, schema: update_schema) -> get_schema:
        if not schema:
            raise InvalidSchemaError("Schema is required")

        clean_kwargs = {key: value for key, value in schema.model_dump().items() if value is not None}
        if not clean_kwargs:
            raise InvalidSchemaError("No valid data to update")

        await self.session.execute(
            update(self.model).where(self.model.id == record_id).values(**clean_kwargs)
        )
        await self.session.commit()
        return await self.get(record_id)

    async def delete(self, record_id: int):
        await self.session.execute(delete(self.model).where(self.model.id == record_id))
        await self.session.commit()


    async def validate(self, obj: SQLModel) -> Schema:
        return self.get_schema.model_validate(obj)
