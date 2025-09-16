# app/config/logging.py
# Configuración del sistema de logging estructurado para IRIS
# Usa structlog para logs JSON estructurados y trazabilidad completa

import structlog
import logging
import sys
from app.config.settings import settings
from typing import Any, Dict

def configure_logging():
    """
    Configura el sistema de logging estructurado para IRIS

    Features:
    - Logs en formato JSON para fácil parsing
    - Timestamps automáticos
    - Niveles de log configurables
    - Context enriquecido para cada request
    - Separación entre logs de desarrollo y producción
    """

    # === CONFIGURACIÓN BÁSICA DE LOGGING ===
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.log_level.upper())
    )

    # === PROCESADORES DE STRUCTLOG ===
    shared_processors = [
        # Agregar timestamp a cada log
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),

        # Agregar información del stack cuando hay errores
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
    ]

    # === CONFIGURACIÓN PARA DESARROLLO ===
    if settings.debug:
        processors = shared_processors + [
            # En desarrollo: logs más legibles para humanos
            structlog.dev.ConsoleRenderer(colors=True)
        ]
    else:
        # === CONFIGURACIÓN PARA PRODUCCIÓN ===
        processors = shared_processors + [
            # En producción: logs JSON para parsing automático
            structlog.processors.JSONRenderer()
        ]

    # === CONFIGURAR STRUCTLOG ===
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        context_class=dict,
        cache_logger_on_first_use=True,
    )

# === LOGGER HELPER FUNCTIONS PARA IRIS ===

def get_logger(name: str = None):
    """
    Obtiene un logger estructurado para usar en cualquier módulo

    Args:
        name: Nombre del logger (usualmente __name__)

    Returns:
        Logger estructurado configurado
    """
    return structlog.get_logger(name)

def log_business_event(
    event_type: str,
    business_id: str = None,
    user_id: str = None,
    **kwargs
):
    """
    Helper para loggear eventos importantes de negocio en IRIS

    Args:
        event_type: Tipo de evento (ej: "appointment_created", "points_awarded")
        business_id: ID del salón donde ocurre el evento
        user_id: ID del usuario que realizó la acción
        **kwargs: Datos adicionales específicos del evento
    """
    logger = get_logger("iris.business")

    # Context básico para todos los eventos de negocio
    context = {
        "event_type": event_type,
        "business_id": business_id,
        "user_id": user_id,
        **kwargs
    }

    logger.info("business_event", **context)

def log_security_event(
    event_type: str,
    user_id: str = None,
    ip_address: str = None,
    success: bool = True,
    **kwargs
):
    """
    Helper para loggear eventos de seguridad y autenticación

    Args:
        event_type: Tipo de evento (ej: "login_attempt", "token_validation")
        user_id: ID del usuario involucrado
        ip_address: IP desde donde se hizo la request
        success: Si la operación fue exitosa
        **kwargs: Datos adicionales
    """
    logger = get_logger("iris.security")

    context = {
        "event_type": event_type,
        "user_id": user_id,
        "ip_address": ip_address,
        "success": success,
        **kwargs
    }

    # Log level basado en el éxito de la operación
    if success:
        logger.info("security_event", **context)
    else:
        logger.warning("security_event", **context)

def log_database_event(
    operation: str,
    table: str,
    record_id: str = None,
    business_id: str = None,
    duration_ms: float = None,
    **kwargs
):
    """
    Helper para loggear operaciones de base de datos

    Args:
        operation: Tipo de operación (SELECT, INSERT, UPDATE, DELETE)
        table: Tabla afectada
        record_id: ID del registro afectado
        business_id: ID del salón (para multi-tenancy)
        duration_ms: Duración de la query en milisegundos
        **kwargs: Datos adicionales
    """
    logger = get_logger("iris.database")

    context = {
        "operation": operation,
        "table": table,
        "record_id": record_id,
        "business_id": business_id,
        "duration_ms": duration_ms,
        **kwargs
    }

    # Log level basado en performance
    if duration_ms and duration_ms > 1000:  # Más de 1 segundo
        logger.warning("slow_query", **context)
    else:
        logger.info("database_operation", **context)

def log_appointment_event(
    event_type: str,
    appointment_id: str,
    business_id: str,
    customer_id: str = None,
    employee_id: str = None,
    service_name: str = None,
    appointment_datetime: str = None,
    **kwargs
):
    """
    Helper específico para eventos de appointments (core de IRIS)

    Args:
        event_type: Tipo de evento (created, cancelled, completed, etc.)
        appointment_id: ID de la cita
        business_id: ID del salón
        customer_id: ID del cliente
        employee_id: ID del empleado
        service_name: Nombre del servicio
        appointment_datetime: Fecha y hora de la cita
        **kwargs: Datos adicionales
    """
    logger = get_logger("iris.appointments")

    context = {
        "event_type": f"appointment_{event_type}",
        "appointment_id": appointment_id,
        "business_id": business_id,
        "customer_id": customer_id,
        "employee_id": employee_id,
        "service_name": service_name,
        "appointment_datetime": appointment_datetime,
        **kwargs
    }

    logger.info("appointment_event", **context)

def log_loyalty_event(
    event_type: str,
    business_id: str,
    customer_id: str,
    points: int = None,
    appointment_id: str = None,
    reward_name: str = None,
    **kwargs
):
    """
    Helper específico para eventos del sistema de fidelización

    Args:
        event_type: Tipo de evento (points_earned, points_redeemed, etc.)
        business_id: ID del salón
        customer_id: ID del cliente
        points: Cantidad de puntos involucrados
        appointment_id: ID de la cita relacionada (si aplica)
        reward_name: Nombre de la recompensa canjeada (si aplica)
        **kwargs: Datos adicionales
    """
    logger = get_logger("iris.loyalty")

    context = {
        "event_type": f"loyalty_{event_type}",
        "business_id": business_id,
        "customer_id": customer_id,
        "points": points,
        "appointment_id": appointment_id,
        "reward_name": reward_name,
        **kwargs
    }

    logger.info("loyalty_event", **context)

# === INICIALIZACIÓN AUTOMÁTICA ===
# Configurar logging cuando se importa este módulo
configure_logging()

# Export del logger principal
logger = get_logger("iris")