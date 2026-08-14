from PySide6.QtWidgets import QWidget

from app.database import Database
from app.models.model import BaseModel


class Controller:
    def __init__(self, db: Database, model: BaseModel, view: QWidget) -> None: ...
