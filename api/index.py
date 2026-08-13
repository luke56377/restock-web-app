import os
from fastapi import FastAPI
from supabase import create_client, Client

app = FastAPI()

# 從 Vercel 環境變數讀取金鑰
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

# 確保兩者都有值才建立 Supabase 客戶端
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Supabase connection error: {e}")

@app.get("/api/products")
def search_products(keyword: str = ""):
    if not supabase:
        return []
    
    try:
        query = supabase.table("products").select("*")
        if keyword:
            # 搜尋編號或名稱
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
