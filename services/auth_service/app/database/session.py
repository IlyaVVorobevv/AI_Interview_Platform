from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.database.config import settings


DATABASE_URL = settings.database_url

engine = create_async_engine(
    url=DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
