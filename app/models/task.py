from app.database import Base
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
