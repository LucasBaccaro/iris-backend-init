# app/routers/promotions.py
# Router para sistema de promociones informativas

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_promotions():
    """Endpoint para promociones - En desarrollo"""
    return {"message": "Endpoint para promociones - En desarrollo", "status": "pending"}