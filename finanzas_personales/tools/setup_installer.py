"""Empaqueta la aplicacion de escritorio con cx_Freeze."""

import subprocess
import sys
from pathlib import Path


try:
    from cx_Freeze import Executable, setup
except ImportError:
    print("ERROR: cx_Freeze no esta instalado")
    print("Instalalo con: pip install cx_Freeze")
    sys.exit(1)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
VERSION = "0.2.0"
sys.path.insert(0, str(PROJECT_ROOT))

IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

LOGO_PATH = PROJECT_ROOT / "assets" / "ui" / "logo.png"
ICON_PNG_PATH = PROJECT_ROOT / "assets" / "icons" / "app_icon.png"
ICON_ICO_PATH = PROJECT_ROOT / "assets" / "icons" / "app_icon.ico"
ICON_ICNS_PATH = PROJECT_ROOT / "assets" / "icons" / "app_icon.icns"
MANIFEST_PATH = PROJECT_ROOT / "src" / "shared" / "app_manifest.manifest"

INCLUDE_FILES = [
    (str(PROJECT_ROOT / "src"), "src"),
    (str(PROJECT_ROOT / "assets"), "assets"),
    (str(PROJECT_ROOT / "docs"), "docs"),
    (str(PROJECT_ROOT / "README.md"), "README.md"),
    (str(PROJECT_ROOT / "LICENSE"), "LICENSE"),
]

INCLUDES = [
    "wx",
    "wx.adv",
    "matplotlib",
    "matplotlib.backends.backend_wxagg",
    "numpy",
    "cv2",
    "PIL",
    "sqlite3",
]

EXCLUDES = [
    "tkinter",
    "unittest",
    "email",
    "http",
    "xml",
    "pydoc",
    "pdb",
    "pytest",
]

BUILD_OPTIONS = {
    "packages": ["src"],
    "excludes": EXCLUDES,
    "includes": INCLUDES,
    "include_files": INCLUDE_FILES,
    "optimize": 2,
    "build_exe": f"build/FinanzasPersonales-{sys.platform}",
    "include_msvcr": IS_WINDOWS,
}


def ensure_brand_assets() -> None:
    """Genera iconos derivados del logo principal si aun no existen."""
    if not LOGO_PATH.exists():
        print(f"[WARN] No se encontro el logo base en: {LOGO_PATH}")
        return

    if ICON_PNG_PATH.exists() and ICON_ICO_PATH.exists():
        return

    generator_script = PROJECT_ROOT / "tools" / "generate_brand_assets.py"
    result = subprocess.run([sys.executable, str(generator_script)], cwd=PROJECT_ROOT)
    if result.returncode != 0:
        raise RuntimeError("No se pudieron generar los iconos de marca para el instalador.")


def pick_first_existing(*paths: Path) -> str | None:
    """Devuelve la primera ruta existente de la lista."""
    for path in paths:
        if path.exists():
            return str(path)
    return None


def build_executables():
    """Devuelve opciones y ejecutables segun el sistema operativo."""
    ensure_brand_assets()

    if IS_WINDOWS:
        windows_icon = pick_first_existing(ICON_ICO_PATH, ICON_PNG_PATH, LOGO_PATH)
        options = {
            "build_exe": BUILD_OPTIONS,
            "bdist_msi": {
                "upgrade_code": "{12345678-1234-1234-1234-123456789012}",
                "add_to_path": False,
                "initial_target_dir": r"[LocalAppDataFolder]\FinanzasPersonales",
            },
        }
        executables = [
            Executable(
                script=str(PROJECT_ROOT / "src" / "main.py"),
                base="Win32GUI",
                target_name="FinanzasPersonales.exe",
                icon=windows_icon,
                shortcut_name="Finanzas Personales",
                shortcut_dir="StartMenuFolder",
                manifest=str(MANIFEST_PATH) if MANIFEST_PATH.exists() else None,
            )
        ]
        return options, executables

    if IS_MACOS:
        mac_icon = pick_first_existing(ICON_ICNS_PATH, ICON_PNG_PATH, LOGO_PATH)
        options = {
            "build_exe": BUILD_OPTIONS,
            "bdist_mac": {
                "bundle_name": "Finanzas Personales",
                "iconfile": mac_icon,
                "plist_items": [
                    ("CFBundleIdentifier", "com.finanzaspersonales.desktop"),
                    ("CFBundleShortVersionString", VERSION),
                    ("CFBundleVersion", VERSION),
                    ("NSHumanReadableCopyright", "Copyright 2026 Finanzas Personales contributors"),
                ],
            },
            "bdist_dmg": {
                "volume_label": "Finanzas Personales",
                "applications_shortcut": True,
            },
        }
        executables = [
            Executable(
                script=str(PROJECT_ROOT / "src" / "main.py"),
                target_name="FinanzasPersonales",
                icon=mac_icon,
            )
        ]
        return options, executables

    if IS_LINUX:
        linux_icon = pick_first_existing(ICON_PNG_PATH, LOGO_PATH)
        options = {"build_exe": BUILD_OPTIONS}
        executables = [
            Executable(
                script=str(PROJECT_ROOT / "src" / "main.py"),
                target_name="finanzas-personales",
                icon=linux_icon,
            )
        ]
        return options, executables

    raise RuntimeError(f"Sistema operativo no soportado: {sys.platform}")


SETUP_OPTIONS, EXECUTABLES = build_executables()

setup(
    name="Finanzas Personales",
    version=VERSION,
    description="Aplicacion de escritorio offline para gestionar finanzas personales",
    author="Finanzas Personales contributors",
    options=SETUP_OPTIONS,
    executables=EXECUTABLES,
)
