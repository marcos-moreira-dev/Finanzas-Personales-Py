# 🎓 Guía para Principiantes - Conceptos Básicos

## ¿Qué es este proyecto?

Este es un **programa de escritorio** (como Word o Excel) que corre en tu computadora y te ayuda a llevar el control de tus finanzas personales: ingresos, gastos, categorías y resúmenes.

## Conceptos Fundamentales de Software

### ¿Qué es una "Aplicación de Escritorio"?

Imagina la diferencia entre:

- **Aplicación Web**: Como Facebook o Gmail, necesitas internet y un navegador
- **Aplicación de Escritorio**: Como Word o Paint, se instala en tu computadora y funciona sin internet

**Este proyecto es una aplicación de escritorio**, lo que significa:

- Se instala en tu computadora
- Funciona sin conexión a internet
- Tus datos se guardan localmente
- Tiene el aspecto clásico de programas de Windows

### ¿Qué significa "Arquitectura de Software"?

Piensa en construir una casa. No empiezas amontonando ladrillos al azar, ¿verdad? Primero haces planos:

- Dónde van las habitaciones
- Dónde está la cocina
- Cómo llega la electricidad

**La arquitectura de software son esos "planos"** de un programa. Define:

- Cómo se organiza el código
- Qué partes hacen qué cosas
- Cómo se comunican entre sí

### Las 4 Capas de este Proyecto

Este programa está dividido en 4 capas, como pisos de un edificio:

```
┌─────────────────────────────────────┐
│  4. PRESENTACIÓN                    │  ← Lo que ves en pantalla
│  (Ventanas, botones, formularios)   │     (wxPython)
├─────────────────────────────────────┤
│  3. APLICACIÓN                      │  ← La lógica del negocio
│  (Qué hacer y cuándo)               │     (Servicios)
├─────────────────────────────────────┤
│  2. INFRAESTRUCTURA                 │  ← Guardar datos, gráficos
│  (Base de datos, archivos)          │     (SQLite, Matplotlib)
├─────────────────────────────────────┤
│  1. DOMINIO                         │  ← Las reglas del negocio
│  (Personas, Movimientos, Reglas)    │     (Entidades)
└─────────────────────────────────────┘
```

## Conceptos del Dominio (El Negocio)

### ¿Qué es el "Dominio"?

El dominio es **el problema que estamos resolviendo**. En este caso: gestionar finanzas personales.

Imagina que abres un negocio de helados. Tu "dominio" sería:

- Los helados
- Los clientes
- Las ventas
- Los sabores
- Las reglas: "un helado cuesta $2", "hay que cobrar antes de entregar"

En este proyecto, el dominio incluye:

### Entidades Principales

#### 1. Persona 👤

**¿Qué es?** La persona que usa el programa para llevar sus finanzas.

**Datos que guardamos:**

- Nombre y apellido
- Teléfono, correo
- Una foto (opcional)
- Notas u observaciones

**Ejemplo:** Juan Pérez, teléfono 555-1234, correo juan@email.com

#### 2. Movimiento 💰

**¿Qué es?** Cada vez que entra o sale dinero.

**Tipos de movimiento:**

- **INGRESO**: Dinero que recibes (sueldo, venta, regalo)
- **GASTO**: Dinero que gastas (comida, transporte, ropa)

**Ejemplos:**

- "Recibí $1000 de sueldo" → INGRESO
- "Gasté $50 en supermercado" → GASTO

#### 3. Categoría 🏷️

**¿Qué es?** Una etiqueta para clasificar los movimientos.

**Ejemplos:**

- Sueldo
- Alimentación
- Transporte
- Entretenimiento

**Para qué sirve:** Para saber "¿en qué gasto más?", "¿cuánto gano de sueldo vs freelance?"

#### 4. Resumen 📊

**¿Qué es?** Un cálculo que muestra cómo vas financieramente.

**Ejemplos:**

- "Este mes ganaste $2000 y gastaste $1500"
- "Tu saldo total es $5000"
- "Gastas más en comida que en transporte"

## Conceptos de Infraestructura (La Tecnología)

### ¿Qué es la "Infraestructura"?

Es **cómo hacemos que funcione** el dominio. Son los "cables", "tuberías" y "herramientas" que necesitamos.

### Componentes de Infraestructura en este Proyecto

#### 1. Base de Datos SQLite 🗄️

**¿Qué es?** Un archivo en tu computadora donde se guardan todos los datos.

**Análogo:** Como una libreta donde escribes todo, pero digital y organizada.

**¿Por qué SQLite?**

- No necesitas instalar nada extra
- Los datos se guardan en un solo archivo
- Es rápido y confiable
- Funciona sin internet

**Ubicación:** `data/finanzas.db`

#### 2. wxPython 🖼️

**¿Qué es?** La herramienta para crear ventanas, botones y formularios.

**Análogo:** Como los bloques de LEGO para construir la interfaz.

**¿Por qué wxPython?**

- Se ve como un programa nativo de Windows
- Tiene "look clásico" de los años 2005-2010
- Es estable y maduro

#### 3. Matplotlib 📈

**¿Qué es?** La herramienta para hacer gráficos.

**Análogo:** Como una hoja de Excel donde haces gráficos de barras y pastel.

#### 4. Repositorios 📦

**¿Qué es?** Código que se encarga de leer y escribir en la base de datos.

**Análogo:** Como el archivero de una oficina que sabe exactamente dónde guardar y buscar cada documento.

**Patrón Repository:** Es una forma de organizar el código donde:

- Una clase se encarga SOLO de guardar/buscar Personas
- Otra clase SOLO de Movimientos
- Otra SOLO de Categorías

Esto hace que el código sea más organizado y fácil de cambiar.

### ¿Qué es un "Patrón de Diseño"?

Son **soluciones probadas** a problemas comunes. Como recetas de cocina que ya sabemos que funcionan.

#### Patrones usados en este proyecto:

**1. Repository (Repositorio)**

- **Problema:** ¿Cómo guardamos datos sin mezclar código de base de datos con lógica de negocio?
- **Solución:** Crear clases especiales que solo hacen eso: guardar y buscar

**2. Service (Servicio)**

- **Problema:** ¿Dónde ponemos la lógica de negocio? (ej: "calcular saldo")
- **Solución:** Clases que orquestan operaciones y aplican reglas

**3. MVP (Model-View-Presenter)**

- **Problema:** ¿Cómo organizamos la interfaz de usuario?
- **Solución:** Separar en tres partes:
  - **Model:** Los datos
  - **View:** La pantalla (botones, campos)
  - **Presenter:** El intermediario que conecta ambos

**4. Layered Architecture (Arquitectura por Capas)**

- **Problema:** ¿Cómo evitar que todo el código esté mezclado?
- **Solución:** Dividir en capas que solo se comunican con la capa de abajo

## Flujo de Datos (Cómo funciona todo junto)

Cuando haces clic en "Guardar Persona", esto sucede:

```
┌─────────────────────────────────────────────┐
│  1. VISTA (wxPython)                        │
│     Detecta el clic del botón               │
│     ↓                                       │
│  2. PRESENTER                               │
│     Recoge los datos del formulario         │
│     Valida que estén completos              │
│     ↓                                       │
│  3. SERVICIO (Aplicación)                   │
│     Aplica reglas de negocio                │
│     "¿El nombre está vacío?"                │
│     ↓                                       │
│  4. REPOSITORIO (Infraestructura)           │
│     Guarda en SQLite                        │
│     ↓                                       │
│  5. BASE DE DATOS                           │
│     Se guarda en el archivo .db             │
└─────────────────────────────────────────────┘
```

## Estructura de Carpetas Explicada

```
finanzas_personales/
├── src/                          # CÓDIGO FUENTE
│   ├── domain/                   # DOMINIO (reglas del negocio)
│   │   ├── persona.py           # Entidad Persona
│   │   ├── movimiento.py        # Entidad Movimiento
│   │   ├── categoria.py         # Entidad Categoría
│   │   └── resumen.py           # Entidad Resumen
│   │
│   ├── application/              # LÓGICA DE APLICACIÓN
│   │   └── services/            # Servicios que coordinan todo
│   │       ├── persona_service.py
│   │       └── movimiento_service.py
│   │
│   ├── infrastructure/           # INFRAESTRUCTURA (técnico)
│   │   ├── db/                  # Base de datos
│   │   │   ├── database.py      # Conexión SQLite
│   │   │   └── seeds.py         # Datos iniciales
│   │   ├── repositories/        # Acceso a datos
│   │   │   ├── persona_repository.py
│   │   │   ├── movimiento_repository.py
│   │   │   └── categoria_repository.py
│   │   ├── charts/              # Gráficos
│   │   ├── export/              # Exportar CSV
│   │   └── camera/              # Webcam para fotos
│   │
│   └── presentation/             # INTERFAZ DE USUARIO
│       ├── views/               # Ventanas y formularios
│       ├── presenters/          # Lógica de presentación
│       └── viewmodels/          # Datos para la vista
│
├── docs/                         # DOCUMENTACIÓN
├── data/                         # BASE DE DATOS (generado)
├── assets/                       # IMÁGENES Y RECURSOS
└── tests/                        # PRUEBAS AUTOMÁTICAS
```

## Glosario de Términos Técnicos

| Término         | Significado Simple                                      |
| --------------- | ------------------------------------------------------- |
| **Entidad**     | Una "cosa" importante del negocio (Persona, Movimiento) |
| **Repositorio** | Clase que guarda y busca en la base de datos            |
| **Servicio**    | Clase que hace operaciones de negocio                   |
| **DTO**         | Objeto para transferir datos entre capas                |
| **CRUD**        | Crear, Leer, Actualizar, Eliminar (operaciones básicas) |
| **Query**       | Una pregunta a la base de datos                         |
| **Schema**      | La estructura de las tablas en la BD                    |
| **Migración**   | Cambios en la estructura de la BD                       |
| **Seed**        | Datos iniciales que se cargan al crear la BD            |
| **Foreign Key** | Enlace entre tablas (ej: Movimiento → Persona)          |

## ¿Por qué tanta organización?

Imagina que escribes todo el código en un solo archivo de 10,000 líneas:

- ❌ Es difícil encontrar errores
- ❌ Si cambias algo, puede romper otra cosa
- ❌ No puedes reutilizar código
- ❌ Es difícil que otra persona entienda tu código

**Organizando en capas:**

- ✅ Cada cosa tiene su lugar
- ✅ Puedes cambiar la base de datos sin tocar la interfaz
- ✅ Puedes probar partes individuales
- ✅ Es más fácil de entender y mantener

## Próximos Pasos

1. **Lee** `docs/modelo_de_datos.md` - Entiende las tablas de la BD
2. **Lee** `docs/arquitectura.md` - Entiende la estructura técnica
3. **Instala** el programa siguiendo `README.md`
4. **Explora** el código fuente con esta guía a la mano

## ¿Preguntas?

Si no entiendes algo:

1. Busca en este archivo primero
2. Revisa los comentarios en el código
3. Consulta los archivos .md en la carpeta docs/

¡Recuerda: todos empezamos sin saber nada! 🚀
