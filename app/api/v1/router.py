from fastapi import APIRouter

from app.api.v1.endpoint.task import router as task_router
from app.api.v1.endpoint.auth import router as user_auth_router

api_router = APIRouter()

api_router.include_router(task_router, prefix="/tasks", tags=["Tasks"])

api_router.include_router(user_auth_router, prefix="/auth", tags=["Authentication"])
