from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.course import Course


class CourseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_by_id(self, course_id: int) -> Course | None:
        query = select(Course).where(Course.id == course_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, course: Course) -> Course:
        self.db.add(course)
        await self.db.commit()
        await self.db.refresh(course)
        return course

    async def get_all(self, limit: int, offset: int) -> List[Course]:
        query = select(Course).order_by(Course.id).offset(offset).limit(limit)
        result = await self.db.scalars(query)
        courses = result.all()
        return courses


