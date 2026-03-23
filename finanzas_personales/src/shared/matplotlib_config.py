"""
Configuración de Matplotlib - Finanzas Personales

Configura rcParams globales de matplotlib para que los gráficos
se vean más nítidos, limpios y profesionales.

Se debe importar UNA VEZ al inicio, antes de crear figuras.

Responsabilidad ÚNICA:
- Configurar DPI de renderizado
- Establecer familias de fuente
- Ajustar antialias y calidad de renderizado
- Establecer colores por defecto modernos

Uso:
    >>> from src.shared.matplotlib_config import configure_matplotlib
    >>> configure_matplotlib()
    >>> import matplotlib.pyplot as plt
    >>> fig, ax = plt.subplots()
"""

import logging

logger = logging.getLogger(__name__)


def configure_matplotlib():
    """
    Configura matplotlib globalmente para nitidez y calidad visual.

    Llamar UNA VEZ antes de crear figuras.
    """
    try:
        import matplotlib
        import matplotlib.pyplot as plt

        # ============================================================
        # DPI DE RENDERIZADO
        # ============================================================
        # dpi=80 es el default antiguo. Monitores modernos tienen 96-144 DPI.
        # Subir a 100 mejora nitidez sin hacer los gráficos enormes.
        # El dpi de la figura también afecta a los textos y líneas.

        matplotlib.rcParams['figure.dpi'] = 100

        # DPI al guardar (separado del de pantalla)
        matplotlib.rcParams['savefig.dpi'] = 150

        # ============================================================
        # FUENTES
        # ============================================================
        # Usar la fuente del sistema para coherencia con la app.

        import sys
        if sys.platform == 'win32':
            matplotlib.rcParams['font.family'] = 'sans-serif'
            matplotlib.rcParams['font.sans-serif'] = [
                'Segoe UI', 'Tahoma', 'Arial', 'DejaVu Sans'
            ]
        elif sys.platform == 'darwin':
            matplotlib.rcParams['font.family'] = 'sans-serif'
            matplotlib.rcParams['font.sans-serif'] = [
                'Helvetica Neue', 'Helvetica', 'Arial', 'DejaVu Sans'
            ]
        else:
            matplotlib.rcParams['font.family'] = 'sans-serif'
            matplotlib.rcParams['font.sans-serif'] = [
                'DejaVu Sans', 'Liberation Sans', 'Arial'
            ]

        # Tamaño base de fuente (se hereda por todos los gráficos)
        matplotlib.rcParams['font.size'] = 9

        # ============================================================
        # ANTIALIASING Y CALIDAD
        # ============================================================
        matplotlib.rcParams['text.antialiased'] = True
        matplotlib.rcParams['lines.antialiased'] = True
        matplotlib.rcParams['patch.antialiased'] = True

        # ============================================================
        # ESTILO DE FIGURA
        # ============================================================
        # Fondo limpio
        matplotlib.rcParams['figure.facecolor'] = '#FFFFFF'
        matplotlib.rcParams['axes.facecolor'] = '#FAFAFA'

        # Bordes de ejes más sutiles
        matplotlib.rcParams['axes.edgecolor'] = '#CCCCCC'
        matplotlib.rcParams['axes.linewidth'] = 0.8

        # Grid más sutil
        matplotlib.rcParams['grid.color'] = '#E0E0E0'
        matplotlib.rcParams['grid.linewidth'] = 0.5
        matplotlib.rcParams['grid.alpha'] = 0.5

        # ============================================================
        # COLORES POR DEFECTO
        # ============================================================
        # Paleta moderna (Tableau-like, más limpia que la default)
        matplotlib.rcParams['axes.prop_cycle'] = matplotlib.cycler(color=[
            '#4E79A7',  # azul
            '#F28E2B',  # naranja
            '#E15759',  # rojo
            '#76B7B2',  # teal
            '#59A14F',  # verde
            '#EDC948',  # amarillo
            '#B07AA1',  # púrpura
            '#FF9DA7',  # rosa
            '#9C755F',  # marrón
            '#BAB0AC',  # gris
        ])

        # ============================================================
        # TICKS Y LABELS
        # ============================================================
        matplotlib.rcParams['xtick.major.width'] = 0.8
        matplotlib.rcParams['ytick.major.width'] = 0.8
        matplotlib.rcParams['xtick.major.size'] = 4
        matplotlib.rcParams['ytick.major.size'] = 4
        matplotlib.rcParams['xtick.color'] = '#666666'
        matplotlib.rcParams['ytick.color'] = '#666666'

        # Labels de ejes
        matplotlib.rcParams['axes.labelcolor'] = '#333333'
        matplotlib.rcParams['axes.labelsize'] = 9

        # Título
        matplotlib.rcParams['axes.titlesize'] = 11
        matplotlib.rcParams['axes.titleweight'] = 'bold'
        matplotlib.rcParams['axes.titlecolor'] = '#222222'

        # ============================================================
        # LEYENDA
        # ============================================================
        matplotlib.rcParams['legend.fontsize'] = 8
        matplotlib.rcParams['legend.framealpha'] = 0.9
        matplotlib.rcParams['legend.edgecolor'] = '#CCCCCC'

        # ============================================================
        # LÍNEAS Y MARCADORES
        # ============================================================
        matplotlib.rcParams['lines.linewidth'] = 1.5
        matplotlib.rcParams['lines.markersize'] = 5

        logger.info("Matplotlib configurado: dpi=100, antialias=on, estilo moderno")

    except ImportError:
        logger.debug("matplotlib no disponible, configuración omitida")
    except Exception as e:
        logger.warning(f"Error configurando matplotlib: {e}")
