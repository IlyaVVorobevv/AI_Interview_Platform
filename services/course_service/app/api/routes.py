from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db


router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/db-check")
async def db_check(db: AsyncSession = Depends(get_db)):
    query = text("SELECT 1")
    result = await db.execute(query)
    return result.scalar_one_or_none()