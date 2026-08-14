from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.utils import Utils

from .model import BaseModel


class Sale(BaseModel):
    """
    Sales model class.

    id: Mapped[int]
    quantity: Mapped[float]
    product_id: Mapped[int]
    price: Mapped[float]
    date: Mapped[str]
    """

    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    quantity: Mapped[float] = mapped_column(default=1.00)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    price: Mapped[float] = mapped_column()
    date: Mapped[str] = mapped_column(default=Utils.get_current_date)
