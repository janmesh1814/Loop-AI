from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, List, Optional
import httpx
import asyncio
from datetime import datetime

from .models import Store, Order, StoreMetrics, HealthScore
from .services import HealthScoreService, AnomalyDetectionService

app = FastAPI(title="Restaurant Dashboard API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://loop-ai-vert.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock API base URL
MOCK_API_URL = "http://localhost:3001"

# Initialize services
health_service = HealthScoreService()
anomaly_service = AnomalyDetectionService()

@app.get("/")
async def root():
    return {"message": "Restaurant Dashboard API", "version": "1.0.0"}

@app.get("/api/metrics/store/{store_id}")
async def get_store_metrics(store_id: str) -> StoreMetrics:
    """
    Get performance metrics for a specific store.
    Should fetch data from mock API and calculate metrics.
    """
    # TODO: Implement this endpoint
    # 1. Fetch store data from mock API
    # 2. Fetch recent orders for the store
    # 3. Calculate metrics (success rate, avg processing time, revenue)
    # 4. Return StoreMetrics object
    
    raise HTTPException(status_code=501, detail="Not implemented yet")

@app.get("/api/health-score/{store_id}")
async def get_health_score(store_id: str) -> HealthScore:
    """
    Calculate and return health score for a store.
    This is where you implement your custom algorithm!
    """
    # TODO: Implement your health score algorithm
    # Consider factors like:
    # - Order success rate
    # - Processing time vs average
    # - Revenue trends
    # - Order volume
    # - Error patterns
    
    # For now, return a placeholder
    return HealthScore(
        store_id=store_id,
        score=75,
        status="healthy",
        factors={
            "success_rate": 85,
            "processing_time": 70,
            "revenue_trend": 75
        },
        timestamp=datetime.now()
    )

@app.get("/api/orders/summary")
async def get_orders_summary(
    store_id: Optional[str] = None,
    platform: Optional[str] = None,
    hours: int = 24
) -> Dict:
    """
    Get summary of orders with optional filters.
    """
    # TODO: Implement order summary
    # 1. Fetch orders from mock API with filters
    # 2. Calculate summary statistics
    # 3. Detect any anomalies
    
    return {
        "total_orders": 0,
        "completed": 0,
        "failed": 0,
        "cancelled": 0,
        "anomalies": []
    }

@app.websocket("/ws/orders")
async def websocket_orders(websocket: WebSocket):
    """
    WebSocket endpoint for real-time order updates.
    Connect to mock API WebSocket and forward updates.
    """
    await websocket.accept()
    
    # TODO: Implement WebSocket connection
    # 1. Connect to mock API WebSocket
    # 2. Forward messages to client
    # 3. Handle disconnections
    
    try:
        while True:
            # Placeholder - implement actual WebSocket logic
            await websocket.receive_text()
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        await websocket.close()

@app.get("/api/anomalies/detect")
async def detect_anomalies(store_id: Optional[str] = None) -> List[Dict]:
    """
    Detect operational anomalies across stores.
    """
    # TODO: Implement anomaly detection
    # Check for:
    # - High failure rates (>20%)
    # - Processing time >2x average
    # - No orders for >10 minutes
    
    anomalies = anomaly_service.detect_anomalies(store_id)
    return anomalies

# Helper function to fetch from mock API
async def fetch_from_mock_api(endpoint: str) -> Dict:
    """
    Helper to fetch data from mock API.
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{MOCK_API_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    
# Below are the API's to be developed by me for fetching data from digital ocean.

BASE_URL = "https://assessment-6xdhr.ondigitalocean.app"

async def get_store(store_id: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/stores/{store_id}")
        res.raise_for_status()
        return res.json()

async def get_store_orders(store_id: str, client: httpx.AsyncClient):
    res = await client.get(
        f"{BASE_URL}/api/stores/{store_id}/orders"
    )
    res.raise_for_status()
    return res.json()

async def get_all_stores():
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BASE_URL}/api/stores")
        res.raise_for_status()
        return res.json()

async def get_store_orders_single(store_id: str):
    async with httpx.AsyncClient(timeout=20.0) as client:
        return await get_store_orders(store_id, client)
    
@app.get("/api/dashboard/store/{store_id}")
async def dashboard_store(store_id: str):
    print("Dashboard store function called")

    try:
        store = await get_store(store_id)

        orders_response = await get_store_orders_single(store_id)

        if isinstance(orders_response, dict):
            orders = orders_response.get("orders", [])
        elif isinstance(orders_response, list):
            orders = orders_response
        else:
            orders = []

        return {
            "store": store,
            "orders": orders
        }

    except Exception as e:
        print("DASHBOARD STORE ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
 
@app.get("/api/dashboard/summary")
async def dashboard_summary():
    print("Summary function called")

    try:
        response = await get_all_stores()
        stores = response.get("stores", [])

        semaphore = asyncio.Semaphore(10)
        timeout = httpx.Timeout(20.0)

        async with httpx.AsyncClient(timeout=timeout) as client:

            async def fetch_orders(store):
                store_id = store.get("id")
                if not store_id:
                    return []

                async with semaphore:
                    orders_response = await get_store_orders(store_id, client)
                    return orders_response.get("orders", [])

            tasks = [fetch_orders(store) for store in stores]
            all_orders = await asyncio.gather(*tasks, return_exceptions=True)

        total_orders = 0
        total_revenue = 0.0

        for orders in all_orders:
            if isinstance(orders, Exception):
                continue

            total_orders += len(orders)

            for order in orders:
                try:
                    total_revenue += float(order.get("total_amount", 0))
                except (TypeError, ValueError):
                    continue

        return {
            "stores": stores,
            "totalStores": len(stores),
            "totalOrders": total_orders,
            "totalRevenue": round(total_revenue, 2)
        }

    except Exception as e:
        print("SUMMARY ERROR:", repr(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
