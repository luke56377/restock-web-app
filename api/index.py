import os
from fastapi import FastAPI
from supabase import Client, create_client

app = FastAPI()

# 從 Vercel 環境變數讀取金鑰
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")

supabase: Client = (
    create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL else None
)


@app.get("/api/products")
def search_products(keyword: str = ""):
  if not supabase:
    return []
  query = supabase.table("products").select("*")
  if keyword:
    query = query.or_(f"code.ilike.%{keyword}%,name.ilike.%{keyword}%")
  response = query.execute()
  return response.data


@app.post("/api/orders")
def create_order(data: dict):
  if not supabase:
    return {"status": "error", "message": "No database connection"}
  response = supabase.table("orders").insert(data).execute()
  return {"status": "success", "data": response.data}
