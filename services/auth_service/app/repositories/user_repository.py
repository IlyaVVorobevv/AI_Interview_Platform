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

    async def create(self, user: User) -> User:
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update(self, user: User) -> User:
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def delete(self, user: User) -> None:
        await self.db.delete(user)
        await self.db.commit()
        return None