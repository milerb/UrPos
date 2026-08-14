from PySide6.QtWidgets import QGridLayout, QPushButton, QWidget

from app.models import User

from .table import TableView


class UserWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        layout = QGridLayout()
        self.add_button = QPushButton("Add User", self)
        self.delete_button = QPushButton("Delete", self)
        self.update_button = QPushButton("Update", self)
        self.table = TableView(User)

        layout.addWidget(self.table, 0, 0, 1, 3)
        layout.addWidget(self.add_button, 1, 0)
        layout.addWidget(self.update_button, 1, 1)
        layout.addWidget(self.delete_button, 1, 2)

        self.setLayout(layout)
