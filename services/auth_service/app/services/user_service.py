from typing import List

from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserUpdate


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        return user

    async def get_users(self, limit: int, offset: int) -> List[User]:
        users = await self.user_repository.get_all(limit, offset)
        return users

    async def update_user(self, user_id: int, data_for_update: UserUpdate) -> User:
        user = await self.user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")
        data_dict = data_for_update.model_dump(exclude_unset=True)
        if not data_dict:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="No fields provided for update")

        for field, value in data_dict.items():
            if field == "email":
                user_by_email = await self.user_repository.get_by_email(value)
                if user_by_email:
                    if user.id != user_by_email.id:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                            detail="Email already registered")

            if field == "username":
                user_by_username = await self.user_repository.get_by_username(value)
                if user_by_username:
                    if user.id != user_by_username.id:
                        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                            detail="Username already registered")

            setattr(user, field, value)
        user = await self.user_repository.update(user)
        return user


