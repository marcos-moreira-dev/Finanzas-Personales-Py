# Modelo de Datos

## Diagrama Entidad-Relación

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│  persona    │       │  movimiento  │       │  categoria  │
├─────────────┤       ├──────────────┤       ├─────────────┤
│ id          │──┐    │ id           │   ┌───│ id          │
│ nombres     │  │    │ persona_id   │◄──┘   │ nombre      │
│ apellidos   │  │    │ fecha        │       │ tipo         │
│ identificacion│ │    │ tipo         │       │ color       │
│ telefono    │  │    │ categoria_id │◄──────│ activa      │
│ correo      │  │    │ monto        │       │ descripcion │
│ fecha_registro│ │    │ descripcion  │       └─────────────┘
│ observaciones│ │    │ medio        │
│ foto_path   │  │    │ referencia   │
└─────────────┘  │    └──────────────┘
                 │
                 │    ┌──────────────┐
                 └──► │    foto      │
                      ├──────────────┤
                      │ id           │
                      │ persona_id   │
                      │ ruta         │
                      │ fecha_carga  │
                      └──────────────┘
```

## Tablas

### persona

| Campo          | Tipo                | Descripción              |
| -------------- | ------------------- | ------------------------ |
| id             | INTEGER PRIMARY KEY | Identificador único      |
| nombres        | TEXT NOT NULL       | Nombres de la persona    |
| apellidos      | TEXT NOT NULL       | Apellidos de la persona  |
| identificacion | TEXT UNIQUE         | Identificación opcional  |
| telefono       | TEXT                | Teléfono de contacto     |
| correo         | TEXT                | Correo electrónico       |
| fecha_registro | DATE                | Fecha de registro        |
| observaciones  | TEXT                | Notas adicionales        |
| foto_path      | TEXT                | Ruta a la foto de perfil |

### movimiento

| Campo        | Tipo                | Descripción                                   |
| ------------ | ------------------- | --------------------------------------------- |
| id           | INTEGER PRIMARY KEY | Identificador único                           |
| persona_id   | INTEGER FK          | Referencia a persona                          |
| fecha        | DATE NOT NULL       | Fecha del movimiento                          |
| tipo         | TEXT NOT NULL       | 'INGRESO' o 'GASTO'                           |
| categoria_id | INTEGER FK          | Referencia a categoría                        |
| monto        | REAL NOT NULL       | Monto positivo                                |
| descripcion  | TEXT                | Descripción del movimiento                    |
| medio        | TEXT                | Medio de pago (efectivo, transferencia, etc.) |
| referencia   | TEXT                | Referencia externa                            |

### categoria

| Campo       | Tipo                | Descripción                            |
| ----------- | ------------------- | -------------------------------------- |
| id          | INTEGER PRIMARY KEY | Identificador único                    |
| nombre      | TEXT NOT NULL       | Nombre de la categoría                 |
| tipo        | TEXT NOT NULL       | 'INGRESO', 'GASTO' o 'AMBOS'           |
| color       | TEXT                | Código de color para gráficos          |
| activa      | BOOLEAN             | Si está activa para nuevos movimientos |
| descripcion | TEXT                | Descripción de la categoría            |

## Índices

- `idx_movimiento_persona`: persona_id en movimiento
- `idx_movimiento_fecha`: fecha en movimiento
- `idx_movimiento_categoria`: categoria_id en movimiento
- `idx_persona_nombre`: nombres + apellidos en persona

## Restricciones

- El monto de un movimiento debe ser siempre positivo
- El tipo determina si suma o resta al saldo
- Una categoría inactiva no puede usarse en nuevos movimientos
- Un movimiento siempre debe estar asociado a una persona válida
