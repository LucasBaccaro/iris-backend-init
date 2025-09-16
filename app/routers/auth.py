# app/routers/auth.py
# Router para manejo de autenticación y verificación de tokens
# Este módulo NO maneja registro/login (eso lo hace Supabase)
# Solo verifica tokens JWT y extrae información de usuario

from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, Dict, Any
import logging

from app.middleware.auth import (
    get_current_user,
    get_optional_user,
    verify_business_access,
    AuthenticationError,
    AuthorizationError
)
from app.config.logging import log_business_event

# Configurar logging
logger = logging.getLogger(__name__)

# Crear el router de autenticación
router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={
        401: {"description": "Authentication failed"},
        403: {"description": "Authorization failed"}
    }
)

@router.get("/verify", response_model=dict)
async def verify_token(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Endpoint para verificar que un token JWT es válido

    Returns:
        Información básica sobre la validez del token
    """
    log_business_event(
        event_type="auth_token_verified",
        user_id=current_user['user_id'],
        email=current_user['email']
    )

    return {
        "status": "valid",
        "message": "Token is valid",
        "user_id": current_user['user_id'],
        "email": current_user['email'],
        "role": current_user['role']
    }

@router.get("/me", response_model=dict)
async def get_current_user_info(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Endpoint para obtener información del usuario actual

    Returns:
        Información completa del usuario autenticado
    """
    log_business_event(
        event_type="user_info_requested",
        user_id=current_user['user_id'],
        email=current_user['email']
    )

    return {
        "user_id": current_user['user_id'],
        "email": current_user['email'],
        "role": current_user['role'],
        "authenticated": True,
        "token_info": {
            "issued_at": current_user.get('iat'),
            "expires_at": current_user.get('exp'),
            "issuer": current_user.get('iss'),
            "audience": current_user.get('aud')
        }
    }

@router.post("/verify-business-access", response_model=dict)
async def verify_business_access_endpoint(
    business_id: str,
    required_role: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Endpoint para verificar acceso a un business específico

    Args:
        business_id: ID del business a verificar
        required_role: Rol mínimo requerido (opcional)

    Returns:
        Confirmación de acceso al business
    """
    try:
        has_access = await verify_business_access(
            user_id=current_user['user_id'],
            business_id=business_id,
            required_role=required_role
        )

        log_business_event(
            event_type="business_access_verified",
            business_id=business_id,
            user_id=current_user['user_id'],
            required_role=required_role
        )

        return {
            "status": "authorized",
            "message": "Access granted to business",
            "business_id": business_id,
            "user_id": current_user['user_id'],
            "required_role": required_role
        }

    except AuthorizationError as e:
        log_business_event(
            event_type="business_access_denied",
            business_id=business_id,
            user_id=current_user['user_id'],
            required_role=required_role,
            error=str(e)
        )
        raise e