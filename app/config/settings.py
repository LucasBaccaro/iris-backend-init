# app/config/settings.py
# Configuración de variables de entorno para IRIS
# Este archivo maneja todas las configuraciones de la aplicación

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """
    Clase que maneja todas las configuraciones de IRIS
    Las variables se pueden cargar desde archivo .env o variables de entorno del sistema
    """

    # === CONFIGURACIÓN GENERAL DE LA APP ===
    app_name: str = "IRIS - Sistema de Gestión para Salones"
    app_version: str = "1.0.0"
    debug: bool = True  # En producción cambiar a False

    # === CONFIGURACIÓN DE SUPABASE ===
    # URL del proyecto de Supabase (ej: https://xxxxx.supabase.co)
    supabase_url: str

    # Clave pública de Supabase (anon key)
    supabase_key: str

    # Clave secreta de Supabase (service_role key) - para operaciones admin
    supabase_service_key: Optional[str] = None

    # === CONFIGURACIÓN DE SEGURIDAD ===
    # Clave secreta para verificar JWT tokens de Supabase
    jwt_secret: str

    # Algoritmo usado para JWT (Supabase usa HS256 por defecto)
    jwt_algorithm: str = "HS256"

    # === CONFIGURACIÓN DE TIMEZONE ===
    # Timezone principal para Argentina (Buenos Aires)
    default_timezone: str = "America/Argentina/Buenos_Aires"

    # Timezones soportadas para expansión futura
    supported_timezones: list = [
        "America/Argentina/Buenos_Aires",
        "America/Argentina/Cordoba",
        "America/Argentina/Mendoza",
        "America/Argentina/Tucuman"
    ]

    # === CONFIGURACIÓN DE BASE DE DATOS ===
    # Pool de conexiones (para optimizar performance)
    db_pool_size: int = 20
    db_max_overflow: int = 30

    # === CONFIGURACIÓN DE CORS ===
    # Dominios permitidos para CORS (en desarrollo "*", en producción dominios específicos)
    allowed_origins: list = ["*"]  # En producción: ["https://iris-frontend.com"]

    # === CONFIGURACIÓN DE LOGGING ===
    log_level: str = "INFO"  # DEBUG, INFO, WARNING, ERROR

    class Config:
        """
        Configuración de Pydantic para cargar variables de entorno
        """
        env_file = ".env"  # Buscar archivo .env en la raíz del proyecto
        env_file_encoding = "utf-8"
        case_sensitive = False  # Las variables no son case-sensitive


# Instancia global de configuración que se usará en toda la app
settings = Settings()

# Función helper para verificar que las configuraciones obligatorias estén presentes
def validate_settings():
    """
    Valida que todas las configuraciones críticas estén configuradas
    Se ejecuta al inicio de la aplicación
    """
    required_settings = [
        ("supabase_url", settings.supabase_url),
        ("supabase_key", settings.supabase_key),
        ("jwt_secret", settings.jwt_secret),
    ]

    missing_settings = []
    for setting_name, setting_value in required_settings:
        if not setting_value:
            missing_settings.append(setting_name)

    if missing_settings:
        raise ValueError(
            f"Faltan las siguientes configuraciones obligatorias: {', '.join(missing_settings)}\n"
            f"Por favor, configura estas variables en el archivo .env o como variables de entorno"
        )

    print("✅ Configuraciones validadas correctamente")
    return True

# Función para obtener la configuración de Supabase
def get_supabase_config():
    """
    Retorna la configuración necesaria para conectar con Supabase
    """
    return {
        "url": settings.supabase_url,
        "key": settings.supabase_key,
        "service_key": settings.supabase_service_key
    }