from PySide6.QtWidgets import QTabWidget, QWidget


class MainTab(QTabWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # Maintab Header
        # Maintab Status Bar

    def setup(self, tabs: dict[str, QWidget]):
        """Setup generated tabs into the main tab"""
        for k, v in tabs.items():
            self.addTab(v, k)
