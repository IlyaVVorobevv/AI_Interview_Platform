from fastapi import HTTPException, status
from pydantic import EmailStr

from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserLogin
from app.models.user import User
from app.security.jwt import create_access_token
from app.security.password import hash_password, verify_password


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def email_exists(self, user_email: EmailStr) -> bool:
        user = await self.user_repository.get_by_email(user_email)
        return user is not None

    async def username_exists(self, user_username: str) -> bool:
        user = await self.user_repository.get_by_username(user_username)
        return user is not None

    async def register_user(self, user_register: UserCreate) -> User:
        if await self.email_exists(user_register.email):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email already registered")

        if await self.username_exists(user_register.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username already registered")

        hashed_password = hash_password(user_register.password)

        new_user = User(
            email=user_register.email,
            username=user_register.username,
            hashed_password=hashed_password
        )

        return await self.user_repository.create(new_user)

    async def authenticate_user(self, user_login: UserLogin) -> User:
        user = await self.user_repository.get_by_email(user_login.email)
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid email or password")

        if not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid email or password")

        return user

    def generate_access_token(self, user: User) -> str:
        return create_access_token({"sub": user.email, "user_id": user.id})