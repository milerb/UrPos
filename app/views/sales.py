from PySide6.QtWidgets import (
    QDoubleSpinBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.models import Sale

from .table import TableView


class SalesWindow(QWidget):
    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.price = 0.00
        self.name_label = QLabel("Item Name:", self)
        self.name = QLineEdit(self, placeholderText="Item Name...")
        self.quantity_label = QLabel("Quantity:", self)
        self.quantity = QDoubleSpinBox(self, minimum=1, maximum=50)
        self.price_label = QLabel("0.00")
        self.add_button = QPushButton("Add Sale", self)
        self.sale_panel = QGroupBox(self, title="Sales")

        self.delete_button = QPushButton("Delete", self)
        self.update_button = QPushButton("Update", self)
        self.table = TableView(Sale)

        input_layout = QVBoxLayout()
        input_layout.addWidget(self.name_label)
        input_layout.addWidget(self.name)
        input_layout.addWidget(self.quantity_label)
        input_layout.addWidget(self.quantity)
        input_layout.addStretch()
        input_layout.addWidget(self.add_button)
        self.sale_panel.setLayout(input_layout)

        table_layout = QGridLayout()
        table_layout.addWidget(self.table, 0, 0, 1, 3)
        table_layout.addWidget(self.update_button, 1, 1)
        table_layout.addWidget(self.delete_button, 1, 2)

        main_layout = QHBoxLayout()
        # Add groupbox to main layout.
        main_layout.addWidget(self.sale_panel, stretch=3)
        # Add table layout to main layout.
        main_layout.addLayout(table_layout, stretch=7)

        self.setLayout(main_layout)
        self.set_price(self.price)

    def set_price(self, price: float) -> None:
        self.price_label.setText(f"{price:.2f} Php")
