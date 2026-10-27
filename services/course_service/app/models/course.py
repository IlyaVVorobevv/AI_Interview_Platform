import datetime

from app.database.base import Base
from sqlalchemy import String, Text, Boolean, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), unique=False, nullable=False)
    description: Mapped[str] = mapped_column(Text, unique=False, nullable=True)
    subject: Mapped[str] = mapped_column(String(100), unique=False, nullable=False)

    exam_type: Mapped[str] = mapped_column(String(10), unique=False, nullable=False)

    __table_args__ = (CheckConstraint("exam_type IN ('OGE', 'EGE', 'oge', 'ege', 'Oge', 'Ege')",
                                      name="check_exam_type_values"),)

    is_published: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
