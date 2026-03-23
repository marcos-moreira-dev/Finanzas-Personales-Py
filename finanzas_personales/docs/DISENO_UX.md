# 🎨 DISEÑO UX - FINANZAS PERSONALES

## Interfaz Clásica de Oficina 2005-2010 con Accesibilidad WCAG 2.1 AA

---

## 📐 SISTEMA DE DISEÑO

### Paleta de Colores (Estilo Clásico Sobrio)

```
COLORES PRINCIPALES:
├── Fondo Ventana:     #F0F0F0 (Gris claro - fondo Windows clásico)
├── Fondo Paneles:     #FFFFFF (Blanco - áreas de contenido)
├── Borde:            #C0C0C0 (Gris medio - bordes 3D)
├── Texto Principal:   #000000 (Negro - máximo contraste)
├── Texto Secundario: #666666 (Gris oscuro)
│
├── PRIMARIO (Acciones):
│   ├── Principal:    #2E5C8A (Azul oscuro corporativo)
│   ├── Hover:        #3D7AB5 (Azul medio)
│   └── Active:       #1E3D5C (Azul muy oscuro)
│
├── ÉXITO (Ingresos):
│   ├── Verde:        #2E7D32 (Verde bosque)
│   └── Fondo:        #E8F5E9 (Verde muy claro)
│
├── ERROR/PÉRDIDA (Gastos):
│   ├── Rojo:         #C62828 (Rojo oscuro)
│   └── Fondo:        #FFEBEE (Rojo muy claro)
│
└── ADVERTENCIA:
    ├── Amarillo:     #F9A825 (Ámbar)
    └── Fondo:        #FFFDE7 (Amarillo claro)
```

**Contraste WCAG 2.1 AA:**

- Texto negro (#000000) sobre fondo blanco: 21:1 ✅ (AAA)
- Texto negro sobre gris claro: 15:1 ✅ (AAA)
- Texto blanco sobre azul (#2E5C8A): 7.2:1 ✅ (AA)
- Texto blanco sobre verde/rojo: >4.5:1 ✅ (AA)

### Tipografía (Sistema Clásico)

```
FUENTE PRINCIPAL: System Default (Según SO)
├── Windows:  Tahoma, 8-9pt
├── Linux:    Sans-serif, 9pt
└── macOS:    Lucida Grande, 11pt

JERARQUÍA:
├── Título Ventana:   14px, Bold
├── Título Panel:     12px, Bold
├── Subtítulo:        11px, Bold
├── Texto Normal:     9-10px, Regular
├── Texto Pequeño:    8px, Regular
└── Datos Tabla:      9px, Regular (Monospace para números)
```

### Espaciado y Dimensiones

```
ESCALA DE ESPACIADO (8px base):
├── xs:  4px   (micro)
├── sm:  8px   (pequeño)
├── md:  16px  (medio)
├── lg:  24px  (grande)
├── xl:  32px  (extra grande)
└── xxl: 48px  (sección)

DIMENSIONES ELEMENTOS:
├── Botón mínimo:     80x24px
├── Input altura:     22px
├── Fila tabla:       24px
├── Panel lateral:    280px (ancho fijo)
├── Toolbar:          32px (alto)
└── Margen interno:   8-12px
```

---

## 🖥️ WIREFRAMES DETALLADOS

### 1. VENTANA PRINCIPAL (Master-Detail)

```
┌────────────────────────────────────────────────────────────────────────────┐
│≡ Archivo  Editar  Ver  Herramientas  Ayuda                          [_][□][×]│
├────────────────────────────────────────────────────────────────────────────┤
│[📝] Nuevo  [💾] Guardar  [🗑️] Eliminar  |  [🔍] Buscar: [____________] [🔎]│
├──────────────────┬─────────────────────────────────────────────────────────┤
│                  │                                                         │
│ 👤 PERSONAS      │  ┌─────────────────────────────────────────────────────┐│
│                  │  │  FICHA: Juan Pérez García                          ││
│ [🔍____________] │  │                                                     ││
│                  │  │ [General] [💰 Movimientos] [📊 Resumen] [⚙️ Más ▼]││
│ ▼ Juan Pérez G.  │  ├─────────────────────────────────────────────────────┤│
│   María López M. │  │                                                     ││
│   Carlos Ruiz S. │  │  [CONTENIDO DE LA PESTAÑA ACTIVA]                  ││
│   Ana Martínez   │  │                                                     ││
│                  │  │                                                     ││
│ [➕ Nueva Persona│  │                                                     ││
│                  │  │                                                     ││
│ Total: 3 personas│  │                                                     ││
│                  │  │                                                     ││
├──────────────────┴─────────────────────────────────────────────────────────┤
│  Listo  |  Persona: Juan Pérez García  |  Saldo: $2,450.00               │
└────────────────────────────────────────────────────────────────────────────┘

ANATOMÍA:
├── Barra de Título: Menú clásico, botones ventana
├── Toolbar: Iconos 16px + tooltips, separadores verticales
├── Panel Izquierdo (280px):
│   ├── Header "PERSONAS" (12px, bold, fondo gris)
│   ├── Buscador con icono
│   ├── Lista scrollable (selección azul #2E5C8A)
│   └── Botón Nueva (ancho completo)
├── Área Principal:
│   ├── Header ficha con nombre
│   ├── Pestañas (estilo clásico, activa con borde inferior)
│   └── Área contenido dinámico
└── Barra Estado: Información contextual, totales
```

### 2. PESTAÑA GENERAL (Datos Persona)

```
┌────────────────────────────────────────────────────────────────┐
│ FICHA: Juan Pérez García                              [✏️ Editar]│
├────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────┐  ┌────────────────────────────┐  │
│  │  👤                     │  │  DATOS PERSONALES          │  │
│  │                         │  │                            │  │
│  │  [Foto de Perfil        │  │  Nombres:    [Juan        ]│  │
│  │   150x150px             │  │                            │  │
│  │   con borde 3D          │  │  Apellidos:  [Pérez García]│  │
│  │   gris]                 │  │                            │  │
│  │                         │  │  Identidad:  [12345678-9  ]│  │
│  │  [📷 Cambiar Foto]      │  │                            │  │
│  │  [🗑️ Eliminar]          │  │  Teléfono:   [5555-0100   ]│  │
│  │                         │  │                            │  │
│  └──────────────────────────┘  │  Correo:     [juan@email.]│  │
│                                │                            │  │
│  ┌────────────────────────────┐│  Fecha Reg:  15/03/2024   │  │
│  │  OBSERVACIONES             ││  (solo lectura)            │  │
│  │                            ││                            │  │
│  │  [                          │└────────────────────────────┘  │
│  │   Área de texto            │                                 │
│  │   multilinea              ]│  ┌─────────────────────────┐   │
│  │                            │  │ [💾 Guardar Cambios]    │   │
│  │  Máx. 500 caracteres       │  │ [❌ Cancelar]           │   │
│  └────────────────────────────┘  └─────────────────────────┘   │
│                                                                 │
└────────────────────────────────────────────────────────────────┘

ESTADOS DE CAMPOS:
├── Normal: Borde gris #C0C0C0, fondo blanco
├── Focus: Borde azul #2E5C8A, outline 2px azul claro
├── Error: Borde rojo #C62828, fondo #FFEBEE
└── Deshabilitado: Fondo #E0E0E0, texto gris

ACCESIBILIDAD:
├── Labels asociados a inputs (for + id)
├── Orden tabular lógico (izq→der, arriba→abajo)
├── Tooltips descriptivos
└── Validación visual inmediata
```

### 3. PESTAÑA MOVIMIENTOS (Con Categorías Visibles)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ FICHA: Juan Pérez García - Movimientos                          [💾] [📊]  │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  FILTRAR POR:                                          [➕ Nuevo Ingreso]  │
│  ┌──────────────┐ ┌──────────────┐ ┌────────────────┐  [➖ Nuevo Gasto]    │
│  │📅 Mes:       │ │📅 Año:       │ │🏷️ Categoría:   │                       │
│  │[Enero ▼]     │ │[2024   ▼]    │ │[Todas    ▼]    │                       │
│  └──────────────┘ └──────────────┘ └────────────────┘                       │
│                                                                             │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  📋 MOVIMIENTOS (12 registros)                                             │
│                                                                             │
│  Fecha     │Tipo    │Categoría          │Descripción      │Monto      │⚙️   │
│  ──────────┼────────┼───────────────────┼─────────────────┼───────────┼─────│
│  15/03/2024│💵 ING │💼 Sueldo          │Salario mensual  │$2,500.00  │[✏️🗑️]│
│  14/03/2024│💸 GAS │🍽️ Alimentación   │Supermercado     │$-150.50   │[✏️🗑️]│
│  10/03/2024│💸 GAS │🚗 Transporte     │Gasolina         │$-50.00    │[✏️🗑️]│
│  05/03/2024│💸 GAS │🏠 Vivienda       │Pago de renta    │$-800.00   │[✏️🗑️]│
│  01/03/2024│💵 ING │💻 Freelance      │Proyecto web     │$500.00    │[✏️🗑️]│
│  ...       │...    │...                │...              │...        │...  │
│                                                                             │
├────────────────────────────────────────────────────────────────────────────┤
│  📊 RESUMEN DEL PERÍODO                                                     │
│  Ingresos: $3,000.00  │  Gastos: $1,000.50  │  Saldo: $1,999.50 [+💚]      │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

CATEGORÍAS CON ICONOS (Seeds visibles):
INGRESOS (💵):
  💼 Sueldo        💻 Freelance      📈 Inversiones    🛒 Ventas
  🎁 Regalos       ↩️ Reembolsos    💰 Otros

GASTOS (💸):
  🍽️ Alimentación  🚗 Transporte     🏠 Vivienda       🏥 Salud
  📚 Educación     🎬 Entretenimiento👕 Ropa           💻 Tecnología
  🐾 Mascotas      ✈️ Viajes          💰 Ahorro         📄 Impuestos
  🛡️ Seguros       📝 Otros

ESTILOS TABLA:
├── Header: Fondo #E0E0E0, texto bold, borde inferior 2px
├── Filas alternadas: Blanco / #F5F5F5 (zebra striping)
├── Selección: Fondo #2E5C8A, texto blanco
├── Ingresos: Texto verde #2E7D32
├── Gastos: Texto rojo #C62828
└── Hover fila: Fondo #E3F2FD (azul muy claro)

ACCESIBILIDAD:
├── Encabezados de columna descriptivos
├── Ordenamiento por click en header
├── Navegación por teclado (↑↓ para moverse)
├── Botones acción con aria-label
└── Contraste número/monto ≥ 4.5:1
```

### 4. PESTAÑA CATEGORÍAS (Gestión de Seeds)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ FICHA: Juan Pérez García - Categorías                         [➕ Nueva]   │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  CATEGORÍAS DE INGRESOS                                    [🔍 Buscar...]  │
│  ═══════════════════════                                                    │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Icono │ Nombre          │Tipo    │Color  │Estado   │Descripción      │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ 💼    │ Sueldo          │INGRESO │🟢 Verde│✅ Activa│Ingresos trabajo │  │
│  │ 💻    │ Freelance       │INGRESO │🟢 Verde│✅ Activa│Trabajos ind.    │  │
│  │ 📈    │ Inversiones     │INGRESO │🟢 Verde│✅ Activa│Dividendos       │  │
│  │ 🛒    │ Ventas          │INGRESO │🟢 Verde│✅ Activa│Venta productos  │  │
│  │ 🎁    │ Regalos         │INGRESO │🔵 Azul │✅ Activa│Dinero recibido  │  │
│  │ ...   │ ...             │...     │...     │...      │...              │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  CATEGORÍAS DE GASTOS                                                       │
│  ═════════════════════                                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Icono │ Nombre          │Tipo    │Color  │Estado   │Descripción      │  │
│  ├──────────────────────────────────────────────────────────────────────┤  │
│  │ 🍽️    │ Alimentación    │GASTO   │🔴 Rojo │✅ Activa│Comida           │  │
│  │ 🚗    │ Transporte      │GASTO   │🟠 Narja│✅ Activa│Gasolina, etc.   │  │
│  │ 🏠    │ Vivienda        │GASTO   │🟤 Café │✅ Activa│Renta, servicios │  │
│  │ 🏥    │ Salud           │GASTO   │🔴 Rojo │✅ Activa│Doctores, med.   │  │
│  │ ⏸️    │ Entretenimiento │GASTO   │🟡 Amar.│⏸️ Inact.│Cine, juegos     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  LEYENDA:                                                                  │
│  ✅ Activa - Disponible para nuevos movimientos                            │
│  ⏸️ Inactiva - Oculta pero conserva historial                              │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

FUNCIONALIDADES:
├── Doble click: Editar categoría
├── Click derecho: Menú contextual (Editar, Activar/Desactivar, Eliminar)
├── Drag & drop: Reordenar (cambiar orden de visualización)
├── Nueva: Crear categoría personalizada
└── Filtro: Buscar por nombre
```

### 5. PESTAÑA RESUMEN (Gráficos y Estadísticas)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ FICHA: Juan Pérez García - Resumen Financiero                 [📄 Exportar] │
├────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │   💰 SALDO       │  │   📈 INGRESOS    │  │   📉 GASTOS      │          │
│  │                  │  │                  │  │                  │          │
│  │   $2,450.00      │  │   $3,500.00      │  │   $1,050.00      │          │
│  │                  │  │                  │  │                  │          │
│  │   ↑ 15% vs mes   │  │   +$500 vs ant.  │  │   -$200 vs ant.  │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                             │
│  ┌────────────────────────────────────┐  ┌──────────────────────────────┐  │
│  │  📊 EVOLUCIÓN MENSUAL              │  │  🥧 DISTRIBUCIÓN GASTOS      │  │
│  │                                    │  │                              │  │
│  │   $3K┤     ┌──┐                   │  │         [GRÁFICO PASTEL]     │  │
│  │       │  ┌─┘  └──┐  ┌──┐          │  │                              │  │
│  │   $2K┤  ┌┘       └──┘  │          │  │   🍽️ Alimentación   35%     │  │
│  │       │─┘              └──┐        │  │   🏠 Vivienda       30%     │  │
│  │   $1K┤                   │        │  │   🚗 Transporte     15%     │  │
│  │       └────┬────┬────┬────┘        │  │   🏥 Salud          10%     │  │
│  │            Ene  Feb  Mar           │  │   📚 Educación       5%     │  │
│  │                                    │  │   📝 Otros           5%     │  │
│  └────────────────────────────────────┘  └──────────────────────────────┘  │
│                                                                             │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │  🏆 CATEGORÍAS MÁS UTILIZADAS (TOP 5)                              │    │
│  ├────────────────────────────────────────────────────────────────────┤    │
│  │  #1 🍽️ Alimentación     $450.00 (43% del total)    ████████████    │    │
│  │  #2 🏠 Vivienda         $350.00 (33% del total)    █████████      │    │
│  │  #3 🚗 Transporte       $150.00 (14% del total)    ████            │    │
│  │  #4 🏥 Salud            $80.00  (8% del total)     ██              │    │
│  │  #5 📝 Otros            $20.50  (2% del total)     █               │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│                                                                             │
└────────────────────────────────────────────────────────────────────────────┘

GRÁFICOS:
├── Barras: Evolución mensual (Ingresos vs Gastos)
├── Pastel: Distribución de gastos por categoría
├── Barras horizontales: Top categorías con porcentaje visual
└── Todos los gráficos con leyendas y tooltips
```

### 6. DIÁLOGO: NUEVO MOVIMIENTO

```
┌─────────────────────────────────────────────────────────────┐
│ 💵 Nuevo Ingreso                                    [×]     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  💰 Monto:              $ [2,500.00                    ]    │
│                          ↑ Campo numérico con formato       │
│                                                             │
│  📅 Fecha:              [15/03/2024 ▼]                      │
│                          (Date picker)                      │
│                                                             │
│  🏷️ Categoría:         [💼 Sueldo                 ▼]        │
│                          (Dropdown con iconos)              │
│                                                             │
│  📝 Descripción:        [Salario mensual marzo...      ]    │
│                                                             │
│  💳 Medio de pago:      [🏦 Transferencia          ▼]        │
│                                                             │
│  #️⃣ Referencia:         [REF-2024-001              ]        │
│                          (Opcional)                         │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │ 💡 PREVISUALIZACIÓN:                                   │  │
│  │                                                        │  │
│  │    Ingreso de $2,500.00 en categoría Sueldo           │  │
│  │    Fecha: 15/03/2024                                  │  │
│  │    Nuevo saldo: $4,950.00                             │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│        [💾 Guardar]    [💾 Guardar y Nuevo]    [❌ Cancelar] │
│                                                             │
└─────────────────────────────────────────────────────────────┘

VALIDACIÓN EN TIEMPO REAL:
├── Monto: > 0, formato moneda
├── Fecha: No futura, válida
├── Categoría: Requerida
├── Descripción: Máx. 200 caracteres
└── Mensaje error inline (rojo) si inválido

ACCESIBILIDAD:
├── Tab order lógico
├── Enter para siguiente campo
├── Escape para cancelar
├── Ctrl+S para guardar
└── Tooltips en cada campo
```

---

## 🎨 COMPONENTES DE UI

### Botones

```
ESTADOS DE BOTÓN:

Primario (Acción principal):
┌────────────────────────┐
│ 💾 Guardar             │  ← Normal: Fondo #2E5C8A, texto blanco
└────────────────────────┘
┌────────────────────────┐
│ 💾 Guardar             │  ← Hover: Fondo #3D7AB5
└────────────────────────┘
┌────────────────────────┐
│ 💾 Guardar             │  ← Active: Fondo #1E3D5C
└────────────────────────┘
┌────────────────────────┐
│ 💾 Guardar             │  ← Focus: Outline azul 2px
└────────────────────────┘
┌────────────────────────┐
│ 💾 Guardar             │  ← Disabled: Fondo gris, texto gris
└────────────────────────┘

Secundario:
┌────────────────────────┐
│ ❌ Cancelar            │  ← Normal: Fondo #E0E0E0, texto negro
└────────────────────────┘
```

### Inputs y Formularios

```
ESTADOS DE INPUT:

Normal:
┌────────────────────────┐
│ Nombre                 │
└────────────────────────┘
  ↑ Label arriba del campo

Focus:
┌────────────────────────┐
│ Juan                   │
└────────────────────────┘
  ↑ Borde azul #2E5C8A
  ↑ Outline 2px azul claro

Error:
┌────────────────────────┐
│                        │
└────────────────────────┘
  ↑ Borde rojo #C62828
  ↑ Fondo #FFEBEE
  ⚠️ El nombre es obligatorio

Deshabilitado:
┌────────────────────────┐
│ Juan Pérez             │
└────────────────────────┘
  ↑ Fondo gris #E0E0E0
  ↑ Texto gris #666666
```

### Dropdowns (Combos)

```
CATEGORÍA:
┌──────────────────────────┐▼│
│ 🏷️ Seleccionar...          │
└──────────────────────────┘─┘

ABIERTO:
┌──────────────────────────┐
│ 🏷️ Seleccionar...        │
├──────────────────────────┤
│ 💼 Sueldo                │
│ 💻 Freelance             │
│ 📈 Inversiones           │
│ 🛒 Ventas                │
│ ─────────────────────────│
│ 🍽️ Alimentación          │
│ 🚗 Transporte            │
│ 🏠 Vivienda              │
└──────────────────────────┘
```

---

## ♿ ACCESIBILIDAD WCAG 2.1 AA

### Navegación por Teclado

```
SECUENCIA DE TABULACIÓN:

1. Menú superior (Alt+F, Alt+E, etc.)
2. Toolbar (botones izq→der)
3. Panel lateral:
   3.1 Buscador
   3.2 Lista personas (↑↓ navegar, Enter seleccionar)
   3.3 Botón Nueva
4. Área principal:
   4.1 Pestañas (←→ cambiar)
   4.2 Contenido pestaña activa
5. Barra estado (solo lectura)

ATAJOS DE TECLADO:
├── Ctrl+N: Nueva persona
├── Ctrl+S: Guardar
├── Ctrl+F: Buscar
├── F1: Ayuda
├── Escape: Cancelar/Cerrar diálogo
├── Enter: Aceptar/Guardar
├── Ctrl+Tab: Siguiente pestaña
├── Ctrl+Shift+Tab: Pestaña anterior
└── Alt+F4: Salir
```

### Atributos ARIA

```html
<!-- Menú superior -->
<nav role="navigation" aria-label="Menú principal">
  <button role="menuitem" aria-haspopup="true">Archivo</button>
</nav>

<!-- Panel de personas -->
<section aria-label="Listado de personas">
  <input type="search" aria-label="Buscar persona" />
  <ul role="listbox" aria-label="Personas">
    <li role="option" aria-selected="true">Juan Pérez</li>
  </ul>
</section>

<!-- Pestañas -->
<div role="tablist" aria-label="Secciones de ficha">
  <button role="tab" aria-selected="true">General</button>
  <button role="tab">Movimientos</button>
</div>

<!-- Tabla -->
<table role="grid" aria-label="Movimientos financieros">
  <thead>
    <tr role="row">
      <th role="columnheader" scope="col">Fecha</th>
      <th role="columnheader" scope="col">Monto</th>
    </tr>
  </thead>
</table>

<!-- Botones de acción -->
<button aria-label="Editar movimiento">
  <span aria-hidden="true">✏️</span>
</button>
```

### Contraste y Legibilidad

```
VERIFICACIÓN DE CONTRASTE:

✅ Texto normal (14-18px):
   - Negro (#000) sobre blanco: 21:1 (AAA)
   - Gris oscuro (#333) sobre blanco: 12:1 (AAA)
   - Blanco sobre azul (#2E5C8A): 7.2:1 (AA)

✅ Texto grande (18px+ o 14px bold):
   - Blanco sobre verde (#2E7D32): 4.8:1 (AA)
   - Blanco sobre rojo (#C62828): 5.2:1 (AA)

✅ Componentes UI:
   - Borde input: #666 sobre #FFF (5.7:1) ✅
   - Icono botón: #333 sobre #E0E0E0 (4.6:1) ✅
   - Texto deshabilitado: #999 sobre #FFF (2.8:1) ⚠️ (aceptable para disabled)
```

### Responsive (Minimización)

```
VENTANA PEQUEÑA (< 900px):
- Panel lateral: Colapsable (botón ≡ para expandir)
- Pestañas: Cambiar a dropdown
- Tabla: Scroll horizontal con columnas prioritarias
- Toolbar: Mostrar solo iconos (sin texto)

VENTANA MÍNIMA (< 600px):
- Mostrar solo vista móvil simplificada
- Advertir usuario: "Ventana muy pequeña"
```

---

## 📋 ESPECIFICACIONES TÉCNICAS

### Colores Exactos (Hex)

```python
# src/shared/design_tokens.py
COLORS = {
    # Fondos
    'window_bg': '#F0F0F0',
    'panel_bg': '#FFFFFF',
    'border': '#C0C0C0',

    # Texto
    'text_primary': '#000000',
    'text_secondary': '#666666',
    'text_disabled': '#999999',

    # Primario
    'primary': '#2E5C8A',
    'primary_hover': '#3D7AB5',
    'primary_active': '#1E3D5C',
    'primary_light': '#E3F2FD',

    # Semánticos
    'success': '#2E7D32',
    'success_light': '#E8F5E9',
    'error': '#C62828',
    'error_light': '#FFEBEE',
    'warning': '#F9A825',
    'warning_light': '#FFFDE7',

    # Tabla
    'table_header': '#E0E0E0',
    'table_row_odd': '#FFFFFF',
    'table_row_even': '#F5F5F5',
    'table_hover': '#E3F2FD',
    'table_selected': '#2E5C8A',
}
```

### Dimensiones (px)

```python
DIMENSIONS = {
    # Ventana
    'window_min_width': 900,
    'window_min_height': 600,
    'window_default': (1200, 800),

    # Paneles
    'sidebar_width': 280,
    'toolbar_height': 32,
    'statusbar_height': 24,

    # Elementos
    'button_height': 24,
    'button_min_width': 80,
    'input_height': 22,
    'table_row_height': 24,
    'tab_height': 28,

    # Espaciado
    'padding_xs': 4,
    'padding_sm': 8,
    'padding_md': 16,
    'padding_lg': 24,
}
```

### Iconos (Mapeo)

```python
ICONS = {
    # Acciones
    'save': 'assets/icons/save.svg',
    'edit': 'assets/icons/edit.svg',
    'delete': 'assets/icons/trash.svg',
    'add': 'assets/icons/plus.svg',
    'search': '🔍',

    # Categorías Ingresos
    'sueldo': '💼',
    'freelance': '💻',
    'inversiones': '📈',
    'ventas': '🛒',
    'regalos': '🎁',
    'reembolsos': '↩️',

    # Categorías Gastos
    'alimentacion': '🍽️',
    'transporte': '🚗',
    'vivienda': '🏠',
    'salud': '🏥',
    'educacion': '📚',
    'entretenimiento': '🎬',
    'ropa': '👕',
    'tecnologia': '💻',
    'mascotas': '🐾',
    'viajes': '✈️',
    'ahorro': '💰',
    'impuestos': '📄',
    'seguros': '🛡️',
    'otros_gastos': '📝',

    # Tipos
    'ingreso': '💵',
    'gasto': '💸',
    'transferencia': '🔄',
}
```

---

## 🚀 IMPLEMENTACIÓN EN wxPYTHON

### Ejemplo: Panel Principal

```python
import wx
from src.shared.design_tokens import COLORS, DIMENSIONS

class MainWindow(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Finanzas Personales",
                        size=DIMENSIONS['window_default'])

        self.SetMinSize((DIMENSIONS['window_min_width'],
                        DIMENSIONS['window_min_height']))

        # Panel principal con fondo clásico
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(COLORS['window_bg'])

        # Layout principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # Toolbar
        toolbar = self._create_toolbar()
        main_sizer.Add(toolbar, 0, wx.EXPAND | wx.ALL,
                      DIMENSIONS['padding_sm'])

        # Splitter: Panel lateral + Área principal
        splitter = wx.SplitterWindow(self.panel)

        # Panel lateral (Lista personas)
        self.sidebar = self._create_sidebar(splitter)

        # Área principal (Pestañas)
        self.main_area = self._create_main_area(splitter)

        splitter.SplitVertically(self.sidebar, self.main_area,
                                DIMENSIONS['sidebar_width'])
        splitter.SetMinimumPaneSize(DIMENSIONS['sidebar_width'])

        main_sizer.Add(splitter, 1, wx.EXPAND | wx.ALL,
                      DIMENSIONS['padding_sm'])

        # Barra de estado
        statusbar = self._create_statusbar()
        main_sizer.Add(statusbar, 0, wx.EXPAND)

        self.panel.SetSizer(main_sizer)

    def _create_toolbar(self):
        """Crea toolbar clásica con iconos"""
        toolbar = wx.Panel(self.panel, size=(-1, DIMENSIONS['toolbar_height']))
        toolbar.SetBackgroundColour(COLORS['panel_bg'])

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Botón Nuevo
        btn_new = wx.Button(toolbar, label="➕ Nuevo",
                           size=(80, DIMENSIONS['button_height']))
        btn_new.SetBackgroundColour(COLORS['primary'])
        btn_new.SetForegroundColour('#FFFFFF')
        sizer.Add(btn_new, 0, wx.ALL, DIMENSIONS['padding_xs'])

        # Separador
        sizer.Add(wx.StaticLine(toolbar, style=wx.LI_VERTICAL),
                 0, wx.EXPAND | wx.ALL, DIMENSIONS['padding_xs'])

        # Campo de búsqueda
        search_ctrl = wx.SearchCtrl(toolbar, size=(200, -1))
        sizer.Add(search_ctrl, 0, wx.ALL, DIMENSIONS['padding_xs'])

        toolbar.SetSizer(sizer)
        return toolbar
```

---

## ✅ CHECKLIST DE IMPLEMENTACIÓN

### Fase 1: Estructura Base

- [ ] Ventana principal con dimensiones mínimas
- [ ] Layout Master-Detail (Sidebar + Main Area)
- [ ] Barra de herramientas superior
- [ ] Barra de estado inferior
- [ ] Menú superior clásico

### Fase 2: Panel Lateral

- [ ] Header "PERSONAS"
- [ ] Campo de búsqueda funcional
- [ ] Lista scrollable con selección visual
- [ ] Botón "Nueva Persona"
- [ ] Contador de personas

### Fase 3: Pestañas Principales

- [ ] Pestaña General (formulario datos)
- [ ] Pestaña Movimientos (tabla con filtros)
- [ ] Pestaña Categorías (lista con iconos)
- [ ] Pestaña Resumen (gráficos placeholder)

### Fase 4: Accesibilidad

- [ ] Orden de tabulación lógico
- [ ] Labels asociados a inputs
- [ ] Tooltips en botones
- [ ] Colores con contraste ≥4.5:1
- [ ] Estados focus visibles

### Fase 5: Detalles Visuales

- [ ] Colores según sistema de diseño
- [ ] Iconos en categorías
- [ ] Formato de moneda ($X,XXX.XX)
- [ ] Fechas formato DD/MM/YYYY
- [ ] Estados hover/active en botones

---

## 📚 RECURSOS

### Archivos Relacionados

- `src/presentation/views/main_window.py` - Implementación principal
- `src/presentation/views/person_list_panel.py` - Panel lateral
- `src/presentation/views/person_detail_view.py` - Pestañas
- `src/shared/design_tokens.py` - Tokens de diseño
- `assets/icons/` - Iconos SVG

### Referencias UX

- Windows UX Guidelines (clásico)
- WCAG 2.1 AA Checklist
- Material Design (para patrones, no estética)

---

**Versión:** 1.0.0  
**Fecha:** 2024-03-21  
**Estado:** Listo para implementación
