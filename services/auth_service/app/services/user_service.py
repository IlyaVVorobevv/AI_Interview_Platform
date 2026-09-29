from typing import List

from fastapi import HTTPException, status

from app.repositories.user_repository import UserRepository
from app.models.user import User

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
