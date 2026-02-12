from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QLabel,
    QMessageBox,
    QTabWidget,
    QLineEdit,
    QComboBox,
)
from PyQt6.QtCore import Qt

from ..services import WarehouseService
from .dialogs import ArticleDialogWindow


class WarehouseMainWindow(QMainWindow):
    """Hauptfenster der Autozubehör-Lagerverwaltungsanwendung"""

    def __init__(self, service: WarehouseService):
        super().__init__()
        self.service = service

        self.setWindowTitle("Autozubehör – Lagerverwaltung v0.1.0")
        self.setGeometry(100, 100, 1100, 650)

        self._create_ui()
        self._refresh_articles()  # direkt beim Start laden

    def _create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()

        # Tabs
        self.tabs = QTabWidget()
        self._create_articles_tab()
        self._create_movements_tab()
        self._create_reports_tab()

        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)

    # -------------------- TAB: ARTIKEL --------------------

    def _create_articles_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Suche/Filter (UI-only, optional; kann später an service angebunden werden)
        filter_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Suche (Artikel-Nr oder Name)")

        self.category_filter = QComboBox()
        self.category_filter.addItem("Alle")
        self.category_filter.addItems([
            "Reifen",
            "Öl & Flüssigkeiten",
            "Batterien",
            "Bremsen",
            "Licht & Elektrik",
            "Scheibenwischer",
            "Innenraum",
            "Werkzeug",
            "Sonstiges",
        ])

        search_btn = QPushButton("Suchen")
        search_btn.clicked.connect(self._refresh_articles)

        filter_row.addWidget(QLabel("Suche:"))
        filter_row.addWidget(self.search_input, 2)
        filter_row.addWidget(QLabel("Kategorie:"))
        filter_row.addWidget(self.category_filter, 1)
        filter_row.addWidget(search_btn)

        layout.addLayout(filter_row)

        # Buttons
        button_layout = QHBoxLayout()
        add_btn = QPushButton("Artikel hinzufügen")
        refresh_btn = QPushButton("Aktualisieren")
        delete_btn = QPushButton("Löschen")

        add_btn.clicked.connect(self._add_article)
        refresh_btn.clicked.connect(self._refresh_articles)
        delete_btn.clicked.connect(self._delete_article)

        button_layout.addWidget(add_btn)
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(delete_btn)
        layout.addLayout(button_layout)

        # Tabelle (Domain: id, name, category, quantity, price)
        self.articles_table = QTableWidget()
        self.articles_table.setColumnCount(6)
        self.articles_table.setHorizontalHeaderLabels(
            ["Artikel-Nr", "Name", "Kategorie", "Bestand", "Preis (€)", "Gesamtwert (€)"]
        )
        self.articles_table.setSelectionBehavior(
            self.articles_table.SelectionBehavior.SelectRows
        )
        self.articles_table.setEditTriggers(
            self.articles_table.EditTrigger.NoEditTriggers
        )
        layout.addWidget(self.articles_table)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Artikel")

    def _add_article(self):
        dialog = ArticleDialogWindow(self, title="Autozubehör-Artikel hinzufügen")
        if dialog.exec():
            data = dialog.get_data()
            try:
                # Domain bleibt gleich: create_product(...)
                self.service.create_product(
                    product_id=data["product_id"],
                    name=data["name"],
                    description=data["description"],
                    price=data["price"],
                    category=data["category"],
                    initial_quantity=data["quantity"],
                )
                QMessageBox.information(self, "Erfolg", "Artikel erfolgreich hinzugefügt.")
                self._refresh_articles()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    def _refresh_articles(self):
        # Domain liefert dict: {product_id: product}
        products = self.service.get_all_products()

        # UI-Filter (nur oberflächlich, damit es auch ohne Service-Filter geht)
        search = self.search_input.text().strip().lower()
        cat = self.category_filter.currentText().strip()

        filtered = []
        for product_id, product in products.items():
            if cat != "Alle" and getattr(product, "category", "") != cat:
                continue

            if search:
                hay = f"{product_id} {getattr(product, 'name', '')}".lower()
                if search not in hay:
                    continue

            filtered.append((product_id, product))

        self.articles_table.setRowCount(len(filtered))

        for row, (product_id, product) in enumerate(filtered):
            self.articles_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.articles_table.setItem(row, 1, QTableWidgetItem(product.name))
            self.articles_table.setItem(row, 2, QTableWidgetItem(product.category))
            self.articles_table.setItem(row, 3, QTableWidgetItem(str(product.quantity)))
            self.articles_table.setItem(row, 4, QTableWidgetItem(f"{product.price:.2f}"))
            self.articles_table.setItem(
                row, 5, QTableWidgetItem(f"{product.get_total_value():.2f}")
            )

        self.articles_table.resizeColumnsToContents()

    def _get_selected_article_id(self) -> str | None:
        row = self.articles_table.currentRow()
        if row < 0:
            return None
        item = self.articles_table.item(row, 0)
        return item.text().strip() if item else None

    def _delete_article(self):
        pid = self._get_selected_article_id()
        if not pid:
            QMessageBox.information(self, "Info", "Bitte zuerst einen Artikel auswählen.")
            return

        QMessageBox.information(self, "Info", "Delete-Funktion wird implementiert.")
        # später: self.service.delete_product(pid) + refresh

    # -------------------- TAB: BEWEGUNGEN --------------------

    def _create_movements_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        info_label = QLabel("Lagerbewegungen (Einkauf/Verkauf/Defekt/Inventur) werden hier angezeigt.")
        layout.addWidget(info_label)

        self.movements_table = QTableWidget()
        self.movements_table.setColumnCount(5)
        self.movements_table.setHorizontalHeaderLabels(
            ["Zeitstempel", "Artikel", "Typ", "Menge", "Grund"]
        )
        self.movements_table.setEditTriggers(
            self.movements_table.EditTrigger.NoEditTriggers
        )
        layout.addWidget(self.movements_table)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Lagerbewegungen")

    # -------------------- TAB: REPORTS --------------------

    def _create_reports_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()
        inventory_btn = QPushButton("Lagerbestandsbericht")
        movement_btn = QPushButton("Bewegungsprotokoll")

        inventory_btn.clicked.connect(self._show_inventory_report)
        movement_btn.clicked.connect(self._show_movement_report)

        button_layout.addWidget(inventory_btn)
        button_layout.addWidget(movement_btn)
        layout.addLayout(button_layout)

        hint = QLabel("Reports werden später als Text/Datei angezeigt (statt MessageBox).")
        layout.addWidget(hint)

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Berichte")

    def _show_inventory_report(self):
        QMessageBox.information(self, "Lagerbestandsbericht", "Report-Funktion wird implementiert.")

    def _show_movement_report(self):
        QMessageBox.information(self, "Bewegungsprotokoll", "Report-Funktion wird implementiert.")