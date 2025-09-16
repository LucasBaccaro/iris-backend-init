# app/models/common.py
# Modelos Pydantic comunes y utilidades para IRIS

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime, time
from enum import Enum
import uuid

class ResponseStatus(str, Enum):
    """Estados de respuesta estándar"""
    SUCCESS = "success"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

class TimezoneInfo(BaseModel):
    """Información de timezone para responses"""
    timezone: str = Field(default="America/Argentina/Buenos_Aires")
    utc_offset: str = Field(default="-03:00")

class PaginationParams(BaseModel):
    """Parámetros de paginación para listados"""
    page: int = Field(default=1, ge=1, description="Número de página")
    limit: int = Field(default=20, ge=1, le=100, description="Elementos por página")

    @property
    def offset(self) -> int:
        """Calcula el offset para la query"""
        return (self.page - 1) * self.limit

class PaginationInfo(BaseModel):
    """Información de paginación para responses"""
    page: int
    limit: int
    total: int
    pages: int
    has_next: bool
    has_prev: bool

class BaseResponse(BaseModel):
    """Respuesta base para todos los endpoints"""
    status: ResponseStatus
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    timezone_info: TimezoneInfo = Field(default_factory=TimezoneInfo)

class SuccessResponse(BaseResponse):
    """Respuesta exitosa con datos"""
    status: ResponseStatus = ResponseStatus.SUCCESS
    data: Optional[Any] = None
    pagination: Optional[PaginationInfo] = None

class ErrorResponse(BaseResponse):
    """Respuesta de error"""
    status: ResponseStatus = ResponseStatus.ERROR
    error_code: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

class BusinessHours(BaseModel):
    """Modelo para horarios de negocio"""
    day_of_week: int = Field(ge=0, le=6, description="Día de la semana (0=Domingo)")
    open_time: time = Field(description="Hora de apertura")
    close_time: time = Field(description="Hora de cierre")
    is_closed: bool = Field(default=False, description="Si está cerrado ese día")

    @validator('close_time')
    def validate_hours(cls, v, values):
        if 'open_time' in values and not values.get('is_closed', False):
            if v <= values['open_time']:
                raise ValueError('Close time must be after open time')
        return v

class LocationInfo(BaseModel):
    """Información de ubicación"""
    address: str = Field(min_length=10, max_length=200)
    city: str = Field(min_length=2, max_length=50)
    state: str = Field(min_length=2, max_length=50)
    postal_code: Optional[str] = Field(max_length=20)
    country: str = Field(default="Argentina", max_length=50)

    # Coordenadas opcionales para futuras funcionalidades
    latitude: Optional[float] = Field(ge=-90, le=90)
    longitude: Optional[float] = Field(ge=-180, le=180)

class ContactInfo(BaseModel):
    """Información de contacto"""
    phone: Optional[str] = Field(max_length=20)
    email: Optional[str] = Field(max_length=100)
    website: Optional[str] = Field(max_length=200)
    instagram: Optional[str] = Field(max_length=100)
    facebook: Optional[str] = Field(max_length=100)

    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v

class UUIDModel(BaseModel):
    """Modelo base con UUID"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

class TimestampModel(BaseModel):
    """Modelo base con timestamps"""
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class BaseEntity(UUIDModel, TimestampModel):
    """Modelo base para todas las entidades"""
    pass

# Validadores comunes
def validate_phone_number(phone: Optional[str]) -> Optional[str]:
    """Valida número de teléfono argentino"""
    if not phone:
        return phone

    # Remover espacios y caracteres especiales
    clean_phone = ''.join(filter(str.isdigit, phone))

    # Validar formato argentino
    if len(clean_phone) < 8 or len(clean_phone) > 15:
        raise ValueError('Invalid phone number format')

    return phone

def validate_business_hours(hours_list: List[BusinessHours]) -> List[BusinessHours]:
    """Valida que los horarios de negocio sean consistentes"""
    days_seen = set()
    for hour in hours_list:
        if hour.day_of_week in days_seen:
            raise ValueError(f'Duplicate day of week: {hour.day_of_week}')
        days_seen.add(hour.day_of_week)

    return hours_list