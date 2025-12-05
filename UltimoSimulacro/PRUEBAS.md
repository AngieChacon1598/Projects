# Guía de Pruebas del Microservicio

## Endpoints Disponibles

### 1. Health Check
```bash
GET http://localhost:8081/api/health
```
**Respuesta esperada:**
```json
{
  "status": "UP",
  "application": "microservicio-base",
  "port": "8081"
}
```

### 2. Info
```bash
GET http://localhost:8081/api/info
```

### 3. Listar Productos (GET)
```bash
GET http://localhost:8081/api/productos
```
**Respuesta inicial:** `[]` (array vacío - esto es correcto)

### 4. Crear Producto (POST)
```bash
POST http://localhost:8081/api/productos
Content-Type: application/json

{
  "nombre": "Laptop",
  "descripcion": "Laptop Dell Inspiron",
  "precio": 899.99,
  "stock": 5
}
```

### 5. Obtener Producto por ID (GET)
```bash
GET http://localhost:8081/api/productos/1
```

### 6. Actualizar Producto (PUT)
```bash
PUT http://localhost:8081/api/productos/1
Content-Type: application/json

{
  "nombre": "Laptop Actualizada",
  "descripcion": "Laptop Dell Inspiron - Actualizada",
  "precio": 799.99,
  "stock": 3
}
```

### 7. Buscar Productos (GET)
```bash
GET http://localhost:8081/api/productos/buscar?nombre=laptop
```

### 8. Eliminar Producto (DELETE)
```bash
DELETE http://localhost:8081/api/productos/1
```

### 9. Spring Boot Actuator Health
```bash
GET http://localhost:8081/actuator/health
```

## Pruebas con cURL

### Crear un producto
```bash
curl -X POST http://localhost:8081/api/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Mouse",
    "descripcion": "Mouse inalámbrico",
    "precio": 29.99,
    "stock": 20
  }'
```

### Listar productos
```bash
curl http://localhost:8081/api/productos
```

### Health check
```bash
curl http://localhost:8081/api/health
```

## Pruebas con Postman o Insomnia

1. **Crear Producto:**
   - Método: POST
   - URL: `http://localhost:8081/api/productos`
   - Headers: `Content-Type: application/json`
   - Body (raw JSON):
   ```json
   {
     "nombre": "Teclado",
     "descripcion": "Teclado mecánico",
     "precio": 79.99,
     "stock": 15
   }
   ```

2. **Listar Productos:**
   - Método: GET
   - URL: `http://localhost:8081/api/productos`

## Notas

- ✅ El array vacío `[]` es la respuesta correcta cuando no hay productos
- ✅ La base de datos H2 es en memoria, se reinicia cada vez que reinicias la aplicación
- ✅ El puerto es flexible mediante la variable de entorno `PORT` (default: 8080)
- ✅ Todos los endpoints están funcionando correctamente

