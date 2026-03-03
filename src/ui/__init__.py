import sys
from PyQt6.QtWidgets import QApplication

from ..adapters.repository import RepositoryFactory
from ..backend import WarehouseUseCases
from .main_window import WarehouseMainWindow


def main():
    app = QApplication(sys.argv)

    # SQLite Database - speichert Produkte in data/warehouse.db
    repo = RepositoryFactory.create_repository("sqlite")
    use_cases = WarehouseUseCases(repo)

    window = WarehouseMainWindow(use_cases)
    window.show()

    sys.exit(app.exec())