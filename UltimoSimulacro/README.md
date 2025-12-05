# Microservicio Base - Hackathon

Microservicio Spring Boot con H2 Database para hackathon.

## Características

- ✅ Microservicio Spring Boot con H2 (no requiere secret)
- ✅ Puerto flexible mediante variable de entorno `PORT`
- ✅ Dockerización multi-stage optimizada (100-300MB)
- ✅ Manifiestos de Kubernetes listos para desplegar

## Estructura del Proyecto

```
.
├── src/
│   └── main/
│       ├── java/com/hackathon/
│       │   ├── MicroservicioBaseApplication.java
│       │   ├── controller/
│       │   ├── entity/
│       │   └── repository/
│       └── resources/
│           └── application.yml
├── Dockerfile
├── .dockerignore
├── pom.xml
└── 02-angie-chacon-*.yml (manifiestos Kubernetes)
```

## Endpoints Disponibles

- `GET /api/health` - Health check
- `GET /api/info` - Información de la aplicación
- `GET /api/productos` - Listar todos los productos
- `GET /api/productos/{id}` - Obtener producto por ID
- `POST /api/productos` - Crear producto
- `PUT /api/productos/{id}` - Actualizar producto
- `DELETE /api/productos/{id}` - Eliminar producto
- `GET /api/productos/buscar?nombre=...` - Buscar productos
- `GET /actuator/health` - Spring Boot Actuator health
- `GET /h2-console` - Consola H2 Database

## Construcción y Dockerización

### 1. Construir la imagen Docker

```bash
docker build -t 02-angie-chacon:1.0 .
```

### 2. Verificar el tamaño de la imagen

```bash
docker images | grep 02-angie-chacon
```

La imagen debe estar entre 100MB - 300MB.

### 3. Probar la imagen localmente

```bash
docker run -p 8080:8080 -e PORT=8080 02-angie-chacon:1.0
```

### 4. Subir a Docker Hub

```bash
# Login a Docker Hub
docker login

# Tag de la imagen (reemplaza USERNAME con tu usuario de Docker Hub)
docker tag 02-angie-chacon:1.0 USERNAME/02-angie-chacon:1.0

# Push a Docker Hub
docker push USERNAME/02-angie-chacon:1.0
```

**Nota:** Si subes a Docker Hub, actualiza el `image` en `02-angie-chacon-deployment.yml` con:
```yaml
image: USERNAME/02-angie-chacon:1.0
```

## Despliegue en Kubernetes

### 1. Aplicar los manifiestos

```bash
# Crear namespace
kubectl apply -f 02-angie-chacon-namespace.yml

# Crear service
kubectl apply -f 02-angie-chacon-service.yml

# Crear deployment
kubectl apply -f 02-angie-chacon-deployment.yml
```

### 2. Verificar el despliegue

```bash
# Ver pods
kubectl get pods -n angie-chacon

# Ver servicios
kubectl get svc -n angie-chacon

# Ver deployment
kubectl get deployment -n angie-chacon
```

### 3. Crear port-forward

```bash
kubectl port-forward -n angie-chacon service/angie-chacon-service 8080:8080
```

### 4. Probar la aplicación

Con el port-forward activo, puedes acceder a:
- http://localhost:8080/api/health
- http://localhost:8080/api/info
- http://localhost:8080/api/productos

## Desarrollo Local

### Requisitos

- Java 17
- Maven 3.6+

### Ejecutar localmente

```bash
mvn clean install
mvn spring-boot:run
```

O con puerto personalizado:

```bash
PORT=9090 mvn spring-boot:run
```

## Notas Importantes

- El microservicio usa H2 en memoria, por lo que **NO requiere secret** en Kubernetes
- El puerto es configurable mediante la variable de entorno `PORT` (default: 8080)
- La imagen Docker usa multi-stage build para optimizar el tamaño
- El deployment está configurado para 2 pods como se requiere

## Operaciones CRUD Dentro del Contenedor

Para realizar operaciones CRUD accediendo al contenedor usando `kubectl exec`:

### 1. Acceder al contenedor

```bash
# Obtener el nombre del pod
kubectl get pods -n angie-chacon

# Acceder al contenedor
kubectl exec -it POD_NAME -n angie-chacon -- sh
```

### 2. Realizar operaciones CRUD

Dentro del contenedor:

```bash
# CREATE
curl -X POST http://angie-chacon-service:8080/api/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Producto Test","descripcion":"Descripción","precio":99.99,"stock":10}'

# READ - Listar
curl http://angie-chacon-service:8080/api/productos

# READ - Por ID
curl http://angie-chacon-service:8080/api/productos/1

# UPDATE
curl -X PUT http://angie-chacon-service:8080/api/productos/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Producto Actualizado","descripcion":"Nueva descripción","precio":89.99,"stock":5}'

# DELETE
curl -X DELETE http://angie-chacon-service:8080/api/productos/1
```

### 3. Ver los logs de las operaciones

En otra terminal:

```bash
# Ver logs en tiempo real
kubectl logs -f POD_NAME -n angie-chacon

# O ver logs de todos los pods
kubectl logs -f deployment/angie-chacon-deployment -n angie-chacon
```

**Los logs mostrarán todas las operaciones CRUD realizadas con detalles completos.**

📖 Ver la guía completa en: `CRUD_DENTRO_CONTENEDOR.md`

## Archivos de Entrega

- ✅ `02-angie-chacon-namespace.yml`
- ✅ `02-angie-chacon-service.yml`
- ✅ `02-angie-chacon-deployment.yml`
- ⚠️ `02-angie-chacon-secret.yml` - **NO REQUERIDO** (H2 no necesita secret)

