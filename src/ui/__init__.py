import sys
from PyQt6.QtWidgets import QApplication

from ..adapters.repository import RepositoryFactory
from ..backend import WarehouseUseCases
from .main_window import WarehouseMainWindow


def main():
    app = QApplication(sys.argv)

<<<<<<< HEAD
    # "json" lädt Testdaten aus data/testdata.json, "memory" startet mit leerem Lager
    repo = RepositoryFactory.create_repository("json")
    use_cases = WarehouseUseCases(repo)
=======
    # Composition Root: Backend wird hier gebaut, UI bekommt nur den Service
    repo = RepositoryFactory.create_repository("memory")
    service = WarehouseService(repo)
>>>>>>> 4b6bc47738ca181283461271151ec2eca525e5d4

    window = WarehouseMainWindow(use_cases)
    window.show()

    sys.exit(app.exec())