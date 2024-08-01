from fastapi import FastAPI,APIRouter
from src.routers.student import studentde

app = FastAPI()

app.include_router(studentde)