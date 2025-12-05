#!/bin/bash

# Script para construir y subir la imagen Docker
# Uso: ./build-and-push.sh [DOCKER_HUB_USERNAME]

IMAGE_NAME="02-angie-chacon:1.0"
DOCKER_HUB_USER=${1:-""}

echo "🔨 Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

if [ $? -ne 0 ]; then
    echo "❌ Error al construir la imagen"
    exit 1
fi

echo "✅ Imagen construida exitosamente"
echo ""
echo "📊 Tamaño de la imagen:"
docker images | grep "02-angie-chacon"

if [ -n "$DOCKER_HUB_USER" ]; then
    echo ""
    echo "🏷️  Taggeando imagen para Docker Hub..."
    docker tag $IMAGE_NAME $DOCKER_HUB_USER/$IMAGE_NAME
    
    echo "📤 Subiendo imagen a Docker Hub..."
    docker push $DOCKER_HUB_USER/$IMAGE_NAME
    
    if [ $? -eq 0 ]; then
        echo "✅ Imagen subida exitosamente a Docker Hub"
        echo ""
        echo "⚠️  Recuerda actualizar el deployment con:"
        echo "   image: $DOCKER_HUB_USER/$IMAGE_NAME"
    else
        echo "❌ Error al subir la imagen"
        exit 1
    fi
else
    echo ""
    echo "ℹ️  Para subir a Docker Hub, ejecuta:"
    echo "   ./build-and-push.sh TU_USUARIO_DOCKER_HUB"
fi

