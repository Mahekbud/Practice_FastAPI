from fastapi import FastAPI
from src.router.employee import employees



app = FastAPI(title="employee_details")

app.include_router(employees)