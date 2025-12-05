# Instrucciones para el Hackathon

## ✅ Checklist de Requisitos

### 1. ✅ Microservicio Base con H2 y Puerto Flexible
- Microservicio Spring Boot creado
- Base de datos H2 en memoria (no requiere secret)
- Puerto configurable mediante variable de entorno `PORT` (default: 8080)

### 2. ✅ Dockerización en 2 Procesos
- Dockerfile multi-stage (build y runtime)
- No depende de la carpeta `target` existente
- `.dockerignore` configurado para excluir `target/`

### 3. ✅ Imagen Docker Optimizada (100-300MB)
- Dockerfile multi-stage usando Alpine Linux
- Imagen base: `eclipse-temurin:17-jre-alpine` (ligera)
- Resultado esperado: ~150-200MB

### 4. ✅ Nombre de Imagen Correcto
- Nombre: `02-angie-chacon:1.0`

### 5. ⚠️ Subir a Docker Hub (Pendiente)
```bash
# 1. Construir la imagen
docker build -t 02-angie-chacon:1.0 .

# 2. Verificar tamaño
docker images | grep 02-angie-chacon

# 3. Login a Docker Hub
docker login

# 4. Tag con tu usuario de Docker Hub
docker tag 02-angie-chacon:1.0 TU_USUARIO/02-angie-chacon:1.0

# 5. Push a Docker Hub
docker push TU_USUARIO/02-angie-chacon:1.0

# 6. Actualizar deployment.yml con:
#    image: TU_USUARIO/02-angie-chacon:1.0
```

### 6. ✅ Manifiestos de Kubernetes
- ✅ `02-angie-chacon-namespace.yml`
- ⚠️ `02-angie-chacon-secret.yml` - **NO REQUERIDO** (H2 no necesita secret)
- ✅ `02-angie-chacon-service.yml`
- ✅ `02-angie-chacon-deployment.yml` (2 pods configurados)

## Pasos para Desplegar

### 1. Construir la Imagen Docker
```bash
docker build -t 02-angie-chacon:1.0 .
```

### 2. Verificar Tamaño de la Imagen
```bash
docker images | grep 02-angie-chacon
```
**Debe estar entre 100MB - 300MB**

### 3. Probar Localmente
```bash
docker run -p 8080:8080 -e PORT=8080 02-angie-chacon:1.0
```

### 4. Subir a Docker Hub (Opcional pero Requerido)
```bash
docker login
docker tag 02-angie-chacon:1.0 TU_USUARIO/02-angie-chacon:1.0
docker push TU_USUARIO/02-angie-chacon:1.0
```

### 5. Desplegar en Kubernetes
```bash
# Aplicar todos los manifiestos
kubectl apply -f 02-angie-chacon-namespace.yml
kubectl apply -f 02-angie-chacon-service.yml
kubectl apply -f 02-angie-chacon-deployment.yml

# Verificar despliegue
kubectl get all -n angie-chacon

# Verificar que hay 2 pods corriendo
kubectl get pods -n angie-chacon
```

### 6. Crear Port-Forward
```bash
kubectl port-forward -n angie-chacon service/angie-chacon-service 8080:8080
```

### 7. Probar la Aplicación
Con el port-forward activo, abre tu navegador en:
- http://localhost:8080/api/health
- http://localhost:8080/api/info
- http://localhost:8080/api/productos

## Archivos de Entrega

Los siguientes archivos deben ser entregados:

1. ✅ `02-angie-chacon-namespace.yml`
2. ✅ `02-angie-chacon-service.yml`
3. ✅ `02-angie-chacon-deployment.yml`
4. ⚠️ `02-angie-chacon-secret.yml` - **NO REQUERIDO** (H2 no necesita secret)

## Notas Importantes

- El microservicio usa H2 en memoria, por lo que **NO requiere secret**
- El puerto es flexible mediante la variable de entorno `PORT`
- El deployment está configurado para 2 pods
- La imagen Docker está optimizada para estar entre 100-300MB
- Si subes a Docker Hub, actualiza el `image` en el deployment

## Solución de Problemas

### La imagen es muy grande (>300MB)
- Verifica que estás usando la imagen Alpine
- Asegúrate de que el multi-stage build está funcionando correctamente

### Los pods no inician
- Verifica los logs: `kubectl logs -n angie-chacon <pod-name>`
- Verifica que la imagen existe: `kubectl describe pod -n angie-chacon <pod-name>`

### Port-forward no funciona
- Verifica que el servicio está corriendo: `kubectl get svc -n angie-chacon`
- Verifica que los pods están listos: `kubectl get pods -n angie-chacon`

