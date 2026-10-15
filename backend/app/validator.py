# backend/app/validator.py
from app.database import MOCK_DB, create_purchase_order

def validate_and_execute_recommendation(sku: str, supplier_id: str, quantity: int):
    inventory = MOCK_DB["inventory"].get(sku)
    supplier = MOCK_DB["suppliers"].get(supplier_id)
    budget = MOCK_DB["budget"]["available"]

    if not inventory or not supplier:
        return {
            "status": "REJECTED",
            "executed_quantity": 0,
            "reason": "Invalid SKU or Supplier ID.",
            "purchase_order": None
        }

    # Constraint Checks
    current_stock = inventory["current_stock"]
    max_capacity = inventory["max_storage_capacity"]
    available_space = max_capacity - current_stock
    moq = supplier["moq"]
    unit_price = supplier["unit_price"]

    # 1. Check MOQ
    if quantity < moq:
        return {
            "status": "REJECTED",
            "executed_quantity": 0,
            "reason": f"Quantity {quantity} is below supplier Minimum Order Quantity ({moq}).",
            "purchase_order": None
        }

    # 2. Check Storage Space
    target_quantity = quantity
    status = "ACCEPTED"
    reason = f"Accepted purchase recommendation of {quantity} units."

    if quantity > available_space:
        target_quantity = available_space
        status = "MODIFIED"
        reason = f"Original request of {quantity} units was reduced to {available_space} due to storage capacity limits."

    # 3. Check Budget
    total_cost = target_quantity * unit_price
    if total_cost > budget:
        max_affordable = int(budget // unit_price)
        if max_affordable < moq:
            return {
                "status": "REJECTED",
                "executed_quantity": 0,
                "reason": f"Insufficient budget (${budget}) to satisfy MOQ ({moq} units = ${moq * unit_price}).",
                "purchase_order": None
            }
        target_quantity = max_affordable
        status = "MODIFIED"
        reason = f"Quantity adjusted to {target_quantity} units to fit within available budget (${budget})."

    # Execute Action (Create Purchase Order)
    po = create_purchase_order(sku, supplier_id, target_quantity, unit_price)

    return {
        "status": status,
        "executed_quantity": target_quantity,
        "reason": reason,
        "purchase_order": po
    }