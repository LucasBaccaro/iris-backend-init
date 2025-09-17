"""
Configuración principal de la aplicación IRIS
"""
import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración de la aplicación"""

    # Aplicación
    app_name: str = "IRIS Backend API"
    app_version: str = "1.0.0"
    debug: bool = True
    environment: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str

    # Supabase Auth (no necesitamos JWT propio)

    # Security
    admin_secret: str

    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:3001"

    # Logging
    log_level: str = "DEBUG"

    # Timezone
    default_timezone: str = "America/Argentina/Buenos_Aires"

    # Rate Limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60

    @property
    def cors_origins(self) -> List[str]:
        """Convertir allowed_origins string a lista"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"  # Ignorar variables extra del .env


# Instancia global de configuración
settings = Settings()