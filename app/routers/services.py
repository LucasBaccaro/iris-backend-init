# app/routers/services.py
# Router para gestión de servicios del salón

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_services():
    """Endpoint para listar servicios - En desarrollo"""
    return {"message": "Endpoint para servicios - En desarrollo", "status": "pending"}