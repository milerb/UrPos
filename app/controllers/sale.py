from PySide6.QtCore import Slot

from app.repository.sale import SalesRepository
from app.views import SalesWindow

from .controller import Controller


class SaleController(Controller):
    def __init__(self, db, model, view: SalesWindow):
        self.db = db
        self.model = model
        self.view = view
        self.sales_repository = SalesRepository(self.db)

        self.view.add_button.clicked.connect(self.on_click_add)
        self.view.delete_button.clicked.connect(self.on_click_delete)
        self.view.update_button.clicked.connect(self.on_click_update)

    @Slot()
    def on_click_add(self) -> None:
        print("add...")

    @Slot()
    def on_click_delete(self) -> None:
        print("delete...")

    @Slot()
    def on_click_update(self) -> None:
        print("Update...")
