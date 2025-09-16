# app/routers/employees.py
# Router para gestión de empleados
# Incluye CRUD de empleados y manejo de horarios

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional, Dict, Any
import logging

from app.models.employee import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse
)
from app.models.common import PaginationParams, SuccessResponse
from app.middleware.auth import get_current_user, verify_business_access
from app.config.database import get_supabase
from app.config.logging import log_business_event

# Configurar logging
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={
        401: {"description": "Authentication required"},
        403: {"description": "Access denied"},
        404: {"description": "Employee not found"}
    }
)

@router.get("/", response_model=EmployeeListResponse)
async def get_employees(
    business_id: str = Query(..., description="ID del business"),
    pagination: PaginationParams = Depends(),
    is_active: Optional[bool] = Query(True, description="Filtrar por estado activo"),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtener lista de empleados de un salón específico
    """
    # Verificar acceso al business
    await verify_business_access(current_user['user_id'], business_id)

    supabase = get_supabase()

    try:
        # Construir query
        query = supabase.table('employees').select('*, employee_hours(*)').eq('business_id', business_id)

        if is_active is not None:
            query = query.eq('is_active', is_active)

        # Obtener total para paginación
        count_result = query.execute()
        total = len(count_result.data)

        # Aplicar paginación
        query = query.range(pagination.offset, pagination.offset + pagination.limit - 1)
        result = query.execute()

        employees_response = [EmployeeResponse(**employee) for employee in result.data]

        log_business_event(
            event_type="employees_listed",
            business_id=business_id,
            user_id=current_user['user_id'],
            total_found=total
        )

        return EmployeeListResponse(
            data=employees_response,
            message=f"Found {total} employees"
        )

    except Exception as e:
        logger.error("Error fetching employees", error=str(e), business_id=business_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching employees"
        )

@router.post("/", response_model=SuccessResponse)
async def create_employee(
    employee_data: EmployeeCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Crear un nuevo empleado
    Solo owners pueden agregar empleados
    """
    # Verificar que es owner del business
    await verify_business_access(current_user['user_id'], employee_data.business_id, required_role='owner')

    supabase = get_supabase()

    try:
        employee_insert = {
            "business_id": employee_data.business_id,
            "user_id": employee_data.user_id,
            "name": employee_data.name,
            "email": employee_data.email,
            "phone": employee_data.phone,
            "specialties": employee_data.specialties,
            "is_active": employee_data.is_active
        }

        result = supabase.table('employees').insert(employee_insert).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create employee"
            )

        employee_id = result.data[0]['id']

        # Insertar horarios si se proporcionaron
        if employee_data.hours:
            hours_inserts = [
                {
                    "employee_id": employee_id,
                    "day_of_week": hour.day_of_week,
                    "start_time": hour.start_time.isoformat(),
                    "end_time": hour.end_time.isoformat(),
                    "is_available": hour.is_available
                }
                for hour in employee_data.hours
            ]
            supabase.table('employee_hours').insert(hours_inserts).execute()

        log_business_event(
            event_type="employee_created",
            business_id=employee_data.business_id,
            user_id=current_user['user_id'],
            employee_id=employee_id,
            employee_name=employee_data.name
        )

        return SuccessResponse(
            message="Employee created successfully",
            data={"employee_id": employee_id, "name": employee_data.name}
        )

    except Exception as e:
        logger.error("Error creating employee", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating employee"
        )

@router.get("/{employee_id}", response_model=SuccessResponse)
async def get_employee(
    employee_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Obtener información detallada de un empleado específico
    """
    supabase = get_supabase()

    try:
        result = supabase.table('employees').select(
            '*, employee_hours(*)'
        ).eq('id', employee_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        employee = result.data[0]

        # Verificar acceso al business del empleado
        await verify_business_access(current_user['user_id'], employee['business_id'])

        log_business_event(
            event_type="employee_viewed",
            business_id=employee['business_id'],
            user_id=current_user['user_id'],
            employee_id=employee_id
        )

        return SuccessResponse(
            message="Employee retrieved successfully",
            data=employee
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error fetching employee", error=str(e), employee_id=employee_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching employee"
        )

@router.put("/{employee_id}", response_model=SuccessResponse)
async def update_employee(
    employee_id: str,
    employee_data: EmployeeUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Actualizar información de un empleado
    Solo owners pueden actualizar empleados
    """
    supabase = get_supabase()

    try:
        # Obtener el empleado para verificar el business_id
        employee_result = supabase.table('employees').select('business_id').eq('id', employee_id).execute()

        if not employee_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        business_id = employee_result.data[0]['business_id']

        # Verificar que es owner del business
        await verify_business_access(current_user['user_id'], business_id, required_role='owner')

        # Preparar datos de actualización
        update_data = {}

        if employee_data.name is not None:
            update_data['name'] = employee_data.name
        if employee_data.email is not None:
            update_data['email'] = employee_data.email
        if employee_data.phone is not None:
            update_data['phone'] = employee_data.phone
        if employee_data.specialties is not None:
            update_data['specialties'] = employee_data.specialties
        if employee_data.is_active is not None:
            update_data['is_active'] = employee_data.is_active

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )

        update_data['updated_at'] = 'now()'

        result = supabase.table('employees').update(update_data).eq('id', employee_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found or no changes made"
            )

        log_business_event(
            event_type="employee_updated",
            business_id=business_id,
            user_id=current_user['user_id'],
            employee_id=employee_id,
            updated_fields=list(update_data.keys())
        )

        return SuccessResponse(
            message="Employee updated successfully",
            data=result.data[0]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error updating employee", error=str(e), employee_id=employee_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error updating employee"
        )

@router.delete("/{employee_id}", response_model=SuccessResponse)
async def delete_employee(
    employee_id: str,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Eliminar (desactivar) un empleado
    Solo owners pueden eliminar empleados
    """
    supabase = get_supabase()

    try:
        # Obtener el empleado para verificar el business_id
        employee_result = supabase.table('employees').select('business_id').eq('id', employee_id).execute()

        if not employee_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        business_id = employee_result.data[0]['business_id']

        # Verificar que es owner del business
        await verify_business_access(current_user['user_id'], business_id, required_role='owner')

        # Soft delete - marcar como inactivo
        result = supabase.table('employees').update({
            'is_active': False,
            'updated_at': 'now()'
        }).eq('id', employee_id).execute()

        if not result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        log_business_event(
            event_type="employee_deleted",
            business_id=business_id,
            user_id=current_user['user_id'],
            employee_id=employee_id
        )

        return SuccessResponse(
            message="Employee deleted successfully",
            data={"employee_id": employee_id, "status": "inactive"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error deleting employee", error=str(e), employee_id=employee_id)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting employee"
        )