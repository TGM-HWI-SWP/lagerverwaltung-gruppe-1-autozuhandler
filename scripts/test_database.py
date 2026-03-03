#!/usr/bin/env python3
"""
Test Script für Datenbank
Demonstriert die Nutzung der SQLite Datenbank mit verschiedenen Methoden
"""

import sys
from pathlib import Path

# Pfad zum Projekt
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.adapters.repository import RepositoryFactory
from src.adapters.models import (
    create_db_session, ProductORM, MovementORM, UserORM, CategoryORM
)


def test_repository_api():
    """Teste Repository-API"""
    print("\n" + "="*70)
    print("📦 Test: Repository API")
    print("="*70)
    
    db_path = PROJECT_ROOT / "data" / "warehouse.db"
    repo = RepositoryFactory.create_repository(
        repository_type="sqlite",
        db_path=str(db_path)
    )
    
    # Alle Produkte laden
    products = repo.load_all_products()
    print(f"\n✓ Geladen: {len(products)} Produkte")
    
    # Erste 3 Produkte
    for i, (prod_id, product) in enumerate(list(products.items())[:3]):
        print(f"\n  {i+1}. {product.name}")
        print(f"     SKU: {product.sku}")
        print(f"     Preis: €{product.price:.2f}")
        print(f"     Bestand: {product.quantity} Stk")
        total = product.get_total_value()
        print(f"     Wert: €{total:.2f}")
    
    # Bewegungen laden
    movements = repo.load_movements()
    print(f"\n✓ Geladen: {len(movements)} Lagerbewegungen")
    
    for i, mov in enumerate(movements[:3]):
        print(f"\n  {i+1}. {mov.movement_type} ({mov.quantity_change:+d})")
        print(f"     Produkt: {mov.product_name}")
        print(f"     Grund: {mov.reason}")
        print(f"     Von: {mov.performed_by}")
    
    # Gesamtwert berechnen
    total_value = sum(p.get_total_value() for p in products.values())
    print(f"\n📊 Lagerwert: €{total_value:,.2f}")
    
    # Bestandsverwaltung
    print("\n🔍 Bestandsanalyse:")
    low_stock = [p for p in products.values() if p.quantity < 5]
    print(f"   Niedriger Bestand (<5 Stk): {len(low_stock)}")
    for p in low_stock:
        print(f"     - {p.name}: {p.quantity} Stk")
    
    high_stock = [p for p in products.values() if p.quantity > 50]
    print(f"   Hoher Bestand (>50 Stk): {len(high_stock)}")
    for p in high_stock:
        print(f"     - {p.name}: {p.quantity} Stk")


def test_orm_api():
    """Teste SQLAlchemy ORM API"""
    print("\n" + "="*70)
    print("🗄️ Test: SQLAlchemy ORM API")
    print("="*70)
    
    db_url = f"sqlite:///{PROJECT_ROOT}/data/warehouse.db"
    engine, SessionLocal = create_db_session(db_url)
    session = SessionLocal()
    
    try:
        # Produkte pro Kategorie
        print("\n📚 Produkte nach Kategorie:")
        categories = session.query(CategoryORM).all()
        for cat in categories[:5]:
            products = session.query(ProductORM).filter(ProductORM.category_id == cat.id).all()
            print(f"\n  {cat.name}:")
            for p in products:
                stock_status = "✓" if p.quantity >= p.min_stock else "⚠"
                print(f"    {stock_status} {p.name}: {p.quantity} Stk @ €{p.price:.2f}")
        
        # Bewegungen zeitlich
        print("\n⏱️ Aktuelle Lagerbewegungen:")
        movements = session.query(MovementORM)\
            .order_by(MovementORM.timestamp.desc())\
            .limit(5)\
            .all()
        
        for mov in movements:
            emoji = "📥" if mov.movement_type == "IN" else "📤"
            print(f"\n  {emoji} {mov.movement_type} ({mov.quantity_change:+d})")
            print(f"     {mov.product.name if mov.product else 'Unbekannt'}")
            print(f"     Grund: {mov.reason}")
            print(f"     Zeit: {mov.timestamp}")
        
        # Benutzer
        print("\n👥 Mitarbeiter:")
        users = session.query(UserORM).all()
        for user in users:
            role_emoji = {
                'admin': '👨‍💼',
                'lagerleiter': '👨‍🔧',
                'mitarbeiter': '👤',
                'viewer': '👁️'
            }.get(user.role, '❓')
            print(f"  {role_emoji} {user.username}: {user.full_name} ({user.role})")
        
        # Statistik
        print("\n📊 Datenbankstatistik:")
        product_count = session.query(ProductORM).count()
        movement_count = session.query(MovementORM).count()
        user_count = session.query(UserORM).count()
        category_count = session.query(CategoryORM).count()
        
        print(f"  Produkte: {product_count}")
        print(f"  Bewegungen: {movement_count}")
        print(f"  Benutzer: {user_count}")
        print(f"  Kategorien: {category_count}")
        
        # Top 5 wertvollste Produkte
        print("\n💰 Top 5 wertvollste Artikel:")
        top_products = sorted(
            session.query(ProductORM).all(),
            key=lambda p: p.get_total_value(),
            reverse=True
        )[:5]
        
        for i, p in enumerate(top_products, 1):
            print(f"  {i}. {p.name}: €{p.get_total_value():,.2f}")
    
    finally:
        session.close()


def test_sql_queries():
    """Teste direkte SQL Queries"""
    print("\n" + "="*70)
    print("🔍 Test: SQL Queries")
    print("="*70)
    
    import sqlite3
    
    db_path = PROJECT_ROOT / "data" / "warehouse.db"
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    try:
        # Query 1: Gesamtbestand
        cursor.execute("SELECT COUNT(*) as count FROM products")
        count = cursor.fetchone()[0]
        print(f"\n✓ Gesamtzahl Produkte: {count}")
        
        # Query 2: Bestand mit Wert
        cursor.execute("""
            SELECT name, quantity, price, quantity * price as total_value
            FROM products
            ORDER BY total_value DESC
            LIMIT 5
        """)
        print("\n✓ Top 5 Produkte nach Lagerwert:")
        for name, qty, price, total in cursor.fetchall():
            print(f"  {name}: {qty} x €{price:.2f} = €{total:.2f}")
        
        # Query 3: Bewegungen pro Typ
        cursor.execute("""
            SELECT movement_type, COUNT(*) as count, SUM(quantity_change) as total
            FROM movements
            GROUP BY movement_type
        """)
        print("\n✓ Lagerbewegungen nach Typ:")
        for mov_type, count, total in cursor.fetchall():
            print(f"  {mov_type}: {count} Bewegungen ({total:+d} Stk)")
        
        # Query 4: Niedrig Bestand
        cursor.execute("""
            SELECT name, quantity, min_stock
            FROM products
            WHERE quantity < min_stock
            ORDER BY quantity ASC
        """)
        low_stock = cursor.fetchall()
        if low_stock:
            print(f"\n⚠️ Produkte mit niedrigem Bestand ({len(low_stock)}):")
            for name, qty, min_s in low_stock:
                print(f"  {name}: {qty} / {min_s} Stk")
        else:
            print(f"\n✓ Alle Produkte haben ausreichenden Bestand")
    
    finally:
        conn.close()


def main():
    print("\n" + "🏭 "*20)
    print("  Warehouse Management System - Datenbanktest")
    print("🏭 "*20)
    
    db_path = PROJECT_ROOT / "data" / "warehouse.db"
    
    if not db_path.exists():
        print(f"\n❌ Datenbank nicht gefunden: {db_path}")
        print("\n Initialisiere mit:")
        print(f"   python scripts/init_database.py")
        return False
    
    try:
        test_repository_api()
        test_orm_api()
        test_sql_queries()
        
        print("\n" + "="*70)
        print("✅ Alle Tests erfolgreich!")
        print("="*70 + "\n")
        return True
    
    except Exception as e:
        print(f"\n❌ Fehler: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
