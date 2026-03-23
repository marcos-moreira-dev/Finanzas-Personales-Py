# Finanzas Personales

Aplicacion de escritorio offline para administrar personas, ingresos, gastos y analisis financiero desde una interfaz clasica construida con `wxPython`.

El proyecto esta pensado para dos usos concretos:
- resolver una necesidad real de control financiero local, sin depender de internet;
- servir como base de estudio para arquitectura por capas, MVP, servicios, repositorios y persistencia con SQLite.

## Propuesta de valor

- Funciona de forma local con `SQLite`, sin backend ni servicios externos.
- Tiene interfaz de escritorio tradicional, facil de usar para contextos administrativos.
- Incluye reportes, metricas, graficos y alertas financieras.
- Mantiene una estructura de codigo clara para aprender y seguir refactorizando.
- Se puede ejecutar rapido en Windows, Linux y macOS.

## Funcionalidades principales

- Gestion de personas con datos generales, foto y observaciones.
- Registro de ingresos y gastos por categoria.
- Resumen financiero con indicadores, comparativas y visualizaciones.
- Herramientas auxiliares para datos demo, diagnostico y empaquetado.
- Pruebas automatizadas sobre servicios, repositorios y presenter.

## Inicio rapido

### Windows

```bat
run.bat
```

### Linux / macOS

```bash
./run.sh
```

### Python puro

```bash
python run.py
```

El lanzador crea el entorno virtual si hace falta, instala dependencias, inicializa la base de datos y abre la aplicacion.

## Instalacion manual para desarrollo

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python src/main.py
```

## Datos demo, pruebas y soporte

### Cargar datos de ejemplo

```bash
python src/infrastructure/db/seeds_demo.py
```

### Ejecutar diagnostico local

```bash
python tools/diagnostico.py
```

### Ejecutar pruebas

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

Si instalas dependencias de desarrollo, tambien puedes usar `pytest`.

## Empaquetado

Los scripts de soporte se movieron a `tools/` para mantener la raiz del repositorio limpia:

```bash
python tools/setup_installer.py build
python tools/setup_installer.py bdist_msi
python tools/setup_installer.py bdist_dmg
```

## Arquitectura

El proyecto sigue una separacion por capas:

1. `domain`: entidades y reglas de negocio.
2. `application`: servicios y casos de uso.
3. `infrastructure`: SQLite, repositorios, exportacion y adaptadores.
4. `presentation`: vistas, presenters y coordinacion de la UI.
5. `shared`: configuracion y utilidades transversales.

Esta organizacion facilita el mantenimiento y ayuda a estudiar responsabilidades bien separadas.

## Estructura del repositorio

```text
finanzas_personales/
|-- assets/              # Recursos visuales
|-- data/                # Datos locales vacios en Git
|-- docs/                # Documentacion tecnica y funcional
|-- src/                 # Codigo fuente principal
|   |-- application/
|   |-- domain/
|   |-- infrastructure/
|   |-- presentation/
|   `-- shared/
|-- tests/               # Pruebas automatizadas
|-- tools/               # Scripts de soporte y packaging
|-- run.bat              # Lanzador rapido en Windows
|-- run.py               # Lanzador universal en Python
|-- run.sh               # Lanzador rapido en Linux/macOS
|-- install.sh           # Instalacion orientada a Linux/macOS
|-- pyproject.toml       # Metadata del proyecto
|-- requirements.txt     # Dependencias base
|-- LICENSE
`-- README.md
```

## Documentacion adicional

- [Arquitectura](docs/arquitectura.md)
- [Modelo de datos](docs/modelo_de_datos.md)
- [Guia para principiantes](docs/GUIA_PRINCIPIANTES.md)
- [Instalacion](docs/INSTALACION.md)
- [Auditoria tecnica](docs/AUDITORIA_ACTUALIZADA.md)
- [Diagnostico visual](docs/DIAGNOSTICO_VISUAL.md)

## Estado actual

La raiz del proyecto fue depurada para publicacion: se retiraron scripts redundantes, se separaron utilidades de soporte en `tools/`, se excluyeron artefactos generados del control de versiones y se reforzo la documentacion base para GitHub.

## Licencia

Distribuido bajo licencia [MIT](LICENSE).
