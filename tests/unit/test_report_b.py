from datetime import datetime

from src.adapters.report import ConsoleReportAdapter
from src.domain.warehouse import Movement


def test_movement_report_empty():
    """
    Testet, ob bei einer leeren Movement-Liste
    eine sinnvolle Meldung im Report ausgegeben wird.
    """
    # Adapter mit keinen Produkten und keinen Bewegungen
    r = ConsoleReportAdapter(products={}, movements=[])

    # Report generieren
    out = r.generate_movement_report()

    # Erwartung: Hinweistext für leere Bewegungen vorhanden
    assert "Keine Lagerbewegungen vorhanden" in out


def test_movement_report_sorted_and_totals():
    """
    Testet:
    1. Ob Bewegungen chronologisch sortiert werden.
    2. Ob Summen für IN- und OUT-Bewegungen korrekt berechnet werden.
    3. Ob die Netto-Veränderung korrekt dargestellt wird.
    """

    # Bewegung 1 (späteres Datum)
    m1 = Movement(
        id="1",
        product_id="P1",
        product_name="A",
        quantity_change=+5,              # Bestand erhöht
        movement_type="IN",
        reason="Einkauf",
        performed_by="max",
        timestamp=datetime(2026, 2, 2, 10, 0),
    )

    # Bewegung 2 (früheres Datum)
    m2 = Movement(
        id="2",
        product_id="P1",
        product_name="A",
        quantity_change=-2,              # Bestand reduziert
        movement_type="OUT",
        reason="Verkauf",
        performed_by="anna",
        timestamp=datetime(2026, 2, 1, 9, 0),
    )

    # Adapter mit zwei unsortierten Bewegungen
    r = ConsoleReportAdapter(products={}, movements=[m1, m2])

    # Report generieren
    out = r.generate_movement_report()

    # --- 1. Chronologische Sortierung prüfen ---
    # Das frühere Datum muss im Text vor dem späteren erscheinen
    assert out.find("2026-02-01 09:00") < out.find("2026-02-02 10:00")

    # --- 2. Summen prüfen ---
    # IN-Summe sollte 5 sein
    assert "Summe IN: 5" in out

    # OUT-Summe sollte 2 sein (ohne Minuszeichen im Text)
    assert "Summe OUT: 2" in out

    # Netto-Bestand sollte 5 - 2 = 3 sein
    assert "Netto: 3" in out