# Diagnóstico Visual - Finanzas Personales

**Fecha:** 2026-03-21
**Alcance:** Auditoría técnica de presentación visual en Windows (DPI, nitidez, controles, matplotlib)

---

## 1. Síntomas Observados

1. La interfaz se percibe borrosa en monitores con DPI escalado (125%, 150%)
2. Botones, inputs y listas tienen apariencia clásica/antigua de Windows
3. Los gráficos de matplotlib se ven menos nítidos de lo esperado
4. Comparado con JavaFX, la UI se percibe más tosca

---

## 2. Causas Identificadas (ordenadas por prioridad)

### Causa 1: Sin DPI Awareness [CRÍTICA]

**Evidencia:**

- `src/main.py` crea `wx.App(False)` sin ningún pre-procesamiento de DPI
- No existe ningún call a `ctypes.windll.shcore.SetProcessDpiAwareness()` en todo el proyecto
- No existe archivo `.manifest` en el proyecto
- La única DPI awareness es interna al backend de matplotlib (no afecta a la app)

**Impacto:** En monitores con escalado >100%, Windows bitmap-scalea toda la ventana. Resultado: texto borroso, controles pixelados, gráficos suavizados artificialmente.

### Causa 2: Sin Visual Styles (Common Controls v6) [CRÍTICA]

**Evidencia:**

- No existe archivo `.manifest` que declare `<dependency>` de Common Controls v6
- `tools/setup_installer.py` (cx_Freeze) no incluye manifest
- `wx.StaticBox` se usa en 8 ubicaciones, `BORDER_SUNKEN` en 3, `SP_3DBORDER` en 1

**Impacto:** Sin el manifest, Windows usa los controles Win32 clásicos (tema "Windows Classic"), no el tema visual moderno de Windows. Botones, inputs, pestañas y barras de scroll se ven planos y con bordes 3D gruesos.

### Causa 3: Fuente por Defecto Inconsistente [MEDIA]

**Evidencia:**

- `design_tokens.py` define `family_windows: 'Tahoma'` pero la mayoría de vistas usan `wx.Font(8, wx.FONTFAMILY_DEFAULT, ...)` que en Windows resuelve a `MS Shell Dlg` (el font del sistema heredado)
- Tamaños de fuente bajos: `size_normal: 9`, `size_small: 8`
- No hay `wx.Font` base configurada a nivel de app

**Impacto:** Fuentes inconsistentes entre controles. En DPI alto, tamaño 9pt se lee como ~7px reales, muy pequeño para lectura cómoda.

### Causa 4: Tamaños de Control Pequeños [MEDIA]

**Evidencia:**

- `design_tokens.py`: `button_height: 24`, `input_height: 22`, `table_row_height: 24`
- En código: botones hardcodeados a `size=(90, 26)`, inputs sin altura mínima
- Estos tamaños asumen 96 DPI (100%)

**Impacto:** En DPI escalado, controles se comprimen visualmente, generando sensación de "apretado" y poco profesional.

### Causa 5: Matplotlib con DPI=80 [MEDIA]

**Evidencia:**

- `person_detail_view.py:411`: `Figure(figsize=(9, 7), dpi=80)`
- Sin configuración global de `rcParams`
- Sin estilo visual definido (usa el default de matplotlib, que es el estilo "ggplot-like" clásico)
- Las fuentes de los gráficos usan tamaños hardcodeados bajos (fontsize=7, 8, 9)

**Impacto:** dpi=80 es la resolución de pantalla estándar de hace 20 años. Monitores modernos tienen 96-144 DPI. Los gráficos se renderizan a resolución baja y luego se escalan, causando suavizado/blur.

### Causa 6: Estilos 3D Obsoletos [MENOR]

**Evidencia:**

- `wx.SP_3DBORDER` en el splitter
- `wx.BORDER_SUNKEN` en ListCtrl y TextCtrl multiline
- Colores hardcoded `border_dark: '#808080'`, `raised/sunken` con bordes 3D

**Impacto:** Contribuye a la sensación de "aplicación de los 2000". Los bordes 3D gruesos no son parte del diseño moderno de Windows.

### Causa 7: Empaquetado sin Manifest [MENOR]

**Evidencia:**

- `tools/setup_installer.py` usa cx_Freeze sin `manifest` parameter en `Executable()`
- Sin `include_msvcr` efectivo para garantizar runtime correcto

**Impacto:** El ejecutable compilado hereda los mismos problemas de DPI y visual styles. Puede verse peor que ejecutando desde .py.

---

## 3. Plan de Cambios Mínimos Recomendados

### Prioridad 1: DPI Awareness (cambio más impactante)

- Crear `src/shared/platform_config.py` con función `configure_dpi_awareness()`
- Llamar ANTES de `wx.App()` en `src/main.py`
- Usar `ctypes` para llamar `SetProcessDpiAwareness(2)` en Windows (Per-Monitor DPI Aware)
- En Linux/macOS: no-op

### Prioridad 2: Visual Styles (Common Controls v6)

- `configure_platform()` ya llama `InitCommonControlsEx` vía ctypes, habilitando controles modernos
- El archivo `.manifest` se mantiene SOLO para cx_Freeze (se embebe en el .exe compilado)
- No se usa `ActivateActCtx` en runtime porque interfiere con la inicialización de wxPython

### Prioridad 3: Fuente Base y Tamaños

- En `src/main.py` o `platform_config.py`, establecer fuente base global de la app
- Ajustar `design_tokens.py` con tamaños más generosos y fuentes modernas
- Usar `wx.Font` con nombre explícito en lugar de `FONTFAMILY_DEFAULT`

### Prioridad 4: Matplotlib Nitidez

- Crear `src/shared/matplotlib_config.py`
- Configurar `rcParams` globales: dpi=100, font.family, antialias, estilos
- Importar en el módulo que usa matplotlib (person_detail_view.py)
- Subir dpi de 80 a 100+ y ajustar figsize

### Prioridad 5: Limpieza de Estilos Obsoletos

- Reemplazar `BORDER_SUNKEN` por `BORDER_THEME` o `BORDER_NONE`
- Reemplazar `SP_3DBORDER` por `SP_LIVE_UPDATE` solo
- Ajustar colores de borde en design_tokens

---

## 4. Riesgos y Trade-offs

| Cambio                   | Riesgo                                            | Mitigación                              |
| ------------------------ | ------------------------------------------------- | --------------------------------------- |
| DPI awareness vía ctypes | Puede fallar si Windows no soporta API            | Try/except con fallback silencioso      |
| Manifest via ctypes      | Complejidad de API Windows                        | Solo se ejecuta en Windows, encapsulado |
| Cambiar fuentes          | Puede romper layout si nueva fuente es más ancha  | Test visual post-cambio                 |
| Subir DPI matplotlib     | Gráficos más grandes, pueden no caber en el panel | Ajustar figsize proporcionalmente       |
| Quitar bordes 3D         | Puede perder distinción visual de contenedores    | Mantener color de fondo distinto        |

---

## 5. Qué NO Hacer

- **NO reescribir la UI completa** - los cambios son quirúrgicos
- **NO crear capa CSS improvisada** - mantener design_tokens como está
- **NO custom-draw controles nativos** - confiar en el theming nativo de Windows
- **NO cambiar lógica de negocio** - todos los cambios son en presentación
- **NO romper multiplataforma** - aíslar código Windows-specific

---

## 6. Limitaciones Propias de wxPython

Honestidad técnica: wxPython (wxWidgets) renderiza controles nativos del OS. Esto significa:

- **Ventaja:** Se adapta al tema del OS automáticamente (si hay visual styles activos)
- **Limitación:** No puede igualar la fluidez de JavaFX (que usa Scene Graph/GPU rendering)
- **Limitación:** Los controles nativos de Windows siempre tendrán un look "Win32", no "fluent/modern"
- **Solución real:** Asegurar que los controles nativos se rendericen con el tema moderno (Common Controls v6 + DPI awareness) y que las dimensiones sean razonables

Con estas correcciones, la app debería verse significativamente más nítida y limpia, aunque no idéntica a una app JavaFX o web moderna. Esa es una limitación arquitectónica de wxWidgets, no un bug.

---

## 7. Archivos que se Modificarán

| Archivo                           | Acción    | Justificación                             |
| --------------------------------- | --------- | ----------------------------------------- |
| `src/shared/platform_config.py`   | NUEVO     | DPI awareness + configuración base        |
| `src/shared/app_manifest.py`      | NUEVO     | Manifest Windows para visual styles + DPI |
| `src/shared/matplotlib_config.py` | NUEVO     | rcParams globales para nitidez            |
| `src/shared/design_tokens.py`     | MODIFICAR | Ajustar tamaños de fuente y controles     |
| `src/main.py`                     | MODIFICAR | Llamar configuración en bootstrap         |
| `tools/setup_installer.py`        | MODIFICAR | Incluir manifest en empaquetado           |
