import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[bytes] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False)

