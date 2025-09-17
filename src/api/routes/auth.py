"""
Endpoints para Autenticación y Registro de Usuarios
"""
from fastapi import APIRouter, Depends, HTTPException, status
from supabase import Client
from typing import Dict, Any
import uuid

from src.core.config import settings
from src.core.auth import get_current_user, require_owner
from src.database.supabase import get_supabase, get_supabase_admin
from src.schemas.auth import (
    OwnerRegisterSchema,
    EmployeeRegisterSchema,
    CustomerRegisterSchema,
    RegisterResponse,
    UserPublic,
    TokenSchema
)

router = APIRouter()

@router.post("/register/owner", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_owner(
    owner_data: OwnerRegisterSchema,
    db: Client = Depends(get_supabase),
    admin_db: Client = Depends(get_supabase_admin)
):
    """
    Registra un nuevo usuario propietario (owner) y crea su negocio inicial.
    Este endpoint es público para que cualquier persona pueda registrar su salón.
    """
    new_user = None
    try:
        # Crear usuario en Supabase Auth
        user_response = admin_db.auth.admin.create_user({
            "email": owner_data.email,
            "password": owner_data.password,
            "email_confirm": True,
        })
        new_user = user_response.user

        if not new_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo crear el usuario en Supabase Auth.")

        # Generar código de acceso único para el negocio
        access_code = str(uuid.uuid4())[:8].upper()

        # Crear el negocio (business) usando el cliente ADMIN
        business_response = admin_db.table("businesses").insert({
            "name": f"Salón de {owner_data.email.split('@')[0]}",
            "address": "Dirección pendiente",
            "access_code": access_code,
            "is_active": True
        }).execute()

        if not business_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo crear el negocio.")
        
        new_business = business_response.data[0]

        # Crear el perfil de usuario (user_profile) usando el cliente ADMIN
        profile_response = admin_db.table("user_profiles").insert({
            "id": new_user.id,
            "role": "owner",
            "business_id": new_business['id'],
        }).execute()

        if not profile_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo crear el perfil de usuario.")

        # Devolver Tokens
        session_response = db.auth.sign_in_with_password({
            "email": owner_data.email,
            "password": owner_data.password
        })
        
        if not session_response.session:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Usuario creado pero no se pudo iniciar sesión.")

        # Construir la respuesta
        user_public = UserPublic(id=new_user.id, email=new_user.email, role="owner")
        token_schema = TokenSchema(access_token=session_response.session.access_token, refresh_token=session_response.session.refresh_token)
        
        return RegisterResponse(user=user_public, tokens=token_schema)

    except Exception as e:
        if new_user:
            try:
                admin_db.auth.admin.delete_user(new_user.id)
            except Exception as delete_e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error crítico: Falló la creación y también el rollback. Usuario fantasma creado: {new_user.id}. Error original: {e}. Error de borrado: {delete_e}"
                )
        
        if "duplicate key value violates unique constraint" in str(e) and "users_email_key" in str(e):
             raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado."
            )
        
        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ocurrió un error inesperado durante el registro: {e}"
            )


@router.post("/register/employee", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_employee(
    employee_data: EmployeeRegisterSchema,
    current_user: Dict[str, Any] = Depends(require_owner),
    db: Client = Depends(get_supabase),
    admin_db: Client = Depends(get_supabase_admin)
):
    """
    Permite a un propietario registrar un nuevo empleado.
    Solo los owners autenticados pueden acceder a este endpoint.
    """
    new_user = None
    try:
        # Obtener business_id del owner autenticado (viene de RoleChecker)
        business_id = current_user.get("business_id")
        if not business_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner no tiene business_id asociado.")

        # Crear usuario en Supabase Auth
        user_response = admin_db.auth.admin.create_user({
            "email": employee_data.email,
            "password": employee_data.password,
            "email_confirm": True,
        })
        new_user = user_response.user

        if not new_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo crear el usuario en Supabase Auth.")

        # Crear el perfil de usuario (user_profile) usando el cliente ADMIN
        profile_response = admin_db.table("user_profiles").insert({
            "id": new_user.id,
            "role": "employee",
            "business_id": business_id,
        }).execute()

        if not profile_response.data:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo crear el perfil de usuario.")

        # Devolver Tokens
        session_response = db.auth.sign_in_with_password({
            "email": employee_data.email,
            "password": employee_data.password
        })

        if not session_response.session:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Usuario creado pero no se pudo iniciar sesión.")

        # Construir la respuesta
        user_public = UserPublic(id=new_user.id, email=new_user.email, role="employee")
        token_schema = TokenSchema(access_token=session_response.session.access_token, refresh_token=session_response.session.refresh_token)

        return RegisterResponse(user=user_public, tokens=token_schema)

    except Exception as e:
        if new_user:
            try:
                admin_db.auth.admin.delete_user(new_user.id)
            except Exception as delete_e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error crítico: Falló la creación y también el rollback. Usuario fantasma creado: {new_user.id}. Error original: {e}. Error de borrado: {delete_e}"
                )

        if "duplicate key value violates unique constraint" in str(e) and "users_email_key" in str(e):
             raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado."
            )

        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ocurrió un error inesperado durante el registro: {e}"
            )


@router.post("/register/customer", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register_customer(
    customer_data: CustomerRegisterSchema,
    db: Client = Depends(get_supabase),
    admin_db: Client = Depends(get_supabase_admin)
):
    """
    Permite el auto-registro de clientes.
    Este endpoint es público y puede ser llamado por cualquier usuario no autenticado.
    """
    new_user = None
    try:
        # Crear usuario en Supabase Auth usando sign_up para auto-registro
        user_response = db.auth.sign_up({
            "email": customer_data.email,
            "password": customer_data.password
        })

        if not user_response.user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No se pudo crear el usuario en Supabase Auth.")

        new_user = user_response.user

        # Crear el perfil de usuario (user_profile) usando el cliente ADMIN
        profile_response = admin_db.table("user_profiles").insert({
            "id": new_user.id,
            "role": "customer",
            "business_id": None,  # Los clientes pueden pertenecer a múltiples negocios
        }).execute()

        if not profile_response.data:
            # Si falla la creación del perfil, intentar eliminar el usuario
            try:
                admin_db.auth.admin.delete_user(new_user.id)
            except:
                pass  # Si no se puede eliminar, al menos reportar el error principal
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="No se pudo crear el perfil de usuario.")

        # Verificar si tenemos tokens de la sesión
        tokens = None
        if user_response.session:
            tokens = TokenSchema(
                access_token=user_response.session.access_token,
                refresh_token=user_response.session.refresh_token
            )
        else:
            # Si no hay sesión (puede pasar con sign_up si requiere confirmación)
            # Intentar hacer sign_in para obtener tokens
            try:
                session_response = db.auth.sign_in_with_password({
                    "email": customer_data.email,
                    "password": customer_data.password
                })
                if session_response.session:
                    tokens = TokenSchema(
                        access_token=session_response.session.access_token,
                        refresh_token=session_response.session.refresh_token
                    )
            except:
                # Si no se puede hacer sign_in, puede ser porque necesita confirmación de email
                tokens = TokenSchema(access_token="pending_confirmation", refresh_token="pending_confirmation")

        # Construir la respuesta
        user_public = UserPublic(id=new_user.id, email=new_user.email, role="customer")

        return RegisterResponse(user=user_public, tokens=tokens)

    except Exception as e:
        if new_user:
            try:
                admin_db.auth.admin.delete_user(new_user.id)
            except Exception as delete_e:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error crítico: Falló la creación y también el rollback. Usuario fantasma creado: {new_user.id}. Error original: {e}. Error de borrado: {delete_e}"
                )

        if "duplicate key value violates unique constraint" in str(e) and "users_email_key" in str(e):
             raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El email ya está registrado."
            )

        if isinstance(e, HTTPException):
            raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Ocurrió un error inesperado durante el registro: {e}"
            )
