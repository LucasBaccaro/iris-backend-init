# app/routers/auth.py
# Router para manejo de autenticación y verificación de tokens
# Este módulo NO maneja registro/login (eso lo hace Supabase)
# Solo verifica tokens JWT y extrae información de usuario

from fastapi import APIRouter, Depends, HTTPException, status, Header
from typing import Optional
import logging

# Configurar logging
logger = logging.getLogger(__name__)

# Crear el router de autenticación
router = APIRouter()

@router.get("/verify")
async def verify_token():
    """
    Endpoint para verificar que un token JWT es válido
    Se implementará en el Día 2 cuando hagamos el middleware de auth
    """
    return {
        "message": "Endpoint de verificación de token - En desarrollo",
        "status": "pending"
    }

@router.get("/me")
async def get_current_user():
    """
    Endpoint para obtener información del usuario actual
    Se implementará en el Día 2 cuando hagamos el middleware de auth
    """
    return {
        "message": "Endpoint para obtener usuario actual - En desarrollo",
        "status": "pending"
    }