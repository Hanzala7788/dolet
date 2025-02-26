# app/main.py
from fastapi import FastAPI
from app.routers.v1.router import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"message": "Hello World"}
