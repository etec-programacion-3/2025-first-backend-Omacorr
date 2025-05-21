from fastapi import APIRouter
from app.api.routes.libros import router as libros_router

api_router = APIRouter()
api_router.include_router(libros_router, prefix="/libros", tags=["libros"])