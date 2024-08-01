from fastapi import FastAPI
from src.routers.users import Users

app = FastAPI(title="User_detail")

app.include_router(Users)