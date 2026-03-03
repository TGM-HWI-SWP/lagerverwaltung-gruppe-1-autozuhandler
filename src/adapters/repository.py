"""Repository Adapter - In-Memory und persistente Implementierungen"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.warehouse import Movement
from ..ports import RepositoryPort

try:
    from sqlalchemy.orm import Session
    from .models import Base, ProductORM, MovementORM, init_db, get_database_url, create_db_session
    SQLALCHEMY_AVAILABLE = True
except ImportError:
    SQLALCHEMY_AVAILABLE = False


class InMemoryRepository(RepositoryPort):
    """In-Memory Repository - schnell für Tests und schnelle Prototypen"""

    def __init__(self):
        self.products: Dict[str, Product] = {}
        self.movements: List[Movement] = []

    def save_product(self, product: Product) -> None:
        """Produkt im Memory speichern"""
        self.products[product.id] = product

    def load_product(self, product_id: str) -> Optional[Product]:
        """Produkt aus Memory laden"""
        return self.products.get(product_id)

    def load_all_products(self) -> Dict[str, Product]:
        """Alle Produkte aus Memory laden"""
        return self.products.copy()

    def delete_product(self, product_id: str) -> None:
        """Produkt aus Memory löschen"""
        if product_id in self.products:
            del self.products[product_id]

    def save_movement(self, movement: Movement) -> None:
        """Bewegung im Memory speichern"""
        self.movements.append(movement)

    def load_movements(self) -> List[Movement]:
        """Alle Bewegungen aus Memory laden"""
        return self.movements.copy()


class JsonRepository(RepositoryPort):
    """JSON-basiertes Repository - lädt Testdaten aus JSON-Datei"""

    def __init__(self, json_path: Optional[str] = None):
        self.products: Dict[str, Product] = {}
        self.movements: List[Movement] = []
        
        if json_path is None:
            # Standard: data/testdata.json relativ zum Projektverzeichnis
            json_path = Path(__file__).parent.parent.parent / "data" / "testdata.json"
        
        self.json_path = Path(json_path)
        self._load_from_json()

    def _load_from_json(self) -> None:
        """Daten aus JSON-Datei laden"""
        if not self.json_path.exists():
            return
        
        with open(self.json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # Produkte laden
        for prod_data in data.get("products", []):
            product = Product(
                id=prod_data["product_id"],
                name=prod_data["name"],
                description=prod_data.get("description", ""),
                price=prod_data["price"],
                quantity=prod_data.get("quantity", 0),
                sku=prod_data.get("sku", ""),
                category=prod_data.get("category", ""),
            )
            self.products[product.id] = product
        
        # Bewegungen laden
        for mov_data in data.get("movements", []):
            timestamp = mov_data.get("timestamp")
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            else:
                timestamp = datetime.now()
            
            movement = Movement(
                id=mov_data["id"],
                product_id=mov_data["product_id"],
                product_name=mov_data.get("product_name", ""),
                quantity_change=mov_data["quantity_change"],
                movement_type=mov_data["movement_type"],
                reason=mov_data.get("reason"),
                timestamp=timestamp,
                performed_by=mov_data.get("performed_by", "system"),
            )
            self.movements.append(movement)

    def save_product(self, product: Product) -> None:
        """Produkt speichern"""
        self.products[product.id] = product

    def load_product(self, product_id: str) -> Optional[Product]:
        """Produkt laden"""
        return self.products.get(product_id)

    def load_all_products(self) -> Dict[str, Product]:
        """Alle Produkte laden"""
        return self.products.copy()

    def delete_product(self, product_id: str) -> None:
        """Produkt löschen"""
        if product_id in self.products:
            del self.products[product_id]

    def save_movement(self, movement: Movement) -> None:
        """Bewegung speichern"""
        self.movements.append(movement)

    def load_movements(self) -> List[Movement]:
        """Alle Bewegungen laden"""
        return self.movements.copy()


class RepositoryFactory:
    """Factory für Repository-Instanzen"""

    @staticmethod
    def create_repository(repository_type: str = "memory", db_path: Optional[str] = None) -> RepositoryPort:
        """
        Repository basierend auf Typ erstellen

        Args:
            repository_type: "memory", "json", "sqlite" oder andere
            db_path: Pfad zur SQLite Datenbank (nur für "sqlite")

        Returns:
            RepositoryPort Instanz

        Raises:
            ValueError: Unbekannter Repository-Typ
            ImportError: SQLAlchemy nicht verfügbar für sqlite
        """
        if repository_type == "memory":
            return InMemoryRepository()
        elif repository_type == "json":
            return JsonRepository()
        elif repository_type == "sqlite":
            if not SQLALCHEMY_AVAILABLE:
                raise ImportError(
                    "SQLAlchemy nicht verfügbar. Installiere mit: pip install sqlalchemy"
                )
            if db_path is None:
                db_path = str(Path(__file__).parent.parent.parent / "data" / "warehouse.db")
            return SqliteRepository(db_path)
        else:
            raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")


class SqliteRepository(RepositoryPort):
    """SQLite-basiertes Repository mit SQLAlchemy ORM"""

    def __init__(self, db_path: str):
        """
        Initialisiere SQLite Repository

        Args:
            db_path: Pfad zur SQLite Datenbank-Datei
        """
        if not SQLALCHEMY_AVAILABLE:
            raise ImportError("SQLAlchemy erforderlich für SqliteRepository")

        self.db_path = str(db_path)
        self.db_url = f"sqlite:///{self.db_path}"
        self.engine, self.SessionLocal = create_db_session(self.db_url)
        
        # Stelle sicher, dass Schema existiert
        init_db(self.db_url)

    def _product_orm_to_domain(self, product_orm) -> Optional[Product]:
        """Konvertiere ORM-Produkt zu Domain-Model"""
        if product_orm is None:
            return None
        
        return Product(
            id=product_orm.id,
            name=product_orm.name,
            description=product_orm.description or "",
            price=product_orm.price,
            quantity=product_orm.quantity,
            sku=product_orm.sku,
            category=product_orm.category.name if product_orm.category else "",
            created_at=product_orm.created_at or datetime.now(),
            updated_at=product_orm.updated_at or datetime.now(),
            notes=product_orm.notes,
        )

    def _domain_to_product_orm(self, product: Product):
        """Konvertiere Domain-Model zu ORM-Produkt"""
        return ProductORM(
            id=product.id,
            warehouse_id="WH001",  # Default Warehouse
            sku=product.sku,
            name=product.name,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
            created_at=product.created_at,
            updated_at=product.updated_at,
            notes=product.notes,
        )

    def _movement_orm_to_domain(self, movement_orm) -> Optional[Movement]:
        """Konvertiere ORM-Bewegung zu Domain-Model"""
        if movement_orm is None:
            return None
        
        return Movement(
            id=movement_orm.id,
            product_id=movement_orm.product_id,
            product_name=movement_orm.product.name if movement_orm.product else "",
            quantity_change=movement_orm.quantity_change,
            movement_type=movement_orm.movement_type,
            reason=movement_orm.reason,
            timestamp=movement_orm.timestamp or datetime.now(),
            performed_by=movement_orm.performed_by,
        )

    def _domain_to_movement_orm(self, movement: Movement):
        """Konvertiere Domain-Model zu ORM-Bewegung"""
        return MovementORM(
            id=movement.id,
            product_id=movement.product_id,
            warehouse_id="WH001",  # Default Warehouse
            quantity_change=movement.quantity_change,
            movement_type=movement.movement_type,
            reason=movement.reason,
            timestamp=movement.timestamp,
            performed_by=movement.performed_by,
        )

    def save_product(self, product: Product) -> None:
        """Produkt speichern"""
        session = self.SessionLocal()
        try:
            # Prüfe ob Produkt bereits existiert
            existing = session.query(ProductORM).filter(ProductORM.id == product.id).first()
            
            if existing:
                # Update
                existing.name = product.name
                existing.description = product.description
                existing.price = product.price
                existing.quantity = product.quantity
                existing.sku = product.sku
                existing.updated_at = datetime.now()
            else:
                # Insert
                product_orm = self._domain_to_product_orm(product)
                session.add(product_orm)
            
            session.commit()
        finally:
            session.close()

    def load_product(self, product_id: str) -> Optional[Product]:
        """Produkt laden"""
        session = self.SessionLocal()
        try:
            product_orm = session.query(ProductORM).filter(ProductORM.id == product_id).first()
            return self._product_orm_to_domain(product_orm)
        finally:
            session.close()

    def load_all_products(self) -> Dict[str, Product]:
        """Alle Produkte laden"""
        session = self.SessionLocal()
        try:
            products_orm = session.query(ProductORM).all()
            return {
                product_orm.id: self._product_orm_to_domain(product_orm)
                for product_orm in products_orm
            }
        finally:
            session.close()

    def delete_product(self, product_id: str) -> None:
        """Produkt löschen"""
        session = self.SessionLocal()
        try:
            product_orm = session.query(ProductORM).filter(ProductORM.id == product_id).first()
            if product_orm:
                session.delete(product_orm)
                session.commit()
        finally:
            session.close()

    def save_movement(self, movement: Movement) -> None:
        """Bewegung speichern"""
        session = self.SessionLocal()
        try:
            movement_orm = self._domain_to_movement_orm(movement)
            session.add(movement_orm)
            session.commit()
        finally:
            session.close()

    def load_movements(self) -> List[Movement]:
        """Alle Lagerbewegungen laden"""
        session = self.SessionLocal()
        try:
            movements_orm = session.query(MovementORM).all()
            return [self._movement_orm_to_domain(m) for m in movements_orm]
        finally:
            session.close()

    def close(self) -> None:
        """Datenbank-Verbindung schließen"""
        self.engine.dispose()
    
    def __del__(self):
        """Cleanup bei Destruktion"""
        try:
            self.close()
        except:
            pass

