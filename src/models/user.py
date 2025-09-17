"""
Modelos de datos Pydantic para Usuarios
"""
from uuid import UUID
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    """Modelo base para un usuario autenticado."""
    id: UUID
    email: EmailStr
    is_authenticated: bool = True
