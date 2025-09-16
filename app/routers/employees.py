# app/routers/employees.py
# Router para gestión de empleados
# Incluye CRUD de empleados y manejo de horarios

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_employees():
    """Endpoint para listar empleados - En desarrollo"""
    return {"message": "Endpoint para empleados - En desarrollo", "status": "pending"}