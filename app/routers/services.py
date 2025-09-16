# app/routers/services.py
# Router para gestión de servicios del salón

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
import logging

from app.models.service import (
    ServiceCreate,
    ServiceUpdate,
    ServiceResponse,
    ServiceListResponse
)
from app.models.common import PaginationParams, SuccessResponse
from app.middleware.auth import get_current_user, verify_business_access
from app.config.database import get_supabase
from app.config.logging import log_business_event

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/services",
    tags=["services"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Access denied"},
        404: {"description": "Service not found"}
    }
)

@router.get("/", response_model=ServiceListResponse)
async def get_services(
    business_id: str = Query(..., description="ID del business"),
    pagination: PaginationParams = Depends(),
    category: Optional[str] = Query(None, description="Filtrar por categoría"),
    is_active: Optional[bool] = Query(True, description="Filtrar por estado activo"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtener lista de servicios de un salón específico
    """
    # Verificar acceso al business
    await verify_business_access(current_user['user_id'], business_id)

    supabase = get_supabase()

    try:
        # Construir query
        query = supabase.table('services').select('*').eq('business_id', business_id)

        if category:
            query = query.eq('category', category)
        if is_active is not None:
            query = query.eq('is_active', is_active)

        # Obtener total para paginación
        count_result = query.execute()
        total = len(count_result.data)

        # Aplicar paginación
        query = query.range(pagination.offset, pagination.offset + pagination.limit - 1)
        result = query.execute()

        services_response = [ServiceResponse(**service) for service in result.data]

        log_business_event(
            event_type="services_listed",
            business_id=business_id,
            user_id=current_user['user_id'],
            total_found=total
        )

        return ServiceListResponse(
            data=services_response,
            message=f"Found {total} services"
        )

    except Exception as e:
        logger.error("Error fetching services", error=str(e), business_id=business_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching services"
        )

@router.post("/", response_model=SuccessResponse)
async def create_service(
    service_data: ServiceCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Crear un nuevo servicio
    Solo owners y employees pueden crear servicios
    """
    # Verificar acceso al business (employee level)
    await verify_business_access(current_user['user_id'], service_data.business_id, required_role='employee')

    supabase = get_supabase()

    try:
        service_insert = {
            "business_id": service_data.business_id,
            "name": service_data.name,
            "description": service_data.description,
            "duration_minutes": service_data.duration_minutes,
            "price": float(service_data.price),
            "loyalty_points": service_data.loyalty_points,
            "is_active": service_data.is_active,
            "category": service_data.category
        }

        result = supabase.table('services').insert(service_insert).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create service"
            )

        service_id = result.data[0]['id']

        log_business_event(
            event_type="service_created",
            business_id=service_data.business_id,
            user_id=current_user['user_id'],
            service_id=service_id,
            service_name=service_data.name
        )

        return SuccessResponse(
            message="Service created successfully",
            data={"service_id": service_id, "name": service_data.name}
        )

    except Exception as e:
        logger.error("Error creating service", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating service"
        )

@router.get("/{service_id}", response_model=SuccessResponse)
async def get_service(
    service_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtener información detallada de un servicio específico
    """
    supabase = get_supabase()

    try:
        result = supabase.table('services').select('*').eq('id', service_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        service = result.data[0]

        # Verificar acceso al business del servicio
        await verify_business_access(current_user['user_id'], service['business_id'])

        log_business_event(
            event_type="service_viewed",
            business_id=service['business_id'],
            user_id=current_user['user_id'],
            service_id=service_id
        )

        return SuccessResponse(
            message="Service retrieved successfully",
            data=service
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error fetching service", error=str(e), service_id=service_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching service"
        )

@router.put("/{service_id}", response_model=SuccessResponse)
async def update_service(
    service_id: str,
    service_data: ServiceUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Actualizar información de un servicio
    Solo owners y employees pueden actualizar
    """
    supabase = get_supabase()

    try:
        # Obtener el servicio para verificar el business_id
        service_result = supabase.table('services').select('business_id').eq('id', service_id).execute()

        if not service_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        business_id = service_result.data[0]['business_id']

        # Verificar acceso al business (employee level)
        await verify_business_access(current_user['user_id'], business_id, required_role='employee')

        # Preparar datos de actualización
        update_data = {}

        if service_data.name is not None:
            update_data['name'] = service_data.name
        if service_data.description is not None:
            update_data['description'] = service_data.description
        if service_data.duration_minutes is not None:
            update_data['duration_minutes'] = service_data.duration_minutes
        if service_data.price is not None:
            update_data['price'] = float(service_data.price)
        if service_data.loyalty_points is not None:
            update_data['loyalty_points'] = service_data.loyalty_points
        if service_data.is_active is not None:
            update_data['is_active'] = service_data.is_active
        if service_data.category is not None:
            update_data['category'] = service_data.category

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )

        update_data['updated_at'] = 'now()'

        result = supabase.table('services').update(update_data).eq('id', service_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found or no changes made"
            )

        log_business_event(
            event_type="service_updated",
            business_id=business_id,
            user_id=current_user['user_id'],
            service_id=service_id,
            updated_fields=list(update_data.keys())
        )

        return SuccessResponse(
            message="Service updated successfully",
            data=result.data[0]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating service", error=str(e), service_id=service_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating service"
        )

@router.delete("/{service_id}", response_model=SuccessResponse)
async def delete_service(
    service_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Eliminar (desactivar) un servicio
    Solo owners pueden eliminar servicios
    """
    supabase = get_supabase()

    try:
        # Obtener el servicio para verificar el business_id
        service_result = supabase.table('services').select('business_id').eq('id', service_id).execute()

        if not service_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        business_id = service_result.data[0]['business_id']

        # Verificar que es owner del business
        await verify_business_access(current_user['user_id'], business_id, required_role='owner')

        # Soft delete - marcar como inactivo
        result = supabase.table('services').update({
            'is_active': False,
            'updated_at': 'now()'
        }).eq('id', service_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )

        log_business_event(
            event_type="service_deleted",
            business_id=business_id,
            user_id=current_user['user_id'],
            service_id=service_id
        )

        return SuccessResponse(
            message="Service deleted successfully",
            data={"service_id": service_id, "status": "inactive"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting service", error=str(e), service_id=service_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting service"
        )