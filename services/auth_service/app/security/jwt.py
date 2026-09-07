from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Any
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.config import settings
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt

def decode_access_token(token: str) -> dict | None:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme),
                           db: AsyncSession = Depends(get_db)) -> User:

    auth_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail="Could not validate data",
                                   headers={"WWW-Authenticate": "Bearer"})
    repository = UserRepository(db)
    payload = decode_access_token(token)
    if payload is None:
        raise auth_exception

    user_email = payload.get("sub")
    if user_email is None:
        raise auth_exception
    if not isinstance(user_email, str):
        raise auth_exception

    user = await repository.get_by_email(user_email)
    if user is None:
        raise auth_exception
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=403,
                            detail="Inactive user")
    return current_user

async def get_current_superuser(current_user: User = Depends(get_current_active_user)) -> User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403,
                            detail="Not enough permissions")
    return current_user