# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Restaurant Ordering API", version="1.0.0")

# CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class MenuItem(BaseModel):
    id: int
    name: str
    price: float
    category: str
    available: bool = True

class OrderItem(BaseModel):
    item_id: int
    quantity: int
    notes: Optional[str] = None

class Order(BaseModel):
    id: int
    table_number: Optional[int] = None
    items: List[OrderItem]
    status: str = "pending"  # pending, preparing, ready, completed

# Sample data
sample_menu = [
    MenuItem(id=1, name="Classic Burger", price=12.99, category="mains"),
    MenuItem(id=2, name="French Fries", price=4.99, category="sides"),
    MenuItem(id=3, name="Soda", price=2.99, category="drinks"),
]

@app.get("/")
async def root():
    return {"message": "Restaurant Ordering API is running!"}

@app.get("/api/menu", response_model=List[MenuItem])
async def get_menu():
    return sample_menu

@app.get("/api/menu/{category}")
async def get_menu_by_category(category: str):
    return [item for item in sample_menu if item.category == category]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)