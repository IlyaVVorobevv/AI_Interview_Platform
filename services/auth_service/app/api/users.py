from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService
from app.schemas.user import UserResponse, UserUpdate
from app.models.user import User
from app.security.jwt import get_current_active_user, get_current_superuser

async def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    return UserService(repository)

router_user = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router_user.get("", response_model=list[UserResponse])
async def get_users(user_service: UserService = Depends(get_user_service),
                    limit: int = Query(default=10, ge=0, le=100),
                    offset: int = Query(default=0, ge=0)):
    users = await user_service.get_users(limit, offset)
    return users

@router_user.get("/me", response_model=UserResponse)
async def get_user(current_user: User = Depends(get_current_active_user)):
    return current_user

@router_user.get("/admin")
async def admin_only(current_user: User = Depends(get_current_superuser)):
    return {"message": "Welcome, admin"}

@router_user.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_service: UserService = Depends(get_user_service),
                         user_id: int = Path(gt=0)):
    user = await user_service.get_user_by_id(user_id)
    return user

@router_user.patch("/me", response_model=UserResponse)
async def update_current_user(data_for_update: UserUpdate,
                              current_user: User = Depends(get_current_active_user),
                              user_service: UserService = Depends(get_user_service)):
    update_user = await user_service.update_user(current_user.id, data_for_update)
    return update_user
