# app/models/service.py
# Modelos Pydantic para services (servicios del salón)

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from decimal import Decimal

from .common import BaseEntity, SuccessResponse, PaginationInfo

class ServiceBase(BaseModel):
    """Modelo base para Service"""
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(max_length=500)
    duration_minutes: int = Field(ge=5, le=480)  # 5 minutos a 8 horas
    price: Decimal = Field(ge=0, decimal_places=2)
    loyalty_points: int = Field(ge=0, default=0)
    is_active: bool = Field(default=True)
    category: Optional[str] = Field(max_length=50)

    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be positive')
        return v

class ServiceCreate(ServiceBase):
    """Modelo para crear un service"""
    business_id: str

class ServiceUpdate(BaseModel):
    """Modelo para actualizar un service"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    duration_minutes: Optional[int] = Field(None, ge=5, le=480)
    price: Optional[Decimal] = Field(None, ge=0, decimal_places=2)
    loyalty_points: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None
    category: Optional[str] = Field(None, max_length=50)

class ServiceResponse(ServiceBase, BaseEntity):
    """Modelo de respuesta para Service"""
    business_id: str

class ServiceListResponse(SuccessResponse):
    """Respuesta para listado de services"""
    data: List[ServiceResponse]
    pagination: Optional[PaginationInfo] = None