from fastapi import HTTPException
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import select, update, delete

engine = create_async_engine("sqlite+aiosqlite:///schemes.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class ConfigOrm(Model):
    __tablename__ = "schemes"

    id: Mapped[int] = mapped_column(primary_key=True)
    scheme: Mapped[str]
    sc_values: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


class ConfigRepository:
    @classmethod
    async def add_one(cls, data) -> int:
        async with new_session() as session:
            config = ConfigOrm(**data)
            session.add(config)
            await session.flush()
            await session.commit()
            return config.id



    @classmethod
    async def find_one(cls, scheme_id) -> str:
        async with new_session() as session:
            query = select(ConfigOrm.sc_values).where(ConfigOrm.id == scheme_id)
            result = await session.execute(query)
            sc_array = result.scalar()
            if not sc_array:
                raise HTTPException(status_code=404, detail="Item not found")
            return sc_array

    @classmethod
    async def update_one(cls, data, scheme_id) -> bool:
        async with new_session() as session:
            query = update(ConfigOrm).returning(ConfigOrm.id).where(ConfigOrm.id == scheme_id).values(
                {"scheme": data['scheme'], "sc_values": data['sc_values']})
            response = await session.execute(query)
            await session.flush()
            await session.commit()
            if not len(response.fetchall()):
                await session.rollback()
                raise HTTPException(status_code=404, detail="Item not found")
            return True


    @classmethod
    async def delete_one(cls, scheme_id) -> bool:
        async with new_session() as session:
            query = delete(ConfigOrm).returning(ConfigOrm.id).where(ConfigOrm.id == scheme_id)
            response = await session.execute(query)
            await session.flush()
            await session.commit()
            if not len(response.fetchall()):
                await session.rollback()
                raise HTTPException(status_code=404, detail="Item not found")
            return True

