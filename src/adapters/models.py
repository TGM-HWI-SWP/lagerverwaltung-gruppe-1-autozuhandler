"""SQLAlchemy ORM Models für SQLite Datenbank"""

from datetime import datetime
from sqlalchemy import (
    Column, String, Float, Integer, DateTime, Text, Boolean, 
    ForeignKey, CheckConstraint, Index, create_engine
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from typing import Optional

Base = declarative_base()


class UserORM(Base):
    """Benutzer/Mitarbeiter des Lagers"""
    __tablename__ = 'users'
    
    id = Column(String(50), primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(255))
    email = Column(String(100))
    role = Column(String(50), default='mitarbeiter')
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    
    movements = relationship("MovementORM", back_populates="user")
    
    def __repr__(self):
        return f"<User {self.username} ({self.role})>"


class WarehouseORM(Base):
    """Lagerhalle/Lagerstandort"""
    __tablename__ = 'warehouses'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    location = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    products = relationship("ProductORM", back_populates="warehouse")
    movements = relationship("MovementORM", back_populates="warehouse")
    snapshots = relationship("InventorySnapshotORM", back_populates="warehouse")
    
    def __repr__(self):
        return f"<Warehouse {self.name}>"


class CategoryORM(Base):
    """Produktkategorie"""
    __tablename__ = 'categories'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.now)
    
    products = relationship("ProductORM", back_populates="category")
    
    def __repr__(self):
        return f"<Category {self.name}>"


class BrandORM(Base):
    """Produkthersteller/Marke"""
    __tablename__ = 'brands'
    
    id = Column(String(50), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    country = Column(String(100))
    website = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)
    
    products = relationship("ProductORM", back_populates="brand")
    
    def __repr__(self):
        return f"<Brand {self.name}>"


class ProductORM(Base):
    """Produkt im Lager"""
    __tablename__ = 'products'
    
    id = Column(String(50), primary_key=True)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id'), nullable=False)
    sku = Column(String(100), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    category_id = Column(String(50), ForeignKey('categories.id'))
    brand_id = Column(String(50), ForeignKey('brands.id'))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, default=0)
    location = Column(String(50))
    min_stock = Column(Integer, default=5)
    max_stock = Column(Integer, default=1000)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    notes = Column(Text)
    
    warehouse = relationship("WarehouseORM", back_populates="products")
    category = relationship("CategoryORM", back_populates="products")
    brand = relationship("BrandORM", back_populates="products")
    movements = relationship("MovementORM", back_populates="product")
    snapshots = relationship("InventorySnapshotORM", back_populates="product")
    
    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
        CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
        Index('idx_products_warehouse', 'warehouse_id'),
        Index('idx_products_category', 'category_id'),
        Index('idx_products_brand', 'brand_id'),
        Index('idx_products_sku', 'sku'),
    )
    
    def __repr__(self):
        return f"<Product {self.sku}: {self.name} (Qty: {self.quantity})>"
    
    def get_total_value(self) -> float:
        """Gesamtwert des Produktbestands berechnen"""
        return self.price * self.quantity
    
    def is_low_stock(self) -> bool:
        """Prüfe ob Bestand unter Minimum ist"""
        return self.quantity < self.min_stock
    
    def is_overstocked(self) -> bool:
        """Prüfe ob Bestand über Maximum ist"""
        return self.quantity > self.max_stock


class MovementORM(Base):
    """Lagerbewegung (IN/OUT/CORRECTION/ADJUSTMENT)"""
    __tablename__ = 'movements'
    
    id = Column(String(50), primary_key=True)
    product_id = Column(String(50), ForeignKey('products.id'), nullable=False)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id'), nullable=False)
    quantity_change = Column(Integer, nullable=False)
    movement_type = Column(String(20), nullable=False)
    reason = Column(Text)
    performed_by = Column(String(100), ForeignKey('users.id'), default='system')
    timestamp = Column(DateTime, default=datetime.now)
    
    product = relationship("ProductORM", back_populates="movements")
    warehouse = relationship("WarehouseORM", back_populates="movements")
    user = relationship("UserORM", back_populates="movements")
    histories = relationship("MovementHistoryORM", back_populates="movement")
    
    __table_args__ = (
        CheckConstraint(
            "movement_type IN ('IN', 'OUT', 'CORRECTION', 'ADJUSTMENT')",
            name='check_movement_type'
        ),
        Index('idx_movements_product', 'product_id'),
        Index('idx_movements_warehouse', 'warehouse_id'),
        Index('idx_movements_timestamp', 'timestamp'),
        Index('idx_movements_user', 'performed_by'),
    )
    
    def __repr__(self):
        return f"<Movement {self.movement_type}: {self.quantity_change} ({self.id})>"


class MovementHistoryORM(Base):
    """Historischer Bestandsverlauf für Auditing"""
    __tablename__ = 'movement_history'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    movement_id = Column(String(50), ForeignKey('movements.id'), nullable=False)
    product_id = Column(String(50), ForeignKey('products.id'), nullable=False)
    quantity_before = Column(Integer)
    quantity_after = Column(Integer)
    timestamp = Column(DateTime, default=datetime.now)
    
    movement = relationship("MovementORM", back_populates="histories")
    product = relationship("ProductORM")
    
    def __repr__(self):
        return f"<MovementHistory {self.product_id}: {self.quantity_before} -> {self.quantity_after}>"


class InventorySnapshotORM(Base):
    """Tägliche Bestandsabbildung für Reporting"""
    __tablename__ = 'inventory_snapshots'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    warehouse_id = Column(String(50), ForeignKey('warehouses.id'), nullable=False)
    product_id = Column(String(50), ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer)
    total_value = Column(Float)
    snapshot_date = Column(String(10), nullable=False)  # YYYY-MM-DD Format
    
    warehouse = relationship("WarehouseORM", back_populates="snapshots")
    product = relationship("ProductORM", back_populates="snapshots")
    
    __table_args__ = (
        Index('idx_inventory_snapshots_date', 'snapshot_date'),
    )
    
    def __repr__(self):
        return f"<InventorySnapshot {self.product_id} on {self.snapshot_date}: {self.quantity} units>"


def get_database_url(db_path: str = "warehouse.db") -> str:
    """Erzeugt SQLite Connection String"""
    return f"sqlite:///{db_path}"


def create_db_session(db_url: str = None):
    """Erstellt SQLAlchemy Session für Datenbank-Operationen"""
    if db_url is None:
        db_url = get_database_url()
    
    engine = create_engine(db_url, echo=False)
    Session = sessionmaker(bind=engine)
    return engine, Session


def init_db(db_url: str = None):
    """Initialisiert Datenbank-Schema"""
    if db_url is None:
        db_url = get_database_url()
    
    engine = create_engine(db_url, echo=False)
    Base.metadata.create_all(engine)
    return engine

