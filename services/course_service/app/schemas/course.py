import datetime

from pydantic import BaseModel, Field, ConfigDict, AfterValidator
from typing import Annotated


def check_exam_type(exam_type) -> str:
    if exam_type in ('OGE', 'EGE', 'oge', 'ege', 'Oge', 'Ege'):
        return exam_type
    raise ValueError("Invalid exam_type")

valid_exam_type = Annotated[str, AfterValidator(check_exam_type)]


class CourseCreate(BaseModel):
    title: str = Field(min_length=3, description="Введите заголовок курса")
    description: str | None = None
    subject: str = Field(min_length=3, description="Введите название предмета")
    exam_type: valid_exam_type = Field(min_length=3, max_length=3, description="Выберите ОГЭ или ЕГЭ")
    is_published: bool = Field(default=False)


class CourseUpdate(BaseModel):
    title: str | None = Field(min_length=3, default=None)
    description: str | None = None
    subject: str | None = Field(min_length=3, default=None)
    exam_type: valid_exam_type | None = None
    is_published: bool | None = None

class CourseRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    subject: str
    exam_type: str
    is_published: bool
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)