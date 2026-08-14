from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget

from app.models import Supplier

from .table import TableView


class SupplierWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        layout = QGridLayout()
        self.add_button = QPushButton("Add Supplier", self)
        self.delete_button = QPushButton("Delete", self)
        self.update_button = QPushButton("Update", self)

        self.supplier_table = TableView(Supplier)

        layout.addWidget(self.supplier_table, 0, 0, 1, 3)
        layout.addWidget(self.add_button, 1, 0)
        layout.addWidget(self.update_button, 1, 1)
        layout.addWidget(self.delete_button, 1, 2)

        self.setLayout(layout)
