"""
Endpoints de testing para verificar configuración
"""
from fastapi import APIRouter, Depends, HTTPException
from supabase import Client
from src.database.supabase import get_supabase, get_supabase_admin
from src.core.auth import get_current_user
from typing import Dict, Any

router = APIRouter()


@router.get("/ping")
async def ping():
    """Test básico de conectividad"""
    return {"message": "pong", "status": "ok"}


@router.get("/supabase-connection")
async def test_supabase_connection(supabase: Client = Depends(get_supabase)):
    """Testear conexión con Supabase"""
    try:
        # Test simple: obtener info del proyecto
        response = supabase.table("businesses").select("id").limit(1).execute()

        return {
            "status": "connected",
            "message": "Conexión con Supabase exitosa",
            "tables_accessible": True,
            "response_data": response.data
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error conectando con Supabase: {str(e)}"
        )


@router.get("/database-test")
async def test_database_access(supabase: Client = Depends(get_supabase_admin)):
    """Testear acceso a las tablas principales"""
    try:
        tables_status = {}

        # Testear acceso a cada tabla principal
        main_tables = [
            "businesses",
            "services",
            "employees",
            "appointments",
            "loyalty_points",
            "promotions"
        ]

        for table in main_tables:
            try:
                response = supabase.table(table).select("*").limit(1).execute()
                tables_status[table] = {
                    "accessible": True,
                    "count": len(response.data)
                }
            except Exception as e:
                tables_status[table] = {
                    "accessible": False,
                    "error": str(e)
                }

        return {
            "status": "success",
            "message": "Test de acceso a base de datos completado",
            "tables": tables_status
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error en test de base de datos: {str(e)}"
        )


@router.get("/auth-test")
async def test_auth(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Testear autenticación (requiere token válido)"""
    return {
        "status": "authenticated",
        "message": "Autenticación funcionando correctamente",
        "user_id": current_user.get("id"),
        "user_email": current_user.get("email"),
        "user_metadata": current_user.get("user_metadata", {})
    }


@router.get("/example-business")
async def get_example_business(supabase: Client = Depends(get_supabase)):
    """Obtener el negocio de ejemplo creado en el script SQL"""
    try:
        response = supabase.table("businesses").select("""
            id,
            name,
            address,
            access_code,
            services (
                id,
                name,
                price,
                duration_minutes,
                points_awarded
            )
        """).eq("name", "Salón de Belleza Ejemplo").execute()

        if not response.data:
            return {
                "status": "not_found",
                "message": "No se encontró el negocio de ejemplo",
                "suggestion": "Verifica que el script SQL se ejecutó correctamente"
            }

        return {
            "status": "found",
            "message": "Negocio de ejemplo encontrado",
            "business": response.data[0]
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error obteniendo negocio de ejemplo: {str(e)}"
        )