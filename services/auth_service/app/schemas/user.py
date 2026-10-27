import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Введите email")
    username: str = Field(min_length=3, description="Введите имя пользователя")
    password: str = Field(min_length=8, description="Введите пароль")

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None

    @field_validator("email", mode="before")
    @classmethod
    def check_email(cls, email: Any) -> EmailStr | None:
        if email is None:
            raise ValueError()
        return email

    @field_validator("username", mode="before")
    @classmethod
    def check_username(cls, username: Any) -> str | None:
        if username is None:
            raise ValueError()
        return username

    model_config = ConfigDict(extra="forbid")