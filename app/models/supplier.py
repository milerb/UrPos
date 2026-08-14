from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.utils import Utils

from .model import BaseModel


class Supplier(BaseModel):
    """
    Supplier model class.

    id: Mapped[int],
    name: Mapped[str],
    address: Mapped[str],
    date_added: Mapped[str],
    is_active: Mapped[bool]
    """

    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    address: Mapped[str] = mapped_column(String(50))
    date_added: Mapped[str] = mapped_column(default=Utils.get_current_date)
    is_active: Mapped[bool] = mapped_column(default=True)
