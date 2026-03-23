"""
Script auxiliar para empaquetar la aplicacion.

Se mueve a `tools/` para que la raiz del repositorio quede enfocada en el
uso diario (`run.py`, `run.bat`, `run.sh`) y la documentacion publica.

Uso:
    python tools/setup_installer.py build
    python tools/setup_installer.py bdist_msi
    python tools/setup_installer.py bdist_dmg
"""

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

IS_WINDOWS = sys.platform == "win32"
IS_MACOS = sys.platform == "darwin"
IS_LINUX = sys.platform.startswith("linux")

INCLUDE_FILES = [
    (str(PROJECT_ROOT / "src"), "src"),
    (str(PROJECT_ROOT / "assets"), "assets"),
    (str(PROJECT_ROOT / "docs"), "docs"),
    (str(PROJECT_ROOT / "README.md"), "README.md"),
]

INCLUDES = [
    "wx",
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


def build_executables():
    """Devuelve opciones y ejecutables segun el sistema operativo."""
    if IS_WINDOWS:
        icon_path = PROJECT_ROOT / "assets/icons/app_icon.ico"
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
                script=str(PROJECT_ROOT / "src/main.py"),
                base="Win32GUI",
                target_name="FinanzasPersonales.exe",
                icon=str(icon_path) if icon_path.exists() else None,
                shortcut_name="Finanzas Personales",
                shortcut_dir="StartMenuFolder",
                manifest=(
                    str(PROJECT_ROOT / "src/shared/app_manifest.manifest")
                    if (PROJECT_ROOT / "src/shared/app_manifest.manifest").exists()
                    else None
                ),
            )
        ]
        return options, executables

    if IS_MACOS:
        icon_path = PROJECT_ROOT / "assets/icons/app_icon.icns"
        options = {
            "build_exe": BUILD_OPTIONS,
            "bdist_mac": {
                "bundle_name": "Finanzas Personales",
                "iconfile": str(icon_path) if icon_path.exists() else None,
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
                script=str(PROJECT_ROOT / "src/main.py"),
                target_name="FinanzasPersonales",
                icon=str(icon_path) if icon_path.exists() else None,
            )
        ]
        return options, executables

    if IS_LINUX:
        icon_path = PROJECT_ROOT / "assets/icons/app_icon.png"
        options = {"build_exe": BUILD_OPTIONS}
        executables = [
            Executable(
                script=str(PROJECT_ROOT / "src/main.py"),
                target_name="finanzas-personales",
                icon=str(icon_path) if icon_path.exists() else None,
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
