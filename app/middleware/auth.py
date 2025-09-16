# app/middleware/auth.py
# Middleware y utilidades para autenticación JWT con Supabase
# Implementa el sistema de autenticación híbrido: Supabase Auth + validación manual FastAPI

from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
import jwt
import logging
from datetime import datetime

from app.config.settings import settings
from app.config.database import get_supabase

# Configurar logging
logger = logging.getLogger(__name__)

# Esquema de autenticación Bearer
security = HTTPBearer(auto_error=False)

class AuthenticationError(HTTPException):
    """Excepción personalizada para errores de autenticación"""
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"}
        )

class AuthorizationError(HTTPException):
    """Excepción personalizada para errores de autorización"""
    def __init__(self, detail: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

async def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verifica un token JWT de Supabase y retorna el payload decodificado

    Args:
        token: Token JWT de Supabase

    Returns:
        Dict con información del usuario decodificada del JWT

    Raises:
        AuthenticationError: Si el token es inválido o ha expirado
    """
    try:
        # Decodificar el JWT usando la clave secreta de Supabase
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm]
        )

        # Verificar que el token no haya expirado
        if 'exp' in payload:
            exp_timestamp = payload['exp']
            if datetime.utcnow().timestamp() > exp_timestamp:
                raise AuthenticationError("Token has expired")

        # Log del evento de autenticación exitosa
        logger.info(
            "jwt_token_verified",
            user_id=payload.get('sub'),
            email=payload.get('email'),
            exp=payload.get('exp')
        )

        return payload

    except jwt.ExpiredSignatureError:
        logger.warning("jwt_token_expired", token_prefix=token[:20] + "...")
        raise AuthenticationError("Token has expired")

    except jwt.InvalidTokenError as e:
        logger.warning("jwt_token_invalid", error=str(e), token_prefix=token[:20] + "...")
        raise AuthenticationError("Invalid token")

    except Exception as e:
        logger.error("jwt_verification_error", error=str(e))
        raise AuthenticationError("Token verification failed")

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Dict[str, Any]:
    """
    Dependency para obtener el usuario actual basado en el JWT token

    Args:
        credentials: Credenciales HTTP Bearer del request

    Returns:
        Dict con información del usuario autenticado

    Raises:
        AuthenticationError: Si no hay token o es inválido
    """
    if not credentials:
        logger.warning("missing_authorization_header")
        raise AuthenticationError("Authorization header missing")

    # Verificar el token JWT
    user_payload = await verify_jwt_token(credentials.credentials)

    # Extraer información básica del usuario del JWT
    user_info = {
        'user_id': user_payload.get('sub'),
        'email': user_payload.get('email'),
        'role': user_payload.get('role', 'customer'),  # Por defecto customer
        'aud': user_payload.get('aud'),
        'exp': user_payload.get('exp'),
        'iat': user_payload.get('iat'),
        'iss': user_payload.get('iss')
    }

    # Validar que tenemos la información mínima necesaria
    if not user_info['user_id']:
        raise AuthenticationError("Invalid token: missing user ID")

    if not user_info['email']:
        raise AuthenticationError("Invalid token: missing email")

    logger.info(
        "user_authenticated",
        user_id=user_info['user_id'],
        email=user_info['email'],
        role=user_info['role']
    )

    return user_info

async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[Dict[str, Any]]:
    """
    Dependency para obtener el usuario actual de forma opcional
    Similar a get_current_user pero no requiere autenticación

    Args:
        credentials: Credenciales HTTP Bearer del request (opcional)

    Returns:
        Dict con información del usuario si está autenticado, None si no
    """
    if not credentials:
        return None

    try:
        return await get_current_user(credentials)
    except AuthenticationError:
        return None

async def require_role(required_role: str, user: Dict[str, Any]) -> bool:
    """
    Verifica que el usuario tenga el rol requerido

    Args:
        required_role: Rol requerido ('owner', 'employee', 'customer')
        user: Información del usuario obtenida de get_current_user

    Returns:
        True si tiene el rol requerido

    Raises:
        AuthorizationError: Si no tiene el rol requerido
    """
    user_role = user.get('role', 'customer')

    # Jerarquía de roles: owner > employee > customer
    role_hierarchy = {
        'owner': 3,
        'employee': 2,
        'customer': 1
    }

    user_level = role_hierarchy.get(user_role, 0)
    required_level = role_hierarchy.get(required_role, 0)

    if user_level >= required_level:
        logger.info(
            "role_authorization_success",
            user_id=user['user_id'],
            user_role=user_role,
            required_role=required_role
        )
        return True
    else:
        logger.warning(
            "role_authorization_failed",
            user_id=user['user_id'],
            user_role=user_role,
            required_role=required_role
        )
        raise AuthorizationError(
            f"Required role: {required_role}, current role: {user_role}"
        )

async def verify_business_access(
    user_id: str,
    business_id: str,
    required_role: Optional[str] = None
) -> bool:
    """
    Verifica que un usuario tenga acceso a un business específico
    Implementa la lógica multi-tenant

    Args:
        user_id: ID del usuario
        business_id: ID del business a verificar
        required_role: Rol mínimo requerido para el acceso (opcional)

    Returns:
        True si tiene acceso

    Raises:
        AuthorizationError: Si no tiene acceso al business
    """
    supabase = get_supabase()

    try:
        # Verificar si el usuario es owner del business
        owner_check = supabase.table('business_owners').select('*').eq(
            'business_id', business_id
        ).eq('user_id', user_id).execute()

        if owner_check.data:
            logger.info(
                "business_access_granted",
                user_id=user_id,
                business_id=business_id,
                access_type="owner"
            )
            return True

        # Verificar si es empleado del business
        employee_check = supabase.table('employees').select('*').eq(
            'business_id', business_id
        ).eq('user_id', user_id).eq('is_active', True).execute()

        if employee_check.data:
            # Si se requiere rol específico, verificar jerarquía
            if required_role and required_role == 'owner':
                raise AuthorizationError(
                    "Owner access required for this business operation"
                )

            logger.info(
                "business_access_granted",
                user_id=user_id,
                business_id=business_id,
                access_type="employee"
            )
            return True

        # Si no es owner ni employee, denegar acceso
        logger.warning(
            "business_access_denied",
            user_id=user_id,
            business_id=business_id
        )
        raise AuthorizationError(
            "You don't have access to this business"
        )

    except Exception as e:
        logger.error(
            "business_access_verification_error",
            user_id=user_id,
            business_id=business_id,
            error=str(e)
        )
        raise AuthorizationError("Unable to verify business access")

# Decoradores de conveniencia para roles específicos
def require_owner(user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency que requiere rol de owner"""
    async def _verify():
        await require_role('owner', user)
        return user
    return _verify

def require_employee(user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency que requiere rol de employee o superior"""
    async def _verify():
        await require_role('employee', user)
        return user
    return _verify

def require_customer(user: Dict[str, Any] = Depends(get_current_user)):
    """Dependency que requiere cualquier usuario autenticado"""
    async def _verify():
        await require_role('customer', user)
        return user
    return _verify