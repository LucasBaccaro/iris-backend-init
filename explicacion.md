 Supabase Auth maneja:
  - ✅ Registro/Login de usuarios
  - ✅ Tokens JWT
  - ✅ Verificación básica de tokens

  Pero NO maneja:
  - ❌ Multi-tenancy (un user en múltiples salones)
  - ❌ Roles por business (puedo ser owner de Salón A y employee de Salón B)
  - ❌ Validación de acceso a recursos (¿puede este user editar este appointment?)

  🏗️ El Sistema Híbrido:

  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
  │   SUPABASE      │    │   NUESTRO       │    │   RESULTADO     │
  │                 │    │   MIDDLEWARE    │    │                 │
  │ • Login/Signup  │ +  │ • Roles         │ =  │ • Auth completo │
  │ • JWT tokens    │    │ • Multi-tenant  │    │ • Autorización  │
  │ • User básico   │    │ • Permissions   │    │ • Seguridad     │
  └─────────────────┘    └─────────────────┘    └─────────────────┘

  📋 Ejemplo Real:

  Usuario: lucas@email.com
  - Salón A: Owner (puede todo)
  - Salón B: Employee (solo ver/editar appointments)
  - Salón C: Customer (solo agendar citas)

  Supabase solo sabe: "lucas@email.com existe y tiene token válido"

  Nuestro sistema sabe: "lucas puede editar services de Salón A, pero NO de Salón B"