"""
Schemas Pydantic para Autenticación
"""
from uuid import UUID
from pydantic import BaseModel, EmailStr

class OwnerRegisterSchema(BaseModel):
    email: EmailStr
    password: str

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

class RegisterResponse(BaseModel):
    user: UserPublic
    tokens: TokenSchema

class EmployeeRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str | None = None

class CustomerRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    first_name: str | None = None
    last_name: str | None = None