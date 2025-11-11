import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from schemas import Pizza, Order
from database import db, create_document, get_documents

app = FastAPI(title="Pizza API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Pizza API running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

# Pizza endpoints
@app.get("/api/pizzas")
def list_pizzas():
    pizzas = get_documents("pizza")
    for p in pizzas:
        p["_id"] = str(p["_id"])  # serialize ObjectId
    return pizzas

@app.post("/api/pizzas")
def create_pizza(pizza: Pizza):
    pizza_id = create_document("pizza", pizza)
    return {"id": pizza_id}

@app.post("/api/pizzas/seed")
def seed_pizzas():
    # If there are already pizzas, skip seeding
    existing = get_documents("pizza", {}, limit=1)
    if existing:
        return {"seeded": False, "message": "Menu already has items"}

    defaults = [
        Pizza(
            name="Margherita",
            description="Classic tomato, mozzarella, basil",
            price_small=7.0,
            price_medium=9.5,
            price_large=12.0,
            vegetarian=True,
            image="https://images.unsplash.com/photo-1548366086-7a0f1f1a557d?q=80&w=1200&auto=format&fit=crop"
        ),
        Pizza(
            name="Pepperoni",
            description="Loaded with pepperoni and mozzarella",
            price_small=8.0,
            price_medium=11.0,
            price_large=13.5,
            vegetarian=False,
            image="https://images.unsplash.com/photo-1604068549290-de188494b9a6?q=80&w=1200&auto=format&fit=crop"
        ),
        Pizza(
            name="Veggie Supreme",
            description="Bell peppers, onions, olives, mushrooms",
            price_small=8.5,
            price_medium=11.5,
            price_large=14.0,
            vegetarian=True,
            image="https://images.unsplash.com/photo-1506354666786-959d6d497f1a?q=80&w=1200&auto=format&fit=crop"
        ),
        Pizza(
            name="BBQ Chicken",
            description="BBQ sauce, chicken, red onions, cilantro",
            price_small=9.0,
            price_medium=12.5,
            price_large=15.0,
            vegetarian=False,
            image="https://images.unsplash.com/photo-1548365328-9f547fb09530?q=80&w=1200&auto=format&fit=crop"
        ),
    ]

    for p in defaults:
        create_document("pizza", p)

    return {"seeded": True, "count": len(defaults)}

# Orders
@app.post("/api/orders")
def create_order(order: Order):
    if not order.items or len(order.items) == 0:
        raise HTTPException(status_code=400, detail="Order must contain at least one item")
    order_id = create_document("order", order)
    return {"id": order_id, "status": "received"}

@app.get("/api/orders")
def list_orders():
    orders = get_documents("order")
    for o in orders:
        o["_id"] = str(o["_id"])  # serialize ObjectId
    return orders

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
