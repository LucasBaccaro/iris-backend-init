# app/routers/appointments.py
# Router para sistema de reservas y appointments

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_appointments():
    """Endpoint para listar reservas - En desarrollo"""
    return {"message": "Endpoint para reservas - En desarrollo", "status": "pending"}