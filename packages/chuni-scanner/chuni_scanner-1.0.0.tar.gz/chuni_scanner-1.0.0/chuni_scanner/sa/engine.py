from sqlalchemy import select
from sqlalchemy.inspection import inspect
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Union, List, Type, TypeVar, Sequence
from sqlalchemy.dialects.mysql import insert as mysql_insert
from sqlalchemy.orm import InstrumentedAttribute, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


T = TypeVar("T")


class DatabaseEngine:
    def __init__(self, url_scheme, table_base: Type[DeclarativeBase]) -> None:
        self._engine = create_async_engine(url_scheme, echo=False, future=True)
        self._session_maker = async_sessionmaker(self._engine, expire_on_commit=False)
        self._table_base = table_base

    async def init_engine(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(self._table_base.metadata.create_all)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession | None]:
        async with self._session_maker() as _session:
            yield _session

    async def shutdown_engine(self) -> None:
        await self._engine.dispose()

    async def select(
        self,
        target: Union[Type[T], InstrumentedAttribute],
        *conditions,
        one_result: bool = False,
    ) -> Union[T, List[T]] | None:
        async with self.session() as session:
            stmt = select(target)
            if conditions:
                stmt = stmt.where(*conditions)
            result = await session.execute(stmt)
            if one_result:
                return result.scalar_one_or_none()
            return result.scalars().all()

    async def add(self, instances: T | Sequence[T]) -> T | list[T] | None:
        async with self.session() as session:
            if isinstance(instances, list):
                session.add_all(instances)
            else:
                session.add(instances)
            await session.commit()
            if isinstance(instances, list):
                for inst in instances:
                    await session.refresh(inst)
                return instances
            else:
                await session.refresh(instances)
                return instances

    async def upsert(self, instances: T | Sequence[T]) -> T | list[T] | None:
        if not isinstance(instances, list):
            instances = [instances]
            single = True
        else:
            single = False
        if not instances:
            return [] if not single else None
        model = type(instances[0])
        table = model.__table__
        pk_columns = [col.name for col in inspect(model).primary_key]
        if not pk_columns:
            raise ValueError("Model has no primary key defined")
        values_list = []
        for instance in instances:
            values = {col.name: getattr(instance, col.name) for col in table.columns if hasattr(instance, col.name)}
            values_list.append(values)
        async with self.session() as session:
            stmt = mysql_insert(table).values(values_list)
            stmt = stmt.on_duplicate_key_update(
                {k: stmt.inserted[k] for k in table.columns.keys() if k not in pk_columns}
            )
            await session.execute(stmt)
            await session.commit()
            result_list = []
            for values in values_list:
                filter_kwargs = {k: values[k] for k in pk_columns}
                result = await session.execute(select(model).filter_by(**filter_kwargs))
                result_list.append(result.scalar_one_or_none())
            return result_list[0] if single else result_list
