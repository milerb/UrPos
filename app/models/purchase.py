from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.utils import Utils

from .model import BaseModel


class Purchase(BaseModel):
    """
    Purchases model class.

    id: Mapped[int],
    quantity: Mapped[int],
    product_id: Mapped[int],
    purchase_date: Mapped[str],
    supplier: Mapped[int],
    reciever: Mapped[str]
    """

    __tablename__ = "Purchases"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    quantity: Mapped[int] = mapped_column(default=1)
    product_id: Mapped[int]
    purchase_date: Mapped[str] = mapped_column(default=Utils.get_current_date)
    supplier: Mapped[int] = mapped_column(ForeignKey("suppliers.id"))
    reciever: Mapped[str] = mapped_column(default="")
