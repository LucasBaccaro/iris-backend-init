# app/models/auth.py
# Modelos Pydantic para autenticación y autorización

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

from .common import BaseResponse, SuccessResponse

class UserRole(str, Enum):
    """Roles de usuario en el sistema"""
    OWNER = "owner"
    EMPLOYEE = "employee"
    CUSTOMER = "customer"

class AuthTokenPayload(BaseModel):
    """Payload del JWT token de Supabase"""
    user_id: str = Field(alias='sub')
    email: str
    role: UserRole = Field(default=UserRole.CUSTOMER)
    aud: str
    exp: int  # Expiration timestamp
    iat: int  # Issued at timestamp
    iss: str  # Issuer

    class Config:
        validate_by_name = True

class UserInfo(BaseModel):
    """Información básica del usuario"""
    user_id: str
    email: str
    role: UserRole
    authenticated: bool = True

class TokenInfo(BaseModel):
    """Información del token JWT"""
    issued_at: Optional[int] = None
    expires_at: Optional[int] = None
    issuer: Optional[str] = None
    audience: Optional[str] = None

class CurrentUserResponse(SuccessResponse):
    """Respuesta para endpoint /auth/me"""
    data: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, user_info: UserInfo, token_info: TokenInfo, **kwargs):
        data = {
            "user_id": user_info.user_id,
            "email": user_info.email,
            "role": user_info.role,
            "authenticated": user_info.authenticated,
            "token_info": token_info.dict()
        }
        super().__init__(data=data, message="User information retrieved successfully", **kwargs)

class TokenVerificationResponse(SuccessResponse):
    """Respuesta para endpoint /auth/verify"""
    data: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, user_info: UserInfo, **kwargs):
        data = {
            "status": "valid",
            "message": "Token is valid",
            "user_id": user_info.user_id,
            "email": user_info.email,
            "role": user_info.role
        }
        super().__init__(data=data, message="Token verified successfully", **kwargs)

class BusinessAccessRequest(BaseModel):
    """Request para verificar acceso a business"""
    business_id: str = Field(min_length=1, max_length=100)
    required_role: Optional[UserRole] = None

    @validator('business_id')
    def validate_business_id(cls, v):
        if not v.strip():
            raise ValueError('Business ID cannot be empty')
        return v.strip()

class BusinessAccessResponse(SuccessResponse):
    """Respuesta para verificación de acceso a business"""
    data: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, business_id: str, user_id: str, required_role: Optional[str] = None, **kwargs):
        data = {
            "status": "authorized",
            "message": "Access granted to business",
            "business_id": business_id,
            "user_id": user_id,
            "required_role": required_role
        }
        super().__init__(data=data, message="Business access verified successfully", **kwargs)

class UserBusinessAccess(BaseModel):
    """Información de acceso de usuario a un business"""
    business_id: str
    business_name: str
    access_type: str  # 'owner' o 'employee'
    role: UserRole
    permissions: List[str] = Field(default_factory=list)

class UserBusinessesResponse(SuccessResponse):
    """Respuesta con businesses a los que tiene acceso el usuario"""
    data: Dict[str, Any] = Field(default_factory=dict)

    def __init__(self, businesses: List[UserBusinessAccess], **kwargs):
        data = {
            "businesses": [business.dict() for business in businesses],
            "total": len(businesses)
        }
        super().__init__(data=data, message="User businesses retrieved successfully", **kwargs)

# Decoradores y funciones helper para validation
class RoleHierarchy:
    """Jerarquía de roles para autorización"""
    LEVELS = {
        UserRole.CUSTOMER: 1,
        UserRole.EMPLOYEE: 2,
        UserRole.OWNER: 3
    }

    @classmethod
    def has_permission(cls, user_role: UserRole, required_role: UserRole) -> bool:
        """Verifica si un rol tiene permisos para realizar una acción"""
        user_level = cls.LEVELS.get(user_role, 0)
        required_level = cls.LEVELS.get(required_role, 0)
        return user_level >= required_level

    @classmethod
    def get_permissions(cls, role: UserRole) -> List[str]:
        """Obtiene las permisos para un rol específico"""
        permissions = []

        if role in [UserRole.CUSTOMER, UserRole.EMPLOYEE, UserRole.OWNER]:
            permissions.extend([
                "read_own_appointments",
                "create_own_appointments",
                "cancel_own_appointments"
            ])

        if role in [UserRole.EMPLOYEE, UserRole.OWNER]:
            permissions.extend([
                "read_business_appointments",
                "update_appointments",
                "manage_availability",
                "view_business_stats"
            ])

        if role == UserRole.OWNER:
            permissions.extend([
                "manage_business",
                "manage_employees",
                "manage_services",
                "manage_promotions",
                "view_financial_reports",
                "manage_business_settings"
            ])

        return permissions