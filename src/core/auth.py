"""
Sistema de autenticación simplificado con Supabase
Solo validación de tokens JWT de Supabase
"""
from typing import Dict, Any
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.database.supabase import get_supabase
from supabase import Client

# Bearer token scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    supabase: Client = Depends(get_supabase)
) -> Dict[str, Any]:
    """
    Obtener usuario actual validando el token JWT de Supabase
    El token viene del frontend que se autenticó con Supabase
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Supabase valida automáticamente el JWT
        user_response = supabase.auth.get_user(credentials.credentials)

        if not user_response.user:
            raise credentials_exception

        return {
            "id": user_response.user.id,
            "email": user_response.user.email,
            "user_metadata": user_response.user.user_metadata or {},
            "app_metadata": user_response.user.app_metadata or {}
        }

    except Exception:
        raise credentials_exception


class RoleChecker:
    """
    Verificador de roles basado en user_metadata de Supabase
    """

    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: Dict[str, Any] = Depends(get_current_user)):
        user_role = current_user.get("user_metadata", {}).get("role")

        if not user_role or user_role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permisos insuficientes para esta operación"
            )
        return current_user


# Checkers de roles para usar como dependencies
require_owner = RoleChecker(["owner"])
require_employee = RoleChecker(["owner", "employee"])
require_any_user = RoleChecker(["owner", "employee", "customer"])


def get_user_business_id(current_user: Dict[str, Any]) -> str:
    """
    Extraer business_id del usuario para filtros multi-tenant
    """
    business_id = (
        current_user.get("app_metadata", {}).get("business_id") or
        current_user.get("user_metadata", {}).get("business_id")
    )

    if not business_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario no asociado a ningún negocio"
        )

    return business_id


async def get_current_user_with_business(
    current_user: Dict[str, Any] = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Obtener usuario actual con business_id validado
    """
    business_id = get_user_business_id(current_user)
    current_user["business_id"] = business_id
    return current_user