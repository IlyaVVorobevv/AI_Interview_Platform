from typing import List
from fastapi import APIRouter, Depends, Path, status
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_db
from app.repositories.course import CourseRepository
from app.services.course import CourseService
from app.schemas.course import CourseRead, CourseCreate, CourseUpdate


async def get_course_service(db: AsyncSession = Depends(get_db)):
    repository = CourseRepository(db)
    return CourseService(repository)


courses_router = APIRouter(prefix="/courses",
                           tags=["Courses"])


@courses_router.get("/{course_id}", response_model=CourseRead)
async def get_course_by_id(course_id: int = Path(gt=0),
                           service: CourseService = Depends(get_course_service)):
    course = await service.get_course_by_id(course_id)
    return course

@courses_router.post("", response_model=CourseRead, status_code=201, description="Course Created")
async def create_course(course_data: CourseCreate,
                        service: CourseService = Depends(get_course_service)):
    course = await service.create_course(course_data)
    return course

@courses_router.get("", response_model=List[CourseRead])
async def get_courses(service: CourseService = Depends(get_course_service),
                      limit: int = Query(default=10, gt=0, le=100),
                      offset: int = Query(default=0, ge=0)):
    courses = await service.get_courses(limit, offset)
    return courses

@courses_router.patch("/{course_id}", response_model=CourseRead)
async def update_course(service: CourseService = Depends(get_course_service),
                        course_id: int = Path(gt=0),
                        course_data: CourseUpdate = ...):
    course = await service.update_course(course_id, course_data)
    return course

@courses_router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(service: CourseService = Depends(get_course_service),
                        course_id: int = Path(gt=0)):
    await service.delete_course(course_id)