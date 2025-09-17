"""
Configuración y cliente de Supabase
"""
from supabase import create_client, Client
from src.core.config import settings


class SupabaseClient:
    """Cliente singleton de Supabase"""

    _instance = None
    _client: Client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._client is None:
            self._client = create_client(
                settings.supabase_url,
                settings.supabase_anon_key
            )

    @property
    def client(self) -> Client:
        """Obtener el cliente de Supabase"""
        return self._client

    def get_admin_client(self) -> Client:
        """Obtener cliente con privilegios administrativos"""
        return create_client(
            settings.supabase_url,
            settings.supabase_service_role_key
        )


# Instancia global del cliente
supabase_client = SupabaseClient()


def get_supabase() -> Client:
    """Dependency para obtener el cliente de Supabase"""
    return supabase_client.client


def get_supabase_admin() -> Client:
    """Dependency para obtener el cliente administrativo de Supabase"""
    return supabase_client.get_admin_client()