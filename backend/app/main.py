# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.database import get_inventory, get_supplier, get_budget
from app.validator import validate_and_execute_recommendation

app = FastAPI(title="Rappi AI Purchasing Agent API")

# Frontend se connect karne ke liye CORS policy allow karein
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RecommendationRequest(BaseModel):
    sku: str
    supplier_id: str
    recommended_quantity: int

@app.get("/")
def home():
    return {"message": "Rappi AI Purchasing Agent Service is Running!"}

@app.post("/api/v1/evaluate")
def evaluate_recommendation(req: RecommendationRequest):
    inv_data = get_inventory(req.sku)
    supp_data = get_supplier(req.supplier_id)
    curr_budget = get_budget()

    if not inv_data or not supp_data:
        return {"error": "Invalid SKU or Supplier"}

    investigation_report = {
        "current_stock": inv_data["current_stock"],
        "max_capacity": inv_data["max_storage_capacity"],
        "available_space": inv_data["max_storage_capacity"] - inv_data["current_stock"],
        "available_budget": curr_budget,
        "supplier_moq": supp_data["moq"],
        "unit_price": supp_data["unit_price"]
    }

    result = validate_and_execute_recommendation(
        sku=req.sku,
        supplier_id=req.supplier_id,
        quantity=req.recommended_quantity
    )

    return {
        "input_recommendation": req.model_dump(),
        "investigation": investigation_report,
        "decision": result["status"],
        "execution_details": result
    }