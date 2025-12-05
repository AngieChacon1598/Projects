"""
Configuración global para gráficos profesionales
"""
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================================
# COLORES
# ============================================================================
COLORES_PROFESIONALES = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E', 
                         '#7209B7', '#3A86FF', '#FF006E', '#8338EC', '#FB5607']

COLORES_COMPARATIVO = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

COLORES_GRADOS = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']

# ============================================================================
# TAMAÑOS DE FIGURAS
# ============================================================================
TAMANO_BARRAS = (12, 6)
TAMANO_PASTEL = (10, 8)
TAMANO_BARRAS_HORIZONTALES = (12, 8)
TAMANO_COMPARATIVO = (16, 6)
TAMANO_DASHBOARD = (16, 10)
TAMANO_SCATTER = (12, 8)
TAMANO_HISTOGRAMA = (10, 6)

# ============================================================================
# ESTILO Y FORMATO
# ============================================================================
COLOR_TEXTO = '#2c3e50'
COLOR_BORDE = '#34495e'
ALPHA_BARRAS = 0.8
GROSOR_BORDE_BARRAS = 1.2

# ============================================================================
# TAMAÑOS DE TEXTO
# ============================================================================
TAMANO_TEXTO_BARRAS = 11
TAMANO_TEXTO_PASTEL = 12
TAMANO_LEYENDA = 11
TAMANO_TITULO_SECUNDARIO = 13
TAMANO_TITULO_DASHBOARD = 16

# ============================================================================
# FUNCIONES DE CONFIGURACIÓN
# ============================================================================
def configurar_estilo_global():
    """Configura el estilo global de matplotlib"""
    try:
        plt.style.use('seaborn-v0_8-darkgrid')
    except:
        try:
            plt.style.use('seaborn-darkgrid')
        except:
            plt.style.use('default')
    
    sns.set_palette("husl")
    plt.rcParams.update({
        'figure.figsize': (12, 6),
        'font.size': 10,
        'axes.unicode_minus': False,
        'font.family': 'sans-serif'
    })

def aplicar_estilo_ejes(ax):
    """Aplica estilo profesional a los ejes"""
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(COLOR_BORDE)
    ax.spines['bottom'].set_color(COLOR_BORDE)

def aplicar_grid(ax, eje='y', alpha=0.3):
    """Aplica grid al gráfico"""
    if eje == 'y':
        ax.grid(axis='y', alpha=alpha, linestyle='--', linewidth=0.5)
    elif eje == 'x':
        ax.grid(axis='x', alpha=alpha, linestyle='--', linewidth=0.5)
    else:
        ax.grid(True, alpha=alpha, linestyle='--', linewidth=0.5)

def aplicar_titulo(ax, titulo, tamano=None):
    """Aplica título al gráfico"""
    if tamano is None:
        tamano = TAMANO_TITULO_SECUNDARIO
    ax.set_title(titulo, fontsize=tamano, fontweight='bold', 
                 color=COLOR_TEXTO, pad=15)

def aplicar_etiquetas(ax, xlabel=None, ylabel=None):
    """Aplica etiquetas a los ejes"""
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=11, color=COLOR_TEXTO, fontweight='bold')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=11, color=COLOR_TEXTO, fontweight='bold')

