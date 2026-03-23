# Plan de Implementación - Mejoras Visuales

**Fecha:** 2026-03-21
**Estado:** Implementado
**Diagnóstico previo:** [DIAGNOSTICO_VISUAL.md](./DIAGNOSTICO_VISUAL.md)

---

## Resumen de Cambios

Se aplicaron correcciones quirúrgicas para mejorar nitidez y presentación visual de la aplicación en Windows, sin reescritura de la arquitectura ni tocar lógica de negocio.

---

## Archivos Nuevos

### `src/shared/platform_config.py`

**Propósito:** Módulo centralizado de configuración de plataforma y DPI.

**Qué hace:**

- `configure_platform()` - Habilita DPI awareness en Windows vía ctypes (Per-Monitor DPI Aware)
- `configure_wx_app(app)` - Configura fuente base Segoe UI después de crear wx.App
- `get_dpi_scale()` - Retorna el factor de escala actual (1.25 = 125%)
- `scaled(value)` - Escala un valor en píxeles según DPI actual

**Por qué:** Sin DPI awareness, Windows bitmap-scalea toda la ventana causando borrosidad. Sin fuente base explícita, los controles usan MS Shell Dlg (heredada).

### `src/shared/app_manifest.py`

**Propósito:** Generador y aplicador de manifest Windows.

**Qué hace:**

- `apply_windows_manifest()` - Activa el manifest vía Activation Context API
- Declara Common Controls v6 para visual styles modernos
- Declara DPI Awareness (Per-Monitor v2/v1)

**Por qué:** Sin Common Controls v6, Windows usa controles Win32 clásicos (planos, con bordes 3D gruesos). El manifest es el estándar de Microsoft para esto.

### `src/shared/app_manifest.manifest`

**Propósito:** Archivo de manifest físico para cx_Freeze.

**Por qué:** cx_Freeze puede embeber este archivo directamente en el .exe, así el ejecutable compilado también tiene visual styles y DPI awareness sin depender del runtime de Python.

### `src/shared/matplotlib_config.py`

**Propósito:** Configuración centralizada de matplotlib.

**Qué hace:**

- `configure_matplotlib()` - Ajusta rcParams globales:
  - dpi: 80 → 100
  - Fuente: Segoe UI / DejaVu Sans según plataforma
  - Antialiasing activado
  - Paleta de colores moderna (Tableau-like)
  - Fondo, grid, ticks y leyenda más limpios

**Por qué:** dpi=80 era el estándar de hace 20 años. Los gráficos se renderizaban a baja resolución y se escalaban, causando blur.

---

## Archivos Modificados

### `src/shared/design_tokens.py`

**Cambios:**

- `FONTS.family_windows`: `'Tahoma'` → `'Segoe UI'`
- `FONTS.family_mac`: `'Lucida Grande'` → `'Helvetica Neue'`
- `FONTS.size_normal`: 9 → 10
- `FONTS.size_small`: 8 → 9
- `FONTS.size_table`: 9 → 10
- `FONTS.size_monospace`: 9 → 10
- `DIMENSIONS.button_height`: 24 → 28
- `DIMENSIONS.button_min_width`: 80 → 84
- `DIMENSIONS.toolbar_height`: 36 → 38
- `DIMENSIONS.menubar_height`: 24 → 26
- `DIMENSIONS.statusbar_height`: 24 → 26
- `DIMENSIONS.tabbar_height`: 28 → 30
- `DIMENSIONS.input_height`: 22 → 26
- `DIMENSIONS.dropdown_height`: 24 → 28
- `DIMENSIONS.table_row_height`: 24 → 26
- `DIMENSIONS.table_header_height`: 28 → 30
- `DIMENSIONS.list_item_height`: 28 → 30

**Por qué:** Los tamaños originales (9pt fuente, 22px input) asumían 96 DPI puro. En monitores modernos con 125-150% escalado, se leían como 7px reales. Los nuevos tamaños son más cómodos sin cambiar el layout.

### `src/main.py`

**Cambios:**

- Imports nuevos: `configure_platform`, `configure_wx_app`, `configure_matplotlib`
- En `create_wx_app()`:
  1. `configure_platform()` - ANTES de wx.App (DPI awareness + Common Controls v6)
  2. `wx.App(False)` - creación de la app
  3. `configure_wx_app(app)` - DESPUÉS de wx.App (fuente base)
  4. `configure_matplotlib()` - configura gráficos

**Nota:** Se eliminó `apply_windows_manifest()` del bootstrap porque `ActivateActCtx` interfiere con la inicialización interna de wxPython causando un deadlock. `configure_platform()` ya cubre DPI awareness (shcore/user32) y Common Controls v6 (InitCommonControlsEx) de forma segura. El archivo `.manifest` sigue siendo útil para cx_Freeze (se embebe en el .exe).

### `tools/setup_installer.py`

**Cambios:**

- Añadido `manifest="src/shared/app_manifest.manifest"` al `Executable()` de Windows

**Por qué:** El ejecutable compilado debe tener el manifest embebido para que DPI awareness y visual styles funcionen sin depender del Python runtime.

---

## Qué Mejora y Qué No

### Resuelto

1. **DPI awareness** - La app ahora declara Per-Monitor DPI Aware, Windows no bitmap-scalea la ventana. Texto y controles se renderizan a la resolución correcta.
2. **Visual styles** - Common Controls v6 activa el tema moderno de Windows. Botones, inputs, pestañas y scrollbars se ven con el estilo nativo actual.
3. **Nitidez de matplotlib** - dpi=100 + antialiasing + fuentes del sistema. Los gráficos se renderizan a mayor resolución.
4. **Legibilidad** - Fuente Segoe UI 10pt en lugar de MS Shell Dlg 9pt. Controles con más espacio vertical.

### Limitaciones que persisten (propias de wxPython/wxWidgets)

- **No es GPU-renderizado** - wxPython usa controles nativos del OS, no un scene graph como JavaFX. No puede igualar la fluidez de animaciones o transiciones.
- **Controles nativos = look nativo** - Los controles se ven como Windows, no como una UI web o mobile. Es una decisión arquitectónica, no un bug.
- **StaticBox tiene bordes** - Incluso con visual styles, `wx.StaticBox` tiene un borde visible alrededor del grupo. Es el comportamiento nativo.
- **ListCtrl es básico** - `wx.ListCtrl` no soporta CSS ni estilos avanzados. Para una apariencia más rica se necesitaría `wx.dataview.DataViewCtrl` o custom drawing (no recomendado por ahora).

---

## Cómo Verificar

```bash
# 1. Verificar imports
python -c "from src.shared.platform_config import configure_platform; print('OK')"

# 2. Verificar DPI awareness
python -c "
from src.shared.platform_config import configure_platform, get_dpi_scale
configure_platform()
print(f'DPI Scale: {get_dpi_scale()}')
"
# Debería mostrar "DPI awareness: Per-Monitor DPI Aware v1" y un factor de escala

# 3. Verificar matplotlib
python -c "
from src.shared.matplotlib_config import configure_matplotlib
configure_matplotlib()
import matplotlib; print(f'DPI={matplotlib.rcParams[\"figure.dpi\"]}')
"
# Debería mostrar DPI=100

# 4. Ejecutar la app completa
python src/main.py
# - Texto más nítido
# - Controles con apariencia moderna de Windows (no clásicos)
# - Gráficos más limpios
```

---

## Nota sobre Emapaquetado (cx_Freeze)

El manifest físico (`src/shared/app_manifest.manifest`) está listo para que cx_Freeze lo embeba en el .exe. Ya se añadió la referencia en `tools/setup_installer.py`.

Para generar el ejecutable:

```bash
pip install cx_Freeze
python tools/setup_installer.py build
```

El ejecutable resultante tendrá DPI awareness y visual styles embebidos.
