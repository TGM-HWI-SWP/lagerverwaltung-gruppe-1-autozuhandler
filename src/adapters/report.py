"""Report Adapter - Report-Generierung"""

from typing import Dict

from ..ports import ReportPort


class ConsoleReportAdapter(ReportPort):
    """Report-Adapter für Konsolenausgabe"""

    def __init__(self, products: Dict = None, movements: list = None):
        self.products = products or {}
        self.movements = movements or []

    def generate_inventory_report(self) -> str:
        """
        Lagerbestandsbericht als Text generieren

        Returns:
            Formatierter Bericht
        """
        if not self.products:
            return "Lager ist leer.\n"

        report = "=" * 60 + "\n"
        report += "LAGERBESTANDSBERICHT\n"
        report += "=" * 60 + "\n\n"

        total_value = 0
        for product_id, product in self.products.items():
            value = product.get_total_value()
            total_value += value
            report += f"ID: {product_id}\n"
            report += f"  Name: {product.name}\n"
            report += f"  Kategorie: {product.category}\n"
            report += f"  Bestand: {product.quantity}\n"
            report += f"  Preis: {product.price:.2f} €\n"
            report += f"  Gesamtwert: {value:.2f} €\n\n"

        report += "-" * 60 + "\n"
        report += f"Gesamtwert Lager: {total_value:.2f} €\n"
        report += "=" * 60 + "\n"

        return report

    def generate_movement_report(self) -> str:
        """
        Bewegungsprotokoll als Text generieren (Report B)

        Returns:
            Formatierter Bericht
        """
        if not self.movements:
            return "Keine Lagerbewegungen vorhanden.\n"

        movements_sorted = sorted(self.movements, key=lambda m: m.timestamp)

        total_in = sum(m.quantity_change for m in movements_sorted if m.quantity_change > 0)
        total_out = sum(-m.quantity_change for m in movements_sorted if m.quantity_change < 0)
        net = total_in - total_out

        report = "=" * 80 + "\n"
        report += "BEWEGUNGSPROTOKOLL\n"
        report += "=" * 80 + "\n"
        report += "Zeit               | Artikel | Typ | Menge | User | Grund\n"
        report += "-" * 80 + "\n"

        for m in movements_sorted:
            ts = m.timestamp.strftime("%Y-%m-%d %H:%M")
            reason = (m.reason or "-").replace("\n", " ").strip()
            report += (
                f"{ts} | {m.product_id} | {m.movement_type} | {m.quantity_change:+d} | "
                f"{m.performed_by} | {reason}\n"
            )

        report += "-" * 80 + "\n"
        report += f"Summe IN: {total_in} | Summe OUT: {total_out} | Netto: {net}\n"
        report += f"Gesamtbewegungen: {len(movements_sorted)}\n"
        report += "=" * 80 + "\n"

        return report