import sys  # noqa: EXE002

from PySide6.QtCore import QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from app.controllers import (
    ProductController,
    SaleController,
    SupplierController,
    UserController,
)
from app.controllers.controller import Controller
from app.controllers.purchase import PurchaseController
from app.database import Database
from app.models import Product, Purchase, Sale, Supplier, User
from app.utils import LogHandler
from app.views import MainTab, ProductWindow, SalesWindow, SupplierWindow, UserWindow
from app.views.purchases import PurchaseWindow

LogHandler.config()
logger = LogHandler.logger(__name__)


class MainWindow(QMainWindow):
    """
    Main window class.
    """

    def __init__(self):
        super().__init__()

        self.setWindowTitle("UrPOS")
        self.setMinimumSize(QSize(800, 400))
        self.view = QWidget(self)
        self.maintab = MainTab(self.view)

        layout = QVBoxLayout()
        layout.addWidget(self.maintab)
        # Set the layout to the view not the mainwindow.
        self.view.setLayout(layout)
        self.setCentralWidget(self.view)


class AppController:
    """
    Main controller class.
    """

    def __init__(self, db: Database, main_window: MainWindow) -> None:
        self.database = db
        self.main_window = main_window
        # Stores active controllers to prevent garbage collection.
        self.active_controllers: list[Controller | None] = []
        self.views: dict[str, QWidget] = {}

        # 1 ============================= #
        # Create instances for the tabs.
        # This is where you add tab components to be added in the maintab view.
        salestab = SalesWindow(self.main_window.maintab)
        productstab = ProductWindow(self.main_window.maintab)
        purchasetab = PurchaseWindow(self.main_window.maintab)
        suppliertab = SupplierWindow(self.main_window.maintab)
        userstab = UserWindow(self.main_window.maintab)

        # 2 ============================= #
        # Add tabs into views.
        self.views["Sales"] = salestab
        self.views["Products"] = productstab
        self.views["Purchases"] = purchasetab
        self.views["Suppliers"] = suppliertab
        self.views["Users"] = userstab

        # 3 ============================= #
        # Create controllers for the views.
        sales_controller = SaleController(self.database, Sale(), salestab)
        products_controller = ProductController(self.database, Product(), productstab)
        purchase_controller = PurchaseController(self.database, Purchase(), purchasetab)
        supplier_controller = SupplierController(self.database, Supplier(), suppliertab)
        users_controller = UserController(self.database, User(), userstab)

        # 4 ============================= #
        # Add controllers to self.
        self.active_controllers.append(sales_controller)
        self.active_controllers.append(products_controller)
        self.active_controllers.append(purchase_controller)
        self.active_controllers.append(supplier_controller)
        self.active_controllers.append(users_controller)

        # Add the components into the View for rendering.
        self.main_window.maintab.setup(self.views)
        self.main_window.show()


# Application main function.
def main():
    """
    Main function.
    """

    app = QApplication(sys.argv)
    database = Database()  # Create a single database instance.

    window = MainWindow()  # Create main window.
    app_controller = AppController(database, window)  # Create main controller.
    app_controller.main_window.show()

    logger.info(msg="App Started!")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
