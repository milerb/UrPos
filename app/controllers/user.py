from PySide6.QtCore import Slot

from app.repository.user import UserRepository
from app.views import UserWindow

from .controller import Controller


class UserController(Controller):
    def __init__(self, db, model, view: UserWindow):
        self.db = db
        self.model = model
        self.view = view
        self.user_repository = UserRepository(self.db)

        self.view.add_button.clicked.connect(self.on_click_add)
        self.view.delete_button.clicked.connect(self.on_click_delete)
        self.view.update_button.clicked.connect(self.on_click_update)

    @Slot()
    def on_click_add(self) -> None:
        print("Add...")

    @Slot()
    def on_click_delete(self) -> None:
        print("delete...")

    @Slot()
    def on_click_update(self) -> None:
        print("Update...")
