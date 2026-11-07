from sqlalchemy.ext.asyncio import AsyncSession

from app.models.course import Course
from shared.repositories.base import BaseRepository


class CourseRepository(BaseRepository[Course]):
    def __init__(self, db: AsyncSession) -> None:
        super().__init__(Course, db)

