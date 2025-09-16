# app/middleware/logging_middleware.py
# Middleware para logging automático de todas las HTTP requests
# Captura información de cada request/response para trazabilidad completa

import time
import uuid
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.config.logging import get_logger
from typing import Callable
import json

logger = get_logger("iris.http")

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware que loggea automáticamente todas las HTTP requests y responses

    Features:
    - Request ID único para cada request
    - Tiempo de procesamiento
    - Información del cliente (IP, User-Agent)
    - Status codes y errores
    - Payload logging (configurable)
    """

    async def dispatch(self, request: Request, call_next: Callable):
        # === GENERAR REQUEST ID ÚNICO ===
        request_id = str(uuid.uuid4())[:8]  # ID corto para logs
        request.state.request_id = request_id

        # === INFORMACIÓN BÁSICA DE LA REQUEST ===
        start_time = time.time()
        client_ip = self._get_client_ip(request)
        user_agent = request.headers.get("user-agent", "unknown")

        # === LOG DE REQUEST ENTRANTE ===
        logger.info(
            "http_request_start",
            request_id=request_id,
            method=request.method,
            url=str(request.url),
            path=request.url.path,
            query_params=dict(request.query_params),
            client_ip=client_ip,
            user_agent=user_agent,
            content_length=request.headers.get("content-length", 0)
        )

        # === PROCESAR REQUEST ===
        try:
            response = await call_next(request)

            # === CALCULAR TIEMPO DE PROCESAMIENTO ===
            process_time = (time.time() - start_time) * 1000  # En milisegundos

            # === LOG DE RESPONSE EXITOSO ===
            logger.info(
                "http_request_complete",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                process_time_ms=round(process_time, 2),
                response_size=response.headers.get("content-length", "unknown")
            )

            # === LOG DE WARNING SI ES MUY LENTO ===
            if process_time > 2000:  # Más de 2 segundos
                logger.warning(
                    "slow_request",
                    request_id=request_id,
                    method=request.method,
                    path=request.url.path,
                    process_time_ms=round(process_time, 2)
                )

            return response

        except Exception as e:
            # === LOG DE ERROR ===
            process_time = (time.time() - start_time) * 1000

            logger.error(
                "http_request_error",
                request_id=request_id,
                method=request.method,
                path=request.url.path,
                error=str(e),
                error_type=type(e).__name__,
                process_time_ms=round(process_time, 2)
            )

            # Re-raise la excepción para que FastAPI la maneje
            raise e

    def _get_client_ip(self, request: Request) -> str:
        """
        Obtiene la IP real del cliente considerando proxies y load balancers
        """
        # Revisar headers comunes de proxies
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            # Tomar la primera IP de la lista (cliente original)
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("x-real-ip")
        if real_ip:
            return real_ip

        # Fallback a la IP directa
        if request.client:
            return request.client.host

        return "unknown"

class RequestContextMiddleware(BaseHTTPMiddleware):
    """
    Middleware para agregar contexto de request a todos los logs
    Permite que cualquier log tenga automáticamente el request_id
    """

    async def dispatch(self, request: Request, call_next: Callable):
        # Agregar contexto global para structlog
        import structlog

        request_id = getattr(request.state, 'request_id', None)
        if request_id:
            # Bind del request_id al contexto de structlog
            with structlog.contextvars.bound_contextvars(
                request_id=request_id,
                path=request.url.path,
                method=request.method
            ):
                return await call_next(request)
        else:
            return await call_next(request)

def log_business_operation(
    operation: str,
    business_id: str = None,
    user_id: str = None,
    details: dict = None,
    success: bool = True
):
    """
    Helper para loggear operaciones específicas de negocio dentro de endpoints

    Args:
        operation: Nombre de la operación (ej: "create_appointment", "award_points")
        business_id: ID del salón donde ocurre la operación
        user_id: ID del usuario que ejecuta la operación
        details: Detalles específicos de la operación
        success: Si la operación fue exitosa
    """

    log_data = {
        "operation": operation,
        "business_id": business_id,
        "user_id": user_id,
        "success": success
    }

    if details:
        log_data.update(details)

    if success:
        logger.info("business_operation", **log_data)
    else:
        logger.error("business_operation_failed", **log_data)