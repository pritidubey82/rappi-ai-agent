# backend/app/database.py

# Fake ERP System Database
MOCK_DB = {
    "inventory": {
        "SKU-101": {
            "name": "Avocado Hass 1kg",
            "current_stock": 150,
            "max_storage_capacity": 500,  # Max 500 units aane ki jagah hai (Capacity constraint)
            "unit_cost": 3.50,
            "expected_daily_demand": 40
        }
    },
    "budget": {
        "available": 2000.00  # Total available budget $2000
    },
    "suppliers": {
        "SUPP-01": {
            "name": "AgroFresh Logistics",
            "lead_time_days": 2,
            "moq": 100,  # Minimum Order Quantity = 100 units
            "unit_price": 3.50
        }
    },
    "purchase_orders": []
}

# Functions Data Read / Write karne ke liye

def get_inventory(sku: str):
    return MOCK_DB["inventory"].get(sku)

def get_budget():
    return MOCK_DB["budget"]["available"]

def get_supplier(supplier_id: str):
    return MOCK_DB["suppliers"].get(supplier_id)

def create_purchase_order(sku: str, supplier_id: str, quantity: int, cost: float):
    po_id = f"PO-{len(MOCK_DB['purchase_orders']) + 1001}"
    po = {
        "po_id": po_id,
        "sku": sku,
        "supplier_id": supplier_id,
        "quantity": quantity,
        "cost": cost,
        "status": "CREATED"
    }
    MOCK_DB["purchase_orders"].append(po)
    return po