# 🧪 Comandos de Testing - IRIS Day 2

**Quick reference para probar las APIs implementadas en el Día 2**

## 🚀 **Setup Rápido**

```bash
# 1. Activar entorno
source iris-env/bin/activate

# 2. Ejecutar FastAPI
python main.py

# 3. En otro terminal, ejecutar tests
python test_day2.py
```

## 📋 **Tests Automáticos**

```bash
# Test completo de APIs sin autenticación
python test_day2.py

# Health check rápido
curl http://localhost:8000/health

# Ver documentación
open http://localhost:8000/docs
```

## 🔑 **Testing con Autenticación**

### **Necesitas:**
1. **Usuario en Supabase** con email/password
2. **JWT token** obtenido de Supabase
3. **Business creado** para testing

### **Obtener JWT Token:**
```bash
# Método 1: Desde Supabase Dashboard
# Settings → API → Generate access token

# Método 2: Login programático (ejemplo)
curl -X POST 'https://YOUR_PROJECT.supabase.co/auth/v1/token?grant_type=password' \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "your_password"
  }'
```

### **Testing con Token:**
```bash
# Reemplaza YOUR_JWT_TOKEN con tu token real
export JWT_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Test auth endpoints
curl -H "Authorization: Bearer $JWT_TOKEN" \
     http://localhost:8000/auth/verify

curl -H "Authorization: Bearer $JWT_TOKEN" \
     http://localhost:8000/auth/me

# Test business endpoints
curl -H "Authorization: Bearer $JWT_TOKEN" \
     http://localhost:8000/businesses/

# Crear business (JSON example)
curl -X POST http://localhost:8000/businesses/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mi Salón Test",
    "description": "Salón de prueba",
    "location": {
      "address": "Av. Corrientes 1234",
      "city": "Buenos Aires",
      "state": "CABA",
      "country": "Argentina"
    },
    "contact": {
      "phone": "+54 11 1234-5678",
      "email": "contacto@salon.com"
    }
  }'
```

## 🏢 **Testing CRUD Businesses**

```bash
# Listar businesses del usuario
curl -H "Authorization: Bearer $JWT_TOKEN" \
     "http://localhost:8000/businesses/"

# Ver business específico
curl -H "Authorization: Bearer $JWT_TOKEN" \
     "http://localhost:8000/businesses/BUSINESS_ID"

# Actualizar business (ejemplo)
curl -X PUT "http://localhost:8000/businesses/BUSINESS_ID" \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Nuevo Nombre"}'

# Desactivar business (soft delete)
curl -X DELETE "http://localhost:8000/businesses/BUSINESS_ID" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

## 💇 **Testing CRUD Services**

```bash
# Listar services de un business
curl -H "Authorization: Bearer $JWT_TOKEN" \
     "http://localhost:8000/services/?business_id=BUSINESS_ID"

# Crear service
curl -X POST http://localhost:8000/services/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "BUSINESS_ID",
    "name": "Corte de Cabello",
    "description": "Corte y peinado",
    "duration_minutes": 45,
    "price": 1500.00,
    "loyalty_points": 15,
    "category": "Cabello"
  }'

# Ver service específico
curl -H "Authorization: Bearer $JWT_TOKEN" \
     "http://localhost:8000/services/SERVICE_ID"
```

## 👥 **Testing CRUD Employees**

```bash
# Listar employees de un business
curl -H "Authorization: Bearer $JWT_TOKEN" \
     "http://localhost:8000/employees/?business_id=BUSINESS_ID"

# Crear employee (solo owners)
curl -X POST http://localhost:8000/employees/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "business_id": "BUSINESS_ID",
    "name": "Juan Pérez",
    "email": "juan@salon.com",
    "phone": "+54 11 9876-5432",
    "specialties": ["Corte", "Peinado", "Coloración"]
  }'
```

## 🔍 **Verificar Base de Datos**

```sql
-- En Supabase SQL Editor
-- Ver businesses creados
SELECT id, name, city, is_active, created_at
FROM businesses
ORDER BY created_at DESC;

-- Ver services
SELECT s.name, s.price, b.name as business_name
FROM services s
JOIN businesses b ON s.business_id = b.id
WHERE s.is_active = true;

-- Ver employees
SELECT e.name, e.email, b.name as business_name
FROM employees e
JOIN businesses b ON e.business_id = b.id
WHERE e.is_active = true;
```

## ⚠️ **Errores Comunes**

### **401 Unauthorized**
- Token JWT inválido o expirado
- Header de Authorization mal formateado
- Usuario no existe en Supabase

### **403 Forbidden**
- Usuario no tiene acceso al business
- Rol insuficiente (ej: employee tratando de crear business)

### **404 Not Found**
- Business/Service/Employee no existe
- ID mal formateado

### **422 Unprocessable Entity**
- Datos de request inválidos
- Validaciones de Pydantic fallaron

## 🎯 **Tests de Validación**

```bash
# Test validación de email
curl -X POST http://localhost:8000/employees/ \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"business_id": "BUSINESS_ID", "name": "Test", "email": "invalid-email"}'
# Expected: 422 error

# Test acceso a business sin permisos
curl -H "Authorization: Bearer $JWT_TOKEN" \
     "http://localhost:8000/services/?business_id=OTRO_BUSINESS_ID"
# Expected: 403 error

# Test rol insuficiente
curl -X DELETE "http://localhost:8000/services/SERVICE_ID" \
  -H "Authorization: Bearer $EMPLOYEE_TOKEN"
# Expected: 403 error (solo owners pueden eliminar)
```

## 📊 **Logs para Debugging**

Los logs aparecen en la terminal donde ejecutas `python main.py`:

```json
{
  "event": "http_request_start",
  "request_id": "abc123",
  "method": "GET",
  "url": "/businesses/",
  "timestamp": "2024-01-15T10:30:00Z"
}

{
  "event": "business_access_verified",
  "user_id": "user123",
  "business_id": "business456",
  "timestamp": "2024-01-15T10:30:01Z"
}
```

---

**🎉 Con estos comandos puedes probar todas las APIs del Día 2!**