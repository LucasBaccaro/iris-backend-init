# app/config/logging_examples.py
# Ejemplos de uso del sistema de logging estructurado para IRIS
# Este archivo muestra cómo usar las diferentes funciones de logging

from app.config.logging import (
    get_logger,
    log_business_event,
    log_security_event,
    log_database_event,
    log_appointment_event,
    log_loyalty_event
)

# === EJEMPLOS DE USO EN ENDPOINTS ===

def ejemplo_crear_appointment():
    """
    Ejemplo de logging al crear una nueva appointment
    """

    # Logger básico
    logger = get_logger("iris.appointments")

    # Datos de ejemplo
    appointment_id = "apt_123456"
    business_id = "bus_789"
    customer_id = "usr_456"
    employee_id = "emp_321"
    service_name = "Corte Dama"
    datetime_str = "2024-01-15T14:00:00-03:00"

    # === LOG ESPECÍFICO DE APPOINTMENT ===
    log_appointment_event(
        event_type="created",
        appointment_id=appointment_id,
        business_id=business_id,
        customer_id=customer_id,
        employee_id=employee_id,
        service_name=service_name,
        appointment_datetime=datetime_str,
        # Datos adicionales específicos
        price=1500,
        duration_minutes=30,
        points_to_award=15
    )

    # === LOG GENÉRICO DE NEGOCIO ===
    log_business_event(
        event_type="appointment_created",
        business_id=business_id,
        user_id=customer_id,
        appointment_id=appointment_id,
        revenue=1500
    )

def ejemplo_otorgar_puntos():
    """
    Ejemplo de logging al otorgar puntos de fidelización
    """

    appointment_id = "apt_123456"
    customer_id = "usr_456"
    business_id = "bus_789"
    points_awarded = 15

    # === LOG DE LOYALTY POINTS ===
    log_loyalty_event(
        event_type="points_earned",
        business_id=business_id,
        customer_id=customer_id,
        points=points_awarded,
        appointment_id=appointment_id,
        # Detalles adicionales
        service_name="Corte Dama",
        points_multiplier=1.0
    )

def ejemplo_login_fallido():
    """
    Ejemplo de logging cuando falla una autenticación
    """

    user_email = "customer@example.com"
    ip_address = "192.168.1.100"

    # === LOG DE SEGURIDAD ===
    log_security_event(
        event_type="login_attempt",
        user_id=None,  # No sabemos el user_id porque falló el login
        ip_address=ip_address,
        success=False,
        # Detalles del error
        email=user_email,
        error_reason="invalid_password",
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)"
    )

def ejemplo_query_lenta():
    """
    Ejemplo de logging para queries de base de datos lentas
    """

    # === LOG DE DATABASE PERFORMANCE ===
    log_database_event(
        operation="SELECT",
        table="appointments",
        business_id="bus_789",
        duration_ms=2500,  # Muy lento!
        # Detalles de la query
        filters={"employee_id": "emp_321", "date_range": "2024-01-15 to 2024-01-22"},
        result_count=150
    )

def ejemplo_error_de_negocio():
    """
    Ejemplo de logging cuando hay un error de lógica de negocio
    """

    logger = get_logger("iris.business")

    # Error: Intentar crear appointment en horario ocupado
    logger.error(
        "double_booking_prevented",
        appointment_id="apt_new",
        business_id="bus_789",
        employee_id="emp_321",
        requested_datetime="2024-01-15T14:00:00-03:00",
        # Detalles del conflicto
        conflicting_appointment_id="apt_existing",
        conflict_duration_minutes=30,
        customer_id="usr_456"
    )

def ejemplo_metricas_de_negocio():
    """
    Ejemplo de logging de métricas importantes para el dashboard
    """

    logger = get_logger("iris.metrics")

    # Métricas diarias de un salón
    logger.info(
        "daily_business_metrics",
        business_id="bus_789",
        date="2024-01-15",
        # Métricas calculadas
        appointments_completed=25,
        appointments_cancelled=3,
        appointments_no_show=1,
        total_revenue=37500,
        points_awarded=375,
        points_redeemed=50,
        new_customers=5,
        returning_customers=20
    )

# === EJEMPLOS DE LOGGING EN DIFERENTES CONTEXTOS ===

def ejemplo_logging_en_endpoint():
    """
    Ejemplo completo de cómo usar logging en un endpoint de FastAPI
    """

    # Simular datos del endpoint
    user_id = "usr_123"
    business_id = "bus_456"

    logger = get_logger("iris.api")

    # === 1. LOG DE INICIO DE OPERACIÓN ===
    logger.info(
        "endpoint_start",
        operation="get_business_appointments",
        user_id=user_id,
        business_id=business_id
    )

    try:
        # === 2. LOG DE VALIDACIONES ===
        logger.info(
            "business_access_validated",
            user_id=user_id,
            business_id=business_id,
            user_role="owner"
        )

        # === 3. LOG DE OPERACIÓN DE BASE DE DATOS ===
        log_database_event(
            operation="SELECT",
            table="appointments",
            business_id=business_id,
            duration_ms=150,
            result_count=42
        )

        # === 4. LOG DE ÉXITO ===
        logger.info(
            "endpoint_success",
            operation="get_business_appointments",
            user_id=user_id,
            business_id=business_id,
            results_returned=42
        )

    except Exception as e:
        # === 5. LOG DE ERROR ===
        logger.error(
            "endpoint_error",
            operation="get_business_appointments",
            user_id=user_id,
            business_id=business_id,
            error=str(e),
            error_type=type(e).__name__
        )

# === LOGGING CONDICIONAL PARA DESARROLLO ===

def ejemplo_debug_logging():
    """
    Ejemplo de logging que solo aparece en modo debug
    """

    logger = get_logger("iris.debug")

    # Este log solo aparece si DEBUG=true en .env
    logger.debug(
        "validation_details",
        business_id="bus_123",
        validation_checks={
            "business_exists": True,
            "user_has_access": True,
            "business_is_active": True,
            "within_business_hours": True
        }
    )

# === COMENTARIOS PARA USAR EN CÓDIGO REAL ===
"""
En tus endpoints reales, usa logging así:

```python
@router.post("/appointments")
async def create_appointment(appointment_data: AppointmentCreate):
    logger = get_logger("iris.appointments")

    logger.info("appointment_creation_started",
                customer_id=appointment_data.customer_id,
                business_id=appointment_data.business_id)

    try:
        # Tu lógica aquí...
        result = await appointment_service.create(appointment_data)

        # Log de éxito
        log_appointment_event(
            event_type="created",
            appointment_id=result.id,
            business_id=appointment_data.business_id,
            # ... otros datos
        )

        return result

    except ConflictError as e:
        logger.warning("appointment_conflict",
                      requested_time=appointment_data.datetime,
                      error=str(e))
        raise HTTPException(409, "Horario no disponible")
```
"""