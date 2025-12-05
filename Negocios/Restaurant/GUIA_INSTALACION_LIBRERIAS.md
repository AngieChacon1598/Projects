# Guía de Instalación de Librerías para Análisis de Datos

Esta guía te ayudará a instalar todas las librerías necesarias para realizar análisis de datos con Python.

## Tabla de Contenidos

1. [Requisitos del Sistema](#requisitos-del-sistema)
2. [Instalación Básica](#instalación-básica)
3. [Instalación por Categorías](#instalación-por-categorías)
4. [Instalación con Conda](#instalación-con-conda)
5. [Verificación de Instalación](#verificación-de-instalación)
6. [Solución de Problemas](#solución-de-problemas)
7. [Requisitos por Proyecto](#requisitos-por-proyecto)

---

## Requisitos del Sistema

### Python

- **Versión mínima recomendada:** Python 3.8 o superior
- **Verificar versión:**
  ```bash
  python --version
  # o
  python3 --version
  ```

### Gestor de Paquetes

- **pip** (incluido con Python 3.4+)
  ```bash
  pip --version
  # o
  pip3 --version
  ```

---

## Instalación Básica

### Instalación Individual

```bash
# Instalar pandas
pip install pandas

# Instalar numpy
pip install numpy

# Instalar matplotlib
pip install matplotlib

# Instalar seaborn
pip install seaborn

# Instalar openpyxl (para archivos Excel)
pip install openpyxl

# Instalar xlrd (para archivos Excel antiguos .xls)
pip install xlrd
```

### Instalación Múltiple en una Línea

```bash
pip install pandas numpy matplotlib seaborn openpyxl xlrd
```

### Instalación con Versiones Específicas

```bash
pip install pandas==2.0.0 numpy==1.24.0 matplotlib==3.7.0 seaborn==0.12.0
```

---

## Instalación por Categorías

### 📊 Librerías Esenciales para Análisis de Datos

```bash
# Análisis de datos
pip install pandas numpy

# Visualización
pip install matplotlib seaborn

# Archivos Excel
pip install openpyxl xlrd
```

### 📈 Librerías para Visualización Avanzada

```bash
# Visualización básica
pip install matplotlib seaborn

# Visualización interactiva (opcional)
pip install plotly bokeh

# Gráficos estadísticos avanzados
pip install scipy statsmodels
```

### 🔬 Librerías para Análisis Estadístico

```bash
# Estadística básica
pip install scipy

# Estadística avanzada
pip install statsmodels

# Pruebas estadísticas
pip install pingouin
```

### 📁 Librerías para Manejo de Archivos

```bash
# Archivos Excel
pip install openpyxl xlrd

# Archivos CSV avanzados
pip install chardet  # Detección de codificaciones

# Archivos JSON
# (json viene incluido con Python)

# Archivos Parquet
pip install pyarrow fastparquet
```

### 🎨 Librerías para Estilo y Configuración

```bash
# Estilos de matplotlib
# (viene incluido con matplotlib)

# Configuración de gráficos
pip install seaborn  # Incluye estilos profesionales
```

---

## Instalación con Conda

### Si usas Anaconda o Miniconda

```bash
# Instalación básica
conda install pandas numpy matplotlib seaborn

# Instalación desde conda-forge (más actualizado)
conda install -c conda-forge pandas numpy matplotlib seaborn openpyxl

# Crear entorno virtual con todas las librerías
conda create -n analisis_datos pandas numpy matplotlib seaborn openpyxl
conda activate analisis_datos
```

---

## Verificación de Instalación

### Script de Verificación Completo

Crea un archivo `verificar_instalacion.py`:

```python
"""
Script para verificar que todas las librerías estén instaladas correctamente
"""

import sys

def verificar_libreria(nombre, import_name=None):
    """Verifica si una librería está instalada"""
    if import_name is None:
        import_name = nombre
    
    try:
        __import__(import_name)
        print(f"✓ {nombre} está instalado correctamente")
        return True
    except ImportError:
        print(f"✗ {nombre} NO está instalado")
        return False

def obtener_version(nombre):
    """Obtiene la versión de una librería"""
    try:
        modulo = __import__(nombre)
        if hasattr(modulo, '__version__'):
            return modulo.__version__
        else:
            return "Instalado (versión no disponible)"
    except:
        return "No instalado"

print("=" * 60)
print("VERIFICACIÓN DE INSTALACIÓN DE LIBRERÍAS")
print("=" * 60)
print(f"\nPython: {sys.version}")
print(f"Versión: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")

print("\n" + "-" * 60)
print("LIBRERÍAS ESENCIALES")
print("-" * 60)

librerias_esenciales = {
    'pandas': 'pandas',
    'numpy': 'numpy',
    'matplotlib': 'matplotlib',
    'seaborn': 'seaborn',
    'openpyxl': 'openpyxl',
}

todas_instaladas = True
for nombre, import_name in librerias_esenciales.items():
    if not verificar_libreria(nombre, import_name):
        todas_instaladas = False

print("\n" + "-" * 60)
print("VERSIONES INSTALADAS")
print("-" * 60)

for nombre, import_name in librerias_esenciales.items():
    version = obtener_version(import_name)
    print(f"{nombre:15} : {version}")

print("\n" + "-" * 60)
print("LIBRERÍAS OPCIONALES")
print("-" * 60)

librerias_opcionales = {
    'scipy': 'scipy',
    'xlrd': 'xlrd',
    'chardet': 'chardet',
    'statsmodels': 'statsmodels',
}

for nombre, import_name in librerias_opcionales.items():
    verificar_libreria(nombre, import_name)

print("\n" + "=" * 60)
if todas_instaladas:
    print("✓ TODAS LAS LIBRERÍAS ESENCIALES ESTÁN INSTALADAS")
else:
    print("✗ FALTAN ALGUNAS LIBRERÍAS ESENCIALES")
    print("\nPara instalar las librerías faltantes, ejecuta:")
    print("pip install pandas numpy matplotlib seaborn openpyxl")
print("=" * 60)
```

### Ejecutar Verificación

```bash
python verificar_instalacion.py
```

### Verificación Rápida en Python

```python
# Abrir Python o IPython
python

# Verificar importaciones
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

print("✓ Todas las librerías están instaladas")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {plt.matplotlib.__version__}")
print(f"Seaborn: {sns.__version__}")
```

---

## Solución de Problemas

### Error: "pip no se reconoce como comando"

**Solución Windows:**
```bash
# Usar python -m pip
python -m pip install pandas

# O agregar Python al PATH del sistema
```

**Solución Linux/Mac:**
```bash
# Usar pip3
pip3 install pandas

# O python3 -m pip
python3 -m pip install pandas
```

### Error: "Permission denied" o "Acceso denegado"

**Solución:**
```bash
# Windows: Ejecutar como administrador o usar --user
pip install --user pandas

# Linux/Mac: Usar sudo (con precaución)
sudo pip install pandas

# Mejor opción: Usar entorno virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows
pip install pandas
```

### Error: "Microsoft Visual C++ 14.0 is required"

**Solución Windows:**
- Instalar [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- O instalar versiones precompiladas:
  ```bash
  pip install --only-binary :all: pandas numpy
  ```

### Error: "No module named 'pandas'"

**Solución:**
```bash
# Verificar que estás usando el Python correcto
which python  # Linux/Mac
where python  # Windows

# Reinstalar
pip uninstall pandas
pip install pandas

# Verificar instalación
python -c "import pandas; print(pandas.__version__)"
```

### Error al instalar openpyxl

**Solución:**
```bash
# Actualizar pip primero
python -m pip install --upgrade pip

# Luego instalar openpyxl
pip install openpyxl

# Si persiste, instalar dependencias manualmente
pip install et-xmlfile
pip install openpyxl
```

### Error: "Could not find a version that satisfies the requirement"

**Solución:**
```bash
# Actualizar pip
python -m pip install --upgrade pip

# Actualizar setuptools
pip install --upgrade setuptools

# Intentar sin especificar versión
pip install pandas
```

### Problemas con Matplotlib en Windows

**Solución:**
```bash
# Instalar dependencias adicionales
pip install pillow

# Si hay problemas con backend, instalar:
pip install PyQt5
# o
pip install tkinter
```

---

## Requisitos por Proyecto

### Proyecto: Análisis de Restaurantes

**Librerías requeridas:**
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

**Archivo requirements.txt:**
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
```

**Instalación desde requirements.txt:**
```bash
pip install -r requirements.txt
```

### Proyecto: Análisis Estadístico Avanzado

**Librerías requeridas:**
```bash
pip install pandas numpy matplotlib seaborn scipy statsmodels
```

**Archivo requirements.txt:**
```
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0
scipy>=1.10.0
statsmodels>=0.14.0
```

### Proyecto: Análisis con Visualización Interactiva

**Librerías requeridas:**
```bash
pip install pandas numpy matplotlib seaborn plotly
```

---

## Crear Archivo requirements.txt

### Método 1: Generar automáticamente

```bash
# Generar requirements.txt desde el entorno actual
pip freeze > requirements.txt
```

### Método 2: Crear manualmente

Crea un archivo `requirements.txt`:

```
# Librerías esenciales para análisis de datos
pandas>=2.0.0
numpy>=1.24.0
matplotlib>=3.7.0
seaborn>=0.12.0

# Manejo de archivos Excel
openpyxl>=3.1.0
xlrd>=2.0.0

# Análisis estadístico (opcional)
scipy>=1.10.0

# Detección de codificaciones (opcional)
chardet>=5.0.0
```

### Instalar desde requirements.txt

```bash
pip install -r requirements.txt
```

---

## Entornos Virtuales (Recomendado)

### Crear Entorno Virtual

**Windows:**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

# Instalar librerías
pip install pandas numpy matplotlib seaborn
```

**Linux/Mac:**
```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Instalar librerías
pip install pandas numpy matplotlib seaborn
```

### Desactivar Entorno Virtual

```bash
deactivate
```

### Ventajas de Entornos Virtuales

- ✅ Aislamiento de proyectos
- ✅ Control de versiones por proyecto
- ✅ Evita conflictos entre proyectos
- ✅ Fácil de compartir (requirements.txt)

---

## Instalación en Diferentes Sistemas Operativos

### Windows

```powershell
# PowerShell o CMD
python -m pip install --upgrade pip
python -m pip install pandas numpy matplotlib seaborn openpyxl
```

### Linux (Ubuntu/Debian)

```bash
# Actualizar sistema
sudo apt update

# Instalar Python y pip si no están instalados
sudo apt install python3 python3-pip

# Instalar librerías
pip3 install --user pandas numpy matplotlib seaborn openpyxl
```

### macOS

```bash
# Usar Homebrew (recomendado)
brew install python3

# Instalar librerías
pip3 install pandas numpy matplotlib seaborn openpyxl
```

---

## Comandos Útiles

### Actualizar Librerías

```bash
# Actualizar una librería específica
pip install --upgrade pandas

# Actualizar todas las librerías
pip list --outdated
pip install --upgrade $(pip list --outdated | awk 'NR>2 {print $1}')
```

### Desinstalar Librerías

```bash
# Desinstalar una librería
pip uninstall pandas

# Desinstalar múltiples librerías
pip uninstall pandas numpy matplotlib
```

### Listar Librerías Instaladas

```bash
# Listar todas las librerías
pip list

# Listar solo las relevantes
pip list | grep -E "pandas|numpy|matplotlib|seaborn"

# Mostrar información de una librería
pip show pandas
```

### Buscar Librerías

```bash
# Buscar librerías en PyPI
pip search pandas  # (puede no estar disponible en todas las versiones)
```

---

## Verificación de Compatibilidad

### Versiones Compatibles Recomendadas

| Librería | Versión Mínima | Versión Recomendada |
|----------|---------------|---------------------|
| Python   | 3.8           | 3.10+              |
| pandas   | 1.5.0         | 2.0.0+             |
| numpy    | 1.21.0        | 1.24.0+            |
| matplotlib | 3.5.0      | 3.7.0+             |
| seaborn  | 0.12.0        | 0.12.0+            |
| openpyxl | 3.0.0         | 3.1.0+             |

### Verificar Compatibilidad

```python
import pandas as pd
import numpy as np
import matplotlib
import seaborn as sns

print("Versiones instaladas:")
print(f"Python: {sys.version}")
print(f"Pandas: {pd.__version__}")
print(f"NumPy: {np.__version__}")
print(f"Matplotlib: {matplotlib.__version__}")
print(f"Seaborn: {sns.__version__}")

# Verificar compatibilidad
if pd.__version__ >= "2.0.0":
    print("✓ Pandas versión compatible")
else:
    print("⚠ Considera actualizar pandas")
```

---

## Instalación para Evaluación/Examen

### Checklist Pre-Evaluación

```bash
# 1. Verificar Python
python --version  # Debe ser 3.8 o superior

# 2. Actualizar pip
python -m pip install --upgrade pip

# 3. Instalar librerías esenciales
pip install pandas numpy matplotlib seaborn openpyxl

# 4. Verificar instalación
python -c "import pandas, numpy, matplotlib, seaborn; print('✓ Todo OK')"

# 5. Probar carga de datos
python -c "import pandas as pd; df = pd.DataFrame({'a': [1,2,3]}); print(df)"
```

### Script de Instalación Completa

Crea un archivo `instalar_todo.bat` (Windows) o `instalar_todo.sh` (Linux/Mac):

**Windows (instalar_todo.bat):**
```batch
@echo off
echo Instalando librerias para analisis de datos...
python -m pip install --upgrade pip
pip install pandas numpy matplotlib seaborn openpyxl xlrd chardet
echo.
echo Verificando instalacion...
python -c "import pandas, numpy, matplotlib, seaborn; print('Instalacion exitosa!')"
pause
```

**Linux/Mac (instalar_todo.sh):**
```bash
#!/bin/bash
echo "Instalando librerías para análisis de datos..."
python3 -m pip install --upgrade pip
pip3 install pandas numpy matplotlib seaborn openpyxl xlrd chardet
echo ""
echo "Verificando instalación..."
python3 -c "import pandas, numpy, matplotlib, seaborn; print('Instalación exitosa!')"
```

---

## Recursos Adicionales

### Documentación Oficial

- [Pandas Installation](https://pandas.pydata.org/docs/getting_started/install.html)
- [NumPy Installation](https://numpy.org/install/)
- [Matplotlib Installation](https://matplotlib.org/stable/users/installing/index.html)
- [Seaborn Installation](https://seaborn.pydata.org/installing.html)

### Repositorios

- [PyPI - Python Package Index](https://pypi.org/)
- [Conda Forge](https://conda-forge.org/)

### Ayuda y Soporte

- [Stack Overflow - Python](https://stackoverflow.com/questions/tagged/python)
- [Python Discord](https://discord.gg/python)
- [r/learnpython](https://www.reddit.com/r/learnpython/)

---

## Resumen Rápido

### Instalación Mínima (Lo Esencial)

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### Instalación Completa (Recomendado)

```bash
pip install pandas numpy matplotlib seaborn openpyxl xlrd chardet scipy
```

### Verificación Rápida

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
print("✓ Todo instalado correctamente")
```

---

**Última actualización:** 2024

**Nota:** Las versiones de las librerías pueden cambiar. Siempre verifica las versiones más recientes en PyPI.

