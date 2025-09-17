# IRIS Backend API

SaaS de gestión para salones de belleza - Backend API

## 🚀 Inicio Rápido
Windows -> python -m venv venv -> venv\Scripts\activate
Mac -> python3 -m venv venv -> source venv/bin/activate

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales de Supabase
```

### 3. Ejecutar la aplicación

```bash
# Desarrollo
python run.py

# O con uvicorn directamente
uvicorn src.main:app --reload
```

### 4. Acceder a la documentación

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
src/
├── api/
│   ├── routes/          # Endpoints de la API
│   ├── middleware/      # Middleware personalizado
│   └── dependencies/    # Dependencies de FastAPI
├── core/
│   ├── config.py       # Configuración de la app
│   └── auth.py         # Autenticación simplificada
├── database/
│   └── supabase.py     # Cliente de Supabase
├── models/             # Modelos de datos (futuro)
├── schemas/            # Schemas de Pydantic
├── services/           # Lógica de negocio
└── main.py            # Aplicación principal
```

## 🔧 Variables de Entorno Necesarias

```env
# Supabase (OBLIGATORIAS)
SUPABASE_URL=your-supabase-project-url
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key

# JWT (OBLIGATORIA)
SECRET_KEY=your-super-secret-jwt-key
```

## 🏗️ Features Implementadas

- ✅ Configuración básica de FastAPI
- ✅ Integración con Supabase
- ✅ Autenticación JWT simplificada
- ✅ CORS configurado
- ✅ Estructura de proyecto escalable

## 📝 Próximos Pasos

1. Crear endpoints CRUD para businesses
2. Implementar sistema de appointments
3. Agregar sistema de loyalty points
4. Tests unitarios

## 🔗 Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [IRIS Planning](./contexts/BACKEND-PLANIFICACION.md)