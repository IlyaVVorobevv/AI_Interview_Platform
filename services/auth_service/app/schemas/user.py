import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


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