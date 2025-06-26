import uuid

from sqlalchemy.orm import Mapped, mapped_column

from src.database.db import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    stock_count: Mapped[int] = mapped_column(nullable=False)
