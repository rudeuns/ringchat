from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
import os
from dotenv import load_dotenv

load_dotenv(".env.local")

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)

Session = sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as connection:
        await connection.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))


async def get_db():
    async with Session() as session:
        try:
            yield session
        finally:
            await session.close()


async def create_db_session():
    session = Session()
    return session


async def close_db_session(session):
    await session.close()
