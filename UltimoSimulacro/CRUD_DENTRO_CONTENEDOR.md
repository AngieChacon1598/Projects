# Guía: Operaciones CRUD Dentro del Contenedor con kubectl

Esta guía te muestra cómo realizar operaciones CRUD accediendo al contenedor usando `kubectl exec` y cómo ver los logs de las operaciones.

## 📋 Requisitos Previos

1. Kubernetes cluster funcionando
2. Aplicación desplegada en el cluster
3. `kubectl` configurado y conectado al cluster

## 🔍 Paso 1: Verificar los Pods

Primero, identifica el nombre de tu pod:

```bash
kubectl get pods -n angie-chacon
```

Deberías ver algo como:
```
NAME                                      READY   STATUS    RESTARTS   AGE
angie-chacon-deployment-xxxxxxxxxx-xxxxx  1/1     Running   0          5m
angie-chacon-deployment-xxxxxxxxxx-yyyyy  1/1     Running   0          5m
```

## 🚀 Paso 2: Acceder al Contenedor

Accede a uno de los pods usando `kubectl exec`:

```bash
# Reemplaza POD_NAME con el nombre real de tu pod
kubectl exec -it POD_NAME -n angie-chacon -- /bin/sh
```

O si el contenedor usa bash:

```bash
kubectl exec -it POD_NAME -n angie-chacon -- /bin/bash
```

**Nota:** Si el contenedor no tiene `/bin/sh` o `/bin/bash`, puedes usar:

```bash
kubectl exec -it POD_NAME -n angie-chacon -- sh
```

## 📝 Paso 3: Verificar que curl está disponible

Dentro del contenedor, verifica si `curl` o `wget` están disponibles:

```bash
which curl
# o
which wget
```

Si no están disponibles, puedes instalarlos (en Alpine):

```bash
apk add --no-cache curl
```

O usar `wget` que suele estar disponible en imágenes Alpine.

## 🎯 Paso 4: Realizar Operaciones CRUD

### Obtener el nombre del servicio interno

Dentro del contenedor, el servicio estará disponible en:
- `angie-chacon-service.angie-chacon.svc.cluster.local:8080`
- O simplemente: `angie-chacon-service:8080`

### 1. CREATE (POST) - Crear un Producto

```bash
curl -X POST http://angie-chacon-service:8080/api/productos \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell",
    "descripcion": "Laptop Dell Inspiron 15",
    "precio": 899.99,
    "stock": 10
  }'
```

**O usando wget:**

```bash
wget --method=POST \
  --header="Content-Type: application/json" \
  --body-data='{"nombre":"Laptop Dell","descripcion":"Laptop Dell Inspiron 15","precio":899.99,"stock":10}' \
  -O- http://angie-chacon-service:8080/api/productos
```

### 2. READ (GET) - Listar Todos los Productos

```bash
curl http://angie-chacon-service:8080/api/productos
```

**O usando wget:**

```bash
wget -O- http://angie-chacon-service:8080/api/productos
```

### 3. READ (GET) - Obtener Producto por ID

```bash
curl http://angie-chacon-service:8080/api/productos/1
```

### 4. UPDATE (PUT) - Actualizar un Producto

```bash
curl -X PUT http://angie-chacon-service:8080/api/productos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Laptop Dell Actualizada",
    "descripcion": "Laptop Dell Inspiron 15 - Modelo 2024",
    "precio": 799.99,
    "stock": 8
  }'
```

### 5. DELETE - Eliminar un Producto

```bash
curl -X DELETE http://angie-chacon-service:8080/api/productos/1
```

## 📊 Paso 5: Ver los Logs de las Operaciones

En **otra terminal** (fuera del contenedor), ejecuta:

```bash
# Ver logs en tiempo real
kubectl logs -f POD_NAME -n angie-chacon

# O ver logs de todos los pods del deployment
kubectl logs -f deployment/angie-chacon-deployment -n angie-chacon

# Ver logs de un pod específico con timestamps
kubectl logs POD_NAME -n angie-chacon --timestamps
```

**Ejemplo de lo que verás en los logs:**

```
2024-10-23 10:15:30 - === OPERACIÓN CRUD: POST - Crear nuevo producto ===
2024-10-23 10:15:30 - Datos del producto a crear - Nombre: Laptop Dell, Descripción: Laptop Dell Inspiron 15, Precio: 899.99, Stock: 10
2024-10-23 10:15:30 - Producto creado exitosamente - ID: 1, Nombre: Laptop Dell
2024-10-23 10:16:45 - === OPERACIÓN CRUD: GET - Listar todos los productos ===
2024-10-23 10:16:45 - Productos encontrados: 1
2024-10-23 10:17:20 - === OPERACIÓN CRUD: PUT - Actualizar producto con ID: 1 ===
2024-10-23 10:17:20 - Producto actualizado exitosamente - ID: 1, Nombre: Laptop Dell Actualizada
2024-10-23 10:18:10 - === OPERACIÓN CRUD: DELETE - Eliminar producto con ID: 1 ===
2024-10-23 10:18:10 - Eliminando producto - ID: 1, Nombre: Laptop Dell Actualizada
2024-10-23 10:18:10 - Producto eliminado exitosamente - ID: 1
```

## 🎬 Script Completo de Ejemplo

Puedes ejecutar todas las operaciones en secuencia:

```bash
# 1. Acceder al contenedor
kubectl exec -it POD_NAME -n angie-chacon -- sh

# 2. Dentro del contenedor, ejecutar:
# CREATE
curl -X POST http://angie-chacon-service:8080/api/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Producto 1","descripcion":"Descripción 1","precio":100.0,"stock":5}'

# READ - Listar
curl http://angie-chacon-service:8080/api/productos

# READ - Por ID
curl http://angie-chacon-service:8080/api/productos/1

# UPDATE
curl -X PUT http://angie-chacon-service:8080/api/productos/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Producto 1 Actualizado","descripcion":"Nueva descripción","precio":120.0,"stock":3}'

# DELETE
curl -X DELETE http://angie-chacon-service:8080/api/productos/1

# 3. Salir del contenedor
exit
```

## 🔍 Verificar Logs en Tiempo Real

En una terminal separada, mientras ejecutas las operaciones:

```bash
# Terminal 1: Acceder al contenedor y hacer operaciones
kubectl exec -it POD_NAME -n angie-chacon -- sh

# Terminal 2: Ver logs en tiempo real
kubectl logs -f POD_NAME -n angie-chacon
```

## 📋 Checklist para la Evaluación

- [ ] ✅ Acceder al contenedor usando `kubectl exec`
- [ ] ✅ Realizar operación CREATE (POST) dentro del contenedor
- [ ] ✅ Realizar operación READ (GET) dentro del contenedor
- [ ] ✅ Realizar operación UPDATE (PUT) dentro del contenedor
- [ ] ✅ Realizar operación DELETE dentro del contenedor
- [ ] ✅ Verificar que los logs muestran todas las operaciones
- [ ] ✅ Los logs muestran detalles de cada operación (tipo, datos, resultado)

## 💡 Tips Importantes

1. **Si curl no está disponible:** Usa `wget` o instálalo con `apk add curl`
2. **URL del servicio:** Usa `angie-chacon-service:8080` (nombre del servicio)
3. **Ver logs:** Usa `kubectl logs -f` para ver logs en tiempo real
4. **Múltiples pods:** Si tienes 2 pods, puedes acceder a cualquiera de ellos
5. **Formato JSON:** Asegúrate de usar comillas simples para el JSON en la línea de comandos

## 🐛 Solución de Problemas

### Error: "curl: command not found"
```bash
apk add --no-cache curl
```

### Error: "Connection refused"
- Verifica que el servicio está corriendo: `kubectl get svc -n angie-chacon`
- Verifica que los pods están listos: `kubectl get pods -n angie-chacon`

### No veo los logs
- Asegúrate de usar `-f` para seguir los logs: `kubectl logs -f POD_NAME -n angie-chacon`
- Verifica que el nivel de logging está en INFO en `application.yml`

