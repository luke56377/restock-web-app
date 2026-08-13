import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

# 讀取環境變數
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase error: {e}")

@app.get("/api/products")
def search_products(keyword: str = ""):
    if not supabase:
        return []
    try:
        query = supabase.table("products").select("*")
        if keyword:
            query = query.or_(f"code.ilike.%{keyword}%,name.ilike.%{keyword}%")
        response = query.execute()
        return response.data
    except Exception as e:
        print(f"Query error: {e}")
        return []

@app.post("/api/orders")
def create_order(data: dict):
    if not supabase:
        return {"status": "error", "message": "No database connection"}
    try:
        response = supabase.table("orders").insert(data).execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 關鍵：供 Vercel Serverless Function 入口呼叫
handler = app
