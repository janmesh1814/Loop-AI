import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI()
BASE_URL = "https://assessment-6xdhr.ondigitalocean.app/"

async def get_store(store_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/stores/{store_id}")
        res.raise_for_status()
        return res.json()

async def get_store_orders(store_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/stores/{store_id}/orders")
        res.raise_for_status()
        return res.json()

async def get_all_stores():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/stores")
        res.raise_for_status()
        return res.json()


@app.get("/api/dashboard/store/{store_id}")
async def dashboard_store(store_id: str):
    print("Dashboard store Function called")
    try:
        store = await get_store(store_id)
        orders = await get_store_orders(store_id)
        return {
            "store": store,
            "orders": orders
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/dashboard/summary")
async def dashboard_summary():
    print("Summary function called")
    try:
        stores = await get_all_stores()

        total_stores = len(stores)
        total_orders = 0
        total_revenue = 0.0

        for store in stores:
            orders = await get_store_orders(store["id"])
            total_orders += len(orders)
            for order in orders:
                total_revenue += order.get("amount", 0)

        return {
            "totalStores": total_stores,
            "totalOrders": total_orders,
            "totalRevenue": round(total_revenue, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
