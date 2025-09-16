# app/routers/businesses.py
# Router para gestión de salones (businesses)
# Incluye CRUD de salones, horarios y configuraciones

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
import logging

from app.models.business import (
    BusinessCreate,
    BusinessUpdate,
    BusinessResponse,
    BusinessListResponse
)
from app.models.common import PaginationParams, SuccessResponse, ErrorResponse
from app.middleware.auth import get_current_user, verify_business_access
from app.config.database import get_supabase
from app.config.logging import log_business_event

# Configurar logging
logger = logging.getLogger(__name__)

# Crear el router de salones
router = APIRouter(
    prefix="/businesses",
    tags=["businesses"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Access denied"},
        404: {"description": "Business not found"}
    }
)

@router.get("/", response_model=BusinessListResponse)
async def get_businesses(
    pagination: PaginationParams = Depends(),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtener lista de salones accesibles para el usuario
    Solo retorna businesses donde el usuario es owner o employee
    """
    supabase = get_supabase()

    try:
        # Obtener businesses donde el usuario es owner
        owner_query = supabase.table('businesses').select(
            '*, business_owners!inner(user_id)'
        ).eq('business_owners.user_id', current_user['user_id']).eq('is_active', True)

        # Obtener businesses donde el usuario es employee
        employee_query = supabase.table('businesses').select(
            '*, employees!inner(user_id)'
        ).eq('employees.user_id', current_user['user_id']).eq(
            'employees.is_active', True
        ).eq('is_active', True)

        # Ejecutar queries
        owner_result = owner_query.execute()
        employee_result = employee_query.execute()

        # Combinar resultados y eliminar duplicados
        all_businesses = {}
        for business in owner_result.data:
            all_businesses[business['id']] = business

        for business in employee_result.data:
            all_businesses[business['id']] = business

        businesses_list = list(all_businesses.values())

        # Aplicar paginación
        total = len(businesses_list)
        start = pagination.offset
        end = start + pagination.limit
        paginated_businesses = businesses_list[start:end]

        # Convertir a modelo de respuesta
        businesses_response = [
            BusinessResponse(**business) for business in paginated_businesses
        ]

        log_business_event(
            event_type="businesses_listed",
            user_id=current_user['user_id'],
            total_found=total
        )

        return BusinessListResponse(
            data=businesses_response,
            message=f"Found {total} businesses"
        )

    except Exception as e:
        logger.error("Error fetching businesses", error=str(e), user_id=current_user['user_id'])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching businesses"
        )

@router.post("/", response_model=SuccessResponse)
async def create_business(
    business_data: BusinessCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Crear un nuevo salón
    El usuario que lo crea se convierte automáticamente en owner
    """
    supabase = get_supabase()

    try:
        # Crear el business
        business_insert = {
            "name": business_data.name,
            "description": business_data.description,
            "address": business_data.location.address,
            "city": business_data.location.city,
            "state": business_data.location.state,
            "postal_code": business_data.location.postal_code,
            "country": business_data.location.country,
            "phone": business_data.contact.phone,
            "email": business_data.contact.email,
            "website": business_data.contact.website,
            "instagram": business_data.contact.instagram,
            "facebook": business_data.contact.facebook,
            "is_active": business_data.is_active
        }

        business_result = supabase.table('businesses').insert(business_insert).execute()

        if not business_result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create business"
            )

        business_id = business_result.data[0]['id']

        # Hacer al usuario owner del business
        owner_insert = {
            "business_id": business_id,
            "user_id": current_user['user_id']
        }

        supabase.table('business_owners').insert(owner_insert).execute()

        # Insertar horarios si se proporcionaron
        if business_data.hours:
            hours_inserts = [
                {
                    "business_id": business_id,
                    "day_of_week": hour.day_of_week,
                    "open_time": hour.open_time.isoformat(),
                    "close_time": hour.close_time.isoformat(),
                    "is_closed": hour.is_closed
                }
                for hour in business_data.hours
            ]
            supabase.table('business_hours').insert(hours_inserts).execute()

        log_business_event(
            event_type="business_created",
            business_id=business_id,
            user_id=current_user['user_id'],
            business_name=business_data.name
        )

        return SuccessResponse(
            message="Business created successfully",
            data={"business_id": business_id, "name": business_data.name}
        )

    except Exception as e:
        logger.error("Error creating business", error=str(e), user_id=current_user['user_id'])
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating business"
        )

@router.get("/{business_id}", response_model=SuccessResponse)
async def get_business(
    business_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtener información detallada de un salón específico
    """
    # Verificar acceso al business
    await verify_business_access(current_user['user_id'], business_id)

    supabase = get_supabase()

    try:
        # Obtener business con horarios
        business_result = supabase.table('businesses').select(
            '*, business_hours(*)'
        ).eq('id', business_id).execute()

        if not business_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )

        business = business_result.data[0]

        log_business_event(
            event_type="business_viewed",
            business_id=business_id,
            user_id=current_user['user_id']
        )

        return SuccessResponse(
            message="Business retrieved successfully",
            data=business
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error fetching business", error=str(e), business_id=business_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching business"
        )

@router.put("/{business_id}", response_model=SuccessResponse)
async def update_business(
    business_id: str,
    business_data: BusinessUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Actualizar información de un salón
    Solo owners pueden actualizar
    """
    # Verificar que es owner del business
    await verify_business_access(current_user['user_id'], business_id, required_role='owner')

    supabase = get_supabase()

    try:
        # Preparar datos de actualización
        update_data = {}

        if business_data.name is not None:
            update_data['name'] = business_data.name
        if business_data.description is not None:
            update_data['description'] = business_data.description
        if business_data.is_active is not None:
            update_data['is_active'] = business_data.is_active

        if business_data.location:
            if business_data.location.address:
                update_data['address'] = business_data.location.address
            if business_data.location.city:
                update_data['city'] = business_data.location.city
            if business_data.location.state:
                update_data['state'] = business_data.location.state
            if business_data.location.postal_code:
                update_data['postal_code'] = business_data.location.postal_code

        if business_data.contact:
            if business_data.contact.phone:
                update_data['phone'] = business_data.contact.phone
            if business_data.contact.email:
                update_data['email'] = business_data.contact.email
            if business_data.contact.website:
                update_data['website'] = business_data.contact.website
            if business_data.contact.instagram:
                update_data['instagram'] = business_data.contact.instagram
            if business_data.contact.facebook:
                update_data['facebook'] = business_data.contact.facebook

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )

        update_data['updated_at'] = 'now()'

        result = supabase.table('businesses').update(update_data).eq(
            'id', business_id
        ).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found or no changes made"
            )

        log_business_event(
            event_type="business_updated",
            business_id=business_id,
            user_id=current_user['user_id'],
            updated_fields=list(update_data.keys())
        )

        return SuccessResponse(
            message="Business updated successfully",
            data=result.data[0]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating business", error=str(e), business_id=business_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating business"
        )

@router.delete("/{business_id}", response_model=SuccessResponse)
async def delete_business(
    business_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Eliminar (desactivar) un salón
    Solo owners pueden eliminar
    """
    # Verificar que es owner del business
    await verify_business_access(current_user['user_id'], business_id, required_role='owner')

    supabase = get_supabase()

    try:
        # Soft delete - marcar como inactivo
        result = supabase.table('businesses').update({
            'is_active': False,
            'updated_at': 'now()'
        }).eq('id', business_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Business not found"
            )

        log_business_event(
            event_type="business_deleted",
            business_id=business_id,
            user_id=current_user['user_id']
        )

        return SuccessResponse(
            message="Business deleted successfully",
            data={"business_id": business_id, "status": "inactive"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting business", error=str(e), business_id=business_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting business"
        )