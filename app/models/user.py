from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.utils import Utils

from .model import BaseModel


class User(BaseModel):
    """
    Users model class.

    id: Mapped[int],
    username: Mapped[str],
    email: Mapped[str],
    password: Mapped[str],
    date_added: Mapped[str],
    is_active: Mapped[bool]
    """

    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, unique=True)
    username: Mapped[str] = mapped_column(String(20), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    password: Mapped[str] = mapped_column(String(30))
    date_added: Mapped[str] = mapped_column(default=Utils.get_current_date)
    is_active: Mapped[bool] = mapped_column(default=True)
