# app/config/database.py
# Cliente de Supabase para IRIS
# Este archivo maneja la conexión con Supabase y proporciona funciones helper

from supabase import create_client, Client
from app.config.settings import settings, validate_settings
import logging

# Configurar logging
logger = logging.getLogger(__name__)

class SupabaseClient:
    """
    Clase singleton para manejar la conexión con Supabase
    Asegura que solo haya una instancia del cliente en toda la aplicación
    """

    _instance = None
    _client: Client = None

    def __new__(cls):
        """
        Patrón singleton: solo crea una instancia de la clase
        """
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Inicializa el cliente de Supabase solo una vez
        """
        if self._client is None:
            try:
                # Validar que las configuraciones estén presentes
                validate_settings()

                # Crear cliente con la clave pública (anon key)
                self._client = create_client(
                    settings.supabase_url,
                    settings.supabase_key
                )

                logger.info("✅ Cliente de Supabase inicializado correctamente")

            except Exception as e:
                logger.error(f"❌ Error al inicializar Supabase: {e}")
                raise e

    @property
    def client(self) -> Client:
        """
        Propiedad para acceder al cliente de Supabase
        """
        if self._client is None:
            raise Exception("Cliente de Supabase no inicializado")
        return self._client

# Instancia global del cliente
supabase_client = SupabaseClient()

def get_supabase() -> Client:
    """
    Función helper para obtener el cliente de Supabase
    Esta función se usará como dependency en FastAPI
    """
    return supabase_client.client

def get_supabase_admin() -> Client:
    """
    Cliente de Supabase con permisos de administrador (service_role)
    Solo usar para operaciones que requieren permisos elevados
    CUIDADO: Este cliente puede saltarse las Row Level Security policies
    """
    if not settings.supabase_service_key:
        raise Exception("Service key de Supabase no configurado")

    return create_client(
        settings.supabase_url,
        settings.supabase_service_key
    )

# === FUNCIONES HELPER PARA OPERACIONES COMUNES ===

async def execute_query(query, params=None):
    """
    Ejecuta una query SQL directa en Supabase
    Útil para queries complejas que no se pueden hacer con el ORM
    """
    try:
        supabase = get_supabase()

        if params:
            result = supabase.rpc('execute_sql', {'query': query, 'params': params})
        else:
            result = supabase.rpc('execute_sql', {'query': query})

        return result.execute()

    except Exception as e:
        logger.error(f"Error ejecutando query: {e}")
        raise e

async def check_connection():
    """
    Verifica que la conexión con Supabase esté funcionando
    Útil para health checks
    """
    try:
        supabase = get_supabase()

        # Intentar hacer una query simple
        result = supabase.table('businesses').select('id').limit(1).execute()

        logger.info("✅ Conexión con Supabase verificada")
        return True

    except Exception as e:
        logger.error(f"❌ Error de conexión con Supabase: {e}")
        return False