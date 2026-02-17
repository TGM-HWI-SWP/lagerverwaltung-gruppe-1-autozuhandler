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
    QTextEdit,
)
from PyQt6.QtCore import Qt

from ..backend import WarehouseUseCases
from .dialogs import ArticleDialogWindow


class WarehouseMainWindow(QMainWindow):
    """Hauptfenster der Autozubehör-Lagerverwaltungsanwendung (Frontend-only)"""

    def __init__(self, use_cases: WarehouseUseCases):
        super().__init__()
        self.use_cases = use_cases

        self.setWindowTitle("Autozubehör – Lagerverwaltung v0.1.0")
        self.setGeometry(100, 100, 1100, 650)

        self._create_ui()
<<<<<<< HEAD
        self._refresh_articles()  # direkt beim Start laden
        self._refresh_movements()
=======
        self._refresh_articles()  # lädt nur über Backend/Service

    # -------------------- UI Aufbau --------------------
>>>>>>> 4b6bc47738ca181283461271151ec2eca525e5d4

    def _create_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        self.tabs = QTabWidget()

        self._create_articles_tab()
        self._create_movements_tab()
        self._create_reports_tab()

        main_layout.addWidget(self.tabs)
        central_widget.setLayout(main_layout)

    def _create_articles_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        # Suche/Filter (Frontend-Filter: filtert nur Anzeige, ändert keine Daten)
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

        # Tabelle
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

<<<<<<< HEAD
    def _add_article(self):
        dialog = ArticleDialogWindow(self, title="Autozubehör-Artikel hinzufügen")
        if dialog.exec():
            data = dialog.get_data()
            try:
                # Domain bleibt gleich: create_product(...)
                self.use_cases.create_product(
                    product_id=data["product_id"],
                    name=data["name"],
                    description=data["description"],
                    price=data["price"],
                    category=data["category"],
                    quantity=data["quantity"],
                )
                QMessageBox.information(self, "Erfolg", "Artikel erfolgreich hinzugefügt.")
                self._refresh_articles()
            except Exception as e:
                QMessageBox.critical(self, "Fehler", str(e))

    def _refresh_articles(self):
        # Domain liefert dict: {product_id: product}
        search = self.search_input.text().strip().lower()
        cat = self.category_filter.currentText().strip()

        products = self.use_cases.list_products(search=search, category=cat)

        self.articles_table.setRowCount(len(products))

        for row, (product_id, product) in enumerate(products.items()):
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

        deleted = self.use_cases.delete_product(pid)
        if not deleted:
            QMessageBox.information(self, "Info", "Artikel wurde nicht gefunden.")
            return
        QMessageBox.information(self, "Erfolg", "Artikel erfolgreich gelöscht.")
        self._refresh_articles()

    # -------------------- TAB: BEWEGUNGEN --------------------

=======
>>>>>>> 4b6bc47738ca181283461271151ec2eca525e5d4
    def _create_movements_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()

        info_label = QLabel("Lagerbewegungen werden hier angezeigt (Backend-Use-Case).")
        layout.addWidget(info_label)

        # Platzhalter: UI ist vorbereitet, Backend liefert später Daten
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

<<<<<<< HEAD
    def _refresh_movements(self):
        movements = self.use_cases.list_movements()
        self.movements_table.setRowCount(len(movements))

        for row, movement in enumerate(sorted(movements, key=lambda m: m.timestamp)):
            self.movements_table.setItem(
                row,
                0,
                QTableWidgetItem(movement.timestamp.strftime("%Y-%m-%d %H:%M:%S")),
            )
            self.movements_table.setItem(
                row,
                1,
                QTableWidgetItem(f"{movement.product_name} ({movement.product_id})"),
            )
            self.movements_table.setItem(row, 2, QTableWidgetItem(movement.movement_type))
            self.movements_table.setItem(
                row, 3, QTableWidgetItem(f"{movement.quantity_change:+d}")
            )
            self.movements_table.setItem(
                row, 4, QTableWidgetItem(movement.reason or "")
            )

        self.movements_table.resizeColumnsToContents()

    # -------------------- TAB: REPORTS --------------------

=======
>>>>>>> 4b6bc47738ca181283461271151ec2eca525e5d4
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

<<<<<<< HEAD
        self.report_output = QTextEdit()
        self.report_output.setReadOnly(True)
        self.report_output.setPlaceholderText("Waehle einen Report aus.")
        layout.addWidget(self.report_output)
=======
        hint = QLabel("Reports werden später durch Backend/Report-Adapter geliefert.")
        layout.addWidget(hint)
>>>>>>> 4b6bc47738ca181283461271151ec2eca525e5d4

        widget.setLayout(layout)
        self.tabs.addTab(widget, "Berichte")

    # -------------------- Frontend Actions --------------------

    def _add_article(self):
        """Frontend: Dialog -> Service Use Case"""
        dialog = ArticleDialogWindow(self, title="Autozubehör-Artikel hinzufügen")
        if not dialog.exec():
            return

        data = dialog.get_data()
        if not data["product_id"] or not data["name"]:
            QMessageBox.warning(self, "Fehler", "Artikel-Nr und Name dürfen nicht leer sein.")
            return

        try:
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
        """Frontend: lädt Daten über Service und zeigt sie an (kein Speichern/JSON)."""
        try:
            products = self.service.get_all_products()  # dict[product_id, Product]
        except Exception as e:
            QMessageBox.critical(self, "Fehler", f"Konnte Produkte nicht laden:\n{e}")
            return

        search_txt = self.search_input.text().strip().lower()
        cat_txt = self.category_filter.currentText().strip()

        # Frontend-Filter: nur Anzeige filtern
        filtered = []
        for product_id, product in products.items():
            pid = str(product_id)
            name = getattr(product, "name", "")
            cat = getattr(product, "category", "")

            if cat_txt != "Alle" and cat != cat_txt:
                continue

            if search_txt and search_txt not in f"{pid} {name}".lower():
                continue

            filtered.append((product_id, product))

        self.articles_table.setRowCount(len(filtered))

        for row, (product_id, product) in enumerate(filtered):
            qty = int(getattr(product, "quantity", 0))
            price = float(getattr(product, "price", 0.0))
            total = float(product.get_total_value()) if hasattr(product, "get_total_value") else qty * price

            self.articles_table.setItem(row, 0, QTableWidgetItem(str(product_id)))
            self.articles_table.setItem(row, 1, QTableWidgetItem(str(getattr(product, "name", ""))))
            self.articles_table.setItem(row, 2, QTableWidgetItem(str(getattr(product, "category", ""))))
            self.articles_table.setItem(row, 3, QTableWidgetItem(str(qty)))
            self.articles_table.setItem(row, 4, QTableWidgetItem(f"{price:.2f}"))
            self.articles_table.setItem(row, 5, QTableWidgetItem(f"{total:.2f}"))

        self.articles_table.resizeColumnsToContents()

    def _get_selected_article_id(self) -> str | None:
        row = self.articles_table.currentRow()
        if row < 0:
            return None
        item = self.articles_table.item(row, 0)
        return item.text().strip() if item else None

    def _delete_article(self):
        """Frontend: ruft Service auf (Backend entscheidet, wie gelöscht wird)."""
        pid = self._get_selected_article_id()
        if not pid:
            QMessageBox.information(self, "Info", "Bitte zuerst einen Artikel auswählen.")
            return

        reply = QMessageBox.question(
            self,
            "Löschen bestätigen",
            f"Artikel '{pid}' wirklich löschen?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply != QMessageBox.StandardButton.Yes:
            return

        # Frontend-only: kein JSON/kein Repository direkt.
        try:
            # Falls Backend es noch nicht hat, fangen wir das sauber ab.
            delete_fn = getattr(self.service, "delete_product", None)
            if delete_fn is None:
                QMessageBox.information(self, "Info", "Löschen ist im Backend noch nicht implementiert.")
                return

            delete_fn(pid)
            QMessageBox.information(self, "Erfolg", f"Artikel '{pid}' wurde gelöscht.")
            self._refresh_articles()
        except Exception as e:
            QMessageBox.critical(self, "Fehler", str(e))

    # -------------------- Reports (Frontend placeholder) --------------------

    def _show_inventory_report(self):
<<<<<<< HEAD
        report = self.use_cases.generate_inventory_report_text()
        self.report_output.setPlainText(report)

    def _show_movement_report(self):
        report = self.use_cases.generate_movement_report_text()
        self.report_output.setPlainText(report)
=======
        QMessageBox.information(self, "Lagerbestandsbericht", "Report-Funktion wird implementiert (Backend).")

    def _show_movement_report(self):
        QMessageBox.information(self, "Bewegungsprotokoll", "Report-Funktion wird implementiert (Backend).")
>>>>>>> 4b6bc47738ca181283461271151ec2eca525e5d4
