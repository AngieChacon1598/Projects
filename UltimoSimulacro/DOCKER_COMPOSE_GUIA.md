# Guía: Orquestación con Docker Compose

Esta guía muestra cómo orquestar aplicaciones usando Docker Compose. **Estas instrucciones son solo de referencia** y no están aplicadas al proyecto actual.

## 📋 ¿Qué es Docker Compose?

Docker Compose es una herramienta para definir y ejecutar aplicaciones Docker multi-contenedor. Permite definir servicios, redes, volúmenes y configuraciones en un archivo YAML.

## 📁 Estructura de Archivos

```
proyecto/
├── docker-compose.yml          # Archivo principal de orquestación
├── docker-compose.override.yml # Configuraciones de desarrollo (opcional)
├── docker-compose.prod.yml     # Configuraciones de producción (opcional)
├── Dockerfile                  # Imagen de la aplicación
├── .env                        # Variables de entorno (opcional)
└── servicios/
    ├── app/
    │   └── Dockerfile
    ├── db/
    │   └── Dockerfile
    └── nginx/
        └── Dockerfile
```

## 📝 Estructura Básica de docker-compose.yml

```yaml
version: '3.8'  # Versión del formato Compose

services:
  # Definición de servicios (contenedores)
  
networks:
  # Definición de redes personalizadas
  
volumes:
  # Definición de volúmenes persistentes
```

## 🎯 Ejemplo 1: Aplicación Simple con Base de Datos

```yaml
version: '3.8'

services:
  # Servicio de la aplicación
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mi-aplicacion
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
      - DB_HOST=db
      - DB_PORT=5432
      - DB_NAME=mydb
      - DB_USER=user
      - DB_PASSWORD=password
    depends_on:
      - db
    networks:
      - app-network
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs

  # Servicio de base de datos
  db:
    image: postgres:15-alpine
    container_name: mi-base-datos
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    ports:
      - "5432:5432"
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
    driver: local
```

## 🎯 Ejemplo 2: Aplicación con Redis y Nginx

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: backend-app
    environment:
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    depends_on:
      - redis
      - db
    networks:
      - backend-network
    restart: unless-stopped

  db:
    image: postgres:15-alpine
    container_name: postgres-db
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=secret123
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - backend-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    container_name: redis-cache
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    networks:
      - backend-network
    restart: unless-stopped
    command: redis-server --appendonly yes

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - app
    networks:
      - backend-network
    restart: unless-stopped

networks:
  backend-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
```

## 🎯 Ejemplo 3: Microservicios con Múltiples Aplicaciones

```yaml
version: '3.8'

services:
  # Microservicio 1
  microservice-1:
    build:
      context: ./microservice-1
      dockerfile: Dockerfile
    container_name: ms1
    ports:
      - "8081:8080"
    environment:
      - SERVICE_NAME=microservice-1
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - microservices-network
    restart: unless-stopped

  # Microservicio 2
  microservice-2:
    build:
      context: ./microservice-2
      dockerfile: Dockerfile
    container_name: ms2
    ports:
      - "8082:8080"
    environment:
      - SERVICE_NAME=microservice-2
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - microservices-network
    restart: unless-stopped

  # API Gateway
  api-gateway:
    build:
      context: ./api-gateway
      dockerfile: Dockerfile
    container_name: api-gateway
    ports:
      - "8080:8080"
    environment:
      - MS1_URL=http://microservice-1:8080
      - MS2_URL=http://microservice-2:8080
    depends_on:
      - microservice-1
      - microservice-2
    networks:
      - microservices-network
    restart: unless-stopped

  # Base de datos compartida
  db:
    image: postgres:15-alpine
    container_name: shared-db
    environment:
      - POSTGRES_DB=shareddb
      - POSTGRES_USER=admin
      - POSTGRES_PASSWORD=admin123
    volumes:
      - shared-db-data:/var/lib/postgresql/data
    networks:
      - microservices-network
    restart: unless-stopped

networks:
  microservices-network:
    driver: bridge

volumes:
  shared-db-data:
```

## 🎯 Ejemplo 4: Usando Variables de Entorno (.env)

### docker-compose.yml
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: ${APP_NAME:-mi-app}
    ports:
      - "${APP_PORT:-8080}:8080"
    environment:
      - DB_HOST=${DB_HOST:-db}
      - DB_PORT=${DB_PORT:-5432}
      - DB_NAME=${DB_NAME:-mydb}
      - DB_USER=${DB_USER:-user}
      - DB_PASSWORD=${DB_PASSWORD:-password}
    depends_on:
      - db
    networks:
      - ${NETWORK_NAME:-app-network}

  db:
    image: postgres:${POSTGRES_VERSION:-15}-alpine
    container_name: ${DB_NAME:-db}
    environment:
      - POSTGRES_DB=${DB_NAME:-mydb}
      - POSTGRES_USER=${DB_USER:-user}
      - POSTGRES_PASSWORD=${DB_PASSWORD:-password}
    volumes:
      - ${VOLUME_NAME:-db-data}:/var/lib/postgresql/data
    networks:
      - ${NETWORK_NAME:-app-network}

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
```

### .env
```env
# Aplicación
APP_NAME=mi-aplicacion
APP_PORT=8080

# Base de datos
DB_HOST=db
DB_PORT=5432
DB_NAME=mydb
DB_USER=admin
DB_PASSWORD=secret123

# PostgreSQL
POSTGRES_VERSION=15

# Volúmenes y Redes
VOLUME_NAME=db-data
NETWORK_NAME=app-network
```

## 🎯 Ejemplo 5: Con Healthchecks y Restart Policies

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: app-with-healthcheck
    ports:
      - "8080:8080"
    environment:
      - PORT=8080
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/actuator/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: always  # always, unless-stopped, on-failure
    depends_on:
      db:
        condition: service_healthy
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    container_name: db-with-healthcheck
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user"]
      interval: 10s
      timeout: 5s
      retries: 5
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: always

networks:
  app-network:
    driver: bridge

volumes:
  db-data:
```

## 🎯 Ejemplo 6: Desarrollo vs Producción

### docker-compose.yml (Base)
```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      - DB_HOST=db
    depends_on:
      - db
    networks:
      - app-network

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_DB=mydb
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
    volumes:
      - db-data:/var/lib/postgresql/data
    networks:
      - app-network

networks:
  app-network:

volumes:
  db-data:
```

### docker-compose.override.yml (Desarrollo - se aplica automáticamente)
```yaml
version: '3.8'

services:
  app:
    ports:
      - "8080:8080"
    volumes:
      - ./src:/app/src  # Hot reload
      - ./logs:/app/logs
    environment:
      - ENV=development
      - DEBUG=true

  db:
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_PASSWORD=dev_password
```

### docker-compose.prod.yml (Producción)
```yaml
version: '3.8'

services:
  app:
    restart: always
    environment:
      - ENV=production
      - DEBUG=false
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M

  db:
    restart: always
    environment:
      - POSTGRES_PASSWORD_FILE=/run/secrets/db_password
    secrets:
      - db_password
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G

secrets:
  db_password:
    file: ./secrets/db_password.txt
```

## 📚 Comandos Docker Compose

### Comandos Básicos

```bash
# Construir y levantar servicios
docker-compose up

# Construir y levantar en segundo plano
docker-compose up -d

# Construir imágenes sin levantar
docker-compose build

# Construir sin cache
docker-compose build --no-cache

# Ver logs
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs app

# Ver logs en tiempo real
docker-compose logs -f

# Detener servicios
docker-compose stop

# Detener y eliminar contenedores
docker-compose down

# Detener, eliminar contenedores y volúmenes
docker-compose down -v

# Reiniciar un servicio
docker-compose restart app

# Ejecutar comando en un servicio
docker-compose exec app sh

# Ejecutar comando en un servicio sin TTY
docker-compose exec -T app ls

# Ver estado de servicios
docker-compose ps

# Escalar servicios (múltiples instancias)
docker-compose up -d --scale app=3

# Usar archivo específico
docker-compose -f docker-compose.prod.yml up -d

# Usar múltiples archivos
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### Comandos Avanzados

```bash
# Validar archivo compose
docker-compose config

# Validar y ver configuración final
docker-compose config | less

# Pausar servicios
docker-compose pause

# Reanudar servicios
docker-compose unpause

# Ver uso de recursos
docker-compose top

# Ejecutar comando en servicio nuevo (sin iniciar)
docker-compose run app sh

# Eliminar imágenes no usadas
docker-compose down --rmi all

# Reconstruir solo un servicio
docker-compose up -d --build app

# Ver variables de entorno
docker-compose config --services
```

## 🔧 Configuraciones Comunes

### Dependencias entre Servicios

```yaml
services:
  app:
    depends_on:
      - db
      - redis
    # Espera a que db esté healthy
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_started
```

### Variables de Entorno

```yaml
services:
  app:
    # Desde archivo .env
    environment:
      - DB_HOST=${DB_HOST}
    
    # Desde archivo específico
    env_file:
      - .env.production
    
    # Múltiples archivos
    env_file:
      - .env
      - .env.local
```

### Volúmenes

```yaml
services:
  app:
    volumes:
      # Montaje simple
      - ./data:/app/data
      
      # Volumen nombrado
      - db-data:/var/lib/postgresql/data
      
      # Solo lectura
      - ./config:/app/config:ro
      
      # Volumen con driver específico
      - cache:/cache
      
volumes:
  db-data:
    driver: local
  cache:
    driver: local
    driver_opts:
      type: tmpfs
      device: tmpfs
```

### Redes

```yaml
services:
  app:
    networks:
      - frontend
      - backend

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # Red interna (sin acceso a internet)
```

### Restart Policies

```yaml
services:
  app:
    # Siempre reiniciar si falla
    restart: always
    
    # Reiniciar a menos que se detenga manualmente
    restart: unless-stopped
    
    # Reiniciar solo si falla
    restart: on-failure
    
    # Con código de salida específico
    restart: on-failure:3
```

## 📋 Mejores Prácticas

1. **Usar versiones específicas de imágenes**
   ```yaml
   image: postgres:15-alpine  # No usar 'latest'
   ```

2. **Definir healthchecks**
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

3. **Usar .env para configuraciones sensibles**
   - No commitear .env con contraseñas
   - Usar .env.example como plantilla

4. **Separar desarrollo y producción**
   - docker-compose.yml (base)
   - docker-compose.override.yml (desarrollo)
   - docker-compose.prod.yml (producción)

5. **Usar volúmenes nombrados para datos persistentes**
   ```yaml
   volumes:
     db-data:  # No usar rutas relativas para producción
   ```

6. **Limitar recursos**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```

7. **Usar depends_on con condiciones**
   ```yaml
   depends_on:
     db:
       condition: service_healthy
   ```

## 🆚 Docker Compose vs Kubernetes

| Característica | Docker Compose | Kubernetes |
|---------------|----------------|------------|
| Uso | Desarrollo local, pequeños proyectos | Producción, orquestación compleja |
| Escalabilidad | Limitada | Alta |
| Configuración | Archivo YAML simple | Manifiestos YAML más complejos |
| Networking | Redes Docker simples | Networking avanzado |
| Load Balancing | Básico | Avanzado |
| Auto-scaling | No | Sí |
| Self-healing | Básico | Avanzado |

## 📝 Notas Importantes

- **Versión de Compose:** Usa `version: '3.8'` o superior para características modernas
- **Orden de inicio:** `depends_on` no espera que el servicio esté listo, solo que esté iniciado
- **Healthchecks:** Usa healthchecks para asegurar que los servicios estén realmente listos
- **Variables de entorno:** Docker Compose lee automáticamente el archivo `.env`
- **Override files:** `docker-compose.override.yml` se aplica automáticamente si existe

## 🔗 Referencias

- [Documentación oficial de Docker Compose](https://docs.docker.com/compose/)
- [Especificación de Compose](https://docs.docker.com/compose/compose-file/)
- [Mejores prácticas de Docker Compose](https://docs.docker.com/compose/production/)



