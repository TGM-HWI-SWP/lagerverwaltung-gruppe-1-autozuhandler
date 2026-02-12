import sys
from PyQt6.QtWidgets import QApplication

from ..adapters.repository import RepositoryFactory
from ..services import WarehouseService
from .main_window import WarehouseMainWindow


def main():
    app = QApplication(sys.argv)

    repo = RepositoryFactory.create_repository("memory")
    service = WarehouseService(repo)

    window = WarehouseMainWindow(service)
    window.show()

    sys.exit(app.exec())