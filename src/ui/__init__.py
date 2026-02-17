import sys
from PyQt6.QtWidgets import QApplication

from ..adapters.repository import RepositoryFactory
from ..services import WarehouseService
from .main_window import WarehouseMainWindow


def main():
    app = QApplication(sys.argv)

    # "json" lädt Testdaten aus data/testdata.json, "memory" startet mit leerem Lager
    repo = RepositoryFactory.create_repository("json")
    service = WarehouseService(repo)

    window = WarehouseMainWindow(service)
    window.show()

    sys.exit(app.exec())