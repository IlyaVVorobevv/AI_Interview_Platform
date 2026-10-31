from app.models.course import Course
from app.schemas.course import CourseCreate
from app.repositories.course import CourseRepository
from app.core.exceptions import CourseNotFoundError


class CourseService:
    def __init__(self, course_repository: CourseRepository) -> None:
        self.course_repository = course_repository

    async def create_course(self, course: CourseCreate) -> Course:
        new_course = Course(title=course.title,
                            description=course.description,
                            subject=course.subject,
                            exam_type=course.exam_type,
                            is_published=course.is_published)


        return await self.course_repository.create(new_course)

    async def get_course(self, course_id: int) -> Course:
        course = await self.course_repository.get_by_id(course_id)
        if course is None:
            raise CourseNotFoundError()
        return course
