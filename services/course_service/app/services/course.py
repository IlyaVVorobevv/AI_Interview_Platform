from fastapi import HTTPException, status
from watchfiles import awatch

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate
from app.repositories.course import CourseRepository
from app.core.exceptions import CourseNotFoundError


class CourseService:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def create_course(self, course: CourseCreate) -> Course:
        try:
            new_course = Course(title=course.title,
                                description=course.description,
                                subject=course.subject,
                                exam_type=course.exam_type,
                                is_published=course.is_published)
            created_course = await self.course_repository.create(new_course)
            await self.course_repository.db.commit()
            await self.course_repository.db.refresh(created_course)
            return created_course
        except Exception:
            await self.course_repository.db.rollback()
            raise


    async def get_course_by_id(self, course_id: int) -> Course:
        course = await self.course_repository.get_by_id(course_id)
        if course is None:
            raise CourseNotFoundError()
        return course

    async def get_courses(self, limit: int, offset: int) -> list[Course]:
        courses = await self.course_repository.get_all(limit, offset)
        return courses

    async def update_course(self, course_id: int, course_data: CourseUpdate) -> Course:
        try:
            course = await self.course_repository.get_by_id(course_id)
            if course is None:
                raise CourseNotFoundError()
            data_dict = course_data.model_dump(exclude_unset=True)

            if not data_dict:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="No fields provided for update")

            for field, value in data_dict.items():
                setattr(course, field, value)
            course = await self.course_repository.update(course)
            await self.course_repository.db.commit()
            return course
        except Exception:
            await self.course_repository.db.rollback()
            raise

    async def delete_course(self, course_id: int) -> None:
        try:
            course = await self.course_repository.get_by_id(course_id)
            if course is None:
                raise CourseNotFoundError()
            await self.course_repository.delete(course)
            await self.course_repository.db.commit()
        except Exception:
            await self.course_repository.db.rollback()
            raise