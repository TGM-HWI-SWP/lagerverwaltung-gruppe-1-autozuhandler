# Datenbank-Setup für Lagerverwaltungssystem

## Übersicht

Das Projekt verfügt jetzt über eine vollständige SQLite-Datenbank mit:
- **Schema**: Strukturierte Datentabellen für Lager, Produkte, Kategorien, Marken und Bewegungen
- **Dump-Daten**: 22 Auto-Zubehör-Produkte mit historischen Lagerbewegungen
- **ORM-Modelle**: SQLAlchemy-Integration für einfache Datenbankoperationen
- **SQLite Repository**: Adapter für das bestehende RepositoryPort-Interface

## Datenbankstruktur

### Tabellen

1. **warehouses** - Lagerhallen/Standorte
   - id, name, location, created_at, updated_at

2. **categories** - Produktkategorien
   - id, name, description, created_at
   - 9 Kategorien: Reifen, Öl & Flüssigkeiten, Batterien, etc.

3. **brands** - Hersteller/Marken
   - id, name, country, website, created_at
   - 20 bekannte Auto-Zulieferer (Michelin, Bosch, Varta, etc.)

4. **products** - Lagerproduke
   - Vollständige Produktinformationen mit Bestandsniveaus
   - 22 Produkte aus verschiedenen Kategorien
   - Felder: id, sku, name, price, quantity, location, min_stock, max_stock, etc.

5. **movements** - Lagerbewegungen (Audit Trail)
   - Typen: IN, OUT, CORRECTION, ADJUSTMENT
   - 14 Beispiel-Bewegungen zwischen 2026-02-15 und 2026-02-19
   - Nachverfolgung: performed_by, timestamp, reason

6. **users** - Mitarbeiter/Benutzer
   - 5 Test-Benutzer mit Rollen (admin, lagerleiter, mitarbeiter, viewer)

7. **inventory_snapshots** - Historische Bestände
   - Tägliche Snapshots für Reporting
   - 44 Snapshots für zwei Tage (2026-02-17 und 2026-02-18)

8. **movement_history** - Detailedere Bewegungshistorie
   - quantity_before, quantity_after für Audit-Trail

### Test-Datensatz

**Lager**: Hauptlager Autozubehör (München, Oberbayern)

**Produkte** (Beispiele):
- Winterreifen Michelin 205/55R16 - €89,99 (24 Stück)
- Motoröl 5W-30 Castrol Edge - €45,99 (35 Stück)
- Autobatterie 12V 60Ah - €79,99 (12 Stück)
- Bremsbeläge VW Golf 7 - €34,99 (20 Stück)
- LED Innenraumbeleuchtung - €24,99 (30 Stück)
- + 17 weitere Produkte

**Gesamtbestand**: ~€20.000+ Lagerwert

## Installation & Initialisierung

### Anforderungen

```bash
pip install sqlalchemy>=2.0.0
```

Oder beide Datenbank-Pakete:
```bash
pip install -e .
```

### Datenbank initialisieren

```bash
# Einfach (in data/ Verzeichnis)
python scripts/init_database.py

# Mit Custom-Pfad
python scripts/init_database.py --db /path/to/warehouse.db

# Existierende Datenbank überschreiben
python scripts/init_database.py --force

# Ohne Backup
python scripts/init_database.py --force --no-backup
```

Das Skript wird:
1. ✓ Das Schema laden und alle Tabellen erstellen
2. ✓ Dump-Daten (Produkte, Bewegungen, etc.) einfügen
3. ✓ Datenbank verifizieren und Statistiken anzeigen

## Verwendung

### Mit Python Code

#### SQLite Repository nutzen

```python
from src.adapters.repository import RepositoryFactory

# SQLite Repository erstellen
repo = RepositoryFactory.create_repository(
    repository_type="sqlite",
    db_path="data/warehouse.db"
)

# Alle Produkte laden
products = repo.load_all_products()
for product_id, product in products.items():
    print(f"{product.id}: {product.name} - {product.quantity} Stk")

# Ein Produkt laden
product = repo.load_product("PROD001")
print(f"Bestand: {product.quantity} x {product.price}€ = {product.get_total_value()}€")

# Lagerbewegungen laden
movements = repo.load_movements()
for movement in movements:
    print(f"{movement.movement_type}: {movement.quantity_change} ({movement.reason})")
```

#### SQLAlchemy ORM direkt nutzen

```python
from src.adapters.models import create_db_session, ProductORM

engine, Session = create_db_session("sqlite:///data/warehouse.db")
session = Session()

# Alle Produkte
products = session.query(ProductORM).all()
for product in products:
    print(f"{product.name}: {product.quantity} @ {product.price}€")

# Produkte nach Kategorie
winter_tires = session.query(ProductORM)\
    .filter(ProductORM.category.has(name='Reifen'))\
    .all()

# Bestandsverlauf
from src.adapters.models import MovementORM
movements = session.query(MovementORM)\
    .filter(MovementORM.movement_type == 'IN')\
    .order_by(MovementORM.timestamp.desc())\
    .all()

session.close()
```

### Mit SQL direkt

```bash
# SQLite CLI
sqlite3 data/warehouse.db

# Beispiel-Queries:
SELECT COUNT(*) FROM products;
SELECT * FROM products WHERE quantity < min_stock;
SELECT SUM(quantity * price) FROM products;
SELECT * FROM movements ORDER BY timestamp DESC;
```

## Datei-Übersicht

```
data/
├── schema.sql          # Datenbank-Schema (DDL)
├── dump.sql            # Dump-Daten (DML)
└── warehouse.db        # SQLite Datenbank (wird erstellt)

src/adapters/
├── models.py           # SQLAlchemy ORM-Modelle
└── repository.py       # Repository Implementierungen

scripts/
└── init_database.py    # Datenbank-Initialisierungsskript
```

## Features

✅ **Vollständiges Schema** mit Constraints und Indexes
✅ **Realistische Dump-Daten** (Auto-Zubehör Szenario)
✅ **Historische Daten** (Bewegungen, Snapshots)
✅ **SQLAlchemy ORM** für typischere Nutzung
✅ **Repository Pattern** Integration mit bestehender Architektur
✅ **Audit Trail** für Lagerveränderungen
✅ **Automatische Initialisierung** mit Verifizierung

## Problembehebung

### "database is locked"

Stelle sicher, dass keine anderen Prozesse die Datenbank nutzen.

### "No module named sqlalchemy"

```bash
pip install sqlalchemy
```

### Datenbank zurücksetzen

```bash
# Backup erstellen
mv data/warehouse.db data/warehouse_backup.db

# Neu initialisieren
python scripts/init_database.py
```

## Weitere Infos

- [SQLAlchemy Dokumentation](https://docs.sqlalchemy.org)
- Siehe [docs/architecture.md](../docs/architecture.md) für Architektur-Details
- Siehe [README.md](../README.md) für Projekt-Übersicht
