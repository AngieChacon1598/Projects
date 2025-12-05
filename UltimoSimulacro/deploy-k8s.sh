#!/bin/bash

# Script para desplegar en Kubernetes
# Uso: ./deploy-k8s.sh

echo "🚀 Desplegando en Kubernetes..."

echo "📦 Creando namespace..."
kubectl apply -f 02-angie-chacon-namespace.yml

echo "🔧 Creando service..."
kubectl apply -f 02-angie-chacon-service.yml

echo "📋 Creando deployment..."
kubectl apply -f 02-angie-chacon-deployment.yml

echo ""
echo "⏳ Esperando que los pods estén listos..."
kubectl wait --for=condition=ready pod -l app=microservicio-base -n angie-chacon --timeout=120s

echo ""
echo "✅ Despliegue completado!"
echo ""
echo "📊 Estado de los recursos:"
kubectl get all -n angie-chacon

echo ""
echo "🔗 Para crear port-forward, ejecuta:"
echo "   kubectl port-forward -n angie-chacon service/angie-chacon-service 8080:8080"

