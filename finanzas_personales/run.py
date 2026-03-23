"""
Lanzador universal del proyecto.

Este script automatiza el arranque local:
1. Verifica que Python este disponible.
2. Crea el entorno virtual del proyecto si hace falta.
3. Instala dependencias si el entorno todavia no esta listo.
4. Inicializa la base de datos SQLite.
5. Ejecuta la aplicacion wxPython.

Se mantiene en la raiz porque es el punto de entrada mas simple para
desarrolladores y para cualquier persona que quiera probar el proyecto.
"""

import platform
import subprocess
import sys
from pathlib import Path


def print_step(step_num, total, message):
    """Imprime un paso con formato uniforme."""
    print(f"\n[{step_num}/{total}] {message}")


def print_ok(message):
    """Imprime un mensaje de exito en ASCII para evitar problemas de consola."""
    print(f"    [OK] {message}")


def print_error(message):
    """Imprime un mensaje de error en ASCII para evitar mojibake."""
    print(f"    [ERROR] {message}")


def check_python():
    """Verifica que Python pueda ejecutarse desde el proceso actual."""
    try:
        result = subprocess.run(
            [sys.executable, "--version"],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except OSError:
        return False


def create_venv():
    """Crea el entorno virtual del proyecto si no existe."""
    venv_path = Path("venv")

    if not venv_path.exists():
        print("    Creando entorno virtual...")
        result = subprocess.run(
            [sys.executable, "-m", "venv", "venv"],
            capture_output=True,
        )
        if result.returncode != 0:
            print_error("No se pudo crear el entorno virtual")
            sys.exit(1)

    print_ok("Entorno virtual listo")


def get_venv_python():
    """Retorna la ruta al ejecutable Python del entorno virtual."""
    if platform.system() == "Windows":
        return str(Path("venv/Scripts/python.exe"))
    return str(Path("venv/bin/python"))


def get_venv_pip():
    """Retorna la ruta al ejecutable pip del entorno virtual."""
    if platform.system() == "Windows":
        return str(Path("venv/Scripts/pip.exe"))
    return str(Path("venv/bin/pip"))


def install_dependencies():
    """Instala dependencias solo si el entorno todavia no puede importar wx."""
    venv_python = get_venv_python()

    # Si wxPython importa bien, asumimos que el entorno principal ya esta preparado.
    result = subprocess.run(
        [venv_python, "-c", "import wx"],
        capture_output=True,
    )

    if result.returncode == 0:
        print_ok("Dependencias ya instaladas")
        return

    print("    Instalando dependencias (puede tardar varios minutos)...")
    pip = get_venv_pip()
    result = subprocess.run(
        [pip, "install", "-r", "requirements.txt"],
        capture_output=False,
    )

    if result.returncode != 0:
        print_error("Fallo la instalacion de dependencias")
        sys.exit(1)

    print_ok("Dependencias instaladas")


def init_database():
    """Inicializa el archivo SQLite y crea el esquema base."""
    venv_python = get_venv_python()

    # Usamos el mismo Python del entorno virtual para que la inicializacion de
    # la BD y la app compartan exactamente las mismas dependencias.
    script = """
import os
import sys

sys.path.insert(0, '.')

from src.infrastructure.config.settings import Config
from src.infrastructure.db.database import Database

os.makedirs(Config.DATA_DIR, exist_ok=True)
db = Database(str(Config.DB_PATH))
db.init_schema()
print("    [OK] Base de datos lista")
"""
    result = subprocess.run(
        [venv_python, "-c", script],
        capture_output=True,
        text=True,
    )

    print(result.stdout, end="")

    if result.returncode != 0:
        print_error("Error inicializando base de datos")
        print(result.stderr)
        sys.exit(1)


def run_app():
    """Ejecuta la interfaz principal."""
    venv_python = get_venv_python()

    print("\n" + "=" * 50)
    print(" INICIANDO APLICACION...")
    print("=" * 50 + "\n")

    try:
        subprocess.run([venv_python, "src/main.py"])
    except KeyboardInterrupt:
        pass

    print("\n" + "=" * 50)
    print(" Aplicacion cerrada")
    print("=" * 50)


def main():
    """Orquesta el arranque local paso a paso."""
    print("=" * 50)
    print(" FINANZAS PERSONALES - LANZADOR AUTOMATICO")
    print("=" * 50)

    print_step(1, 5, "Verificando Python...")
    if not check_python():
        print_error("Python no esta instalado")
        print("    Descarga desde: https://python.org")
        print("    Asegurate de marcar 'Add Python to PATH'")
        input("\nPresiona Enter para salir...")
        sys.exit(1)

    version = sys.version.split()[0]
    print_ok(f"Python {version} detectado")

    # Crear el entorno local del proyecto si todavia no existe.
    print_step(2, 5, "Verificando entorno virtual...")
    create_venv()

    # Instalar librerias solo cuando el entorno aun no esta preparado.
    print_step(3, 5, "Verificando dependencias...")
    install_dependencies()

    # Preparar la base SQLite antes de abrir la interfaz grafica.
    print_step(4, 5, "Inicializando base de datos...")
    init_database()

    print_step(5, 5, "Listo")
    run_app()


if __name__ == "__main__":
    main()
