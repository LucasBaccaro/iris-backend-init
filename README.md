# 🌟 IRIS - Sistema de Gestión para Salones de Belleza

Backend completo desarrollado con **FastAPI** y **Supabase** siguiendo la planificación de `planification.md`.

## 🚀 Estado del Proyecto

### ✅ **Día 1: Setup Base - COMPLETADO**

- [x] **Estructura FastAPI modular** con routers organizados
- [x] **Variables de entorno** para Supabase configuradas
- [x] **Dependencies** completas (FastAPI, Supabase, Pydantic)
- [x] **Sistema de logging estructurado** con Structlog
- [x] **Modelo de datos completo** según planification.md
- [x] **Constraints críticos** para overlapping appointments
- [x] **Timezone handling** completo para Argentina

## 🏗️ Arquitectura

```
iris-backend/
├── app/
│   ├── config/          # Configuración y base de datos
│   ├── routers/         # Endpoints organizados por feature
│   ├── models/          # Modelos Pydantic
│   ├── services/        # Lógica de negocio
│   ├── middleware/      # Logging y autenticación
│   └── utils/           # Utilidades (timezone, validación)
├── database/            # Scripts SQL y migraciones
├── main.py             # Aplicación principal
└── requirements.txt    # Dependencias
```

## 🗄️ Base de Datos

### **Tablas Implementadas** (según planification.md)

- **`businesses`** - Salones con timezone y control ON/OFF
- **`business_hours`** - Horarios por día de semana
- **`services`** - Servicios con precios y puntos
- **`employees`** - Empleados con control disponibilidad
- **`employee_hours`** - Horarios de trabajo por empleado
- **`appointments`** - Reservas con constraint anti-overlapping
- **`special_openings`** - Sobreturnos para dueños
- **`loyalty_points`** - Sistema de puntos automático
- **`loyalty_rewards`** - Recompensas canjeables
- **`loyalty_redemptions`** - Historial de canjes
- **`promotions`** - Promociones informativas
- **`business_faqs`** - FAQs por salón
- **`business_owners`** - Relación propietarios multi-tenant

### **Constraints Críticos**

```sql
-- EL MÁS IMPORTANTE: Prevenir double-booking
EXCLUDE USING gist (
    employee_id WITH =,
    tstzrange(start_datetime, end_datetime) WITH &&
) WHERE (status != 'cancelled' AND is_override = false);
```

## 📊 Sistema de Logging

### **Logging Estructurado con Structlog**

```python
# Logs automáticos para cada request
log_appointment_event(
    event_type="created",
    appointment_id="apt_123",
    business_id="bus_456",
    customer_id="usr_789",
    service_name="Corte Dama"
)
```

### **Tipos de Logs Implementados**

- **HTTP Requests** - Todas las requests automáticamente
- **Business Events** - Appointments, puntos, etc.
- **Security Events** - Autenticación y validación
- **Database Operations** - Queries con performance
- **Error Tracking** - Errores con contexto completo

## 🌍 Timezone Handling

### **Soporte Completo para Argentina**

- **Buenos Aires, Córdoba, Mendoza, Tucumán, etc.**
- **Conversiones automáticas** UTC ↔ Local
- **Validación de horarios** considerando timezone
- **Formateo argentino** DD/MM/YYYY HH:MM

```python
# Ejemplo de uso
handler = TimezoneHandler('America/Argentina/Buenos_Aires')
current_time = handler.get_current_business_time()
formatted = handler.format_for_argentina(datetime.now())
```

## 🔧 Configuración

### **Variables de Entorno**

```bash
# .env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
SUPABASE_SERVICE_KEY=tu-service-key
JWT_SECRET=tu-jwt-secret
DEBUG=true
DEFAULT_TIMEZONE=America/Argentina/Buenos_Aires
```

### **Setup de Base de Datos**

```sql
-- En Supabase SQL Editor:
\i /database/setup_database.sql
```

## 🚀 Setup Rápido (15 minutos)

### **1. Configurar Supabase**

Seguí la guía completa en → **[`SETUP_GUIDE.md`](SETUP_GUIDE.md)**

**Resumen rápido:**
1. Crear proyecto en [supabase.com](https://supabase.com)
2. Ejecutar `database/schema.sql` en SQL Editor
3. Ejecutar `database/constraints_simple.sql` en SQL Editor
4. (Opcional) Ejecutar `database/sample_data.sql` para datos de prueba

### **2. Configurar Environment**

```bash
cp .env.example .env
# Completar con tus credenciales de Supabase
```

### **3. Instalar y Ejecutar**

```bash
pip install -r requirements.txt
python main.py
```

### **4. Verificar que Funciona**

- **API**: http://localhost:8000 → `{"message": "IRIS API está funcionando correctamente"}`
- **Health**: http://localhost:8000/health → `{"status": "healthy", "database": "connected"}`
- **Docs**: http://localhost:8000/docs → Swagger UI

## 🎯 Próximos Pasos (Día 2)

### **Sistema de Autenticación Híbrido**

- [x] Middleware verificador de JWT
- [ ] Funciones de validación de acceso por business_id
- [ ] Decorators para proteger endpoints
- [ ] Sistema de roles (Owner/Employee/Customer)

### **APIs Básicas**

- [ ] CRUD de Businesses
- [ ] CRUD de Employees
- [ ] CRUD de Services
- [ ] CRUD de Appointments (con validación de conflictos)

## 🏆 Features Únicas de IRIS

### **1. Multi-tenant Inteligente**
- Un usuario puede ser **owner** de múltiples salones
- Un usuario puede ser **employee** en algunos y **customer** en otros
- Validación automática por `business_id`

### **2. Sistema de Overlapping Prevention**
- **Constraint PostgreSQL** que previene double-booking
- **Locks de aplicación** para concurrencia
- **Sobreturnos especiales** solo para owners

### **3. Timezone Nativo Argentino**
- Soporte nativo para **todas las provincias**
- **Validación de horarios** considerando zona horaria
- **Formateo argentino** en todas las interfaces

### **4. Logging de Nivel Enterprise**
- **Trazabilidad completa** de todas las operaciones
- **Contexto enriquecido** con business_id, user_id
- **Performance monitoring** automático

## 📚 Documentación Detallada

- **`/database/README.md`** - Documentación completa de la base de datos
- **`/app/config/logging_examples.py`** - Ejemplos de uso del sistema de logging
- **`planification.md`** - Planificación completa del proyecto

## 🎉 Logros del Día 1

✅ **Setup completo** en 1 día (estimado: 2 días)
✅ **Base de datos production-ready** con constraints críticos
✅ **Logging enterprise-grade** listo para producción
✅ **Timezone handling** completo para Argentina
✅ **Arquitectura escalable** preparada para el MVP completo

---

> 💡 **Filosofía IRIS**: Cada línea de código está **comentada en español** y **documentada** para facilitar el mantenimiento y la colaboración del equipo.

**¡IRIS está listo para brillar! ✨**