"""
IRIS Backend API - Aplicaci�n principal
SaaS de Gesti�n para Salones de Belleza
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from src.core.config import settings
from src.api.routes import test

# Crear aplicaci�n FastAPI
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API Backend para IRIS - Sistema de gesti�n de salones de belleza",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

# Middleware de hosts confiables (seguridad)
if not settings.debug:
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*.iris-app.com", "localhost"]
    )


@app.get("/")
async def root():
    """Endpoint ra�z - Health check"""
    return {
        "message": "IRIS Backend API",
        "version": settings.app_version,
        "status": "active",
        "environment": settings.environment
    }


@app.get("/health")
async def health_check():
    """Health check para monitoreo"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z"
    }


# Incluir routers de test
app.include_router(test.router, prefix="/test", tags=["testing"])

# Incluir routers cuando los creemos
# app.include_router(businesses.router, prefix="/api/v1/businesses", tags=["businesses"])
# app.include_router(appointments.router, prefix="/api/v1/appointments", tags=["appointments"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )