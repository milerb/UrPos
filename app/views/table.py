from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView, QTableWidget, QTableWidgetItem
from sqlalchemy import inspect


class TableView(QTableWidget):
    """
    Copied from google gemini.
    Accepts a model to display table columns automatically.
    """

    def __init__(self, model_class: type[Any]):
        super().__init__()

        # 1. Inspect and store columns and headers immediately at creation
        self.columns = [c.key for c in inspect(model_class).mapper.column_attrs]
        labels = [col.replace("_", " ").title() for col in self.columns]

        # 2. Apply explicit structural configurations
        self.setColumnCount(len(self.columns))
        self.setRowCount(0)  # Starts clean and empty
        self.setHorizontalHeaderLabels(labels)

        # 3. Configure look and UX behavior
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Select entire rows when clicked rather than individual cells
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        # Prevent users from double-click editing the cell text directly
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def set_items(self, items: list[Any]) -> None:
        # Dynamically scale the row count to match incoming dataset size
        self.setRowCount(len(items))

        for row_idx, item in enumerate(items):
            for column_id, col_name in enumerate(self.columns):
                value = getattr(item, col_name)

                # Format specific data types cleanly
                if isinstance(value, float):
                    display_text = f"{value:.2f}"
                elif value is None:
                    display_text = ""
                else:
                    display_text = str(value)

                item_widget = QTableWidgetItem(display_text)

                # Hidden Feature: Safely store the database Primary Key ID
                # inside the first column item for background processing
                if column_id == 0:
                    item_widget.setData(Qt.ItemDataRole.UserRole, item.id)

                self.setItem(row_idx, column_id, item_widget)
