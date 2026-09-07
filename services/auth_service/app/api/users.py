from fastapi import APIRouter, Depends

from app.schemas.user import UserResponse
from app.models.user import User
from app.security.jwt import get_current_active_user, get_current_superuser

router_user = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router_user.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@router_user.get("/admin")
async def admin_only(current_user: User = Depends(get_current_superuser)):
    return {"message": "Welcome, admin"}