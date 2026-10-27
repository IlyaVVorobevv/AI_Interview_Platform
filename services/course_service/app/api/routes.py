from fastapi import APIRouter


router = APIRouter()

@router.get("/health")
async def health():
    return {"status": "ok"}

@router.get("/db_check")
async def db_check():
    pass