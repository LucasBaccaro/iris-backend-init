# app/models/business.py
# Modelos Pydantic para businesses (salones)

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime

from .common import (
    BaseEntity,
    SuccessResponse,
    BusinessHours,
    LocationInfo,
    ContactInfo,
    PaginationInfo
)

class BusinessBase(BaseModel):
    """Modelo base para Business"""
    name: str = Field(min_length=2, max_length=100)
    description: Optional[str] = Field(max_length=500)
    location: LocationInfo
    contact: ContactInfo
    is_active: bool = Field(default=True)

class BusinessCreate(BusinessBase):
    """Modelo para crear un business"""
    hours: List[BusinessHours] = Field(default_factory=list)

    @validator('hours')
    def validate_hours(cls, v):
        if len(v) > 7:
            raise ValueError('Cannot have more than 7 days of hours')
        return v

class BusinessUpdate(BaseModel):
    """Modelo para actualizar un business"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    location: Optional[LocationInfo] = None
    contact: Optional[ContactInfo] = None
    is_active: Optional[bool] = None

class BusinessResponse(BusinessBase, BaseEntity):
    """Modelo de respuesta para Business"""
    owner_id: str
    hours: List[BusinessHours] = Field(default_factory=list)

class BusinessListResponse(SuccessResponse):
    """Respuesta para listado de businesses"""
    data: List[BusinessResponse]
    pagination: Optional[PaginationInfo] = None