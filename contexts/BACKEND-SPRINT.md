# **Tareas de Backend para el MVP de Iris**

Este documento detalla todas las tareas de ingeniería de software backend para el desarrollo del MVP de Iris, organizadas por fases y sprints. Cada tarea incluye una breve descripción y una nota sobre el testing asociado.

### **Fase 1: Foundation (Sprints 1-3)**

**1\. Configuración del Entorno y Repositorio**

* \[x\] Crear el repositorio de GitHub.
  ✅ **Completado** - Repositorio creado y configurado
* \[x\] Configurar el entorno de desarrollo local con Python 3.11.
  ✅ **Completado** - Estructura de directorios creada: `src/`, `contexts/`, etc.
* \[x\] Inicializar el proyecto FastAPI.
  ✅ **Completado** - FastAPI configurado en `src/main.py` con CORS y middleware
* \[x\] Crear el archivo requirements.txt con las dependencias necesarias.
  ✅ **Completado** - Incluye FastAPI, Supabase, auth, testing, etc.

**2\. Setup de Supabase y Migraciones**

* \[x\] Configurar un nuevo proyecto en Supabase.
  ✅ **Completado** - Proyecto Supabase configurado por el usuario
* \[x\] Crear el esquema de la base de datos (tablas businesses, employees, services, etc.) y las relaciones.
  ✅ **Completado** - Script SQL completo entregado con todas las tablas, constraints, funciones y datos de ejemplo
* \[ \] Implementar un sistema de migraciones para la base de datos (por ejemplo, con Alembic).
  📋 **Pendiente** - Se priorizó el esquema directo, Alembic se implementará después
* **Testing:** Escribir scripts de prueba para verificar que el esquema se crea y se elimina correctamente.

**3\. Autenticación y Sistema de Roles**

* \[x\] Integrar Supabase Auth con FastAPI para la autenticación de usuarios.
  ✅ **Completado** - Sistema simplificado implementado en `src/core/auth.py` con validación JWT
* \[x\] Crear endpoints para el registro, inicio de sesión y refresco de tokens.
  ✅ **Optimizado** - Auth manejada desde frontend, backend solo valida tokens de Supabase
* \[x\] Implementar la lógica para asignar roles (owner, employee, customer) y manejar los permisos de manera granular (business\_id).
  ✅ **Completado** - RoleChecker y get_user_business_id implementados
* **Testing:** Escribir pruebas unitarias y de integración para asegurar que solo los usuarios autorizados puedan acceder a endpoints específicos.
  ✅ **Implementado** - Endpoints de test creados en `/test/*` para verificar auth y conexiones

**4\. Endpoints CRUD Base**

* \[ \] Desarrollar los endpoints **CRUD** (Crear, Leer, Actualizar, Borrar) para las entidades principales: businesses, employees, services, promotions.  
* \[ \] Implementar la lógica para generar y asociar el access\_code único cuando se crea un negocio.  
* **Testing:** Escribir un conjunto de pruebas para cada endpoint que valide la creación, lectura, actualización y borrado de datos, y que verifique la correcta asignación de business\_id.

### **Fase 2: Core Features (Sprints 4-7)**

**1\. Sistema de Reservas (Núcleo)**

* \[ \] Diseñar e implementar la API de reservas (appointments).  
* \[ \] Desarrollar la lógica de validación para evitar conflictos de horario, considerando los horarios del salón y de los empleados.  
* \[ \] Implementar la lógica de "locks" a nivel de base de datos para prevenir el **double-booking**.  
* \[ \] Crear endpoints para que el owner y el employee puedan alternar su disponibilidad (ON/OFF).  
* **Testing:** Desarrollar pruebas de concurrencia para simular reservas simultáneas y confirmar que la lógica de locks funciona correctamente. Escribir pruebas que verifiquen la validación de horarios y el comportamiento ON/OFF.

**2\. Sistema de Fidelización**

* \[ \] Implementar la lógica para que el sistema otorgue puntos automáticamente después de cada appointment completado.  
* \[ \] Crear endpoints para que el owner pueda configurar las recompensas (loyalty\_rewards).  
* \[ \] Desarrollar la lógica de canje de puntos por descuentos o servicios.  
* **Testing:** Escribir pruebas unitarias que verifiquen el cálculo de puntos y pruebas de integración para el canje, asegurando que los puntos se deducen correctamente.

**3\. Flujo de Onboarding**

* \[ \] Crear los endpoints para el registro inicial del business, sus horarios, servicios y empleados.  
* \[ \] Implementar una transacción de base de datos para asegurar que todo el proceso de onboarding sea atómico (se completa todo o no se guarda nada).  
* **Testing:** Simular el flujo de onboarding completo en una sola prueba para garantizar que todos los datos se persistan correctamente y que no haya errores de integridad.

### **Fase 3: Customer Experience (Sprints 8-10)**

**1\. Gestión de Promociones**

* \[ \] Crear los endpoints **CRUD** para las promociones (promotions).  
* \[ \] Implementar la lógica para que solo se muestren las promociones válidas a los clientes (valid\_from y valid\_until).  
* **Testing:** Probar los casos de CRUD y, de manera crucial, la lógica de validación de fechas.

**2\. Notificaciones**

* \[ \] Integrar un servicio de envío de correos electrónicos (por ejemplo, con Postmark o SendGrid).  
* \[ \] Crear una tarea asíncrona que envíe notificaciones de confirmación de reserva y recordatorios.  
* **Testing:** Escribir una prueba de integración que verifique que la función de envío de notificaciones es invocada con los datos correctos.

**3\. Manejo de Timezones**

* \[ \] Implementar la lógica para que todas las operaciones de fecha y hora se guarden en UTC y se adapten a la timezone del salón para la presentación.  
* **Testing:** Escribir pruebas con diferentes zonas horarias para asegurar que los horarios se calculen y muestren correctamente sin importar dónde se encuentre el cliente o el salón.

### **Fase 4: MVP Launch (Sprints 11-12)**

**1\. Pipeline de CI/CD y Deployment**

* \[ \] Configurar un pipeline de CI/CD para automatizar las pruebas y el despliegue del backend en Railway o Render.  
* **Testing:** Verificación de que el pipeline se ejecuta sin errores al hacer un push al repositorio.

**2\. Monitoreo y Logging**

* \[ \] Configurar structlog para generar logs estructurados y útiles.  
* \[ \] Integrar una herramienta de monitoreo y APM (Application Performance Management) como Sentry o Datadog para el seguimiento de errores y rendimiento.  
* **Testing:** Validar que los logs se están generando correctamente para diferentes eventos y errores.