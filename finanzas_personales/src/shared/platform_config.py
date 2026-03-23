"""
Configuración de Plataforma y DPI - Finanzas Personales

Módulo centralizado para configurar DPI awareness, fuente base
y ajustes de plataforma antes de crear wx.App.

Responsabilidad ÚNICA:
- Habilitar DPI awareness en Windows (Per-Monitor DPI Aware)
- Configurar fuente base global de la aplicación
- Detectar el factor de escala del sistema

Se debe llamar ANTES de wx.App() y ANTES de crear cualquier ventana.

Uso:
    >>> from src.shared.platform_config import configure_platform
    >>> configure_platform()
    >>> app = wx.App(False)
"""

import sys
import logging

logger = logging.getLogger(__name__)


def configure_platform():
    """
    Configura la plataforma antes de crear wx.App.

    Llamar esta función UNA VEZ al inicio de la aplicación,
    antes de cualquier operación con wx.
    """
    if sys.platform == 'win32':
        _configure_windows()
    elif sys.platform == 'darwin':
        _configure_macos()
    else:
        _configure_linux()


def _configure_windows():
    """
    Configuración específica para Windows:
    1. Habilitar DPI awareness (Per-Monitor DPI Aware v1)
    2. Intentar activar visual styles via InitCommonControlsEx
    """
    try:
        import ctypes
        try:
            from ctypes import wintypes
        except ImportError:
            wintypes = None

        # ============================================================
        # DPI AWARENESS
        # ============================================================
        # Llamamos ANTES de que wx o matplotlib inicialicen anything.
        #
        # Opciones de SetProcessDpiAwareness (shcore.dll):
        #   0 = DPI_UNAWARE - no escala
        #   1 = SYSTEM_DPI_AWARE - usa DPI del monitor primario
        #   2 = PER_MONITOR_DPI_AWARE - escala por monitor (mejor)
        #
        # En Windows 10+ también existe SetProcessDpiAwarenessContext.
        # Intentamos el más moderno primero, fallback al básico.

        dpi_configured = False

        # Intento 1: Windows 10 1703+ - Per Monitor DPI Aware v2
        try:
            shcore = ctypes.windll.shcore
            # PROCESS_PER_MONITOR_DPI_AWARE = 2
            result = shcore.SetProcessDpiAwareness(2)
            if result == 0:  # S_OK
                logger.info("DPI awareness: Per-Monitor DPI Aware v1 (shcore)")
                dpi_configured = True
        except (AttributeError, OSError):
            pass

        # Intento 2: SetProcessDPIAware (Windows Vista+, user32)
        if not dpi_configured:
            try:
                user32 = ctypes.windll.user32
                result = user32.SetProcessDPIAware()
                if result:
                    logger.info("DPI awareness: System DPI Aware (user32)")
                    dpi_configured = True
            except (AttributeError, OSError):
                pass

        if not dpi_configured:
            logger.warning("No se pudo configurar DPI awareness en Windows")

        # ============================================================
        # VISUAL STYLES (Common Controls v6)
        # ============================================================
        # InitCommonControlsEx habilita los controles modernos de Windows.
        # Sin esto, los controles usan el estilo clásico Win32.
        try:
            comctl32 = ctypes.windll.comctl32

            # ICC_STANDARD_CLASSES = 0x00004000
            # ICC_WIN95_CLASSES = 0x000000FF
            ICC_FLAGS = 0x00004000 | 0x000000FF

            class INITCOMMONCONTROLSEX(ctypes.Structure):
                _fields_ = [
                    ("dwSize", wintypes.DWORD if wintypes else ctypes.c_ulong),
                    ("dwICC", wintypes.DWORD if wintypes else ctypes.c_ulong),
                ]

            icc = INITCOMMONCONTROLSEX()
            icc.dwSize = ctypes.sizeof(INITCOMMONCONTROLSEX)
            icc.dwICC = ICC_FLAGS

            comctl32.InitCommonControlsEx(ctypes.byref(icc))
            logger.info("Common Controls inicializados (visual styles)")
        except (AttributeError, OSError):
            logger.debug("No se pudo llamar InitCommonControlsEx")

    except Exception as e:
        logger.warning(f"Error configurando plataforma Windows: {e}")


def _configure_macos():
    """Configuración para macOS (generalmente no necesita ajustes)."""
    logger.debug("Plataforma macOS - sin ajustes necesarios")


def _configure_linux():
    """Configuración para Linux."""
    logger.debug("Plataforma Linux - sin ajustes necesarios")


def configure_wx_app(app):
    """
    Loggea la fuente base del sistema para diagnóstico.

    En wxPython no existe wx.SystemSettings.SetFont() - los controles
    usan la fuente del OS por defecto. Para cambiar fuentes se debe
    hacer en cada vista individual (vía design_tokens o wx.Font directo).

    Args:
        app: Instancia de wx.App
    """
    import wx

    # Obtener y loggear la fuente del sistema (solo informativo)
    sys_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
    logger.info(
        f"Fuente del sistema: {sys_font.GetFaceName()} "
        f"{sys_font.GetPointSize()}pt"
    )


def get_dpi_scale():
    """
    Retorna el factor de escala DPI actual del sistema.

    Returns:
        float: Factor de escala (1.0 = 100%, 1.25 = 125%, etc.)
    """
    if sys.platform == 'win32':
        try:
            import ctypes
            user32 = ctypes.windll.user32
            # GetDpiForSystem() disponible desde Windows 10 1607
            try:
                dpi = user32.GetDpiForSystem()
                return dpi / 96.0
            except AttributeError:
                # Fallback: usar HDC del desktop
                gdi32 = ctypes.windll.gdi32
                dc = user32.GetDC(0)
                dpi = gdi32.GetDeviceCaps(dc, 88)  # LOGPIXELSX
                user32.ReleaseDC(0, dc)
                return dpi / 96.0
        except Exception:
            return 1.0
    return 1.0


def scaled(value):
    """
    Escala un valor (en píxeles a 96 DPI) al DPI actual del sistema.

    Útil para dimensiones hardcodeadas que deben adaptarse.

    Args:
        value: Valor en píxeles a 96 DPI

    Returns:
        int: Valor escalado al DPI actual
    """
    return int(value * get_dpi_scale())
