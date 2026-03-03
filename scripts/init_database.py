#!/usr/bin/env python3
"""
Database Initialization Script
Initialisiert die SQLite Datenbank mit Schema und Dump-Daten
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Pfade
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"
SCHEMA_FILE = DATA_DIR / "schema.sql"
DUMP_FILE = DATA_DIR / "dump.sql"
DB_FILE = DATA_DIR / "warehouse.db"


def execute_sql_file(conn: sqlite3.Connection, sql_file: Path, verbose: bool = True) -> None:
    """Führt SQL-Datei aus"""
    if not sql_file.exists():
        raise FileNotFoundError(f"SQL-Datei nicht gefunden: {sql_file}")
    
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # Teile in einzelne Statements auf (vereinfacht)
    statements = [s.strip() for s in sql_content.split(';') if s.strip()]
    
    cursor = conn.cursor()
    for i, statement in enumerate(statements, 1):
        try:
            cursor.execute(statement)
            if verbose and i % 10 == 0:
                print(f"  ✓ {i}/{len(statements)} Statements ausgeführt")
        except sqlite3.Error as e:
            print(f"  ✗ Fehler bei Statement {i}: {e}")
            print(f"    {statement[:100]}...")
            raise
    
    conn.commit()
    if verbose:
        print(f"  ✓ Alle {len(statements)} Statements erfolgreich ausgeführt")


def check_database_exists(db_path: Path) -> bool:
    """Prüft ob Datenbank bereits existiert"""
    return db_path.exists() and db_path.stat().st_size > 0


def backup_existing_database(db_path: Path) -> Path:
    """Erstellt Backup der existierenden Datenbank"""
    if db_path.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = db_path.parent / f"warehouse_backup_{timestamp}.db"
        db_path.rename(backup_path)
        print(f"✓ Backup erstellt: {backup_path}")
        return backup_path
    return None


def verify_database(db_path: Path) -> bool:
    """Verifiziert dass Datenbank korrekt initialisiert wurde"""
    try:
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()
        
        # Prüfe Tabellen
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        expected_tables = [
            'warehouses', 'categories', 'brands', 'products', 'movements',
            'movement_history', 'users', 'inventory_snapshots'
        ]
        
        existing_tables = [t[0] for t in tables]
        
        for table in expected_tables:
            if table not in existing_tables:
                print(f"  ✗ Tabelle '{table}' nicht gefunden")
                return False
            
            # Zähle Zeilen
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            
            if count > 0:
                print(f"  ✓ Tabelle '{table}': {count} Zeilen")
            else:
                print(f"  ⊘ Tabelle '{table}': leer")
        
        conn.close()
        return True
    
    except sqlite3.Error as e:
        print(f"  ✗ Datenbank-Verifizierung fehlgeschlagen: {e}")
        return False


def init_database(db_path: Path = DB_FILE, force: bool = False, backup: bool = True) -> bool:
    """
    Hauptfunktion zur Datenbank-Initialisierung
    
    Args:
        db_path: Pfad zur Datenbank-Datei
        force: Überschreibe existierende Datenbank
        backup: Erstelle Backup bei Überschreibung
    
    Returns:
        True bei Erfolg, False bei Fehler
    """
    
    print("\n" + "=" * 70)
    print("Warehouse Management System - Datenbank Initialisierung")
    print("=" * 70 + "\n")
    
    # Prüfe Datenbank-Existenz
    if check_database_exists(db_path):
        if not force:
            print(f"⚠ Datenbank existiert bereits: {db_path}")
            print("  Verwende --force um zu überschreiben")
            return False
        
        if backup:
            backup_existing_database(db_path)
        else:
            db_path.unlink()
            print(f"✓ Existierende Datenbank gelöscht")
    
    # Erstelle Datenbank-Verzeichnis falls nötig
    db_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Datenbank-Datei: {db_path}\n")
    
    try:
        # Verbindung erstellen
        conn = sqlite3.connect(str(db_path))
        
        # Schema laden
        print("1️⃣  Lade Schema...")
        execute_sql_file(conn, SCHEMA_FILE, verbose=False)
        print("  ✓ Schema erfolgreich laden\n")
        
        # Dump-Daten laden
        print("2️⃣  Lade Dump-Daten...")
        execute_sql_file(conn, DUMP_FILE, verbose=False)
        print("  ✓ Dump-Daten erfolgreich geladen\n")
        
        conn.close()
        
        # Verifiziere
        print("3️⃣  Verifiziere Datenbank...")
        if verify_database(db_path):
            print("\n" + "=" * 70)
            print("✅ Datenbank erfolgreich initialisiert!")
            print("=" * 70 + "\n")
            
            # Statistik
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            products = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM movements")
            movements = cursor.fetchone()[0]
            cursor.execute("SELECT SUM(quantity * price) FROM products")
            total_value = cursor.fetchone()[0] or 0
            conn.close()
            
            print(f"📊 Lager-Statistik:")
            print(f"   • {products} Produkte")
            print(f"   • {movements} Lagerbewegungen")
            print(f"   • Gesamtwert: {total_value:,.2f} €\n")
            
            return True
        else:
            print("\n⚠ Verifikation fehlgeschlagen")
            return False
    
    except Exception as e:
        print(f"\n❌ Fehler bei Datenbank-Initialisierung: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Initialisiert Warehouse Management Datenbank"
    )
    parser.add_argument(
        "--db",
        type=str,
        default=str(DB_FILE),
        help=f"Datenbank-Datei (Standard: {DB_FILE})"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Überschreibe existierende Datenbank"
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Erstelle kein Backup bei Überschreibung"
    )
    
    args = parser.parse_args()
    
    success = init_database(
        db_path=Path(args.db),
        force=args.force,
        backup=not args.no_backup
    )
    
    sys.exit(0 if success else 1)
