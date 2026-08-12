from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# A database setup
# engine - manages the connection pool for the database, and knows how to
#   speak to it via the DB-API driver (e.g. aiosqlite). Created once and
#   shared for the app's lifetime.
# async_sessionmaker - a factory that produces new AsyncSession objects bound
#   to `engine`. Each session is a single unit-of-work (a set of queries plus
#   an optional commit); a new one is created per request via get_db below,
#   rather than reusing one session across requests.
engine = create_async_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

# Creates tables on setup
async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Returns a reference to the database
async def get_db():
    async with SessionLocal() as db:
        yield db
