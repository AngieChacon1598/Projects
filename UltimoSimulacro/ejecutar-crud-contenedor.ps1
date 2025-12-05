# Script PowerShell para ejecutar operaciones CRUD dentro del contenedor
# Uso: 
#   1. Obtener el nombre del pod: kubectl get pods -n angie-chacon
#   2. Ejecutar: .\ejecutar-crud-contenedor.ps1 POD_NAME

param(
    [Parameter(Mandatory=$true)]
    [string]$PodName
)

$namespace = "angie-chacon"
$serviceUrl = "http://angie-chacon-service:8080"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "OPERACIONES CRUD DENTRO DEL CONTENEDOR" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Pod: $PodName" -ForegroundColor Yellow
Write-Host "Namespace: $namespace" -ForegroundColor Yellow
Write-Host ""

# Función para ejecutar comandos dentro del contenedor
function Invoke-ContainerCommand {
    param([string]$Command)
    kubectl exec -it $PodName -n $namespace -- sh -c $Command
}

Write-Host "1. CREATE - Crear producto..." -ForegroundColor Green
Write-Host "----------------------------------------"
$createCmd = "curl -X POST ${serviceUrl}/api/productos -H 'Content-Type: application/json' -d '{\"nombre\":\"Laptop Dell\",\"descripcion\":\"Laptop Dell Inspiron 15\",\"precio\":899.99,\"stock\":10}'"
Invoke-ContainerCommand $createCmd
Write-Host ""

Write-Host "2. CREATE - Crear segundo producto..." -ForegroundColor Green
Write-Host "----------------------------------------"
$createCmd2 = "curl -X POST ${serviceUrl}/api/productos -H 'Content-Type: application/json' -d '{\"nombre\":\"Mouse Logitech\",\"descripcion\":\"Mouse inalámbrico Logitech MX Master\",\"precio\":79.99,\"stock\":25}'"
Invoke-ContainerCommand $createCmd2
Write-Host ""

Write-Host "3. READ - Listar todos los productos..." -ForegroundColor Green
Write-Host "----------------------------------------"
Invoke-ContainerCommand "curl ${serviceUrl}/api/productos"
Write-Host ""

Write-Host "4. READ - Obtener producto por ID (ID=1)..." -ForegroundColor Green
Write-Host "----------------------------------------"
Invoke-ContainerCommand "curl ${serviceUrl}/api/productos/1"
Write-Host ""

Write-Host "5. UPDATE - Actualizar producto con ID=1..." -ForegroundColor Green
Write-Host "----------------------------------------"
$updateCmd = "curl -X PUT ${serviceUrl}/api/productos/1 -H 'Content-Type: application/json' -d '{\"nombre\":\"Laptop Dell Actualizada\",\"descripcion\":\"Laptop Dell Inspiron 15 - Modelo 2024\",\"precio\":799.99,\"stock\":8}'"
Invoke-ContainerCommand $updateCmd
Write-Host ""

Write-Host "6. READ - Verificar actualización..." -ForegroundColor Green
Write-Host "----------------------------------------"
Invoke-ContainerCommand "curl ${serviceUrl}/api/productos/1"
Write-Host ""

Write-Host "7. DELETE - Eliminar producto con ID=2..." -ForegroundColor Green
Write-Host "----------------------------------------"
Invoke-ContainerCommand "curl -X DELETE ${serviceUrl}/api/productos/2"
Write-Host ""

Write-Host "8. READ - Listar productos después de eliminar..." -ForegroundColor Green
Write-Host "----------------------------------------"
Invoke-ContainerCommand "curl ${serviceUrl}/api/productos"
Write-Host ""

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "OPERACIONES CRUD COMPLETADAS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ver los logs, ejecuta en otra terminal:" -ForegroundColor Yellow
Write-Host "kubectl logs -f $PodName -n $namespace" -ForegroundColor White



