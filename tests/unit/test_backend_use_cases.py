"""Unit Tests - Backend Use Cases"""

from src.adapters.repository import InMemoryRepository
from src.backend import WarehouseUseCases


class TestWarehouseUseCases:
    """Tests fuer die Kern-Use-Cases"""

    def setup_method(self):
        self.repo = InMemoryRepository()
        self.use_cases = WarehouseUseCases(self.repo)

    def test_crud_product(self):
        created = self.use_cases.create_product(
            product_id="P100",
            name="Test Produkt",
            description="Desc",
            price=12.5,
            category="Test",
            quantity=4,
            sku="SKU-1",
        )
        assert created.id == "P100"

        fetched = self.use_cases.read_product("P100")
        assert fetched is not None
        assert fetched.name == "Test Produkt"

        updated = self.use_cases.update_product(
            "P100", name="Neu", price=15.0, quantity=7
        )
        assert updated.name == "Neu"
        assert updated.price == 15.0
        assert updated.quantity == 7

        deleted = self.use_cases.delete_product("P100")
        assert deleted is True
        assert self.use_cases.read_product("P100") is None

    def test_generate_inventory_report(self):
        self.use_cases.create_product(
            product_id="P001",
            name="A",
            description="",
            price=10.0,
            quantity=5,
        )
        self.use_cases.create_product(
            product_id="P002",
            name="B",
            description="",
            price=3.0,
            quantity=4,
        )

        report = self.use_cases.generate_inventory_report()

        assert report["title"] == "Lagerstandsreport"
        assert len(report["items"]) == 2
        assert report["total_value"] == 10.0 * 5 + 3.0 * 4

    def test_list_products_filtered(self):
        self.use_cases.create_product(
            product_id="A-1",
            name="Batterie 12V",
            description="",
            price=50.0,
            quantity=2,
            category="Batterien",
        )
        self.use_cases.create_product(
            product_id="B-2",
            name="Reifen 18 Zoll",
            description="",
            price=100.0,
            quantity=1,
            category="Reifen",
        )

        result = self.use_cases.list_products(search="batt", category="Batterien")
        assert list(result.keys()) == ["A-1"]

    def test_create_product_records_movement(self):
        self.use_cases.create_product(
            product_id="M-1",
            name="Oel",
            description="",
            price=10.0,
            quantity=3,
            category="Oel & Fluessigkeiten",
        )

        movements = self.use_cases.list_movements()
        assert len(movements) == 1
        assert movements[0].movement_type == "IN"
