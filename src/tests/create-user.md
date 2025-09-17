# Testing Scripts para Endpoints de Autenticación

## Script Automático de Testing
Ejecutar desde el directorio raíz:
```bash
./test_auth_endpoints.sh
```

## Tests Manuales Individual

### 1. Registrar Owner
```bash
curl -X POST "http://localhost:8000/auth/register/owner" \
-H "Content-Type: application/json" \
-d '{
     "email": "owner1@example.com",
     "password": "password123"
}'
```

### 2. Registrar Employee (requiere token de owner)
```bash
curl -X POST "http://localhost:8000/auth/register/employee" \
-H "Content-Type: application/json" \
-H "Authorization: Bearer YOUR_OWNER_TOKEN" \
-d '{
     "email": "employee1@example.com",
     "password": "password123",
     "first_name": "María",
     "last_name": "García"
}'
```

### 3. Registrar Customer
```bash
curl -X POST "http://localhost:8000/auth/register/customer" \
-H "Content-Type: application/json" \
-d '{
     "email": "customer1@example.com",
     "password": "password123",
     "first_name": "Juan",
     "last_name": "López"
}'
```