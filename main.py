from fastapi import FastAPI
from src.router.product_order import productOrder

app = FastAPI(title="User_detail")

app.include_router(productOrder)