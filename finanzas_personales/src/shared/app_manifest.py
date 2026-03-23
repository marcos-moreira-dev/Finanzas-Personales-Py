"""
Generador de Manifest Windows - Finanzas Personales

Genera y registra el manifest de aplicación Windows para habilitar:
1. Common Controls v6 (visual styles modernos)
2. DPI Awareness (Per-Monitor DPI Aware)

Esto es necesario porque sin manifest, Windows usa los controles
clásicos Win32 que se ven planos y antiguos.

Se debe llamar ANTES de crear cualquier ventana wx.

Uso:
    >>> from src.shared.app_manifest import apply_windows_manifest
    >>> apply_windows_manifest()
"""

import sys
import logging
import os

logger = logging.getLogger(__name__)

# Manifest XML para Windows
# Declara:
# - Common Controls v6 para visual styles
# - Per-Monitor DPI Aware v2 para escalado correcto
# - Per-Monitor DPI Aware v1 como fallback
WINDOWS_MANIFEST = b"""\
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <assemblyIdentity
    version="1.0.0.0"
    processorArchitecture="*"
    name="FinanzasPersonales"
    type="win32"
  />
  <description>Finanzas Personales - Aplicacion de escritorio</description>

  <!-- Common Controls v6 - Habilita visual styles modernos -->
  <dependency>
    <dependentAssembly>
      <assemblyIdentity
        type="win32"
        name="Microsoft.Windows.Common-Controls"
        version="6.0.0.0"
        processorArchitecture="*"
        publicKeyToken="6595b64144ccf1df"
        language="*"
      />
    </dependentAssembly>
  </dependency>

  <!-- DPI Awareness - Per-Monitor DPI Aware v2 (Windows 10 1703+) -->
  <application xmlns="urn:schemas-microsoft-com:asm.v3">
    <windowsSettings>
      <dpiAware xmlns="http://schemas.microsoft.com/SMI/2005/WindowsSettings">true/pm</dpiAware>
      <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">PerMonitorV2,PerMonitor</dpiAwareness>
    </windowsSettings>
  </application>
</assembly>
"""


def apply_windows_manifest():
    """
    Aplica el manifest de Windows para visual styles y DPI awareness.

    Intenta dos métodos:
    1. Activation Context API (el más robusto para Python puro)
    2. Archivo .manifest junto al ejecutable (fallback)

    Solo se ejecuta en Windows. En otras plataformas es no-op.
    """
    if sys.platform != 'win32':
        return

    _apply_activation_context()


def _apply_activation_context():
    """
    Usa la Activation Context API de Windows para cargar el manifest.

    Esto permite que el manifest se aplique sin necesidad de un archivo
    .manifest físico junto al ejecutable.

    Referencia: Microsoft docs on CreateActCtx / ActivateActCtx
    """
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.windll.kernel32

        # ============================================================
        # Estructuras necesarias
        # ============================================================

        ACTCTX_FLAG_PROCESS_RESOURCE = 0x00000002
        ACTCTX_FLAG_ASSEMBLY_DIRECTORY_VALID = 0x00000004

        class ACTCTXW(ctypes.Structure):
            _fields_ = [
                ("cbSize", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("lpSource", ctypes.c_wchar_p),
                ("wProcessorArchitecture", ctypes.c_ushort),
                ("wLangId", ctypes.c_ushort),
                ("lpAssemblyDirectory", ctypes.c_wchar_p),
                ("lpResourceName", ctypes.c_ulonglong),
                ("lpApplicationName", ctypes.c_wchar_p),
                ("hModule", ctypes.c_void_p),
            ]

        # ============================================================
        # Crear archivo temporal con el manifest
        # ============================================================
        import tempfile

        manifest_path = os.path.join(
            tempfile.gettempdir(),
            "finanzas_personales.manifest"
        )

        # Escribir manifest XML
        with open(manifest_path, 'wb') as f:
            f.write(WINDOWS_MANIFEST)

        # ============================================================
        # Crear y activar el activation context
        # ============================================================

        actctx = ACTCTXW()
        actctx.cbSize = ctypes.sizeof(ACTCTXW)
        actctx.dwFlags = ACTCTX_FLAG_PROCESS_RESOURCE
        actctx.lpSource = manifest_path

        handle = kernel32.CreateActCtxW(ctypes.byref(actctx))

        if handle == -1:  # INVALID_HANDLE_VALUE
            error = kernel32.GetLastError()
            logger.debug(f"CreateActCtx falló (error {error}), probablemente ya hay manifest activo")
            # No es crítico - puede que ya esté activo o que el sistema
            # lo maneje por otra vía
            return

        cookie = ctypes.c_ulonglong(0)
        result = kernel32.ActivateActCtx(handle, ctypes.byref(cookie))

        if result:
            logger.info("Windows manifest aplicado: Common Controls v6 + DPI Aware")
        else:
            logger.debug("ActivateActCtx retornó False, continuando sin manifest explícito")

    except Exception as e:
        # No es crítico si falla - la app sigue funcionando,
        # solo pierde visual styles y DPI awareness via manifest
        logger.debug(f"No se pudo aplicar manifest Windows: {e}")


def write_manifest_file(target_dir=None):
    """
    Escribe un archivo .manifest junto al ejecutable.

    Útil para cx_Freeze / PyInstaller donde el manifest debe ser
    un archivo físico con el mismo nombre que el .exe.

    Args:
        target_dir: Directorio donde escribir. Si es None, usa cwd.
    """
    if sys.platform != 'win32':
        return

    if target_dir is None:
        target_dir = os.getcwd()

    manifest_path = os.path.join(target_dir, "FinanzasPersonales.exe.manifest")

    try:
        with open(manifest_path, 'wb') as f:
            f.write(WINDOWS_MANIFEST)
        logger.info(f"Manifest escrito en: {manifest_path}")
    except Exception as e:
        logger.warning(f"No se pudo escribir manifest: {e}")
