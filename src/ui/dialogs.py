from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
)


class ArticleDialogWindow(QDialog):
    """Dialog zum Hinzufügen/Bearbeiten von Autozubehör-Artikeln"""

    def __init__(self, parent=None, title: str = "Artikel hinzufügen"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 420, 320)

        layout = QFormLayout()

        # Pflichtfelder (passen zu eurer Domain: product_id, name, description, price, category, quantity)
        self.article_id_field = QLineEdit()  # = product_id
        self.name_field = QLineEdit()
        self.description_field = QLineEdit()

        self.price_field = QDoubleSpinBox()
        self.price_field.setMaximum(9999999)
        self.price_field.setDecimals(2)

        self.quantity_field = QSpinBox()
        self.quantity_field.setMaximum(10**9)

        # Kategorie als Dropdown (Autozubehör)
        self.category_field = QComboBox()
        self.category_field.addItems([
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

        # Optionale UI-Felder (nur GUI, speichern aktuell NICHT in Domain)
        self.brand_field = QLineEdit()
        self.location_field = QLineEdit()  # Regalplatz/Lagerort

        layout.addRow("Artikel-Nr:", self.article_id_field)
        layout.addRow("Name:", self.name_field)
        layout.addRow("Kategorie:", self.category_field)
        layout.addRow("Marke (optional):", self.brand_field)
        layout.addRow("Lagerort (optional):", self.location_field)
        layout.addRow("Beschreibung:", self.description_field)
        layout.addRow("Preis (€):", self.price_field)
        layout.addRow("Startbestand:", self.quantity_field)

        button_layout = QHBoxLayout()
        ok_btn = QPushButton("Speichern")
        cancel_btn = QPushButton("Abbrechen")

        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)

        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)

        layout.addRow(button_layout)
        self.setLayout(layout)

    def get_data(self) -> dict:
        """Eingegebene Daten abrufen (Domain-Felder + optionale UI-Felder)"""
        return {
            "product_id": self.article_id_field.text().strip(),
            "name": self.name_field.text().strip(),
            "description": self.description_field.text().strip(),
            "price": float(self.price_field.value()),
            "quantity": int(self.quantity_field.value()),
            "category": self.category_field.currentText().strip(),
            # optional (für späteres erweitern)
            "brand": self.brand_field.text().strip(),
            "location": self.location_field.text().strip(),
        }