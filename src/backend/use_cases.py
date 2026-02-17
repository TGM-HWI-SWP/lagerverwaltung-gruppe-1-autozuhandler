"""Backend Use Cases - Kernlogik"""

from datetime import datetime
from typing import Dict, List, Optional

from ..domain.product import Product
from ..domain.warehouse import Movement
from ..ports import RepositoryPort


class WarehouseUseCases:
    """Kern-Use-Cases der Lagerverwaltung"""

    def __init__(self, repository: RepositoryPort):
        self.repository = repository

    # CRUD
    def create_product(
        self,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category: str = "",
        quantity: int = 0,
        sku: str = "",
        notes: Optional[str] = None,
    ) -> Product:
        if self.repository.load_product(product_id) is not None:
            raise ValueError(f"Produkt mit ID {product_id} existiert bereits")

        product = Product(
            id=product_id,
            name=name,
            description=description,
            price=price,
            quantity=quantity,
            category=category,
            sku=sku,
            notes=notes,
        )
        self.repository.save_product(product)
        if quantity > 0:
            movement = Movement(
                id=f"mov_{datetime.now().timestamp()}",
                product_id=product_id,
                product_name=name,
                quantity_change=quantity,
                movement_type="IN",
                reason="Startbestand",
                performed_by="system",
            )
            self.repository.save_movement(movement)
        return product

    def read_product(self, product_id: str) -> Optional[Product]:
        return self.repository.load_product(product_id)

    def list_products(
        self, search: str = "", category: str = "Alle"
    ) -> Dict[str, Product]:
        products = self.repository.load_all_products()
        search = (search or "").strip().lower()
        category = (category or "").strip()

        if not search and (not category or category == "Alle"):
            return products

        filtered: Dict[str, Product] = {}
        for product_id, product in products.items():
            if category and category != "Alle" and product.category != category:
                continue
            if search:
                hay = f"{product_id} {product.name}".lower()
                if search not in hay:
                    continue
            filtered[product_id] = product

        return filtered

    def update_product(
        self,
        product_id: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
        price: Optional[float] = None,
        category: Optional[str] = None,
        quantity: Optional[int] = None,
        sku: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Product:
        product = self.repository.load_product(product_id)
        if product is None:
            raise ValueError(f"Produkt {product_id} nicht gefunden")

        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            if price < 0:
                raise ValueError("Preis kann nicht negativ sein")
            product.price = price
        if category is not None:
            product.category = category
        quantity_delta = 0
        if quantity is not None:
            if quantity < 0:
                raise ValueError("Bestand kann nicht negativ sein")
            quantity_delta = quantity - product.quantity
            product.quantity = quantity
        if sku is not None:
            product.sku = sku
        if notes is not None:
            product.notes = notes

        product.updated_at = datetime.now()
        self.repository.save_product(product)
        if quantity_delta:
            movement = Movement(
                id=f"mov_{datetime.now().timestamp()}",
                product_id=product.id,
                product_name=product.name,
                quantity_change=quantity_delta,
                movement_type="CORRECTION",
                reason="Bestandskorrektur",
                performed_by="system",
            )
            self.repository.save_movement(movement)
        return product

    def delete_product(self, product_id: str) -> bool:
        if self.repository.load_product(product_id) is None:
            return False
        self.repository.delete_product(product_id)
        return True

    def list_movements(self) -> List[Movement]:
        return self.repository.load_movements()

    # Report A: Lagerstandsreport
    def generate_inventory_report(self) -> Dict[str, object]:
        products = self.repository.load_all_products()
        items: List[Dict[str, object]] = []
        total_value = 0.0

        for product_id, product in products.items():
            item_total = product.get_total_value()
            total_value += item_total
            items.append(
                {
                    "id": product_id,
                    "name": product.name,
                    "quantity": product.quantity,
                    "price": product.price,
                    "total_value": item_total,
                }
            )

        return {
            "title": "Lagerstandsreport",
            "generated_at": datetime.now(),
            "items": items,
            "total_value": total_value,
        }

    def generate_inventory_report_text(self) -> str:
        from ..adapters.report import ConsoleReportAdapter

        products = self.repository.load_all_products()
        movements = self.repository.load_movements()
        adapter = ConsoleReportAdapter(products, movements)
        return adapter.generate_inventory_report()

    def generate_movement_report_text(self) -> str:
        from ..adapters.report import ConsoleReportAdapter

        products = self.repository.load_all_products()
        movements = self.repository.load_movements()
        adapter = ConsoleReportAdapter(products, movements)
        return adapter.generate_movement_report()
