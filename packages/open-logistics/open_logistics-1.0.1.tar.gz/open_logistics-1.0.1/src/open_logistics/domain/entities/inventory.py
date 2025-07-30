"""
Domain entities for inventory management.
"""
from typing import Dict, Optional
from pydantic import BaseModel, Field

class InventoryItem(BaseModel):
    """Represents a single item in the inventory."""
    product_id: str
    quantity: int = Field(..., ge=0)
    location: str
    metadata: Optional[Dict] = None

class Inventory(BaseModel):
    """Represents the entire inventory for a location or the whole supply chain."""
    items: Dict[str, InventoryItem] = {}

    def add_item(self, item: InventoryItem):
        """Adds or updates an item in the inventory."""
        self.items[item.product_id] = item

    def get_item(self, product_id: str) -> Optional[InventoryItem]:
        """Retrieves an item from the inventory."""
        return self.items.get(product_id)

    def get_total_quantity(self) -> int:
        """Calculates the total quantity of all items."""
        return sum(item.quantity for item in self.items.values()) 