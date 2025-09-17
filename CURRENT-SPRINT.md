## **SPRINT 2: Autenticación Backend-Centric (Registro y Setup Inicial)**

**Objetivo del Sprint:** Implementar los endpoints de registro de usuarios (Owner, Employee, Customer) que interactúan con Supabase Auth y la tabla `user_profiles` del backend, asegurando la atomicidad y las restricciones de seguridad adecuadas.

**3\. Autenticación y Sistema de Roles**

*   [x] **3.1. Tarea: Integrar el cliente Supabase en FastAPI y configurar la validación JWT.**
    *   **Nota:** La validación de JWT ya estaba implementada en `src/core/auth.py`. Se ha creado el modelo Pydantic `User` en `src/models/user.py` para completar la tarea.
*   [x] **3.2. Tarea: Crear los endpoints de registro de usuarios (`/auth/register/{role}`).**
    *   **Nota:** Implementados los tres endpoints POST en el router de autenticación (`src/api/routes/auth.py`):
        * `POST /auth/register/owner` - Registro público de propietarios con generación de business y access_code
        * `POST /auth/register/employee` - Registro de empleados (requiere autenticación como owner)
        * `POST /auth/register/customer` - Auto-registro público de clientes
    *   **Características implementadas:**
        * Manejo de transacciones/atomicidad con rollback automático
        * Validación de roles usando `RoleChecker` dependency
        * Generación de tokens JWT de sesión para todos los endpoints
        * Manejo robusto de errores con cleanup de usuarios fantasma
    *   **Prompt para el Agente:** "Implementa los siguientes endpoints POST en el router de autenticación (`src/api/auth.py`):

        *   **`POST /auth/register/owner`**
            *   **Descripción:** Permite el registro de propietarios desde el dashboard web. Cada owner crea su propio negocio.
            *   **Lógica:** ✅ Implementada
                1.  Recibe email y password (Pydantic `OwnerRegisterSchema`).
                2.  Crea usuario en Supabase Auth usando `admin.create_user()`.
                3.  Crea un nuevo `business` con `access_code` único generado.
                4.  Inserta perfil en `user_profiles` con `role='owner'` y `business_id`.
                5.  Manejo de atomicidad con rollback automático si falla.
                6.  Devuelve tokens de sesión obtenidos via `sign_in_with_password`.
            *   **Salida:** HTTP 201 Created con usuario, access_token y refresh_token.
        *   **`POST /auth/register/employee`**
            *   **Descripción:** Permite a un propietario registrar un nuevo empleado.
            *   **Autorización:** ✅ Protegido con `require_owner` dependency.
            *   **Lógica:** ✅ Implementada
                1.  Recibe email, password, first_name, last_name (`EmployeeRegisterSchema`).
                2.  Obtiene `business_id` del owner autenticado desde `user_profiles`.
                3.  Crea usuario en Supabase Auth usando `admin.create_user()`.
                4.  Inserta perfil en `user_profiles` con `role='employee'` y `business_id` del owner.
                5.  Manejo de atomicidad con rollback automático si falla.
                6.  Devuelve tokens de sesión del nuevo empleado.
            *   **Salida:** HTTP 201 Created con empleado, access_token y refresh_token.
        *   **`POST /auth/register/customer`**
            *   **Descripción:** Permite el auto-registro público de clientes.
            *   **Lógica:** ✅ Implementada
                1.  Recibe email, password, first_name, last_name (`CustomerRegisterSchema`).
                2.  Usa `auth.sign_up()` para auto-registro con confirmación de email.
                3.  Inserta perfil en `user_profiles` con `role='customer'` y `business_id=null`.
                4.  Manejo de atomicidad con rollback automático si falla.
                5.  Devuelve tokens de sesión o estado "pending_confirmation" según Supabase.
            *   **Salida:** HTTP 201 Created con cliente, access_token y refresh_token.

    *   **Entregable:** ✅ **COMPLETADO** - Implementación de los tres endpoints de registro en FastAPI con validaciones y atomicidad.
    *   **Testing:** ✅ **SCRIPT CREADO**
        *   **Script Automático:** `./test_auth_endpoints.sh` - Testing completo de todos los endpoints
        *   **Tests Implementados:**
            *   ✅ `POST /auth/register/owner` - Registro público de owners
            *   ✅ `POST /auth/register/owner` - Múltiples owners (cada uno con su business)
            *   ✅ `POST /auth/register/employee` - Con owner autenticado (exitoso)
            *   ✅ `POST /auth/register/employee` - Sin autenticación (403 Forbidden)
            *   ✅ `POST /auth/register/customer` - Auto-registro público
            *   ✅ Emails duplicados - Manejo correcto de errores (409 Conflict)
            *   ✅ Validación de tokens JWT generados
        *   **Documentación:** `src/tests/create-user.md` actualizada con ejemplos

---