from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.utils import Utils

from .model import BaseModel


class Product(BaseModel):
    """
    Products model class.

    id: Mapped[int],
    manufacturer: Mapped[str],
    name: Mapped[str],
    packaging: Mapped[str],
    unit_per_pack: Mapped[int],
    price_per_unit: Mapped[float],
    date_added: Mapped[str],
    is_available: Mapped[bool]
    """

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    manufacturer: Mapped[str] = mapped_column(String(20))
    name: Mapped[str] = mapped_column(String(20), unique=True)
    packaging: Mapped[str] = mapped_column(String(10))
    unit_per_pack: Mapped[int] = mapped_column(default=1)
    price_per_unit: Mapped[float] = mapped_column(default=0.00)
    date_added: Mapped[str] = mapped_column(default=Utils.get_current_date)
    is_available: Mapped[bool] = mapped_column(default=True)
