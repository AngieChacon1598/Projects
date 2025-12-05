# Hackathon - Spring WebFlux + Kubernetes

## Microservicio AI con Spring WebFlux

Este proyecto implementa un microservicio completo con Spring WebFlux que incluye:
- **Job Search API**: Búsqueda de trabajos usando JSearch API
- **Language Detection API**: Detección de idiomas usando RapidAPI
- **MongoDB**: Persistencia de datos con Spring Data Reactive MongoDB
- **Docker**: Containerización en 2 procesos
- **Kubernetes**: Despliegue con minikube

## Requisitos del Hackathon

**Microservicio Base**: Spring WebFlux con MongoDB (NoSQL)  
**Dockerización**: 2 procesos (builder + runtime)  
**Imagen Docker**: 220MB (rango 100-300MB)  
**Nombre Imagen**: `angie14/02-angie-chacon:1.0`  
**Docker Hub**: Imagen subida  
**Kubernetes**: Archivos YAML + 2 pods + port-forward  


## Endpoints Disponibles

- **Health Check**: curl http://localhost:8081/actuator/health
- **Job Search**: curl http://localhost:8081/api/v1/jobs/search?query=developer&location=Lima
- **Language Detection**: curl http://localhost:8081/api/v1/language/detect
- **Ver todos los Jobs**: curl http://localhost:8081/api/v1/jobs/all
- **Ver todas las detecciones**: curl http://localhost:8081/api/v1/language/detections

**Ver Logs**: kubectl logs -f deployment/angie-chacon-deployment -n angie-chacon-namespace
**Ver estado de Pods**: kubectl get pods -n angie-chacon-namespace

## Tecnologías Utilizadas

- **Backend**: Spring WebFlux, Spring Boot 3.2.0
- **Base de Datos**: MongoDB Atlas
- **APIs Externas**: JSearch API, Language Detection API
- **Containerización**: Docker
- **Orquestación**: Kubernetes (minikube)
- **Build Tool**: Maven
