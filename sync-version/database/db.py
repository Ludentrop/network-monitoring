from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from .cfg import PATH


engine = create_async_engine(PATH)
Session = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db = Session()
    try:
        yield db
    finally:
        await db.close()


class Database:
    def __init__(self, model):
        self.model = model

    async def get_all(self):
        async with Session() as db:
            results = await db.execute(select(self.model))
            return results.scalars().all()

    async def get_by_id(self, obj_id):
        async with Session() as db:
            results = await db.execute(select(self.model).where(self.model.id == obj_id))
            return results.scalars().first()

    async def create(self, **kwargs):
        async with Session() as db:
            db_obj = self.model(**kwargs)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
