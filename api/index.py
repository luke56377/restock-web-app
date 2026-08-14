import os
import httpx
from fastapi import FastAPI

app = FastAPI()

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

@app.get("/api/products")
async def search_products(keyword: str = ""):
    if not SUPABASE_URL or not SUPABASE_KEY:
        return []
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + SUPABASE_KEY,
        "Content-Type": "application/json"
    }
    
    url = SUPABASE_URL + "/rest/v1/products?select=*"
    if keyword:
        url += "&or=(code.ilike.*" + keyword + "*,name.ilike.*" + keyword + "*)"
        
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(url, headers=headers)
            if res.status_code == 200:
                return res.json()
            return []
        except Exception as e:
            return []

@app.post("/api/orders")
async def create_order(data: dict):
    if not SUPABASE_URL or not SUPABASE_KEY:
        return {"status": "error", "message": "No database configuration"}
        
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": "Bearer " + SUPABASE_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    
    url = SUPABASE_URL + "/rest/v1/orders"
    
    async with httpx.AsyncClient() as client:
        try:
            res = await client.post(url, headers=headers, json=data)
            if res.status_code in [200, 201]:
                return {"status": "success", "data": res.json()}
            return {"status": "error", "message": res.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}

app = app
