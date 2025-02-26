# app/api/v1/routers.py
from fastapi import APIRouter
from app.routers.v1.endpoints.auth import router as auth_router
from app.routers.v1.endpoints.user import router as users_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(users_router, prefix="/users", tags=["users"])
