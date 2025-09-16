# app/routers/loyalty.py
# Router para sistema de fidelización y puntos

from fastapi import APIRouter

router = APIRouter()

@router.get("/points")
async def get_loyalty_points():
    """Endpoint para puntos de fidelización - En desarrollo"""
    return {"message": "Endpoint para puntos - En desarrollo", "status": "pending"}