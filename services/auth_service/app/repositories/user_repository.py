from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from shared.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(User, db)

    async def get_by_email(self, user_email: EmailStr) -> User | None:
        query = select(User).where(User.email == user_email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_by_username(self, user_username: str) -> User | None:
        query = select(User).where(User.username == user_username)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
