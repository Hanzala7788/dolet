# app/main.py
from fastapi import FastAPI
from app.routers.v1.router import router as api_router
from app.routers.v2.router import router as api_router_v2

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")
app.include_router(api_router_v2, prefix="/api/v2")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
