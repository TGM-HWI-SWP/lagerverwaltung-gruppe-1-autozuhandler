from datetime import datetime

from src.adapters.report import ConsoleReportAdapter
from src.domain.warehouse import Movement


def test_movement_report_empty():
    r = ConsoleReportAdapter(products={}, movements=[])
    out = r.generate_movement_report()
    assert "Keine Lagerbewegungen vorhanden" in out


def test_movement_report_sorted_and_totals():
    m1 = Movement(
        id="1",
        product_id="P1",
        product_name="A",
        quantity_change=+5,
        movement_type="IN",
        reason="Einkauf",
        performed_by="max",
        timestamp=datetime(2026, 2, 2, 10, 0),
    )
    m2 = Movement(
        id="2",
        product_id="P1",
        product_name="A",
        quantity_change=-2,
        movement_type="OUT",
        reason="Verkauf",
        performed_by="anna",
        timestamp=datetime(2026, 2, 1, 9, 0),
    )

    r = ConsoleReportAdapter(products={}, movements=[m1, m2])
    out = r.generate_movement_report()

    assert out.find("2026-02-01 09:00") < out.find("2026-02-02 10:00")
    assert "Summe IN: 5" in out
    assert "Summe OUT: 2" in out
    assert "Netto: 3" in out