# Nuevas funcionalidades

Este documento resume las mejoras funcionales y de experiencia de usuario que se incorporaron en la etapa reciente del proyecto.

## Datos demo

Se incluye un generador de datos de ejemplo para poblar la aplicacion sin carga manual.

Comando:

```bash
python src/infrastructure/db/seeds_demo.py
```

Lo que genera:

- 5 personas con datos base realistas.
- Decenas de movimientos distribuidos entre ingresos y gastos.
- Categorias variadas para alimentar reportes y graficos.
- Escenarios utiles para probar busquedas, resumenes y alertas.

## Captura de foto

La ficha de persona contempla flujo de imagen para trabajar con fotografia del perfil:

- carga desde archivo;
- soporte para webcam cuando OpenCV esta disponible;
- guardado organizado dentro de `assets/photos/`.

## Mejoras de resumen financiero

La pestana de resumen se reforzo para ofrecer informacion mas util:

- metricas agregadas;
- comparativas mensuales;
- top de gastos por categoria;
- area de alertas y recomendaciones;
- soporte de scroll cuando el contenido supera el alto visible.

## Ajustes de UX/UI

Se hicieron mejoras de densidad visual y legibilidad:

- botones con mejor padding;
- margenes mas consistentes;
- barra superior y panel lateral mas comodos;
- formularios y bloques informativos con mejor separacion;
- mensajes de menu con contexto cuando una accion aun no tiene flujo completo.

## Scripts y soporte

La raiz del repositorio se limpio y las utilidades auxiliares quedaron agrupadas en `tools/`:

- `python tools/diagnostico.py`
- `python tools/setup_installer.py build`

Esto deja el proyecto mas claro para mantenimiento y mas presentable para GitHub.

## Archivos involucrados

```text
src/infrastructure/db/seeds_demo.py
src/infrastructure/camera/camera_capture.py
src/presentation/views/person_detail_view.py
src/presentation/views/main_window.py
tools/diagnostico.py
tools/setup_installer.py
```
