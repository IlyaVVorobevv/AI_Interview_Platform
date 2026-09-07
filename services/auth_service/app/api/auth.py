from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.token import Token
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from app.database.session import get_db


async def get_user_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    return AuthService(repository)

router_auth = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router_auth.post("/register", response_model=UserResponse, status_code=201)
async def register(user: UserCreate, service: AuthService = Depends(get_user_service)):
    return await service.register_user(user)

@router_auth.post("/login", response_model=Token)
async def login(user: UserLogin, service: AuthService = Depends(get_user_service)):
    authenticated_user = await service.authenticate_user(user)
    access_token = service.generate_access_token(authenticated_user)
    return Token(access_token=access_token, token_type="bearer")

@router_auth.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 service: AuthService = Depends(get_user_service)):
    user_login = UserLogin(
        email=form_data.username,
        password=form_data.password
    )

    authenticated_user = await service.authenticate_user(user_login)

    access_token = service.generate_access_token(authenticated_user)

    return Token(access_token=access_token, token_type="bearer")