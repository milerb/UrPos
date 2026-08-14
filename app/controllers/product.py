from PySide6.QtCore import Slot

from app.repository.product import ProductRepository
from app.views import ProductWindow

from .controller import Controller


class ProductController(Controller):
    def __init__(self, db, model, view: ProductWindow):
        self.db = db
        self.model = model
        self.view = view
        self.product_repository = ProductRepository(self.db)

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
