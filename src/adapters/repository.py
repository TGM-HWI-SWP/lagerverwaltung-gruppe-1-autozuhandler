"""Repository Adapter - In-Memory und persistente Implementierungen"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.warehouse import Movement
from ..ports import RepositoryPort


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
    def create_repository(repository_type: str = "memory") -> RepositoryPort:
        """
        Repository basierend auf Typ erstellen

        Args:
            repository_type: "memory", "json" oder andere (z.B. "sqlite")

        Returns:
            RepositoryPort Instanz
        """
        if repository_type == "memory":
            return InMemoryRepository()
        elif repository_type == "json":
            return JsonRepository()
        else:
            raise ValueError(f"Unbekannter Repository-Typ: {repository_type}")
