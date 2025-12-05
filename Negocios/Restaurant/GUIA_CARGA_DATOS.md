# Guía para Cargar Datasets en un DataFrame con Pandas

Esta guía te ayudará a cargar diferentes tipos de archivos de datos en un DataFrame usando pandas.

## Tabla de Contenidos

1. [Requisitos Previos](#requisitos-previos)
2. [Cargar Archivos CSV](#cargar-archivos-csv)
3. [Cargar Archivos Excel](#cargar-archivos-excel)
4. [Manejo de Codificaciones](#manejo-de-codificaciones)
5. [Manejo de Errores](#manejo-de-errores)
6. [Preparación de Datos](#preparación-de-datos)
7. [Ejemplos Prácticos](#ejemplos-prácticos)

---

## Requisitos Previos

### Instalación de Librerías

```python
# Instalar pandas
pip install pandas

# Para archivos Excel
pip install openpyxl  # Para archivos .xlsx
pip install xlrd      # Para archivos .xls antiguos

# Para análisis de datos
pip install numpy matplotlib seaborn
```

### Importar Librerías

```python
import pandas as pd
import numpy as np
import os
```

---

## Cargar Archivos CSV

### Caso Básico

```python
# Archivo CSV con separador de coma (estándar)
df = pd.read_csv('archivo.csv')
```

### CSV con Separador Personalizado

```python
# CSV con punto y coma (;)
df = pd.read_csv('archivo.csv', sep=';')

# CSV con tabulador
df = pd.read_csv('archivo.csv', sep='\t')

# CSV con pipe
df = pd.read_csv('archivo.csv', sep='|')
```

### CSV con Encabezados Personalizados

```python
# Especificar nombres de columnas
df = pd.read_csv('archivo.csv', names=['Col1', 'Col2', 'Col3'])

# Usar primera fila como encabezado (por defecto)
df = pd.read_csv('archivo.csv', header=0)

# Sin encabezado
df = pd.read_csv('archivo.csv', header=None)
```

### CSV con Manejo de Valores Faltantes

```python
# Especificar valores que representan NaN
df = pd.read_csv('archivo.csv', na_values=['N/A', 'NULL', ''])

# Mantener valores vacíos como strings
df = pd.read_csv('archivo.csv', keep_default_na=False)
```

### CSV con Límites de Filas

```python
# Leer solo las primeras 100 filas
df = pd.read_csv('archivo.csv', nrows=100)

# Saltar las primeras 10 filas
df = pd.read_csv('archivo.csv', skiprows=10)

# Saltar filas específicas
df = pd.read_csv('archivo.csv', skiprows=[0, 2, 5])
```

### CSV con Columnas Específicas

```python
# Leer solo columnas específicas
df = pd.read_csv('archivo.csv', usecols=['Col1', 'Col2', 'Col3'])

# Leer columnas por índice
df = pd.read_csv('archivo.csv', usecols=[0, 1, 2])
```

---

## Cargar Archivos Excel

### Archivo Excel Básico

```python
# Leer archivo .xlsx
df = pd.read_excel('archivo.xlsx')

# Leer archivo .xls (formato antiguo)
df = pd.read_excel('archivo.xls')
```

### Leer Hoja Específica

```python
# Por nombre de hoja
df = pd.read_excel('archivo.xlsx', sheet_name='Hoja1')

# Por índice de hoja (0 = primera hoja)
df = pd.read_excel('archivo.xlsx', sheet_name=0)

# Leer múltiples hojas
hojas = pd.read_excel('archivo.xlsx', sheet_name=['Hoja1', 'Hoja2'])
df1 = hojas['Hoja1']
df2 = hojas['Hoja2']
```

### Excel con Filas y Columnas Específicas

```python
# Saltar filas iniciales
df = pd.read_excel('archivo.xlsx', skiprows=2)

# Leer desde fila específica
df = pd.read_excel('archivo.xlsx', header=2)

# Leer solo columnas específicas
df = pd.read_excel('archivo.xlsx', usecols='A:C,E')
```

---

## Manejo de Codificaciones

### Detectar y Usar Codificación Correcta

```python
import chardet

# Detectar codificación automáticamente
with open('archivo.csv', 'rb') as f:
    raw_data = f.read(10000)
    resultado = chardet.detect(raw_data)
    encoding = resultado['encoding']

df = pd.read_csv('archivo.csv', encoding=encoding)
```

### Probar Múltiples Codificaciones

```python
def cargar_csv_con_codificacion(ruta_archivo, separador=';'):
    """Intenta cargar un CSV probando diferentes codificaciones"""
    codificaciones = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1', 'utf-16']
    
    for encoding in codificaciones:
        try:
            df = pd.read_csv(ruta_archivo, sep=separador, encoding=encoding)
            print(f"✓ Archivo cargado exitosamente con codificación: {encoding}")
            return df
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error con {encoding}: {e}")
            continue
    
    raise Exception("No se pudo cargar el archivo con ninguna codificación")

# Uso
df = cargar_csv_con_codificacion('archivo.csv', separador=';')
```

### Codificaciones Comunes

- **UTF-8**: Estándar internacional, recomendado para nuevos archivos
- **Latin-1 (ISO-8859-1)**: Común en archivos europeos
- **CP1252 (Windows-1252)**: Codificación de Windows
- **UTF-16**: Para archivos con muchos caracteres especiales

---

## Manejo de Errores

### Manejar Líneas Problemáticas

```python
# Saltar líneas con errores (pandas >= 1.3.0)
df = pd.read_csv('archivo.csv', on_bad_lines='skip', engine='python')

# Para versiones antiguas de pandas
df = pd.read_csv('archivo.csv', error_bad_lines=False, warn_bad_lines=False, engine='python')
```

### Manejar Archivos Grandes

```python
# Leer en chunks (pedazos)
chunk_size = 10000
chunks = []

for chunk in pd.read_csv('archivo_grande.csv', chunksize=chunk_size):
    # Procesar cada chunk
    chunks.append(chunk)

# Combinar todos los chunks
df = pd.concat(chunks, ignore_index=True)
```

### Verificar Existencia del Archivo

```python
import os

ruta_archivo = 'data/archivo.csv'

# Verificar si el archivo existe
if not os.path.exists(ruta_archivo):
    raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")

df = pd.read_csv(ruta_archivo)
```

### Función Robusta de Carga

```python
def cargar_datos_robusto(ruta_archivo, separador=';', tipo='csv'):
    """
    Función robusta para cargar datos con manejo de errores
    
    Parámetros:
    - ruta_archivo: Ruta al archivo
    - separador: Separador para CSV (por defecto ';')
    - tipo: 'csv' o 'excel'
    """
    # Verificar existencia
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    # Cargar según tipo
    if tipo == 'csv':
        codificaciones = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        
        for encoding in codificaciones:
            try:
                try:
                    df = pd.read_csv(ruta_archivo, sep=separador, encoding=encoding,
                                   quotechar='"', on_bad_lines='skip', engine='python')
                except TypeError:
                    df = pd.read_csv(ruta_archivo, sep=separador, encoding=encoding,
                                   quotechar='"', error_bad_lines=False,
                                   warn_bad_lines=False, engine='python')
                print(f"✓ Cargado con codificación: {encoding}")
                return df
            except (UnicodeDecodeError, Exception) as e:
                continue
        
        raise Exception("No se pudo cargar el archivo CSV")
    
    elif tipo == 'excel':
        try:
            df = pd.read_excel(ruta_archivo)
            print(f"✓ Archivo Excel cargado exitosamente")
            return df
        except Exception as e:
            raise Exception(f"Error al cargar Excel: {e}")
    
    else:
        raise ValueError("Tipo debe ser 'csv' o 'excel'")

# Uso
df = cargar_datos_robusto('data/archivo.csv', separador=';', tipo='csv')
```

---

## Preparación de Datos

### Convertir Tipos de Datos

```python
# Convertir columnas numéricas
df['MESAS'] = pd.to_numeric(df['MESAS'], errors='coerce')
df['SILLAS'] = pd.to_numeric(df['SILLAS'], errors='coerce')

# Convertir fechas
df['FECHA'] = pd.to_datetime(df['FECHA'], format='%Y%m%d', errors='coerce')

# Convertir a categorías (útil para datos repetitivos)
df['CATEGORIA'] = df['CATEGORIA'].astype('category')
```

### Limpiar Datos

```python
# Eliminar filas con valores faltantes en columnas específicas
df = df.dropna(subset=['COLUMNA1', 'COLUMNA2'])

# Eliminar filas duplicadas
df = df.drop_duplicates()

# Eliminar espacios en blanco en strings
df['COLUMNA'] = df['COLUMNA'].str.strip()

# Reemplazar valores
df['COLUMNA'] = df['COLUMNA'].replace('valor_viejo', 'valor_nuevo')
```

### Información del DataFrame

```python
# Información básica
print(f"Dimensiones: {df.shape[0]} filas x {df.shape[1]} columnas")
print(f"\nColumnas: {df.columns.tolist()}")
print(f"\nPrimeras filas:")
print(df.head())
print(f"\nInformación del dataset:")
print(df.info())
print(f"\nEstadísticas descriptivas:")
print(df.describe())
```

---

## Ejemplos Prácticos

### Ejemplo 1: Cargar CSV con Separador Punto y Coma

```python
import pandas as pd
import os

# Obtener ruta del archivo
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
ruta_archivo = os.path.join(project_root, 'data', 'Restaurantes_calificados.csv')

# Cargar datos
df = pd.read_csv(ruta_archivo, sep=';', encoding='latin-1')

# Preparar datos
df['MESAS'] = pd.to_numeric(df['MESAS'], errors='coerce')
df['SILLAS'] = pd.to_numeric(df['SILLAS'], errors='coerce')

print(f"Dataset cargado: {df.shape[0]} filas x {df.shape[1]} columnas")
```

### Ejemplo 2: Cargar Excel con Múltiples Hojas

```python
import pandas as pd

# Leer todas las hojas
archivo_excel = pd.ExcelFile('datos.xlsx')

# Ver nombres de hojas
print("Hojas disponibles:", archivo_excel.sheet_names)

# Leer hoja específica
df_hoja1 = pd.read_excel(archivo_excel, sheet_name='Hoja1')
df_hoja2 = pd.read_excel(archivo_excel, sheet_name='Hoja2')

# O leer todas las hojas a la vez
todas_hojas = pd.read_excel(archivo_excel, sheet_name=None)
```

### Ejemplo 3: Cargar Datos con Validación

```python
import pandas as pd
import os

def cargar_y_validar(ruta_archivo):
    """Carga datos y valida que tenga las columnas esperadas"""
    
    # Verificar archivo
    if not os.path.exists(ruta_archivo):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    # Cargar
    df = pd.read_csv(ruta_archivo, sep=';', encoding='latin-1')
    
    # Validar columnas requeridas
    columnas_requeridas = ['MESAS', 'SILLAS', 'CATEGORIA', 'DES_DEPA']
    columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
    
    if columnas_faltantes:
        raise ValueError(f"Columnas faltantes: {columnas_faltantes}")
    
    # Validar que no esté vacío
    if df.empty:
        raise ValueError("El DataFrame está vacío")
    
    print(f"✓ Datos cargados y validados: {df.shape[0]} filas")
    return df

# Uso
df = cargar_y_validar('data/archivo.csv')
```

### Ejemplo 4: Cargar desde URL

```python
import pandas as pd

# Cargar CSV desde URL
url = 'https://ejemplo.com/datos.csv'
df = pd.read_csv(url)

# Cargar Excel desde URL
url_excel = 'https://ejemplo.com/datos.xlsx'
df = pd.read_excel(url_excel)
```

### Ejemplo 5: Cargar y Procesar en Chunks

```python
import pandas as pd

# Para archivos muy grandes
def procesar_archivo_grande(ruta_archivo):
    """Procesa un archivo grande en chunks"""
    
    resultados = []
    chunk_size = 10000
    
    for chunk in pd.read_csv(ruta_archivo, chunksize=chunk_size, sep=';'):
        # Procesar cada chunk
        chunk_procesado = chunk.dropna(subset=['COLUMNA_IMPORTANTE'])
        resultados.append(chunk_procesado)
    
    # Combinar resultados
    df_final = pd.concat(resultados, ignore_index=True)
    return df_final

# Uso
df = procesar_archivo_grande('archivo_grande.csv')
```

---

## Resumen de Parámetros Comunes

### `pd.read_csv()` - Parámetros Útiles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `sep` | Separador de columnas | `sep=';'` |
| `encoding` | Codificación del archivo | `encoding='utf-8'` |
| `header` | Fila de encabezados | `header=0` o `header=None` |
| `nrows` | Número de filas a leer | `nrows=1000` |
| `skiprows` | Filas a saltar | `skiprows=5` |
| `usecols` | Columnas a leer | `usecols=[0, 1, 2]` |
| `na_values` | Valores que representan NaN | `na_values=['N/A']` |
| `dtype` | Tipos de datos | `dtype={'col1': 'int64'}` |
| `parse_dates` | Columnas a parsear como fechas | `parse_dates=['fecha']` |

### `pd.read_excel()` - Parámetros Útiles

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `sheet_name` | Nombre o índice de hoja | `sheet_name='Hoja1'` |
| `header` | Fila de encabezados | `header=0` |
| `skiprows` | Filas a saltar | `skiprows=2` |
| `usecols` | Columnas a leer | `usecols='A:C'` |
| `engine` | Motor de lectura | `engine='openpyxl'` |

---

## Buenas Prácticas

1. **Siempre verifica la existencia del archivo** antes de intentar cargarlo
2. **Maneja diferentes codificaciones** para archivos con caracteres especiales
3. **Valida los datos** después de cargarlos (columnas, tipos, valores nulos)
4. **Usa chunks** para archivos muy grandes que no caben en memoria
5. **Documenta** el formato esperado de tus archivos
6. **Guarda logs** de errores para debugging
7. **Convierte tipos** apropiadamente después de cargar
8. **Limpia datos** antes de comenzar el análisis

---

## Solución de Problemas Comunes

### Error: "FileNotFoundError"
```python
# Solución: Verificar ruta y usar rutas absolutas o relativas correctas
import os
ruta = os.path.join(os.getcwd(), 'data', 'archivo.csv')
```

### Error: "UnicodeDecodeError"
```python
# Solución: Probar diferentes codificaciones
for encoding in ['utf-8', 'latin-1', 'cp1252']:
    try:
        df = pd.read_csv('archivo.csv', encoding=encoding)
        break
    except UnicodeDecodeError:
        continue
```

### Error: "ParserError" o líneas mal formateadas
```python
# Solución: Usar engine='python' y on_bad_lines='skip'
df = pd.read_csv('archivo.csv', engine='python', on_bad_lines='skip')
```

### Archivo muy grande
```python
# Solución: Leer en chunks o usar dask
import dask.dataframe as dd
df = dd.read_csv('archivo_grande.csv')
```

---

## Recursos Adicionales

- [Documentación oficial de pandas](https://pandas.pydata.org/docs/)
- [Guía de IO Tools de pandas](https://pandas.pydata.org/docs/user_guide/io.html)
- [Pandas read_csv completo](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)

---

**Última actualización:** 2024

