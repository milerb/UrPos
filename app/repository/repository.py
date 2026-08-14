from typing import Any

from app.database import Database


class Repository:
    """
    Base repository class.
    """

    def __init__(self, db: Database):
        self.db = db

    def add(self, *args, **kwards) -> Any: ...
    def get(self, *args, **kwards) -> Any: ...
    def update(self, *args, **kwards) -> Any: ...
    def delete(self, *args, **kwards) -> Any: ...
