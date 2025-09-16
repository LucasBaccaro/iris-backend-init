# app/routers/businesses.py
# Router para gestión de salones (businesses)
# Incluye CRUD de salones, horarios y configuraciones

from fastapi import APIRouter
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Crear el router de salones
router = APIRouter()

@router.get("/")
async def get_businesses():
    """
    Obtener lista de salones
    Se implementará en el Día 3 con el CRUD completo
    """
    return {
        "message": "Endpoint para listar salones - En desarrollo",
        "status": "pending"
    }

@router.post("/")
async def create_business():
    """
    Crear un nuevo salón
    Se implementará en el Día 3 con el CRUD completo
    """
    return {
        "message": "Endpoint para crear salón - En desarrollo",
        "status": "pending"
    }