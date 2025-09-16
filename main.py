# main.py - Punto de entrada principal de la aplicación IRIS
# Este archivo configura la app FastAPI y incluye todos los routers

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

# Importar configuración de logging (se configura automáticamente)
from app.config.logging import logger, log_business_event

# Importar middleware de logging
from app.middleware.logging_middleware import LoggingMiddleware, RequestContextMiddleware

# Importar todos los routers (los crearemos a continuación)
from app.routers import auth, businesses, employees, services, appointments, loyalty, promotions

# Configuración de la aplicación principal
app = FastAPI(
    title="IRIS - Sistema de Gestión para Salones de Belleza",
    description="MVP para gestión de salones con reservas y sistema de fidelización",
    version="1.0.0",
    docs_url="/docs",  # Documentación en /docs
    redoc_url="/redoc"  # Documentación alternativa en /redoc
)

# === CONFIGURAR MIDDLEWARE ===

# Middleware de logging (debe ir PRIMERO para capturar todo)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestContextMiddleware)

# Configurar CORS para permitir requests desde frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware global para manejo de errores
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """
    Manejador global de errores para dar respuestas consistentes
    También loggea todos los errores para trazabilidad
    """

    # Log del error con contexto completo
    logger.error(
        "unhandled_exception",
        path=str(request.url),
        method=request.method,
        error=str(exc),
        error_type=type(exc).__name__,
        client_ip=request.client.host if request.client else "unknown"
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Error interno del servidor",
            "message": str(exc),
            "path": str(request.url)
        }
    )

# Incluir todos los routers con sus prefijos correspondientes
# Cada router maneja una funcionalidad específica del sistema

# Router de autenticación (verificación de tokens)
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticación"])

# Router de gestión de salones
app.include_router(businesses.router, prefix="/api/businesses", tags=["Salones"])

# Router de gestión de empleados
app.include_router(employees.router, prefix="/api/employees", tags=["Empleados"])

# Router de gestión de servicios
app.include_router(services.router, prefix="/api/services", tags=["Servicios"])

# Router de sistema de reservas
app.include_router(appointments.router, prefix="/api/appointments", tags=["Reservas"])

# Router de sistema de fidelización
app.include_router(loyalty.router, prefix="/api/loyalty", tags=["Fidelización"])

# Router de promociones
app.include_router(promotions.router, prefix="/api/promotions", tags=["Promociones"])

# Endpoint raíz para verificar que la API está funcionando
@app.get("/")
async def root():
    """
    Endpoint raíz que confirma que la API IRIS está operativa
    """

    # Log del acceso al endpoint raíz
    logger.info("root_endpoint_accessed", message="API health check")

    return {
        "message": "IRIS API está funcionando correctamente",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Endpoint de health check para monitoreo
@app.get("/health")
async def health_check():
    """
    Endpoint para verificar el estado de salud de la API
    Útil para monitoring y load balancers
    """

    # Importar la función de check de conexión con Supabase
    from app.config.database import check_connection

    # Verificar conexión con Supabase
    supabase_healthy = await check_connection()

    health_status = {
        "status": "healthy" if supabase_healthy else "unhealthy",
        "service": "iris-backend",
        "version": "1.0.0",
        "database": "connected" if supabase_healthy else "disconnected"
    }

    # Log del health check
    logger.info("health_check", **health_status)

    return health_status

# Ejecutar el servidor solo si ejecutamos este archivo directamente
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Auto-reload en desarrollo
    )