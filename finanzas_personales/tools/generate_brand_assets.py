"""Genera iconos del producto a partir de `assets/ui/logo.png`."""

import sys
from pathlib import Path

from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOGO_PATH = PROJECT_ROOT / "assets" / "ui" / "logo.png"
ICONS_DIR = PROJECT_ROOT / "assets" / "icons"


def build_png(image: Image.Image, destination: Path) -> None:
    """Guarda una version PNG optimizada para el icono de la app."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    icon_image = image.copy().resize((512, 512), Image.Resampling.LANCZOS)
    icon_image.save(destination, format="PNG")


def build_ico(image: Image.Image, destination: Path) -> None:
    """Guarda un icono multi-resolucion para Windows."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    image.save(destination, format="ICO", sizes=sizes)


def build_icns(image: Image.Image, destination: Path) -> None:
    """Intenta generar un icono ICNS para macOS si Pillow lo soporta."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        image.save(destination, format="ICNS")
    except ValueError:
        print("[WARN] Pillow no soporta generar ICNS en este entorno; se omite.")


def main() -> int:
    """Genera los assets derivados del logo principal."""
    if not LOGO_PATH.exists():
        print(f"[ERROR] No se encontro el logo base: {LOGO_PATH}")
        return 1

    image = Image.open(LOGO_PATH).convert("RGBA")
    png_destination = ICONS_DIR / "app_icon.png"
    ico_destination = ICONS_DIR / "app_icon.ico"
    icns_destination = ICONS_DIR / "app_icon.icns"

    build_png(image, png_destination)
    build_ico(image, ico_destination)
    build_icns(image, icns_destination)

    print("[OK] Assets de marca generados")
    print(f"     PNG:  {png_destination}")
    print(f"     ICO:  {ico_destination}")
    if icns_destination.exists():
        print(f"     ICNS: {icns_destination}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
