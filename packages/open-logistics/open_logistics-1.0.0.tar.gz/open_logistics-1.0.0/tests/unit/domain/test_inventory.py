"""
Unit tests for inventory domain entities.
"""
import pytest
from open_logistics.domain.entities.inventory import Inventory, InventoryItem

class TestInventory:
    """Tests for the Inventory aggregate."""

    def test_add_item(self):
        """Test adding an item to the inventory."""
        inventory = Inventory()
        item = InventoryItem(product_id="P1", quantity=10, location="L1")
        inventory.add_item(item)
        assert inventory.get_item("P1") == item
        assert inventory.get_total_quantity() == 10

    def test_update_item(self):
        """Test updating an item in the inventory."""
        inventory = Inventory()
        item1 = InventoryItem(product_id="P1", quantity=10, location="L1")
        inventory.add_item(item1)
        item2 = InventoryItem(product_id="P1", quantity=20, location="L1")
        inventory.add_item(item2)
        assert inventory.get_item("P1").quantity == 20
        assert inventory.get_total_quantity() == 20

    def test_get_item(self):
        """Test retrieving an item."""
        inventory = Inventory()
        item = InventoryItem(product_id="P1", quantity=10, location="L1")
        inventory.add_item(item)
        assert inventory.get_item("P1") == item
        assert inventory.get_item("P2") is None

    def test_get_total_quantity(self):
        """Test calculating total quantity."""
        inventory = Inventory()
        inventory.add_item(InventoryItem(product_id="P1", quantity=10, location="L1"))
        inventory.add_item(InventoryItem(product_id="P2", quantity=5, location="L1"))
        assert inventory.get_total_quantity() == 15
        
    def test_empty_inventory(self):
        """Test an empty inventory."""
        inventory = Inventory()
        assert inventory.get_total_quantity() == 0
        assert inventory.get_item("P1") is None

class TestInventoryItem:
    """Tests for the InventoryItem entity."""

    def test_create_inventory_item(self):
        """Test creating a valid inventory item."""
        item = InventoryItem(product_id="P1", quantity=100, location="L1")
        assert item.product_id == "P1"
        assert item.quantity == 100

    def test_create_invalid_inventory_item(self):
        """Test creating an item with a negative quantity."""
        with pytest.raises(ValueError):
            InventoryItem(product_id="P1", quantity=-10, location="L1") 