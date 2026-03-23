# Arquitectura del Proyecto

## Visión General

La aplicación sigue una arquitectura de **monolito modular** organizada en **tres capas principales**:

1. **Capa de Dominio**: Entidades y reglas de negocio
2. **Capa de Aplicación**: Casos de uso y lógica de coordinación
3. **Capa de Infraestructura**: Persistencia y servicios externos
4. **Capa de Presentación**: Interfaz de usuario (MVP - Model View Presenter)

## Patrones Arquitectónicos

### Monolito Modular

- Una sola aplicación ejecutable
- Módulos internos bien separados
- Base de datos local única (SQLite)

### Arquitectura por Capas (3 Capas)

- **Presentación**: UI con wxPython
- **Aplicación/Negocio**: Servicios y casos de uso
- **Persistencia**: Repositorios y base de datos

### MVP (Model-View-Presenter)

- La vista es pasiva (Passive View)
- El Presenter coordina y procesa datos
- Facilita testing de la lógica de UI

### Master-Detail

- Lista de personas (maestro)
- Ficha detallada con pestañas (detalle)
- Navegación clásica de software de escritorio

## Estructura de Paquetes

```
src/
├── app/                    # Bootstrap y configuración
├── domain/                 # Entidades del dominio
│   ├── persona.py
│   ├── movimiento.py
│   └── categoria.py
├── application/            # Casos de uso
│   ├── services/
│   ├── use_cases/
│   └── dto/
├── infrastructure/         # Implementaciones técnicas
│   ├── db/                # Configuración de base de datos
│   ├── repositories/      # Acceso a datos
│   ├── camera/            # Captura de fotos
│   ├── charts/            # Generación de gráficos
│   └── export/            # Exportación de datos
├── presentation/          # Interfaz de usuario
│   ├── presenters/        # Lógica de presentación
│   ├── viewmodels/        # Datos para la vista
│   └── views/             # Componentes UI
└── shared/                # Utilidades comunes
```

## Flujo de Datos

1. El usuario interactúa con la **Vista** (wxPython)
2. La **Vista** notifica al **Presenter**
3. El **Presenter** coordina con **Servicios** de aplicación
4. Los **Servicios** usan **Repositorios** de infraestructura
5. Los **Repositorios** persisten en **SQLite**
6. El flujo inverso devuelve los datos a la vista

## Entidades Principales

### Persona

Representa al titular de la ficha financiera.

### Movimiento

Transacción financiera (ingreso o gasto) asociada a una persona.

### Categoría

Clasificación de movimientos con tipo y color asociado.

## Decisiones Arquitectónicas

1. **SQLite**: Base de datos local, ligera, sin configuración
2. **wxPython**: Look & feel nativo y clásico de escritorio
3. **MVP**: Facilita testing y separa responsabilidades
4. **Sin ORM**: SQL nativo para mayor control y claridad
5. **Monolito**: Simplicidad para aplicación de escritorio personal
