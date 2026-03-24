# Construccion del instalador

Esta guia resume el flujo recomendado para generar el instalador de `Finanzas Personales` con el branding actual del producto.

## Que hace el flujo

- toma el logo base desde `assets/ui/logo.png`;
- genera iconos derivados en `assets/icons/`;
- empaqueta la aplicacion con `cx_Freeze`;
- produce un build ejecutable y, en Windows, un instalador MSI.

## Requisitos

- Python 3.12 o compatible.
- Dependencias del proyecto instaladas.
- `cx_Freeze` instalado en el mismo entorno que usas para construir.

## Preparar el entorno

```bash
pip install -r requirements.txt
pip install cx_Freeze
```

## Generar assets de marca

Si cambias `assets/ui/logo.png`, vuelve a generar los iconos derivados:

```bash
python tools/generate_brand_assets.py
```

El script crea:

- `assets/icons/app_icon.png`
- `assets/icons/app_icon.ico`
- `assets/icons/app_icon.icns` si Pillow lo soporta en tu entorno

## Construir el instalador

### Build ejecutable

```bash
python tools/setup_installer.py build
```

### MSI en Windows

```bash
python tools/setup_installer.py bdist_msi
```

### Bundle macOS / DMG

```bash
python tools/setup_installer.py bdist_dmg
```

## Resultado esperado

- La aplicacion empaquetada queda bajo `build/`.
- En Windows, `bdist_msi` genera el instalador MSI con icono del producto.
- Los assets de `assets/` y la documentacion base se incluyen en el paquete.

## Notas

- `tools/setup_installer.py` intenta generar los iconos automaticamente si faltan.
- El branding de la ventana y del instalador sale del mismo logo para evitar inconsistencias.
- Si vas a publicar una nueva version, actualiza la version del proyecto antes de construir el MSI final.
