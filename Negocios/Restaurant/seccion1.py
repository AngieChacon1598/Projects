import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Importar configuración de gráficos
from config_graficos import (
    configurar_estilo_global,
    COLORES_PROFESIONALES, COLORES_COMPARATIVO,
    TAMANO_BARRAS, TAMANO_PASTEL, TAMANO_BARRAS_HORIZONTALES,
    TAMANO_COMPARATIVO, TAMANO_SCATTER, TAMANO_HISTOGRAMA,
    COLOR_TEXTO, COLOR_BORDE, ALPHA_BARRAS, GROSOR_BORDE_BARRAS,
    TAMANO_TEXTO_BARRAS, TAMANO_TEXTO_PASTEL, TAMANO_LEYENDA,
    TAMANO_TITULO_SECUNDARIO,
    aplicar_estilo_ejes, aplicar_grid, aplicar_titulo, aplicar_etiquetas
)

# Configurar estilo global de gráficos
configurar_estilo_global()

# ============================================================================
# CARGA DE DATOS
# ============================================================================
def cargar_datos():
    """Carga los datos del archivo CSV"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    ruta_archivo = os.path.join(project_root, 'data', 'Restaurantes_calificados.csv')
    
    if not os.path.exists(ruta_archivo):
        ruta_archivo = os.path.join('data', 'Restaurantes_calificados.csv')
        if not os.path.exists(ruta_archivo):
            raise FileNotFoundError(f"Archivo no encontrado: {ruta_archivo}")
    
    print(f"Cargando datos desde: {ruta_archivo}")
    
    # Cargar CSV con diferentes codificaciones
    for encoding in ['latin-1', 'cp1252', 'iso-8859-1', 'utf-8']:
        try:
            try:
                df = pd.read_csv(ruta_archivo, sep=';', encoding=encoding, quotechar='"', 
                               on_bad_lines='skip', engine='python')
            except TypeError:
                df = pd.read_csv(ruta_archivo, sep=';', encoding=encoding, quotechar='"', 
                               error_bad_lines=False, warn_bad_lines=False, engine='python')
            print(f"✓ Cargado con codificación: {encoding}")
            return df
        except (UnicodeDecodeError, Exception):
            continue
    
    raise Exception("No se pudo cargar el archivo")

# ============================================================================
# FUNCIONES DE ANÁLISIS ESTADÍSTICO
# ============================================================================
def calcular_metricas_estadisticas(serie, titulo):
    """Calcula métricas estadísticas para una serie de datos"""
    if serie.empty:
        return None
    
    total = len(serie)
    conteo = serie.value_counts()
    
    # Métricas básicas
    moda = conteo.index[0]
    frecuencia_moda = conteo.iloc[0]
    porcentaje_moda = (frecuencia_moda / total) * 100
    
    # Diversidad de respuestas (entropía)
    probabilidades = conteo / total
    entropia = -np.sum(probabilidades * np.log2(probabilidades + 1e-10))
    
    # Índice de diversidad
    concentracion = np.sum(probabilidades**2)
    diversidad = 1 - concentracion
    
    return {
        'titulo': titulo,
        'total': total,
        'moda': moda,
        'frecuencia_moda': frecuencia_moda,
        'porcentaje_moda': porcentaje_moda,
        'entropia': entropia,
        'diversidad': diversidad,
        'conteo': conteo
    }

# ============================================================================
# FUNCIONES DE GRAFICADO
# ============================================================================
def graficar_barras(serie, titulo, horizontal=False, mostrar_valores=True):
    """Gráfico de barras profesional (horizontal o vertical)"""
    if serie.empty:
        print(f"No hay datos para: {titulo}")
        return
    
    fig, ax = plt.subplots(figsize=TAMANO_BARRAS_HORIZONTALES if horizontal else TAMANO_BARRAS)
    
    # Ordenar datos
    if horizontal:
        serie_ordenada = serie.sort_values(ascending=True)
    else:
        serie_ordenada = serie.sort_values(ascending=False)
    
    # Colores con gradiente
    colors = plt.cm.viridis(np.linspace(0, 1, len(serie_ordenada)))
    
    if horizontal:
        bars = ax.barh(range(len(serie_ordenada)), serie_ordenada.values,
                       color=colors, edgecolor=COLOR_BORDE, 
                       linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
        
        if mostrar_valores:
            for i, (bar, value) in enumerate(zip(bars, serie_ordenada.values)):
                ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                        f'{int(value)} ({value/serie_ordenada.sum()*100:.1f}%)',
                        ha='left', va='center', fontweight='bold', 
                        fontsize=TAMANO_TEXTO_BARRAS, color=COLOR_TEXTO)
        
        ax.set_yticks(range(len(serie_ordenada)))
        ax.set_yticklabels(serie_ordenada.index, fontsize=11)
        aplicar_etiquetas(ax, xlabel='Cantidad de Restaurantes')
        aplicar_grid(ax, eje='x')
        ax.set_xlim(0, max(serie_ordenada.values) * 1.15)
    else:
        bars = ax.bar(range(len(serie_ordenada)), serie_ordenada.values,
                      color=colors, edgecolor=COLOR_BORDE,
                      linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
        
        if mostrar_valores:
            for i, (bar, value) in enumerate(zip(bars, serie_ordenada.values)):
                ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                        f'{int(value)} ({value/serie_ordenada.sum()*100:.1f}%)',
                        ha='center', va='bottom', fontweight='bold',
                        fontsize=TAMANO_TEXTO_BARRAS, color=COLOR_TEXTO)
        
        ax.set_xticks(range(len(serie_ordenada)))
        ax.set_xticklabels(serie_ordenada.index, fontsize=11, rotation=45, ha='right')
        aplicar_etiquetas(ax, xlabel='Categoría', ylabel='Cantidad de Restaurantes')
        aplicar_grid(ax, eje='y')
        ax.set_ylim(0, max(serie_ordenada.values) * 1.15)
    
    aplicar_titulo(ax, titulo)
    aplicar_estilo_ejes(ax)
    plt.tight_layout()
    plt.show()

def graficar_pastel(serie, titulo):
    """Gráfico de pastel profesional"""
    if serie.empty:
        print(f"No hay datos para: {titulo}")
        return
    
    fig, ax = plt.subplots(figsize=TAMANO_PASTEL)
    
    wedges, texts, autotexts = ax.pie(serie.values,
                                     labels=serie.index,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     colors=COLORES_PROFESIONALES[:len(serie)],
                                     explode=[0.05] * len(serie),
                                     shadow=True,
                                     textprops={'fontsize': 12, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color(COLOR_TEXTO)
        autotext.set_fontweight('bold')
        autotext.set_fontsize(TAMANO_TEXTO_PASTEL)
    
    aplicar_titulo(ax, titulo)
    ax.legend(wedges, [f'{label}: {value}' for label, value in zip(serie.index, serie.values)],
              title="Categorías", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1),
              fontsize=TAMANO_LEYENDA, title_fontsize=12)
    plt.tight_layout()
    plt.show()

def graficar_comparativo(data, titulo, labels, colores=None):
    """Gráfico comparativo con múltiples series"""
    if colores is None:
        colores = COLORES_COMPARATIVO
    
    fig, axes = plt.subplots(1, 2, figsize=TAMANO_COMPARATIVO)
    
    for ax, (label, values) in zip(axes, zip(labels, data)):
        bars = ax.barh(range(len(values)), values,
                       color=colores[:len(values)], edgecolor=COLOR_BORDE,
                       linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
        
        for bar, value in zip(bars, values):
            ax.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{int(value)}', ha='left', va='center',
                    fontweight='bold', fontsize=TAMANO_TEXTO_BARRAS, color=COLOR_TEXTO)
        
        ax.set_yticks(range(len(values)))
        ax.set_yticklabels([str(v) for v in range(len(values))], fontsize=10)
        aplicar_titulo(ax, label, tamano=TAMANO_TITULO_SECUNDARIO)
        aplicar_etiquetas(ax, xlabel='Cantidad')
        aplicar_grid(ax, eje='x')
        aplicar_estilo_ejes(ax)
    
    plt.tight_layout()
    plt.show()

def graficar_scatter(x, y, titulo, xlabel, ylabel, linea_tendencia=True):
    """Gráfico de dispersión con línea de tendencia"""
    fig, ax = plt.subplots(figsize=TAMANO_SCATTER)
    
    ax.scatter(x, y, alpha=0.6, s=50, color=COLORES_PROFESIONALES[0],
               edgecolors=COLOR_BORDE, linewidth=0.5)
    
    if linea_tendencia:
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "r--", alpha=0.8, linewidth=2,
               label=f'Tendencia (y={z[0]:.2f}x+{z[1]:.2f})')
        ax.legend(fontsize=TAMANO_LEYENDA)
    
    aplicar_etiquetas(ax, xlabel=xlabel, ylabel=ylabel)
    aplicar_titulo(ax, titulo)
    aplicar_grid(ax, eje='ambos')
    aplicar_estilo_ejes(ax)
    plt.tight_layout()
    plt.show()

def graficar_histograma(data, titulo, xlabel, valor_promedio=None):
    """Gráfico de histograma"""
    fig, ax = plt.subplots(figsize=TAMANO_HISTOGRAMA)
    
    ax.hist(data, bins=30, color=COLORES_PROFESIONALES[4],
            edgecolor=COLOR_BORDE, alpha=ALPHA_BARRAS)
    
    if valor_promedio is not None:
        ax.axvline(valor_promedio, color='red', linestyle='--',
                  linewidth=2, label=f'Promedio: {valor_promedio:.2f}')
        ax.legend(fontsize=TAMANO_LEYENDA)
    
    aplicar_etiquetas(ax, xlabel=xlabel, ylabel='Frecuencia')
    aplicar_titulo(ax, titulo)
    aplicar_grid(ax, eje='y')
    aplicar_estilo_ejes(ax)
    plt.tight_layout()
    plt.show()

# ============================================================================
# ANÁLISIS PRINCIPAL
# ============================================================================
def main():
    # Cargar y preparar datos
    df = cargar_datos()
    df['MESAS'] = pd.to_numeric(df['MESAS'], errors='coerce')
    df['SILLAS'] = pd.to_numeric(df['SILLAS'], errors='coerce')
    df['FECHA_CORTE'] = pd.to_datetime(df['FECHA_CORTE'], format='%Y%m%d', errors='coerce')
    
    print("\n" + "="*80)
    print(f"Dataset: {df.shape[0]} filas x {df.shape[1]} columnas")
    print("="*80)
    
    metricas_totales = []
    
    # CONSULTA 1: Distribución por categoría
    print("\nCONSULTA 1: Distribución por categoría")
    dist_cat = df['CATEGORIA'].value_counts()
    print(dist_cat)
    
    metricas = calcular_metricas_estadisticas(dist_cat, "Distribución por Categoría")
    if metricas:
        metricas_totales.append(metricas)
        print(f"   - Total: {metricas['total']}")
        print(f"   - Moda: {metricas['moda']} ({metricas['porcentaje_moda']:.1f}%)")
        print(f"   - Diversidad: {metricas['diversidad']:.3f}")
    
    graficar_barras(dist_cat, "Distribución de Restaurantes por Categoría")
    graficar_pastel(dist_cat, "Proporción de Restaurantes por Categoría")
    
    # CONSULTA 2: Capacidad por departamento
    print("\nCONSULTA 2: Capacidad por departamento")
    cap_dept = df.groupby('DES_DEPA').agg({
        'MESAS': ['sum', 'mean', 'count'],
        'SILLAS': ['sum', 'mean']
    }).round(2)
    cap_dept.columns = ['Total_Mesas', 'Promedio_Mesas', 'Cantidad', 'Total_Sillas', 'Promedio_Sillas']
    cap_dept = cap_dept.sort_values('Total_Sillas', ascending=False)
    print("\nTop 10 Departamentos:")
    print(cap_dept.head(10))
    
    top10 = cap_dept.head(10)
    graficar_comparativo(
        [top10['Total_Sillas'].values, top10['Promedio_Sillas'].values],
        "Capacidad por Departamento",
        ['Top 10 - Total de Sillas', 'Top 10 - Promedio de Sillas'],
        colores=['coral', 'lightblue']
    )
    
    # CONSULTA 3: Correlación mesas-sillas
    print("\nCONSULTA 3: Correlación mesas-sillas")
    df_validos = df.dropna(subset=['MESAS', 'SILLAS']).copy()
    corr = df_validos[['MESAS', 'SILLAS']].corr().iloc[0, 1]
    df_validos['RATIO'] = df_validos['SILLAS'] / df_validos['MESAS']
    ratio_prom = df_validos['RATIO'].mean()
    print(f"Correlación: {corr:.4f} | Ratio promedio: {ratio_prom:.2f}")
    
    graficar_scatter(df_validos['MESAS'], df_validos['SILLAS'],
                    "Relación entre Mesas y Sillas",
                    "Número de Mesas", "Número de Sillas")
    
    graficar_histograma(df_validos['RATIO'], "Distribución del Ratio Sillas/Mesas",
                       "Ratio Sillas/Mesas", ratio_prom)
    
    # CONSULTA 4: Distribución geográfica
    print("\nCONSULTA 4: Distribución geográfica")
    dist_prov = df.groupby(['DES_DEPA', 'DES_PROV']).size().reset_index(name='CANTIDAD')
    dist_prov = dist_prov.sort_values('CANTIDAD', ascending=False)
    print("\nTop 15 Provincias:")
    print(dist_prov.head(15).to_string(index=False))
    
    top15 = dist_prov.head(15)
    serie_prov = pd.Series(top15['CANTIDAD'].values,
                          index=[f"{r['DES_PROV']}, {r['DES_DEPA']}" 
                                for _, r in top15.iterrows()])
    graficar_barras(serie_prov, "Top 15 Provincias con Mayor Número de Restaurantes",
                   horizontal=True)
    
    dist_dept = df['DES_DEPA'].value_counts().head(10)
    graficar_barras(dist_dept, "Top 10 Departamentos con Mayor Número de Restaurantes")
    
    # CONSULTA 5: Información de contacto
    print("\nCONSULTA 5: Información de contacto")
    df['TIENE_EMAIL'] = df['E_MAIL'].notna() & (df['E_MAIL'] != '')
    df['TIENE_WEB'] = df['PAGINA_WEB'].notna() & (df['PAGINA_WEB'] != '')
    df['TIENE_TELEFONO'] = df['TELEF1'].notna() & (df['TELEF1'] != '')
    
    info = pd.DataFrame({
        'Con Email': [df['TIENE_EMAIL'].sum()],
        'Con Web': [df['TIENE_WEB'].sum()],
        'Con Teléfono': [df['TIENE_TELEFONO'].sum()],
        'Total': [len(df)]
    })
    info['% Email'] = (info['Con Email'] / info['Total'] * 100).round(2)
    info['% Web'] = (info['Con Web'] / info['Total'] * 100).round(2)
    info['% Teléfono'] = (info['Con Teléfono'] / info['Total'] * 100).round(2)
    print(info.T)
    
    fig, axes = plt.subplots(1, 2, figsize=TAMANO_COMPARATIVO)
    counts = [df['TIENE_EMAIL'].sum(), df['TIENE_WEB'].sum(), df['TIENE_TELEFONO'].sum()]
    labels = ['Email', 'Web', 'Teléfono']
    colores_contacto = ['skyblue', 'lightcoral', 'lightgreen']
    
    axes[0].bar(labels, counts, color=colores_contacto, edgecolor=COLOR_BORDE,
                width=0.6, linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
    aplicar_titulo(axes[0], 'Cantidad con Información de Contacto')
    aplicar_etiquetas(axes[0], ylabel='Cantidad')
    aplicar_grid(axes[0], eje='y')
    aplicar_estilo_ejes(axes[0])
    for i, v in enumerate(counts):
        axes[0].text(i, v, str(v), ha='center', va='bottom',
                    fontweight='bold', fontsize=TAMANO_TEXTO_BARRAS, color=COLOR_TEXTO)
    
    pct = [info['% Email'].iloc[0], info['% Web'].iloc[0], info['% Teléfono'].iloc[0]]
    axes[1].bar(labels, pct, color=colores_contacto, edgecolor=COLOR_BORDE,
                width=0.6, linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
    aplicar_titulo(axes[1], 'Porcentaje con Información de Contacto')
    aplicar_etiquetas(axes[1], ylabel='Porcentaje (%)')
    axes[1].set_ylim(0, 100)
    aplicar_grid(axes[1], eje='y')
    aplicar_estilo_ejes(axes[1])
    for i, v in enumerate(pct):
        axes[1].text(i, v, f'{v:.1f}%', ha='center', va='bottom',
                    fontweight='bold', fontsize=TAMANO_TEXTO_BARRAS, color=COLOR_TEXTO)
    
    plt.tight_layout()
    plt.show()
    
    # CONSULTA 6: Capacidad por categoría
    print("\nCONSULTA 6: Capacidad por categoría")
    cap_cat = df.groupby('CATEGORIA').agg({
        'MESAS': ['mean', 'median', 'std', 'min', 'max'],
        'SILLAS': ['mean', 'median', 'std', 'min', 'max']
    }).round(2)
    cap_cat.columns = ['Mesas_Media', 'Mesas_Mediana', 'Mesas_Std', 'Mesas_Min', 'Mesas_Max',
                        'Sillas_Media', 'Sillas_Mediana', 'Sillas_Std', 'Sillas_Min', 'Sillas_Max']
    print(cap_cat)
    
    fig, axes = plt.subplots(1, 2, figsize=TAMANO_COMPARATIVO)
    df_box = df.dropna(subset=['MESAS', 'CATEGORIA'])
    sns.boxplot(data=df_box, x='CATEGORIA', y='MESAS', ax=axes[0],
                hue='CATEGORIA', palette='Set2', legend=False)
    aplicar_titulo(axes[0], 'Distribución de Mesas por Categoría')
    aplicar_etiquetas(axes[0], xlabel='Categoría', ylabel='Número de Mesas')
    axes[0].tick_params(axis='x', rotation=45)
    aplicar_grid(axes[0], eje='y')
    aplicar_estilo_ejes(axes[0])
    
    df_box2 = df.dropna(subset=['SILLAS', 'CATEGORIA'])
    sns.boxplot(data=df_box2, x='CATEGORIA', y='SILLAS', ax=axes[1],
                hue='CATEGORIA', palette='Set2', legend=False)
    aplicar_titulo(axes[1], 'Distribución de Sillas por Categoría')
    aplicar_etiquetas(axes[1], xlabel='Categoría', ylabel='Número de Sillas')
    axes[1].tick_params(axis='x', rotation=45)
    aplicar_grid(axes[1], eje='y')
    aplicar_estilo_ejes(axes[1])
    plt.tight_layout()
    plt.show()
    
    fig, axes = plt.subplots(1, 2, figsize=TAMANO_COMPARATIVO)
    cats_ord = cap_cat.sort_values('Mesas_Media', ascending=False).index
    
    valores_mesas = [cap_cat.loc[c, 'Mesas_Media'] for c in cats_ord]
    axes[0].bar(range(len(cats_ord)), valores_mesas,
                color='salmon', edgecolor=COLOR_BORDE, width=0.6,
                linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
    axes[0].set_xticks(range(len(cats_ord)))
    axes[0].set_xticklabels(cats_ord, rotation=45, ha='right', fontsize=10)
    aplicar_titulo(axes[0], 'Promedio de Mesas por Categoría')
    aplicar_etiquetas(axes[0], ylabel='Promedio de Mesas')
    aplicar_grid(axes[0], eje='y')
    aplicar_estilo_ejes(axes[0])
    
    valores_sillas = [cap_cat.loc[c, 'Sillas_Media'] for c in cats_ord]
    axes[1].bar(range(len(cats_ord)), valores_sillas,
                color='lightseagreen', edgecolor=COLOR_BORDE, width=0.6,
                linewidth=GROSOR_BORDE_BARRAS, alpha=ALPHA_BARRAS)
    axes[1].set_xticks(range(len(cats_ord)))
    axes[1].set_xticklabels(cats_ord, rotation=45, ha='right', fontsize=10)
    aplicar_titulo(axes[1], 'Promedio de Sillas por Categoría')
    aplicar_etiquetas(axes[1], ylabel='Promedio de Sillas')
    aplicar_grid(axes[1], eje='y')
    aplicar_estilo_ejes(axes[1])
    plt.tight_layout()
    plt.show()
    
    # Resumen final
    print("\n" + "="*80)
    print("ANÁLISIS COMPLETADO")
    print("="*80)
    if metricas_totales:
        print(f"\nTotal de análisis realizados: {len(metricas_totales)}")
        diversidades = [(m['titulo'], m['diversidad']) for m in metricas_totales]
        diversidades.sort(key=lambda x: x[1], reverse=True)
        print(f"Mayor diversidad: {diversidades[0][0]} ({diversidades[0][1]:.3f})")

if __name__ == "__main__":
    main()
