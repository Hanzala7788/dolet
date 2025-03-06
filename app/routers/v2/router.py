from app.routers.v2.user_auth.auth import router as auth_v2_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(auth_v2_router, prefix="/auth", tags=["auth"])