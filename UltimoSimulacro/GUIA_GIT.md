# Guía para Subir al Repositorio Git

## ✅ Respuesta Rápida

**NO necesitas eliminar la imagen Docker.** La imagen Docker es independiente del código y NO se guarda en Git.

## 📦 ¿Qué se sube a Git?

### ✅ Archivos que SÍ debes subir:

1. **Código fuente:**
   - `src/` (todo el código Java)
   - `pom.xml`

2. **Configuración Docker:**
   - `Dockerfile`
   - `.dockerignore`

3. **Manifiestos de Kubernetes:**
   - `02-angie-chacon-namespace.yml`
   - `02-angie-chacon-service.yml`
   - `02-angie-chacon-deployment.yml`

4. **Documentación:**
   - `README.md`
   - `INSTRUCCIONES.md`
   - `PRUEBAS.md`
   - `GUIA_GIT.md` (este archivo)

5. **Scripts:**
   - `build-and-push.sh`
   - `deploy-k8s.sh`

6. **Configuración Git:**
   - `.gitignore`

### ❌ Archivos que NO se suben (ya están en .gitignore):

- `target/` (carpeta de compilación)
- Imágenes Docker (se construyen, no se guardan)
- Archivos de IDE (`.idea/`, `.vscode/`)
- Archivos temporales

## 🚀 Pasos para Subir al Repositorio

### 1. Verificar el estado de Git

```bash
git status
```

### 2. Agregar todos los archivos necesarios

```bash
git add .
```

O agregar archivos específicos:

```bash
git add src/
git add pom.xml
git add Dockerfile
git add .dockerignore
git add .gitignore
git add 02-angie-chacon-*.yml
git add *.md
git add *.sh
```

### 3. Verificar qué se va a subir

```bash
git status
```

Asegúrate de que NO aparezca `target/` en la lista.

### 4. Hacer commit

```bash
git commit -m "Microservicio base para hackathon - Angie Chacon"
```

### 5. Subir al repositorio remoto

```bash
git push origin main
```

O si es la primera vez:

```bash
git remote add origin URL_DE_TU_REPOSITORIO
git branch -M main
git push -u origin main
```

## 📋 Checklist Antes de Subir

- [ ] ✅ `.gitignore` está creado y configurado
- [ ] ✅ `target/` NO aparece en `git status`
- [ ] ✅ Todos los archivos `.yml` de Kubernetes están incluidos
- [ ] ✅ `Dockerfile` y `.dockerignore` están incluidos
- [ ] ✅ Código fuente (`src/`) está incluido
- [ ] ✅ `pom.xml` está incluido
- [ ] ✅ Documentación está incluida

## 🔍 Verificar que todo está bien

Después de subir, puedes clonar el repositorio en otra carpeta para verificar:

```bash
cd ..
git clone URL_DE_TU_REPOSITORIO test-clone
cd test-clone
ls -la
```

Deberías ver todos los archivos necesarios, pero NO deberías ver `target/`.

## 🐳 Sobre la Imagen Docker

**IMPORTANTE:** La imagen Docker:
- ✅ Se construye a partir del código (usando `Dockerfile`)
- ✅ NO se guarda en Git
- ✅ Se construye cuando se necesite con: `docker build -t 02-angie-chacon:1.0 .`
- ✅ Se sube a Docker Hub (no a Git) con: `docker push`

**Para la evaluación:**
1. El código está en Git ✅
2. La imagen Docker se construye desde el código ✅
3. La imagen se sube a Docker Hub ✅
4. Kubernetes usa la imagen de Docker Hub ✅

## 📝 Comandos Útiles

### Ver qué archivos están siendo rastreados
```bash
git ls-files
```

### Ver qué archivos están ignorados
```bash
git status --ignored
```

### Limpiar archivos no rastreados (si es necesario)
```bash
git clean -n  # Ver qué se eliminaría (dry-run)
git clean -f  # Eliminar archivos no rastreados
```

## ⚠️ Notas Importantes

1. **La imagen Docker local:** Puedes mantenerla, no afecta el repositorio Git
2. **target/:** NO debe subirse (ya está en .gitignore)
3. **Docker Hub:** Es diferente de Git, ahí sí subes la imagen Docker
4. **Para la evaluación:** Necesitas tanto el código en Git como la imagen en Docker Hub

