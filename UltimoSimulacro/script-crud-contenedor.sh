#!/bin/sh

# Script para realizar operaciones CRUD dentro del contenedor
# Uso: kubectl exec -it POD_NAME -n angie-chacon -- sh < script-crud-contenedor.sh
# O: kubectl exec -it POD_NAME -n angie-chacon -- sh -c "$(cat script-crud-contenedor.sh)"

SERVICE_URL="http://angie-chacon-service:8080"

echo "=========================================="
echo "OPERACIONES CRUD DENTRO DEL CONTENEDOR"
echo "=========================================="
echo ""

# Verificar si curl está disponible
if ! command -v curl >/dev/null 2>&1; then
    echo "curl no está disponible, intentando instalar..."
    apk add --no-cache curl >/dev/null 2>&1 || echo "No se pudo instalar curl"
fi

echo "1. CREATE - Crear producto..."
echo "----------------------------------------"
curl -X POST ${SERVICE_URL}/api/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell",
    "descripcion": "Laptop Dell Inspiron 15",
    "precio": 899.99,
    "stock": 10
  }'
echo ""
echo ""

echo "2. CREATE - Crear segundo producto..."
echo "----------------------------------------"
curl -X POST ${SERVICE_URL}/api/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Mouse Logitech",
    "descripcion": "Mouse inalámbrico Logitech MX Master",
    "precio": 79.99,
    "stock": 25
  }'
echo ""
echo ""

echo "3. READ - Listar todos los productos..."
echo "----------------------------------------"
curl ${SERVICE_URL}/api/productos
echo ""
echo ""

echo "4. READ - Obtener producto por ID (ID=1)..."
echo "----------------------------------------"
curl ${SERVICE_URL}/api/productos/1
echo ""
echo ""

echo "5. UPDATE - Actualizar producto con ID=1..."
echo "----------------------------------------"
curl -X PUT ${SERVICE_URL}/api/productos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell Actualizada",
    "descripcion": "Laptop Dell Inspiron 15 - Modelo 2024",
    "precio": 799.99,
    "stock": 8
  }'
echo ""
echo ""

echo "6. READ - Verificar actualización..."
echo "----------------------------------------"
curl ${SERVICE_URL}/api/productos/1
echo ""
echo ""

echo "7. DELETE - Eliminar producto con ID=2..."
echo "----------------------------------------"
curl -X DELETE ${SERVICE_URL}/api/productos/2
echo ""
echo ""

echo "8. READ - Listar productos después de eliminar..."
echo "----------------------------------------"
curl ${SERVICE_URL}/api/productos
echo ""
echo ""

echo "=========================================="
echo "OPERACIONES CRUD COMPLETADAS"
echo "=========================================="
echo "Revisa los logs con: kubectl logs -f POD_NAME -n angie-chacon"



