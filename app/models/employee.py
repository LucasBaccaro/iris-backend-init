# app/models/employee.py
# Modelos Pydantic para employees (empleados del salón)

from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import time

from .common import BaseEntity, SuccessResponse, BusinessHours, PaginationInfo

class EmployeeBase(BaseModel):
    """Modelo base para Employee"""
    user_id: Optional[str] = None  # Puede ser null si no tiene usuario aún
    name: str = Field(min_length=2, max_length=100)
    email: Optional[str] = Field(max_length=100)
    phone: Optional[str] = Field(max_length=20)
    specialties: List[str] = Field(default_factory=list)
    is_active: bool = Field(default=True)

    @validator('email')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email format')
        return v

class EmployeeHours(BaseModel):
    """Horarios específicos del empleado"""
    day_of_week: int = Field(ge=0, le=6)
    start_time: time
    end_time: time
    is_available: bool = Field(default=True)

    @validator('end_time')
    def validate_times(cls, v, values):
        if 'start_time' in values and v <= values['start_time']:
            raise ValueError('End time must be after start time')
        return v

class EmployeeCreate(EmployeeBase):
    """Modelo para crear un employee"""
    business_id: str
    hours: List[EmployeeHours] = Field(default_factory=list)

class EmployeeUpdate(BaseModel):
    """Modelo para actualizar un employee"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    specialties: Optional[List[str]] = None
    is_active: Optional[bool] = None

class EmployeeResponse(EmployeeBase, BaseEntity):
    """Modelo de respuesta para Employee"""
    business_id: str
    hours: List[EmployeeHours] = Field(default_factory=list)

class EmployeeListResponse(SuccessResponse):
    """Respuesta para listado de employees"""
    data: List[EmployeeResponse]
    pagination: Optional[PaginationInfo] = None