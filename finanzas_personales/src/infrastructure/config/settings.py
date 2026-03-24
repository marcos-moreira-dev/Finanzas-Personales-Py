"""Configuracion central de la aplicacion."""

import os
import sys
from pathlib import Path


try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")


def get_data_directory() -> Path:
    """Devuelve el directorio de datos local segun la plataforma."""
    custom_path = os.getenv("DB_PATH")
    if custom_path:
        return Path(custom_path).parent

    if IS_WINDOWS:
        app_data = Path(os.environ.get("APPDATA", Path.home() / "AppData/Roaming"))
        return app_data / "FinanzasPersonales"

    if IS_MACOS:
        return Path.home() / "Library/Application Support/FinanzasPersonales"

    xdg_data = os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
    return Path(xdg_data) / "finanzas_personales"


class Config:
    """Parametros y rutas compartidas por toda la aplicacion."""

    APP_NAME = os.getenv("APP_NAME", "Finanzas Personales")
    APP_VERSION = os.getenv("APP_VERSION", "0.2.0")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    BASE_DIR = BASE_DIR
    DATA_DIR = get_data_directory()
    DB_PATH = DATA_DIR / "finanzas.db"
    PHOTOS_DIR = Path(os.getenv("PHOTOS_DIR", DATA_DIR / "photos"))
    EXPORT_DIR = Path(os.getenv("EXPORT_DIR", DATA_DIR / "exports"))

    ASSETS_DIR = BASE_DIR / "assets"
    ICONS_DIR = ASSETS_DIR / "icons"
    UI_DIR = ASSETS_DIR / "ui"
    LOGO_PATH = UI_DIR / "logo.png"
    APP_ICON_ICO_PATH = ICONS_DIR / "app_icon.ico"
    APP_ICON_PNG_PATH = ICONS_DIR / "app_icon.png"
    APP_ICON_ICNS_PATH = ICONS_DIR / "app_icon.icns"

    MAX_PHOTO_SIZE_MB = int(os.getenv("MAX_PHOTO_SIZE_MB", "5"))
    ALLOWED_PHOTO_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp"}

    WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"
    DEFAULT_WINDOW_SIZE = (1200, 800)
    MIN_WINDOW_SIZE = (900, 600)

    @classmethod
    def ensure_directories(cls) -> None:
        """Crea los directorios de datos de la aplicacion si faltan."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.PHOTOS_DIR.mkdir(parents=True, exist_ok=True)
        cls.EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def get_icon_path(cls, icon_name: str) -> str | None:
        """Busca un icono dentro de `assets/icons` con extensiones comunes."""
        direct_path = cls.ICONS_DIR / icon_name
        if direct_path.exists():
            return str(direct_path)

        for extension in (".png", ".ico", ".icns", ".svg"):
            icon_path = cls.ICONS_DIR / f"{icon_name}{extension}"
            if icon_path.exists():
                return str(icon_path)

        return None


Config.ensure_directories()
