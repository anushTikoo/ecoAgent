# Connecting db
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from sqlalchemy.pool import NullPool
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False, #No unnecessary logs
    pool_pre_ping=True,
    poolclass=NullPool  # Avoiding pooling (Training Wheels to prevent crashes and errors)
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@asynccontextmanager
async def lifespan(app):
    # --- STARTUP ---
    try:
        async with engine.begin() as conn:
            await conn.execute(text("SELECT 1;"))
        print("✅ Database connected.")
    except Exception as e:
        print("❌ Database connection failed:", e)
        raise

    yield

    # --- SHUTDOWN ---
    try:
        await engine.dispose()
        print("🔌 Database disconnected.")
    except Exception as e:
        print("⚠️ Error during DB shutdown:", e)