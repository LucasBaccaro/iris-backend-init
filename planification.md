Armame un canvas con todo esta planificacion

# IRIS - MVP Planificación Completa

**Sistema de Gestión para Salones de Belleza**



---



## 📋 Resumen Ejecutivo



**Iris** es un SaaS especializado en gestión de salones de belleza que combina reservas inteligentes con un sistema de fidelización por puntos. El MVP se enfoca en las funcionalidades core para validar el mercado antes de agregar features avanzadas de IA.



### 🎯 Objetivos del MVP

- Validar product-market fit en salones de belleza

- Generar primeros $5K MRR en 6 meses

- Onboarding de 50 salones piloto

- Base sólida para features futuras de IA



---



## 🏗️ Arquitectura del MVP



### Stack Tecnológico

- **Backend**: FastAPI + Python 3.11

- **Base de Datos**: PostgreSQL + Supabase

- **Frontend**: Next.js + TypeScript

- **Autenticación**: Supabase Auth

- **Deployment**: Vercel (Frontend) + Railway/Render (Backend)



### Principios Arquitectónicos

- **Multi-tenant**: Un business_id por cada salón

- **Feature-gated**: Sistema preparado para planes futuros

- **Timezone-aware**: Argentina con preparación para LATAM

- **Concurrency-safe**: Prevención de double-booking



---



## 🎨 Features del MVP



### 1. 📅 **Sistema de Reservas (Core)**



**Funcionalidad:**

- Reservas normales con validación de conflictos

- Sobreturnos especiales creados por el dueño

- Validación automática de horarios (salón + empleado)

- Prevención de double-booking con locks

- ON/OFF del salón: El dueño puede cerrar temporalmente

- ON/OFF del empleado: Empleados pueden pausar su calendario



**User Stories:**

- Como cliente, quiero reservar un corte con María a las 15:00

- Como dueño, quiero crear un sobreturno para atender 3 clientes extras el sábado

- Como empleado, quiero ver mis citas del día desde mi móvil

- Como dueño, quiero poner el salón en modo "cerrado" por emergencia

- Como empleado, quiero pausar mi calendario cuando tengo una emergencia



### 2. 🎁 **Sistema de Fidelización**



**Funcionalidad:**

- Puntos por cada servicio completado

- Configuración de puntos por salón

- Historial de puntos por cliente

- Sistema de canjes: Descuentos por puntos acumulados

- Configuración de recompensas por el dueño



**User Stories:**

- Como cliente, quiero ver mis puntos acumulados

- Como dueño, quiero configurar 10 puntos por cada corte

- Como cliente, quiero ver el historial de mis servicios

- Como cliente, quiero canjear 100 puntos por 10% de descuento

- Como dueño, quiero configurar "200 puntos = corte gratis"



### 3. 📢 **Promociones Informativas**



**Funcionalidad:**

- CRUD simple de promociones

- Display para clientes

- Fechas de validez

- Sin lógica de redención (solo informativo)



**User Stories:**

- Como dueño, quiero crear una promoción "20% off en tinturas"

- Como cliente, quiero ver las promociones activas del salón



### 4. ⚙️ **Configuración de Negocio**



**Funcionalidad:**

- Setup inicial del salón

- Gestión de empleados y sus horarios

- Catálogo de servicios con precios y duración

- FAQs básicas (preparación para IA futura)



**User Stories:**

- Como dueño, quiero agregar un nuevo servicio "Keratina - $5000 - 2hrs"

- Como dueño, quiero configurar que Ana trabaja martes a sábado 14-20h



---



## 🗂️ Modelo de Datos



### Entidades Principales



```sql

-- Salones

businesses (id, name, address, phone, timezone, is_active, created_at)



-- Horarios del salón

business_hours (business_id, day_of_week, open_time, close_time)



-- Servicios

services (id, business_id, name, price, duration_minutes, points_awarded)



-- Empleados

employees (id, business_id, user_id, name, phone, status, is_available)



-- Horarios de empleados

employee_hours (employee_id, day_of_week, start_time, end_time)



-- Reservas

appointments (id, business_id, customer_id, employee_id, service_id,

             start_datetime, end_datetime, status, is_override, created_at)



-- Sobreturnos

special_openings (id, business_id, start_datetime, end_datetime,

                 max_extra_appointments, created_by)



-- Sistema de puntos

loyalty_points (id, business_id, customer_id, appointment_id,

               points_earned, transaction_date, transaction_type)



-- Recompensas canjeables

loyalty_rewards (id, business_id, name, description, points_required,

                reward_type, discount_percentage, free_service_id, created_at)



-- Historial de canjes

loyalty_redemptions (id, business_id, customer_id, reward_id,

                    points_used, status, redeemed_at, used_at)



-- Promociones

promotions (id, business_id, title, description, valid_from, valid_until, status)



-- FAQs (preparación para IA)

business_faqs (id, business_id, question, answer, category, created_at)

```



### Constraints Críticos

```sql

-- Prevenir overlapping appointments

EXCLUDE USING gist (

  employee_id WITH =,

  tstzrange(start_datetime, end_datetime) WITH &&

) WHERE (status != 'cancelled' AND is_override = false);



-- Timezone consistency

CHECK (timezone IN ('America/Argentina/Buenos_Aires', 'America/Argentina/Cordoba', ...))

```



---



## 🔐 Modelo de Usuarios y Roles



### Tipos de Usuario



#### 👑 **Business Owner**

- **Acceso**: Dashboard web completo

- **Permisos**: CRUD total en su salón

- **Features**: Gestión de empleados, servicios, horarios, sobreturnos, promociones

- **Control ON/OFF**: Puede cerrar temporalmente el salón

- **Loyalty Management**: Configurar recompensas y aprobar canjes



#### 💄 **Employee**

- **Acceso**: App móvil

- **Permisos**: Ver sus citas, marcar como completadas

- **Features**: Calendario personal, notificaciones

- **Control de disponibilidad**: Toggle ON/OFF de su calendario



#### 🙋‍♀️ **Customer**

- **Acceso**: App móvil + web

- **Permisos**: Reservar, cancelar, ver historial

- **Features**: Reservas, puntos, promociones

- **Canjes**: Usar puntos para descuentos y servicios gratis



### Multi-rol Support

- Un usuario puede ser employee en Salón A y customer en Salón B

- Un usuario puede ser owner de múltiples salones



---



## 🎨 Flujo de Onboarding



### 1. **Registro del Salón** (5 min)

```

📝 Información Básica

├── Nombre del salón

├── Dirección completa

├── Teléfono de contacto

├── Email principal

└── Provincia (para timezone)



⏰ Horarios del Salón

├── Lunes: 9:00 - 18:00

├── Martes: 9:00 - 18:00

├── Miércoles: Cerrado

└── ...

```



### 2. **Setup de Servicios** (10 min)

```

✂️ Servicios Básicos

├── Corte Dama ($1500, 30min, 15 puntos)

├── Corte Caballero ($1200, 20min, 12 puntos)

├── Tintura ($3000, 90min, 30 puntos)

├── Manicura ($800, 45min, 8 puntos)

└── Pedicura ($1000, 60min, 10 puntos)

```



### 3. **Gestión de Empleados** (15 min)

```

👥 Staff del Salón

├── María Pérez

│   ├── Servicios: Corte, Tintura

│   ├── Horarios: Lun-Vie 9:00-17:00

│   └── Teléfono: +54911xxxxxxx

│

└── Ana García

    ├── Servicios: Manicura, Pedicura

    ├── Horarios: Mar-Sab 14:00-20:00

    └── Teléfono: +54911xxxxxxx

```



### 4. **FAQs Básicas** (5 min)

```

❓ Preguntas Frecuentes

├── "¿Aceptan tarjetas?" → "Sí, aceptamos todas las tarjetas"

├── "¿Tienen estacionamiento?" → "Sí, estacionamiento gratuito"

├── "¿Cómo cancelo una cita?" → "Llamando al salón o desde la app"

└── "¿Hay promociones?" → "Consultá nuestras promos vigentes"

```



### 5. **¡Salón Listo!** ✅

- Link público para que clientes reserven

- Dashboard operativo

- Empleados pueden loguearse



---



## 🚀 Roadmap de Desarrollo



### 🎯 **Fase 1: Foundation** (4-6 semanas)

- [ ] Setup de Supabase + PostgreSQL

- [ ] Modelo de datos completo con migrations

- [ ] FastAPI boilerplate con auth

- [ ] CRUD básico de entidades principales

- [ ] Sistema de roles y permisos



### 🎯 **Fase 2: Core Features** (6-8 semanas)

- [ ] API de appointments con concurrency control

- [ ] Sistema de loyalty points automático

- [ ] Onboarding flow completo

- [ ] Dashboard web para business owners

- [ ] API móvil para employees



### 🎯 **Fase 3: Customer Experience** (4-6 semanas)

- [ ] App web para customer booking

- [ ] Sistema de promociones CRUD

- [ ] Notificaciones básicas (email)

- [ ] Timezone handling completo

- [ ] Testing end-to-end



### 🎯 **Fase 4: MVP Launch** (2-4 semanas)

- [ ] Deploy a producción

- [ ] Monitoring y analytics básico

- [ ] Onboarding de salones piloto

- [ ] Feedback loop y iteración



**Total MVP: 16-24 semanas**



---



## 💰 Modelo de Negocio (Post-MVP)



### Planes Futuros (No en MVP)

- **Básico** ($19.99/mes): Appointments + Loyalty

- **Profesional** ($39.99/mes): + Promociones + AI Assistant

- **Premium** ($79.99/mes): + Analytics + Multi-sucursal



### MVP Strategy

- **Gratis durante beta** para primeros 50 salones

- **$29.99/mes flat** después del periodo de prueba

- Focus en validación y feedback, no en monetización



---



## 🎯 Métricas de Éxito del MVP



### Product Metrics

- **50 salones** onboardeados en 6 meses

- **85% completion rate** del onboarding

- **500+ appointments** procesadas semanalmente

- **<5% churn rate** mensual



### Business Metrics

- **$5K MRR** en 6 meses

- **$100 CAC** (Customer Acquisition Cost)

- **$500 LTV** (Lifetime Value) estimado

- **Net Promoter Score >40**



### Technical Metrics

- **99.5% uptime**

- **<200ms API response time**

- **0 data loss incidents**

- **<1% appointment conflicts**



---



## 🔮 Roadmap Post-MVP



### Features de IA (Fase 2)

1. **AI Assistant**: BD vectorial + FAQs para responder consultas

2. **Instagram Agent**: Recomendaciones automáticas de posts

3. **Smart Scheduling**: Optimización automática de horarios

4. **Predictive Analytics**: Forecasting de demanda



### Expansion Features

1. **Multi-sucursal**: Cadenas de salones

2. **Inventory Management**: Control de stock de productos

3. **Financial Reports**: Reportes contables automáticos

4. **Marketing Automation**: Campañas segmentadas



---



## 🛡️ Consideraciones Técnicas



### Seguridad

- **Autenticación robusta** con Supabase Auth

- **Autorización granular** por business_id

- **Input validation** estricta

- **Rate limiting** por endpoint



### Performance

- **Database indexing** optimizado

- **Caching strategy** con Redis

- **Async processing** para operaciones pesadas

- **Monitoring** con métricas en tiempo real



### Escalabilidad

- **Horizontal scaling** preparado

- **Database sharding** strategy

- **CDN** para assets estáticos

- **Load balancing** configurado



---



## ✅ Checklist Pre-Desarrollo



### Definiciones Técnicas

- [x] Stack tecnológico confirmado

- [x] Modelo de datos diseñado

- [x] Flujo de onboarding definido

- [x] User stories documentadas

- [x] Métricas de éxito establecidas



### Validaciones de Negocio

- [ ] **Entrevistas con salones** (5-10 salones target)

- [ ] **Pricing research** de competidores

- [ ] **Feature priority validation** con usuarios

- [ ] **Go-to-market strategy** definida



### Setup Técnico

- [ ] **Repositorio GitHub** creado

- [ ] **Supabase project** configurado

- [ ] **Environment setup** documentado

- [ ] **CI/CD pipeline** diseñado



---



## 📞 Próximos Pasos Inmediatos



1. **Validar plan con 3-5 salones** locales

2. **Crear repositorio** y estructura de proyecto

3. **Setup de Supabase** y schema inicial

4. **Definir sprint planning** (2 semanas sprints)

5. **Comenzar desarrollo** de foundation



---



*Última actualización: 2025-01-15*

*Versión: 1.0*