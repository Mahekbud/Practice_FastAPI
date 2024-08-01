from fastapi import FastAPI
from src.routers.security import securitysystem
from src.routers.access_refresh_token import access_token

app = FastAPI(title="Security_System")

app.include_router(securitysystem)
app.include_router(access_token)