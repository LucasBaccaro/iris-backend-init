¡Entendido! Vamos a desglosar esto en prompts específicos para cada sprint, con un nivel de detalle mucho mayor para cada tarea. Esto permitirá al agente de IA (y a ti) abordar cada etapa con máxima claridad y precisión.

Adoptaré el tono riguroso acordado, cuestionando, verificando y priorizando la exactitud.

---

# **Plan de Sprints Detallado para el Backend de Iris (MVP)**

Este documento desglosa las tareas de ingeniería de software backend para el MVP de Iris en prompts específicos para cada sprint, incluyendo descripción, requisitos, entregables y testing asociado.

---

### **Fase 1: Foundation**

**Objetivo de la Fase:** Establecer la infraestructura técnica fundamental, incluyendo el entorno de desarrollo, la base de datos con roles, y un sistema de autenticación y autorización robusto controlado por el backend.

---

## **SPRINT 1: Configuración de Entorno y Esquema de Base de Datos Base**

**Objetivo del Sprint:** Tener un proyecto FastAPI inicializado, un entorno de desarrollo funcional, un repositorio configurado, y el esquema de base de datos básico (incluyendo `user_profiles`) definido en Supabase y listo para usar.

**1\. Configuración del Entorno y Repositorio**

*   **1.1. Tarea: Crear el repositorio de GitHub y configurar el control de versiones.**
    *   **Prompt para el Agente:** "Asegura que el repositorio `iris-backend` esté creado en GitHub bajo la organización/cuenta especificada. Configura un flujo de trabajo de Git (ej., `git-flow` simplificado o `main` + `feature branches`) y un archivo `.gitignore` adecuado para proyectos Python/FastAPI, excluyendo dependencias (`venv/`, `__pycache__/`, `.env`) y archivos sensibles."
    *   **Entregable:** Repositorio de GitHub inicializado con estructura básica y `.gitignore`.
    *   **Testing:** Verificación manual de la existencia y configuración del repositorio.
*   **1.2. Tarea: Configurar el entorno de desarrollo local con Python 3.11.**
    *   **Prompt para el Agente:** "Crea un entorno virtual de Python (`venv`) para el proyecto y actívalo. Instala las versiones de Python 3.11 en el entorno de desarrollo. Asegura que la estructura de directorios inicial sea `src/` para el código fuente, y subdirectorios como `src/core/`, `src/api/`, `src/db/`, `src/schemas/`, `src/models/`, `src/utils/` dentro de `src/`."
    *   **Entregable:** Entorno virtual de Python 3.11 configurado y estructura de directorios básica.
    *   **Testing:** Ejecución de `python --version` dentro del `venv` para confirmar 3.11. Verificación de la estructura de carpetas.
*   **1.3. Tarea: Inicializar el proyecto FastAPI.**
    *   **Prompt para el Agente:** "Dentro de `src/`, crea el archivo `main.py`. Configura una aplicación FastAPI básica con un `middleware` para CORS (permitiendo orígenes específicos, métodos y encabezados, especialmente `Authorization`). Incluye un `middleware` para el manejo de excepciones global y un endpoint de salud (`/health`) que retorne un estado HTTP 200."
    *   **Entregable:** `src/main.py` con FastAPI configurado, CORS, middleware de errores, y `/health` endpoint.
    *   **Testing:** Inicio de la aplicación (`uvicorn src.main:app --reload`) y acceso a `/health` desde un navegador/cliente HTTP para verificar el estado 200 y el funcionamiento de CORS con un origen diferente.
*   **1.4. Tarea: Crear el archivo `requirements.txt` con las dependencias necesarias.**
    *   **Prompt para el Agente:** "Identifica e instala las dependencias iniciales para FastAPI, Supabase, autenticación JWT y testing. Crea un archivo `requirements.txt` con estas dependencias. Las dependencias mínimas requeridas incluyen: `fastapi`, `uvicorn[standard]`, `python-jose[cryptography]`, `passlib[bcrypt]`, `supabase-py`, `pydantic`, `psycopg2-binary` (o `asyncpg`), `python-dotenv`, `pytest`, `httpx`."
    *   **Entregable:** `requirements.txt` con las dependencias listadas y confirmación de su instalación.
    *   **Testing:** Ejecución de `pip install -r requirements.txt` en un entorno virtual limpio para verificar que todas las dependencias se instalan sin errores.

**2\. Setup de Supabase y Migraciones**

*   **2.1. Tarea: Configurar un nuevo proyecto en Supabase.**
    *   **Prompt para el Agente:** "Asegura que un proyecto de Supabase esté aprovisionado y que se tenga acceso a su 'Project URL' y 'Anon Key' y 'Service Role Key'. Estas claves se deben almacenar de forma segura (ej. en un archivo `.env` local para desarrollo y variables de entorno en producción)."
    *   **Entregable:** Confirmación de acceso a las credenciales de Supabase.
    *   **Testing:** Ping básico a la API de Supabase desde un script Python con las claves.
*   **2.2. Tarea: Diseñar y crear el esquema inicial de la base de datos, incluyendo la tabla `user_profiles`.**
    *   **Prompt para el Agente:** "Diseña y proporciona el script SQL completo para la creación de las tablas principales (`businesses`, `employees`, `services`, `promotions`, `appointments`) con sus columnas, tipos de datos, claves primarias/foráneas, y constraints. **Enfócate en la tabla `user_profiles` con la siguiente estructura y lógica:**
        *   `CREATE TABLE public.user_profiles (`
        *   `id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,`
        *   `role TEXT NOT NULL DEFAULT 'customer' CHECK (role IN ('owner', 'employee', 'customer')),`
        *   `business_id UUID REFERENCES public.businesses(id) ON DELETE SET NULL,`
        *   `first_name TEXT,`
        *   `last_name TEXT,`
        *   `phone_number TEXT UNIQUE,`
        *   `created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP`
        *   `);`
        *   Asegura que el `business_id` en `user_profiles` sea `NULLable` para soportar clientes generales o propietarios antes de crear su primer negocio. Incluye las relaciones con las otras tablas (ej. `employees` referenciando `user_profiles.id`, `appointments` referenciando `user_profiles.id` como `customer_id` y `employee_id`). Define las políticas de Row Level Security (RLS) básicas para `user_profiles` y `businesses` (ej. `SELECT` a todos para `customer`, `ALL` para `owner`/`employee` en su `business_id`)."
    *   **Entregable:** Script SQL completo para la creación del esquema y configuración de RLS iniciales. Ejecución exitosa de este script en Supabase.
    *   **Testing:** Escribir un script SQL para verificar la existencia de todas las tablas, columnas, claves y constraints. Intentar insertar datos que violen las constraints (ej., rol inválido, `id` de usuario inexistente) para confirmar su funcionamiento.
*   **2.3. Tarea: Implementar un sistema de migraciones para la base de datos (con Alembic).**
    *   **Prompt para el Agente:** "Configura Alembic para el proyecto. Inicializa Alembic y genera la migración inicial que refleje el esquema actual de Supabase (es decir, el script SQL de la tarea anterior). Aplica esta migración para confirmar que Alembic está configurado correctamente para detectar cambios futuros. Asegura que el archivo de configuración de Alembic (`alembic.ini`) esté adaptado para la conexión a PostgreSQL de Supabase."
    *   **Entregable:** Configuración de Alembic en el proyecto, migración inicial generada y aplicada.
    *   **Testing:** Ejecutar `alembic revision --autogenerate -m "Initial schema"` y `alembic upgrade head`. Verificar que no haya errores y que el estado de la base de datos sea el esperado.

---

## **SPRINT 2: Autenticación Backend-Centric (Registro y Setup Inicial)**

**Objetivo del Sprint:** Implementar los endpoints de registro de usuarios (Owner, Employee, Customer) que interactúan con Supabase Auth y la tabla `user_profiles` del backend, asegurando la atomicidad y las restricciones de seguridad adecuadas.

**3\. Autenticación y Sistema de Roles**

*   **3.1. Tarea: Integrar el cliente Supabase en FastAPI y configurar la validación JWT.**
    *   **Prompt para el Agente:** "Crea una instancia global (o dependencia) del cliente Supabase en FastAPI, utilizando las claves `anon_key` y `service_role_key` de forma segura. Implementa una dependencia de FastAPI (`Depends`) que se encargue de:
        1.  Extraer el JWT del encabezado `Authorization: Bearer`.
        2.  Validar el JWT usando `python-jose` o la lógica de validación de Supabase (asegurando que el token esté firmado por Supabase y no haya expirado).
        3.  Extraer el `user_id` (sub) del JWT validado.
        4.  Retornar el `user_id` para su uso en otras dependencias o lógica de negocio.
        Implementa un modelo Pydantic `User` que contenga al menos el `id` (UUID) del usuario y un `is_authenticated` booleano."
    *   **Entregable:** Dependencia de FastAPI `get_current_user` (o similar) que valide JWTs de Supabase y extraiga el `user_id`.
    *   **Testing:** Crear un endpoint de prueba `/protected` que use esta dependencia. Enviar una solicitud con un JWT válido y otra con uno inválido/expirado para verificar las respuestas correctas (200 OK vs 401 Unauthorized).
*   **3.2. Tarea: Crear los endpoints de registro de usuarios (`/auth/register/{role}`).**
    *   **Prompt para el Agente:** "Implementa los siguientes endpoints POST en el router de autenticación (`src/api/auth.py`):

        *   **`POST /auth/register/owner`**
            *   **Descripción:** Permite el registro del primer propietario del sistema.
            *   **Requisitos de Seguridad CRÍTICA:**
                1.  **Restricción de Acceso:** Este endpoint **NO DEBE SER PÚBLICO**. Requiere un encabezado `X-Admin-Secret` con un valor pre-configurado (ej., variable de entorno). Si el `X-Admin-Secret` es incorrecto, responder con 403 Forbidden.
                2.  **Unicidad del Propietario:** Antes de proceder, verificar si ya existe un usuario con `role='owner'` en la tabla `user_profiles`. Si existe, responder con 409 Conflict.
            *   **Lógica:**
                1.  Recibir email y password (Pydantic `OwnerRegisterSchema`).
                2.  Llamar a `supabase_client.auth.admin.create_user()` con el email y password.
                3.  Si la creación en `auth.users` es exitosa:
                    *   Crear un nuevo `business` en `public.businesses` (generando un `access_code` único).
                    *   Insertar una entrada en `public.user_profiles` con el `id` del usuario recién creado, `role='owner'` y el `business_id` del nuevo negocio.
                    *   **Manejo de Transacciones/Atomicidad:** Implementar un bloque `try-except-finally` robusto. Si la creación del `business` o `user_profiles` falla, **eliminar el usuario de `auth.users`** utilizando `supabase_client.auth.admin.delete_user()` para evitar inconsistencias.
                4.  Devolver los tokens de sesión (Access Token, Refresh Token) obtenidos de `supabase_client.auth.admin.invite_user_by_email` o `create_user` si Supabase los retorna directamente, o realizar un `signInWithPassword` si es necesario para obtenerlos.
            *   **Salida:** HTTP 201 Created con el usuario (sin password), Access Token y Refresh Token.
        *   **`POST /auth/register/employee`**
            *   **Descripción:** Permite a un propietario (o un empleado autorizado) registrar un nuevo empleado.
            *   **Autorización:** Este endpoint debe estar protegido por la dependencia de validación JWT (del paso 3.1) y una nueva dependencia `RoleChecker(required_roles=['owner'])` para asegurar que solo los propietarios autenticados puedan acceder.
            *   **Lógica:**
                1.  Recibir email y password (Pydantic `EmployeeRegisterSchema`).
                2.  Obtener el `user_id` y `business_id` del propietario autenticado desde el JWT validado y `user_profiles`.
                3.  Llamar a `supabase_client.auth.admin.create_user()` para el nuevo empleado.
                4.  Si la creación en `auth.users` es exitosa:
                    *   Insertar una entrada en `public.user_profiles` con el `id` del nuevo usuario, `role='employee'` y el `business_id` del propietario que lo registró.
                    *   **Manejo de Transacciones/Atomicidad:** Si la creación del `user_profiles` falla, **eliminar el usuario de `auth.users`**.
                5.  Devolver los tokens de sesión del nuevo empleado.
            *   **Salida:** HTTP 201 Created con el nuevo empleado, Access Token y Refresh Token.
        *   **`POST /auth/register/customer`**
            *   **Descripción:** Permite el auto-registro de clientes. Puede ser llamado por un usuario no autenticado.
            *   **Lógica:**
                1.  Recibir email y password (Pydantic `CustomerRegisterSchema`).
                2.  Llamar a `supabase_client.auth.sign_up()` (para auto-registro) o `supabase_client.auth.admin.create_user()` (si un admin/owner lo registra). Si es `sign_up`, Supabase enviará un correo de confirmación.
                3.  Si la creación en `auth.users` es exitosa:
                    *   Insertar una entrada en `public.user_profiles` con el `id` del nuevo usuario, `role='customer'`.
                    *   Opcionalmente, si la solicitud viene de un `owner`/`employee` autenticado, asociar el `business_id` del solicitante al cliente (dependiendo de la lógica de negocio si un cliente puede pertenecer a varios negocios).
                    *   **Manejo de Transacciones/Atomicidad:** Si la creación del `user_profiles` falla, **eliminar el usuario de `auth.users`** (si se usó `admin.create_user`). Para `sign_up`, Supabase lo maneja, pero si el perfil falla, el usuario existiría pero sin rol, lo cual es un estado indeseado y debe ser detectado.
                4.  Devolver los tokens de sesión del nuevo cliente (si `sign_up` devuelve los tokens o si se usó `admin.create_user`).
            *   **Salida:** HTTP 201 Created con el nuevo cliente, Access Token y Refresh Token.

    *   **Entregable:** Implementación de los tres endpoints de registro en FastAPI con las validaciones y lógicas de atomicidad.
    *   **Testing:**
        *   **Unitarias:** Pruebas para la lógica de atomicidad (simular fallos en la BD y verificar la eliminación en `auth.users`).
        *   **Integración (con `httpx`):**
            *   Probar `POST /auth/register/owner` con `X-Admin-Secret` correcto e incorrecto.
            *   Probar `POST /auth/register/owner` intentando crear un segundo owner.
            *   Probar `POST /auth/register/employee` con un owner autenticado y con un usuario no autorizado.
            *   Probar `POST /auth/register/customer` como auto-registro.
            *   Verificar que `auth.users` y `public.user_profiles` se actualizan correctamente para cada rol.
            *   Verificar que los Access y Refresh Tokens son retornados y parecen válidos (estructura JWT).

---

## **SPRINT 3: Autenticación Avanzada y Endpoints CRUD Base**

**Objetivo del Sprint:** Completar el sistema de autenticación con endpoints de login y refresco de tokens, implementar la lógica de autorización granular basada en roles y `business_id` (RoleChecker), y desarrollar los primeros endpoints CRUD básicos para las entidades principales.

**3\. Autenticación y Sistema de Roles (Continuación)**

*   **3.3. Tarea: Crear los endpoints de autenticación (`/auth/login`, `/auth/refresh_token`).**
    *   **Prompt para el Agente:** "Implementa los siguientes endpoints POST en el router de autenticación (`src/api/auth.py`):

        *   **`POST /auth/login`**
            *   **Descripción:** Permite a un usuario existente iniciar sesión.
            *   **Lógica:**
                1.  Recibir email y password (Pydantic `LoginSchema`).
                2.  Llamar a `supabase_client.auth.sign_in_with_password()`.
                3.  Si la autenticación es exitosa:
                    *   Obtener el `user_id` del usuario autenticado.
                    *   Consultar `public.user_profiles` para obtener el `role` y `business_id` asociados a ese `user_id`.
                4.  Devolver el Access Token (JWT), Refresh Token (ambos de Supabase), y la información de `role` y `business_id` del usuario al frontend.
            *   **Salida:** HTTP 200 OK con el Access Token, Refresh Token, `user_id`, `role`, `business_id`.
        *   **`POST /auth/refresh_token`**
            *   **Descripción:** Permite al frontend obtener un nuevo Access Token cuando el actual expira, utilizando el Refresh Token.
            *   **Lógica:**
                1.  Recibir el Refresh Token del frontend (Pydantic `RefreshTokenSchema`).
                2.  Llamar a `supabase_client.auth.refresh_session()` con el Refresh Token.
                3.  Si el refresco es exitoso:
                    *   Devolver el **nuevo Access Token** y el **nuevo Refresh Token** (si Supabase los rota) al frontend.
            *   **Salida:** HTTP 200 OK con el nuevo Access Token y Refresh Token.
    *   **Entregable:** Implementación de los endpoints `login` y `refresh_token`.
    *   **Testing:**
        *   **Integración:**
            *   Probar `POST /auth/login` con credenciales correctas e incorrectas, verificando las respuestas (200 OK con tokens vs 400/401).
            *   Probar `POST /auth/refresh_token` con un refresh token válido e inválido/expirado, verificando las respuestas y la rotación de tokens.
            *   Simular el ciclo completo: login -> usar Access Token -> esperar expiración (o forzarla con un token de vida muy corta) -> usar Refresh Token -> usar el nuevo Access Token.

*   **3.4. Tarea: Implementar la lógica de roles y permisos granular (`RoleChecker`).**
    *   **Prompt para el Agente:** "Crea una dependencia de FastAPI (`src/core/auth.py`) llamada `RoleChecker` que:
        1.  Tome como argumento una lista de `required_roles` (ej., `['owner', 'employee']`).
        2.  Utilice la dependencia de validación JWT (del paso 3.1) para obtener el `user_id` del usuario autenticado.
        3.  Consulta la tabla `public.user_profiles` para obtener el `role` y `business_id` de ese `user_id`.
        4.  Si el `role` del usuario no está en `required_roles`, eleva una `HTTPException(status_code=403, detail="Not authorized")`.
        5.  Si el rol es válido, devuelve el objeto `User` enriquecido con `role` y `business_id`.
        Crea otra dependencia `get_user_business_id` que utilice `RoleChecker` y retorne únicamente el `business_id` del usuario actual."
    *   **Entregable:** Dependencias `RoleChecker` y `get_user_business_id` funcionales.
    *   **Testing:**
        *   **Unitarias:** Pruebas para `RoleChecker` con diferentes roles y requisitos (ej., usuario 'customer' intentando acceder a un endpoint solo para 'owner').
        *   **Integración:** Aplicar `RoleChecker` a un endpoint de prueba y verificar el acceso con usuarios de diferentes roles y `business_id`.

**4\. Endpoints CRUD Base**

*   \[ \] **Tarea:** Desarrollar los endpoints **CRUD** (Crear, Leer, Actualizar, Borrar) para `businesses`, `employees`, `services`, `promotions`.
    *   **Prompt para el Agente:** "Para cada una de las entidades (`businesses`, `employees`, `services`, `promotions`):
        1.  **Modelos Pydantic:** Crea los esquemas Pydantic (`src/schemas/`) para la validación de entrada (Crear, Actualizar) y la serialización de salida (Leer).
        2.  **Capa de Servicios:** Implementa una capa de servicios (`src/services/`) que contenga la lógica de negocio y las interacciones con la base de datos (utilizando el cliente Supabase para ejecutar consultas SQL o funciones). Esta capa debe ser agnóstica a FastAPI.
        3.  **Routers de FastAPI:** Crea routers dedicados (`src/api/`) con los endpoints HTTP para las operaciones CRUD.
        4.  **Autorización (RoleChecker):** Protege cada endpoint CRUD con la dependencia `RoleChecker` y, donde sea apropiado, con `get_user_business_id` para asegurar que:
            *   Solo los `owners` pueden crear/actualizar/borrar `businesses`.
            *   Los `employees` pueden leer información de su `business`.
            *   Las operaciones sobre `employees`, `services`, `promotions` estén vinculadas al `business_id` del usuario autenticado.
            *   **Filtrado por `business_id`:** Asegura que todas las operaciones de lectura, actualización y borrado de `employees`, `services`, `promotions` solo afecten a recursos que pertenecen al `business_id` del usuario autenticado.
        5.  **Generación de `access_code`:** Al crear un nuevo `business`, implementa la lógica en la capa de servicios para generar un `access_code` único (ej., un UUID corto o string alfanumérico aleatorio) y asociarlo al negocio.
    *   **Entregable:** Conjunto completo de endpoints CRUD para las entidades especificadas, con validación Pydantic, lógica de servicios y autorización `RoleChecker` aplicada.
    *   **Testing:**
        *   **Unitarias:** Pruebas para la capa de servicios (ej., verificar que las funciones de creación/actualización manipulan los datos correctamente sin depender de FastAPI).
        *   **Integración:**
            *   **Creación:** Probar la creación de cada entidad por un usuario autorizado, verificando la persistencia y la asignación del `business_id`. Verificar que el `access_code` se genera para los `businesses`.
            *   **Lectura:** Probar la lectura de colecciones y elementos individuales, verificando que los resultados se filtran por `business_id` del usuario y que los usuarios no pueden ver datos de otros negocios.
            *   **Actualización:** Probar la actualización de datos por usuarios autorizados, verificando que solo pueden modificar recursos de su propio negocio.
            *   **Borrado:** Probar el borrado de datos por usuarios autorizados, verificando la eliminación y las restricciones de integridad.
            *   **Pruebas de Autorización:** Intentar realizar operaciones CRUD con usuarios no autorizados o con el `business_id` incorrecto, verificando las respuestas 403 Forbidden.

---

### **Fase 2: Core Features**

## **SPRINT 4: Sistema de Reservas (Núcleo)**

**Objetivo del Sprint:** Implementar la lógica fundamental para la gestión de reservas de citas, incluyendo la validación de horarios y la prevención de "double-booking".

*   **1.1. Tarea: Diseñar e implementar la API de reservas (`appointments`).**
    *   **Prompt para el Agente:** "Diseña el modelo de base de datos para `appointments` (fecha, hora de inicio, hora de fin, `customer_id`, `employee_id`, `service_id`, `business_id`, estado, etc.). Crea los esquemas Pydantic para crear, leer, actualizar y listar citas. Desarrolla los endpoints CRUD para `appointments` en FastAPI, asegurando que `customer_id`, `employee_id`, `service_id` y `business_id` sean correctamente asociados y validados."
    *   **Entregable:** Modelos de BD, esquemas Pydantic y endpoints CRUD para `appointments`.
    *   **Testing:** Pruebas CRUD básicas con diferentes roles (customer, employee, owner) y validación de la asociación a `business_id`.
*   **1.2. Tarea: Desarrollar la lógica de validación de horarios.**
    *   **Prompt para el Agente:** "Implementa la lógica en la capa de servicios para validar que una nueva reserva de cita no entra en conflicto con:
        1.  Los horarios de operación definidos para el `business`.
        2.  La disponibilidad del `employee` asignado (horario de trabajo, otras citas, etc.).
        Esta lógica debe ejecutarse antes de cualquier intento de inserción en la base de datos."
    *   **Entregable:** Funciones de validación de horarios en la capa de servicios.
    *   **Testing:** Pruebas unitarias para la lógica de validación con escenarios de conflicto y no conflicto (ej., cita fuera de horario del salón, cita superpuesta con otra del empleado).
*   **1.3. Tarea: Implementar la lógica de "locks" para prevenir el `double-booking`.**
    *   **Prompt para el Agente:** "Para prevenir que dos clientes intenten reservar la misma franja horaria para el mismo empleado simultáneamente, implementa un mecanismo de bloqueo a nivel de base de datos. Considera:
        1.  **Bloqueo Pesimista (SQL):** Utilizar `SELECT FOR UPDATE` en la transacción de creación de la cita para bloquear temporalmente las filas relevantes (`employee` y franjas horarias).
        2.  **Constraints de Base de Datos:** Explorar si es posible una constraint `EXCLUDE` en PostgreSQL para rangos de tiempo (PostgreSQL `pg_trgm` o `btree_gist` para `OVERLAPS` con `daterange`/`tsrange` types) para que la base de datos fuerce la unicidad de las franjas horarias por empleado. Esto sería lo más robusto.
    *   **Entregable:** Implementación de la lógica de bloqueo en la creación de citas.
    *   **Testing:** **Pruebas de concurrencia** utilizando múltiples clientes de prueba (`httpx` asíncrono) que intenten reservar la misma franja horaria simultáneamente. Verificar que solo una operación es exitosa y las otras fallan con un error apropiado.
*   **1.4. Tarea: Crear endpoints para que el `owner` y `employee` gestionen su disponibilidad.**
    *   **Prompt para el Agente:** "Implementa endpoints que permitan a los `owners` y `employees` marcar bloques de tiempo como 'no disponibles' (ej., para descansos, reuniones o días libres). Esto debe afectar la lógica de validación de horarios de las citas."
    *   **Entregable:** Endpoints para gestionar la disponibilidad de empleados y la integración con la lógica de validación de reservas.
    *   **Testing:** Probar la marcación de disponibilidad ON/OFF y verificar que las citas intentadas en esos bloques de tiempo sean rechazadas.

---

### **Fase 3: Customer Experience**

## **SPRINT 5: Sistema de Fidelización**

**Objetivo del Sprint:** Desarrollar el sistema de puntos de fidelización, incluyendo la acumulación automática y el canje de recompensas configurables.

*   **2.1. Tarea: Implementar la lógica de otorgamiento automático de puntos.**
    *   **Prompt para el Agente:** "Diseña una tabla `loyalty_points` (o un campo en `user_profiles`) para almacenar los puntos de fidelización de los clientes. Crea un mecanismo (ej., un `trigger` de base de datos o una función en la capa de servicios que se llama al `COMPLETED` de una `appointment`) que automáticamente otorgue puntos a un `customer` después de que una `appointment` se marque como `completed`."
    *   **Entregable:** Lógica de asignación automática de puntos.
    *   **Testing:** Probar la finalización de citas y verificar que los puntos se acumulan correctamente en el perfil del cliente.
*   **2.2. Tarea: Crear endpoints para la configuración de recompensas.**
    *   **Prompt para el Agente:** "Diseña una tabla `loyalty_rewards` para que el `owner` pueda definir recompensas (ej., '500 puntos = 10% de descuento', '1000 puntos = Servicio X gratis'). Crea los endpoints CRUD para `loyalty_rewards`, accesibles solo por `owners`."
    *   **Entregable:** Tabla `loyalty_rewards` y endpoints CRUD para `owners`.
    *   **Testing:** Probar la creación, lectura, actualización y borrado de recompensas por un `owner`.
*   **2.3. Tarea: Desarrollar la lógica de canje de puntos por recompensas.**
    *   **Prompt para el Agente:** "Implementa un endpoint donde un `customer` pueda canjear sus puntos por una `loyalty_reward` disponible. La lógica debe:
        1.  Verificar que el cliente tiene suficientes puntos.
        2.  Deducir los puntos del saldo del cliente.
        3.  Registrar el canje (ej., en una tabla `customer_rewards`).
        4.  Generar un código de descuento o aplicar la recompensa a la siguiente reserva."
    *   **Entregable:** Endpoint y lógica de canje de puntos.
    *   **Testing:** Probar el canje de puntos con clientes con saldo suficiente e insuficiente, verificando la deducción de puntos y el registro del canje.

## **SPRINT 6: Flujo de Onboarding Avanzado y Transaccional**

**Objetivo del Sprint:** Completar el flujo de onboarding para nuevos negocios, asegurando la atomicidad de la creación de múltiples entidades.

*   **3.1. Tarea: Crear los endpoints para el registro inicial del negocio (`owner`, horarios, servicios, empleados).**
    *   **Prompt para el Agente:** "Diseña un endpoint `POST /onboarding` (o similar) que permita a un `owner` recién registrado (o que aún no ha configurado su negocio) proporcionar en una sola solicitud:
        1.  Datos de su `business`.
        2.  Sus horarios de operación (ej., en una tabla `business_hours`).
        3.  Una lista inicial de `services`.
        4.  Una lista de `employees` (cuyos perfiles ya existen o se crean en ese momento).
        Este endpoint debe ser accesible solo por `owners` cuyo `business_id` en `user_profiles` aún es `NULL` o su `business` asociado está incompleto."
    *   **Entregable:** Endpoint `/onboarding` y esquemas Pydantic para los datos combinados.
    *   **Testing:** Probar el endpoint con datos completos e incompletos.
*   **3.2. Tarea: Implementar una transacción de base de datos para el onboarding atómico.**
    *   **Prompt para el Agente:** "Modifica el endpoint de onboarding (`POST /onboarding`) para que todas las operaciones de creación (negocio, horarios, servicios, empleados) se realicen dentro de una **transacción de base de datos única**. Si alguna operación dentro de la transacción falla, la transacción debe ser revertida (`ROLLBACK`), asegurando que ninguna parte del onboarding se persista si no se completa todo el proceso."
    *   **Requisito Clave:** Utilizar las capacidades transaccionales de PostgreSQL/Supabase (ej., `BEGIN; ... COMMIT;` o un gestor de contexto de transacciones en Python si se usa un ORM como SQLAlchemy).
    *   **Entregable:** Endpoint de onboarding con lógica transaccional.
    *   **Testing:** Simular el flujo de onboarding completo en una sola prueba de integración. Introducir fallos intencionales en una de las etapas (ej., datos inválidos para un servicio o empleado) y verificar que ninguna de las otras entidades se haya creado en la base de datos (rollback exitoso).

---

## **SPRINT 7: Gestión de Promociones**

**Objetivo del Sprint:** Desarrollar un sistema completo para la creación, gestión y visualización de promociones.

*   **1.1. Tarea: Crear los endpoints CRUD para las promociones (`promotions`).**
    *   **Prompt para el Agente:** "Crea la tabla `promotions` (si no se hizo antes, con campos como `name`, `description`, `discount_type`, `discount_value`, `valid_from`, `valid_until`, `business_id`, etc.). Implementa los endpoints CRUD completos para `promotions`, accesibles solo por `owners` y `employees` de un `business_id` específico. Asegura la validación Pydantic y el filtrado por `business_id`."
    *   **Entregable:** Tabla `promotions` y endpoints CRUD protegidos.
    *   **Testing:** Pruebas CRUD básicas por un owner. Verificar la asociación con `business_id`.
*   **1.2. Tarea: Implementar la lógica para mostrar promociones válidas a los clientes.**
    *   **Prompt para el Agente:** "Crea un endpoint de lectura de promociones (`GET /promotions`) que sea accesible para `customers` (posiblemente sin autenticación si son promociones públicas o filtrado por `business_id` si un cliente está asociado). Este endpoint debe incluir lógica en la capa de servicios para filtrar las promociones y **solo devolver aquellas donde `valid_from` es menor o igual a la fecha actual y `valid_until` es mayor o igual a la fecha actual**. Además, las promociones deben ser filtradas por el `business_id` al que pertenecen."
    *   **Entregable:** Endpoint de lectura de promociones con lógica de validación de fechas.
    *   **Testing:** Probar el endpoint `GET /promotions` con promociones con fechas válidas, expiradas y futuras. Verificar que solo se muestran las válidas.

---

### **Fase 3: Customer Experience (Continuación)**

## **SPRINT 8: Notificaciones y Manejo de Timezones**

**Objetivo del Sprint:** Implementar un sistema de notificaciones por correo electrónico para confirmaciones y recordatorios, y asegurar un manejo consistente de las zonas horarias en toda la aplicación.

**2\. Notificaciones**

*   **2.1. Tarea: Integrar un servicio de envío de correos electrónicos.**
    *   **Prompt para el Agente:** "Integra un cliente para un servicio de envío de correos electrónicos transaccionales (ej., Postmark, SendGrid, o el servicio de correo de Supabase si aplica) en la capa de utilidades (`src/utils/`). Configura las credenciales de la API de forma segura (variables de entorno). Implementa una función genérica `send_email(to_email, subject, body_html)`."
    *   **Entregable:** Cliente de correo electrónico configurado y función genérica de envío.
    *   **Testing:** Enviar un correo electrónico de prueba básico para verificar la integración.
*   **2.2. Tarea: Crear una tarea asíncrona para notificaciones de reserva y recordatorios.**
    *   **Prompt para el Agente:** "Implementa una tarea asíncrona (ej., utilizando Celery, RQ o un `background task` de FastAPI para el MVP) que:
        1.  Envía una confirmación por correo electrónico al `customer` y `employee` cuando se crea una `appointment`.
        2.  Implementa un `scheduler` (ej., `APScheduler` o un `cron job` si se usa Celery) para enviar recordatorios por correo electrónico 24 horas antes de cada `appointment`."
    *   **Entregable:** Tarea asíncrona para notificaciones y sistema de recordatorios configurado.
    *   **Testing:**
        *   **Integración:** Crear una cita y verificar que los correos de confirmación se envían correctamente.
        *   **Funcional:** Probar el scheduler (si es un componente de prueba) o simular la ejecución del cron job para verificar el envío de recordatorios.

**3\. Manejo de Timezones**

*   **3.1. Tarea: Implementar la lógica para el manejo de zonas horarias.**
    *   **Prompt para el Agente:** "Asegura que todas las operaciones de fecha y hora en el backend sigan la siguiente política:
        1.  **Almacenamiento:** Todas las fechas y horas se guardan en la base de datos en **UTC**.
        2.  **Input/Output (API):** Los endpoints de la API deben aceptar y devolver fechas y horas en formato ISO 8601 con información de zona horaria (o asumir UTC si no se especifica y luego convertir).
        3.  **Presentación:** Al mostrar fechas y horas al `owner`/`employee`/`customer`, se deben adaptar a la `timezone` configurada para el `business` (ej., en una columna `timezone` en la tabla `businesses`).
        Utiliza una librería como `pytz` o `zoneinfo` para las conversiones. Implementa utilidades (`src/utils/time.py`) para convertir entre UTC y la zona horaria del negocio."
    *   **Entregable:** Funciones de utilidad para el manejo de zonas horarias y su aplicación consistente en los modelos Pydantic y lógica de base de datos.
    *   **Testing:** Escribir pruebas unitarias para las funciones de conversión de zona horaria. Pruebas de integración para endpoints que manejan fechas/horas, enviando y recibiendo datos con diferentes zonas horarias, y verificando que se almacenan/muestran correctamente.

---

### **Fase 4: MVP Launch**

## **SPRINT 9: Pipeline de CI/CD y Deployment**

**Objetivo del Sprint:** Configurar la automatización para el testing, build y despliegue del backend en un entorno de producción.

*   **1.1. Tarea: Configurar un pipeline de CI/CD.**
    *   **Prompt para el Agente:** "Configura un pipeline de Continuous Integration/Continuous Deployment (CI/CD) en GitHub Actions (o similar) para el repositorio. El pipeline debe:
        1.  Ejecutar todos los tests (unitarios y de integración) en cada `push` a las ramas `main` y `develop` (o `feature branches`).
        2.  Construir la imagen Docker del backend.
        3.  **Despliegue Continuo (CD):** Desplegar la nueva imagen Docker en un entorno de staging (ej., Railway o Render) después de tests exitosos en la rama `develop`/`main`."
    *   **Entregable:** Archivo de configuración de CI/CD (ej., `.github/workflows/main.yml`) y un despliegue exitoso en el entorno de staging.
    *   **Testing:** Realizar un push al repositorio para verificar que el pipeline se ejecuta sin errores, que los tests pasan y que la aplicación se despliega correctamente en el entorno de staging.

## **SPRINT 10: Monitoreo y Logging**

**Objetivo del Sprint:** Implementar un sistema de logging estructurado y herramientas de monitoreo de rendimiento y errores.

*   **2.1. Tarea: Configurar `structlog` para logging estructurado.**
    *   **Prompt para el Agente:** "Integra `structlog` en la aplicación FastAPI. Configura `structlog` para generar logs estructurados (JSON) que incluyan información clave como `level`, `timestamp`, `event`, `logger`, `user_id`, `business_id` (si aplica), `request_id`, y cualquier metadata relevante para el contexto de la solicitud. Asegura que los logs sean legibles en desarrollo y fácilmente parseables por herramientas de agregación en producción."
    *   **Entregable:** Configuración de `structlog` y ejemplos de logs estructurados en diferentes puntos de la aplicación (ej., inicio de solicitud, error, éxito de operación).
    *   **Testing:** Realizar solicitudes a la API y verificar que los logs se generan en formato JSON con la estructura esperada y los campos de contexto correctos.
*   **2.2. Tarea: Integrar herramientas de monitoreo y APM.**
    *   **Prompt para el Agente:** "Integra una herramienta de monitoreo y APM (Application Performance Management) como Sentry o Datadog para el seguimiento de errores y rendimiento.
        1.  **Seguimiento de Errores:** Configura la integración para capturar automáticamente excepciones no manejadas y errores del backend, enviándolos a la plataforma de monitoreo.
        2.  **Monitoreo de Rendimiento:** Configura la herramienta para instrumentar automáticamente los endpoints de FastAPI y medir métricas clave como latencia, throughput y uso de recursos."
    *   **Entregable:** Cliente de APM/monitoreo configurado y conectado a la plataforma elegida.
    *   **Testing:**
        *   Introducir intencionalmente una excepción no manejada en un endpoint y verificar que Sentry/Datadog captura el error.
        *   Realizar varias solicitudes a diferentes endpoints y verificar que los datos de rendimiento se muestran en el dashboard de la herramienta de monitoreo.

---

Este desglose proporciona un mapa de ruta muy claro y detallado para el desarrollo del MVP, con cada sprint y tarea bien definidos. Si tienes alguna duda sobre un punto específico o quieres profundizar aún más en alguna parte, házmelo saber.