"""
Configuración de la Aplicación

Este módulo gestiona la configuración de la aplicación de forma
centralizada. Lee variables de entorno y proporciona valores por defecto.
"""
import os
import sys
from pathlib import Path

# Intentar cargar dotenv (opcional)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv no está instalado, usar variables de entorno del sistema

# Directorio base del proyecto
BASE_DIR = Path(__file__).parent.parent.parent.parent

# Detectar sistema operativo
IS_WINDOWS = sys.platform == 'win32'
IS_MACOS = sys.platform == 'darwin'
IS_LINUX = sys.platform.startswith('linux')


def get_data_directory():
    """
    Obtiene el directorio de datos según el sistema operativo.
    
    Windows: %APPDATA%/FinanzasPersonales
    Linux: ~/.local/share/finanzas_personales
    macOS: ~/Library/Application Support/FinanzasPersonales
    """
    custom_path = os.getenv('DB_PATH')
    if custom_path:
        return Path(custom_path).parent
    
    if IS_WINDOWS:
        app_data = Path(os.environ.get('APPDATA', Path.home() / 'AppData/Roaming'))
        return app_data / 'FinanzasPersonales'
    elif IS_MACOS:
        return Path.home() / 'Library/Application Support/FinanzasPersonales'
    else:
        xdg_data = os.environ.get('XDG_DATA_HOME', Path.home() / '.local/share')
        return Path(xdg_data) / 'finanzas_personales'


# Configuración de la aplicación
class Config:
    """Configuración central de la aplicación."""
    
    # Datos de la aplicación
    APP_NAME = os.getenv('APP_NAME', 'Finanzas Personales')
    APP_VERSION = os.getenv('APP_VERSION', '0.1.0')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Rutas
    BASE_DIR = BASE_DIR
    DATA_DIR = get_data_directory()
    DB_PATH = DATA_DIR / 'finanzas.db'
    PHOTOS_DIR = Path(os.getenv('PHOTOS_DIR', DATA_DIR / 'photos'))
    EXPORT_DIR = Path(os.getenv('EXPORT_DIR', DATA_DIR / 'exports'))
    ASSETS_DIR = BASE_DIR / 'assets'
    ICONS_DIR = ASSETS_DIR / 'icons'
    
    # Configuración de fotos
    MAX_PHOTO_SIZE_MB = int(os.getenv('MAX_PHOTO_SIZE_MB', '5'))
    ALLOWED_PHOTO_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp'}
    
    # Configuración de UI
    WINDOW_TITLE = f'{APP_NAME} v{APP_VERSION}'
    DEFAULT_WINDOW_SIZE = (1200, 800)
    MIN_WINDOW_SIZE = (900, 600)
    
    @classmethod
    def ensure_directories(cls):
        """Crea los directorios necesarios si no existen."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        cls.EXPORT_DIR.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_icon_path(cls, icon_name):
        """Obtiene la ruta a un icono."""
        # Primero buscar en assets/icons
        icon_path = cls.ICONS_DIR / icon_name
        if icon_path.exists():
            return str(icon_path)
        
        # Luego buscar con extensiones comunes
        for ext in ['.png', '.ico', '.icns']:
            icon_path = cls.ICONS_DIR / f'{icon_name}{ext}'
            if icon_path.exists():
                return str(icon_path)
        
        return None


# Asegurar que los directorios existan al importar
Config.ensure_directories()
