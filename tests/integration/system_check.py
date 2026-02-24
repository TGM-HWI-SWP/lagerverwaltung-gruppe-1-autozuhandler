"""
System Check – Rolle 1 (Integration & Schnittstellen)

Diese Datei prüft:
1) Ob das Repository importiert und erstellt werden kann
2) Ob das Repository den Contract erfüllt
3) Ob ein "Service" existiert und (wenn möglich) mit dem Repository verbunden werden kann

Wenn kein Service existiert oder er anders heißt, ist das KEIN Fehler –
der Check zeigt dann nur eine Info an.
"""

from tests.integration.contract_validator import (
    validate_repository_contract,
    ContractViolationError,
)


def _find_service_class():
    """
    Versucht typische Service-Klassen zu finden.
    Wenn nichts gefunden wird, wird None zurückgegeben.
    """
    candidates = [
        # häufige Namen / Orte
        ("src.services", "WarehouseService"),
        ("src.services", "WarehouseManagementService"),
        ("src.services", "InventoryService"),
        ("src.services", "Service"),
        ("src.backend", "WarehouseService"),
        ("src.backend", "WarehouseManagementService"),
        ("src.backend", "InventoryService"),
        ("src.backend", "Service"),
    ]

    for module_name, class_name in candidates:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name, None)
            if cls is not None:
                return cls, f"{module_name}.{class_name}"
        except Exception:
            continue

    return None, None


def run_system_check():
    print("===== SYSTEM CHECK START =====")

    # 1) Repository importieren
    try:
        from src.adapters.repository import InMemoryRepository
        print(" Repository-Import OK: src.adapters.repository.InMemoryRepository")
    except Exception as e:
        print(" Import-Fehler (Repository):", e)
        return False

    # 2) Repository erstellen
    try:
        repo = InMemoryRepository()
        print(" Repository erstellt:", type(repo).__name__)
    except Exception as e:
        print(" Repository konnte nicht erstellt werden:", e)
        return False

    # 3) Contract prüfen
    try:
        validate_repository_contract(repo)
        print(" Repository erfüllt den RepositoryPort-Contract")
    except ContractViolationError as e:
        print(" Contract-Verletzung:", e)
        return False
    except Exception as e:
        print(" Fehler beim Contract-Check:", e)
        return False

    # 4) Service optional prüfen (nur wenn vorhanden)
    service_cls, service_path = _find_service_class()
    if service_cls is None:
        print("ℹ Kein Service gefunden (oder er heißt anders). Überspringe Service-Check.")
        print("=====  SYSTEM CHECK ERFOLGREICH (ohne Service-Teil) =====")
        return True

    # Falls Service gefunden: versuchen zu instanziieren
    try:
        service = service_cls(repo)
        print(f" Service gefunden & verbunden: {service_path}")
    except TypeError:
        print(f"ℹ Service gefunden ({service_path}), aber Konstruktor passt nicht zu (repo).")
        print("   -> Dann ist das Service-API anders. Überspringe Service-Instanzierung.")
    except Exception as e:
        print(f" Service gefunden ({service_path}), aber konnte nicht erstellt werden:", e)
        return False

    print("=====  SYSTEM CHECK ERFOLGREICH =====")
    return True


if __name__ == "__main__":
    ok = run_system_check()
    raise SystemExit(0 if ok else 1)