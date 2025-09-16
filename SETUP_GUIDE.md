# 🚀 Guía de Setup IRIS - Paso a Paso

**Guía completa para configurar IRIS desde cero en 15 minutos.**

## ✅ Checklist Rápido

- [ ] Proyecto Supabase creado
- [ ] Credenciales copiadas
- [ ] `schema.sql` ejecutado
- [ ] `constraints_simple.sql` ejecutado
- [ ] `sample_data.sql` ejecutado (opcional)
- [ ] Entorno virtual creado y activado
- [ ] Dependencies instaladas (`pip install -r requirements.txt`)
- [ ] Archivo `.env` configurado
- [ ] Conexión FastAPI funcionando

## 📋 **PASO 1: Crear Proyecto Supabase**

### **1.1 - Registro y Proyecto**
1. **Ve a:** https://supabase.com
2. **Click:** "Start your project" → "Sign in with GitHub"
3. **Click:** "New Project"
4. **Completa:**
   - **Name:** `iris-salon-management`
   - **Database Password:** Genera una fuerte y **guárdala**
   - **Region:** US East (más rápido desde Argentina)
5. **Click:** "Create new project"
6. **⏳ Espera:** 2-3 minutos hasta ver el dashboard

### **1.2 - Obtener Credenciales**
1. En el dashboard, **sidebar izquierdo:** Settings → API
2. **Copia estos 4 valores** (los necesitarás para el `.env`):

```
Project URL: https://abcdefgh.supabase.co
anon public: eyJhbGciOiJIUzI1NiIsIn...
service_role: eyJhbGciOiJIUzI1NiIsIn...  <-- ¡ESTE ES SECRETO!
```

3. **Click en:** Settings → API → JWT Settings
4. **Copia:** JWT Secret

## 🗄️ **PASO 2: Configurar Base de Datos**

### **2.1 - Ejecutar Schema Principal**

1. **Sidebar izquierdo:** SQL Editor
2. **Click:** "New query"
3. **Nombre:** "01 - Schema Principal"
4. **Copia y pega** TODO el contenido del archivo `database/schema.sql`
5. **Click:** "RUN" (botón azul)
6. **✅ Verificar:** "Success. No rows returned"

**Si hay error:** Verifica que copiaste TODO el archivo, desde la primera línea hasta la última.

### **2.2 - Aplicar Constraints Críticos**

1. **Click:** "New query" (nueva pestaña)
2. **Nombre:** "02 - Constraints"
3. **Copia y pega** TODO el contenido del archivo `database/constraints_simple.sql`
4. **Click:** "RUN"
5. **✅ Verificar:** "Constraints críticos aplicados correctamente ✅"

**Si hay error:** Probablemente el schema no se ejecutó bien. Vuelve al paso 2.1.

### **2.3 - Datos de Ejemplo (Recomendado)**

1. **Click:** "New query"
2. **Nombre:** "03 - Sample Data"
3. **Copia y pega** TODO el contenido del archivo `database/sample_data.sql`
4. **Click:** "RUN"
5. **✅ Verificar:** "Success. 57+ rows returned"

### **2.4 - Verificar que Todo Funcionó**

**Nueva query con este código:**

```sql
-- Test 1: Verificar tablas (debe devolver 13 filas)
SELECT COUNT(*) as total_tablas FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
    'businesses', 'business_hours', 'services', 'employees',
    'employee_hours', 'appointments', 'special_openings',
    'loyalty_points', 'loyalty_rewards', 'loyalty_redemptions',
    'promotions', 'business_faqs', 'business_owners'
);

-- Test 2: Verificar constraint crítico (debe devolver 1 fila)
SELECT COUNT(*) as constraint_overlapping FROM pg_constraint
WHERE conname = 'prevent_overlapping_appointments';

-- Test 3: Verificar datos de ejemplo (debe devolver 4 filas con datos)
SELECT 'businesses' as tabla, COUNT(*) FROM businesses
UNION ALL SELECT 'services', COUNT(*) FROM services
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'promotions', COUNT(*) FROM promotions;
```

**✅ Resultados esperados:**
- `total_tablas`: 13
- `constraint_overlapping`: 1
- businesses: 2, services: 8, employees: 3, promotions: 2

## 🔐 **PASO 3: Configurar FastAPI**

### **3.1 - Crear Entorno Virtual**

**Recomendado:** Usar entorno virtual para aislar dependencies.

#### **Opción A: Con venv (built-in Python)**

**Mac (usando python3):**
```bash
# Crear entorno virtual
python3 -m venv iris-env

# Activar
source iris-env/bin/activate

# Verificar que está activo (debería mostrar el path del entorno)
which python3
```

**Linux/Windows:**
```bash
# Crear entorno virtual
python -m venv iris-env

# Activar (Linux)
source iris-env/bin/activate

# Activar (Windows)
iris-env\Scripts\activate

# Verificar
which python
```

#### **Opción B: Con conda**
```bash
# Crear entorno virtual
conda create --name iris-env python=3.11

# Activar
conda activate iris-env
```

**✅ Verificar:** En terminal debería aparecer `(iris-env)` al inicio de la línea.

### **3.2 - Crear Archivo .env**

En la **raíz de tu proyecto** (mismo nivel que `main.py`), crea archivo `.env`:

```bash
# === CREDENCIALES SUPABASE ===
# Reemplazar con TUS valores del Paso 1.2
SUPABASE_URL=https://tu-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu-anon-key
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.tu-service-key
JWT_SECRET=tu-jwt-secret-de-supabase

# === CONFIGURACIÓN OPCIONAL ===
DEBUG=true
LOG_LEVEL=INFO
DEFAULT_TIMEZONE=America/Argentina/Buenos_Aires
```

### **3.3 - Instalar Dependencies**

**¡IMPORTANTE!** Asegúrate de que el entorno virtual esté **activo** (ver `(iris-env)` en terminal).

```bash
# Instalar dependencies
pip install -r requirements.txt

# Verificar instalación
pip list | grep fastapi
pip list | grep supabase
```

**✅ Esperado:** Deberías ver fastapi y supabase en la lista.

### **3.4 - Probar Conexión**

**Mac:**
```bash
# Test rápido de conexión
python3 -c "
import asyncio
from app.config.database import check_connection
result = asyncio.run(check_connection())
print('✅ Conexión exitosa' if result else '❌ Error de conexión')
"
```

**Linux/Windows:**
```bash
# Test rápido de conexión
python -c "
import asyncio
from app.config.database import check_connection
result = asyncio.run(check_connection())
print('✅ Conexión exitosa' if result else '❌ Error de conexión')
"
```

### **3.5 - Ejecutar FastAPI**

**Mac:**
```bash
# Opción 1: Con uvicorn
uvicorn main:app --reload

# Opción 2: Con python3
python3 main.py
```

**Linux/Windows:**
```bash
# Opción 1: Con uvicorn
uvicorn main:app --reload

# Opción 2: Con python
python main.py
```

**✅ Verificar:**
- Terminal dice: "Uvicorn running on http://127.0.0.1:8000"
- En browser: http://127.0.0.1:8000 → {"message": "IRIS API está funcionando correctamente"}
- Docs: http://127.0.0.1:8000/docs → Swagger UI carga

## 🎯 **PASO 4: Verificación Final**

### **4.1 - Health Check**

**GET:** http://127.0.0.1:8000/health

**Respuesta esperada:**
```json
{
  "status": "healthy",
  "service": "iris-backend",
  "version": "1.0.0",
  "database": "connected"
}
```

### **4.2 - Logs Funcionando**

En la terminal de FastAPI deberías ver logs como:

```
INFO     iris.http                  http_request_start request_id=a1b2c3d4 method=GET url=http://127.0.0.1:8000/health
INFO     iris                       health_check status=healthy service=iris-backend version=1.0.0 database=connected
INFO     iris.http                  http_request_complete request_id=a1b2c3d4 method=GET path=/health status_code=200 process_time_ms=45.23
```

### **4.3 - Database Browser (Opcional)**

En Supabase dashboard:

1. **Sidebar:** Table Editor
2. **Verificar que ves:** businesses, services, employees, etc.
3. **Click en:** `businesses` → deberías ver "Salón Elegance" y "Beauty Center"

## 🆘 **Errores Comunes**

### **❌ "extension uuid-ossp does not exist"**

**En SQL Editor:**
```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist";
```

### **❌ "ModuleNotFoundError: No module named 'app'"**

**Solución:** Ejecutar FastAPI desde la raíz del proyecto:
```bash
# Asegúrate de estar en la carpeta que contiene main.py
ls -la  # Deberías ver main.py, requirements.txt, .env

# Luego ejecutar
python main.py
```

### **❌ "Error connecting to Supabase"**

1. **Verificar .env:** Que las credenciales sean correctas
2. **Verificar internet:** Que puedas acceder a supabase.com
3. **Test manual:**
```python
from supabase import create_client
client = create_client("tu-url", "tu-key")
print(client.table('businesses').select('name').limit(1).execute())
```

### **❌ "constraint violation" al crear appointments**

¡**Esto es bueno!** Significa que el constraint anti-overlapping funciona.

**Verificar appointments existentes:**
```sql
SELECT employee_id, start_datetime, end_datetime
FROM appointments
WHERE employee_id = 'tu-employee-id'
ORDER BY start_datetime;
```

## 🎉 **¡Setup Completado!**

Si llegaste hasta acá sin errores:

✅ **Base de datos** configurada con 13 tablas
✅ **Constraint anti-overlapping** funcionando
✅ **FastAPI** conectado a Supabase
✅ **Logging estructurado** activo
✅ **Timezone Argentina** configurado
✅ **Datos de ejemplo** para testing

**🚀 ¡IRIS está listo para el desarrollo de APIs!**

---

### **Próximos Pasos:**

1. **Día 2:** Sistema de autenticación híbrido
2. **Día 3:** CRUD de businesses, services, employees
3. **Día 4:** Sistema de appointments con validación
4. **Día 5:** Sistema de loyalty points
5. **Día 6:** Promociones y FAQs
6. **Día 7:** Testing completo y deployment

**💡 Tip:** Guarda este setup en tu documentación personal. Te va a servir para futuros proyectos con FastAPI + Supabase.