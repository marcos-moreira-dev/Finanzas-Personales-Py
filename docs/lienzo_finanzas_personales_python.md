# Lienzo detallado — Aplicación Python: **Finanzas Personales de Escritorio**

## 1. Visión general

Aplicación de escritorio en Python para registrar y consultar la información financiera básica de una persona, con enfoque doméstico y de oficina ligera, diseñada como proyecto didáctico, serio y autocontenido.

La aplicación debe permitir:

- registrar personas
- asociar una foto o imagen de perfil
- registrar ingresos y gastos
- clasificar movimientos por categorías
- consultar saldo y resúmenes mensuales
- mostrar gráficos simples
- persistir datos localmente
- ofrecer una experiencia de escritorio clásica, sobria y nostálgica

No se busca construir un sistema contable profesional ni una plataforma bancaria. La aplicación debe sentirse como un programa de escritorio del estilo:

- gestor personal
- libreta financiera digital
- mini libro de caja doméstico
- software de oficina pequeño pero serio

---

## 2. Objetivo general

Construir una aplicación de escritorio en Python para gestionar ingresos y gastos personales de manera clara, visual y ordenada, con una arquitectura limpia y una interfaz inspirada en programas clásicos de oficina.

---

## 3. Objetivos técnicos

- practicar Python en un proyecto de escritorio real
- trabajar con persistencia local
- modelar entidades financieras básicas sin sobrecomplicar el dominio
- aprender patrones clásicos de arquitectura de escritorio
- trabajar formularios, tablas, filtros, gráficos y fotografía de usuario
- documentar un proyecto con apariencia profesional y estructura mantenible
- poder extenderlo más adelante sin destruir la base

---

## 4. Alcance funcional

La aplicación debe permitir, como mínimo:

- registrar personas
- almacenar datos de contacto básicos
- asociar foto de perfil
- registrar ingresos
- registrar gastos
- clasificar cada movimiento
- consultar movimientos filtrados por mes y categoría
- mostrar saldo total
- mostrar resumen mensual
- presentar gráficos de barras y pastel
- exportar datos simples en CSV o formato futuro equivalente

No se busca, en la primera versión:

- contabilidad formal profesional
- impuestos
- conciliación bancaria
- múltiples monedas avanzadas
- facturación
- cuentas por cobrar complejas
- presupuestos empresariales
- multiusuario en red

---

## 5. Identidad del programa

La aplicación debe sentirse como un software:

- doméstico-serio
- de oficina ligera
- clásico
- funcional
- visualmente ordenado
- con sabor de software de escritorio 2005–2010

### Sensación buscada

- formularios claros
- pestañas o secciones bien separadas
- tablas legibles
- gráficos simples pero útiles
- navegación tipo maestro-detalle
- ventanas y diálogos tradicionales
- aire retro de utilidad de oficina

### No se busca

- estilo web moderno minimalista
- interfaz tipo dashboard SaaS
- animaciones innecesarias
- apariencia infantil
- exceso de efectos visuales contemporáneos

---

## 6. Idea central del dominio

La aplicación gira alrededor de una **persona** y de sus **movimientos financieros básicos**.

El núcleo conceptual es:

- una persona tiene datos generales
- una persona tiene una foto opcional
- una persona tiene movimientos
- cada movimiento pertenece a una categoría
- los movimientos se agrupan y analizan por fecha, tipo y categoría

---

## 7. Entidades principales del dominio

## 7.1 Persona
Representa al titular de la ficha financiera.

Atributos sugeridos:
- id
- nombres
- apellidos
- identificación opcional
- teléfono
- correo
- fecha de registro
- observaciones
- ruta de foto o referencia binaria gestionada por el sistema

## 7.2 Movimiento
Representa una transacción básica.

Atributos sugeridos:
- id
- persona_id
- fecha
- tipo (ingreso o gasto)
- categoría_id
- monto
- descripción
- medio opcional (efectivo, transferencia, etc.)
- referencia opcional

## 7.3 Categoría
Clasifica movimientos.

Atributos sugeridos:
- id
- nombre
- tipo permitido (ingreso, gasto o ambos según decisión)
- color opcional para gráficos
- descripción opcional

## 7.4 Resumen mensual
No necesariamente debe ser tabla persistida. Puede ser una proyección o cálculo.

Debe incluir:
- total de ingresos del mes
- total de gastos del mes
- saldo neto del mes
- categorías predominantes
- comparación simple con otros meses

## 7.5 Archivo o foto
Representa la imagen de perfil del usuario.

Atributos sugeridos:
- id
- persona_id
- ruta física o almacenamiento interno
- fecha de captura o carga
- origen (archivo, webcam)

---

## 8. Casos de uso principales

## 8.1 Crear persona
El usuario registra una nueva ficha personal.

## 8.2 Editar persona
El usuario actualiza datos personales.

## 8.3 Asignar foto
El usuario carga una imagen desde archivo o toma una foto con webcam.

## 8.4 Registrar ingreso
El usuario agrega un ingreso con fecha, categoría y monto.

## 8.5 Registrar gasto
El usuario agrega un gasto con fecha, categoría y monto.

## 8.6 Consultar movimientos
El usuario revisa movimientos por filtros.

## 8.7 Consultar resumen
El usuario revisa saldo, totales y gráficos.

## 8.8 Exportar movimientos
El usuario exporta una tabla simple para análisis externo.

## 8.9 Gestionar categorías
El usuario crea, edita o desactiva categorías.

---

## 9. Estructura funcional de la aplicación

## 9.1 Ventana principal
Debe contener:

- menú superior
- barra de herramientas opcional
- panel de búsqueda/listado de personas
- área central o lateral para abrir ficha
- barra de estado

## 9.2 Ficha de persona
Debe ser el corazón de la aplicación.

Se recomienda usar una estructura con pestañas o secciones claras.

### Pestañas sugeridas

- General
- Foto
- Movimientos
- Categorías
- Resumen
- Observaciones

---

## 10. Diseño funcional por pestañas

## 10.1 Pestaña General
Debe mostrar y editar:

- nombres
- apellidos
- identificación
- teléfono
- correo
- fecha de registro
- observaciones cortas

## 10.2 Pestaña Foto
Debe permitir:

- cargar foto desde archivo
- quitar foto
- reemplazar foto
- capturar desde webcam (futuro o versión intermedia)
- previsualizar la imagen

## 10.3 Pestaña Movimientos
Debe incluir:

- tabla de movimientos
- filtro por mes
- filtro por año
- filtro por categoría
- filtro por tipo
- botón nuevo ingreso
- botón nuevo gasto
- botón editar movimiento
- botón eliminar o anular movimiento

La tabla debe mostrar al menos:
- fecha
- tipo
- categoría
- descripción
- monto

## 10.4 Pestaña Categorías
Debe permitir:

- ver categorías existentes
- crear categoría
- editar categoría
- activar o desactivar categoría

## 10.5 Pestaña Resumen
Debe mostrar:

- saldo total
- ingresos acumulados
- gastos acumulados
- resumen mensual
- gráfico de barras por mes
- gráfico de pastel por categoría de gasto
- lista de categorías más usadas

## 10.6 Pestaña Observaciones
Debe permitir guardar notas libres relacionadas con la persona o con su contexto financiero.

---

## 11. Experiencia de usuario buscada

La aplicación debe sentirse como un programa de escritorio clásico y utilitario.

### Características deseadas

- formularios comprensibles
- botones previsibles
- validaciones directas
- mensajes claros
- tablas con selección simple
- gráficas entendibles
- poco ruido visual
- sensación de “herramienta confiable”

### Estética sugerida

- colores sobrios
- gráficos relativamente vistosos, pero no excesivos
- iconografía simple
- proporciones de software de oficina
- un aire entre agenda digital y gestor personal clásico

---

## 12. Patrones arquitectónicos clásicos que sí tienen sentido aquí

Esta sección se incluye porque el proyecto debe dialogar con la tradición del software de escritorio de 2005–2010.

## 12.1 Monolito modular
### Microconcepto
Una sola aplicación, un solo proceso, una sola base local, pero organizada por módulos internos.

### Por qué encaja
Es lo más natural para una app de escritorio local y personal.

### Decisión sugerida
**Sí.** Debe ser la base estructural del proyecto.

---

## 12.2 Arquitectura por capas (3 capas clásicas)
### Microconcepto
Separar presentación, lógica de negocio y acceso a datos.

### Capas típicas
- presentación
- aplicación o negocio
- persistencia

### Por qué encaja
Fue extremadamente común en software de escritorio y empresarial ligero durante los 2000 y 2010.

### Decisión sugerida
**Sí.** Muy recomendable como marco general.

---

## 12.3 MVC (Modelo–Vista–Controlador)
### Microconcepto
El modelo guarda estado y reglas; la vista muestra; el controlador coordina.

### Contexto histórico
Muy típico en GUIs clásicas, tanto de escritorio como web temprana.

### ¿Encaja aquí?
Sí, pero en escritorio a veces termina con controladores demasiado grandes si no se cuida.

### Decisión sugerida
Puede usarse, pero para esta app yo lo vería más como una referencia conceptual que como el patrón exclusivo.

---

## 12.4 MVP (Model–View–Presenter)
### Microconcepto
La vista queda más pasiva; el presenter coordina y le inyecta datos.

### Contexto histórico
Muy típico en entornos de escritorio y formularios empresariales entre mediados de los 2000 y 2010.

### ¿Encaja aquí?
Muchísimo, porque la app tendrá formularios, tablas, filtros y resúmenes.

### Decisión sugerida
**Muy recomendable** para la capa de presentación si quieres algo clásico y claro.

---

## 12.5 Passive View
### Microconcepto
La vista casi no piensa; solo dibuja y reenvía eventos.

### ¿Encaja aquí?
Sí, especialmente si quieres testear mejor la lógica de pantalla.

### Decisión sugerida
Útil como refinamiento de MVP.

---

## 12.6 Presentation Model
### Microconcepto
Se crea un modelo intermedio adaptado a la interfaz, separado del dominio puro.

### ¿Encaja aquí?
Sí, sobre todo en formularios complejos con validaciones, estados y formato de datos.

### Decisión sugerida
Puede usarse en pantallas como Resumen o Ficha de Persona.

---

## 12.7 Master-Detail
### Microconcepto
A la izquierda o arriba una lista; a la derecha o al abrir, el detalle.

### Contexto histórico
Completamente típico en software de oficina, ERPs ligeros, gestores de clientes y utilitarios de escritorio.

### Decisión sugerida
**Sí, fuertemente recomendado** para el flujo principal.

---

## 12.8 Form-based Application
### Microconcepto
La aplicación se organiza alrededor de formularios de edición y consulta.

### Contexto histórico
Este es quizás el patrón visual más típico de escritorio 2000–2010.

### Decisión sugerida
**Sí.** Debe ser uno de los pilares del proyecto.

---

## 12.9 Document/View
### Microconcepto
Una entidad principal se abre como documento editable con una o varias vistas.

### ¿Encaja aquí?
Sí de manera parcial. La ficha financiera de una persona puede verse como un “documento” o expediente.

### Decisión sugerida
No es obligatorio, pero sirve como inspiración.

---

## 13. Arquitectura frontend típica de escritorio 2005–2010

Esta app no debe pensarse como frontend web moderno, sino como **frontend de escritorio clásico**.

## 13.1 Estructura visual típica de la época

### Elementos frecuentes
- menú superior
- toolbar con iconos
- panel lateral de navegación o listado
- formulario principal en el área central
- pestañas para submódulos
- tabla de registros
- barra de estado abajo
- diálogos modales para crear/editar

### Traducción al proyecto
La aplicación debe sentirse cercana a:
- agenda financiera
- gestor de clientes simple
- mini ERP personal
- software administrativo liviano

---

## 13.2 Patrones de interfaz recomendados para esta app

### Listado + ficha
Una lista de personas abre una ficha detallada.

### Formularios con pestañas
Muy típico cuando un mismo registro tiene varias categorías de información.

### Diálogos modales
Para operaciones cortas:
- nuevo movimiento
- editar categoría
- seleccionar foto

### Panel resumen con gráficas
Típico en software posterior a 2008–2012 cuando ya se empezaron a incorporar dashboards moderados.

### Barra de estado
Debe mostrar mensajes como:
- persona seleccionada
- total de movimientos filtrados
- estado de guardado

---

## 13.3 Referencias implícitas de época

### 2000–2005
- aplicaciones muy basadas en formularios
- menús y toolbars fuertes
- diálogos frecuentes
- pantallas densas pero claras

### 2005–2010
- uso fuerte de pestañas
- master-detail consolidado
- tablas con filtros
- paneles acoplados o secciones laterales
- primeros resúmenes gráficos integrados con sobriedad

### 2010–2015
- un poco más de limpieza visual
- dashboards moderados
- mejor integración de tablas + gráficas
- persistencia y exportación más naturalizadas

### Decisión sugerida para el proyecto
Tomar como base principal la estética y estructura **2005–2010**, con un poco de limpieza posterior, sin parecer web.

---

## 14. Propuesta arquitectónica oficial para la app

### Decisión escrita en piedra
La aplicación debe implementarse como un **monolito modular de escritorio**, organizado en **capas**, con una capa de presentación inspirada en **MVP clásico** y un frontend basado en **formularios, tablas, master-detail y pestañas**, al estilo de software de oficina 2005–2010.

Eso quiere decir:

- una sola app
- una sola base de datos local
- módulos internos separados
- pantallas de escritorio clásicas
- lógica del dominio separada de la UI

---

## 15. Organización recomendada del proyecto

```text
finanzas_personales/
  README.md
  pyproject.toml
  requirements.txt
  .env.example
  .gitignore
  docs/
    arquitectura.md
    roadmap.md
    decisiones/
    modelo_de_datos.md
  assets/
    icons/
    photos/
    ui/
  data/
  src/
    main.py
    app/
      bootstrap.py
      settings.py
    domain/
      persona.py
      movimiento.py
      categoria.py
      resumen.py
    application/
      services/
      use_cases/
      dto/
    infrastructure/
      db/
      repositories/
      camera/
      charts/
      export/
      config/
    presentation/
      presenters/
      viewmodels/
      views/
        main_window.py
        person_list_panel.py
        person_detail_view.py
        dialogs/
        widgets/
    shared/
      constants.py
      enums.py
      validators.py
      errors.py
      utils.py
  tests/
    domain/
    application/
    presentation/
    integration/
```

---

## 16. Requerimientos del modelo de datos

## 16.1 Persona
Debe poder crearse, editarse, consultarse y archivarse.

## 16.2 Movimiento
Debe estar ligado siempre a una persona y tener validaciones mínimas.

## 16.3 Categoría
Debe ser configurable, porque los gastos e ingresos pueden variar según el usuario.

## 16.4 Persistencia
La primera opción razonable es **SQLite**, por ser clásica, local, ligera y totalmente adecuada para este tipo de programa.

---

## 17. Reglas del dominio

- el monto de un movimiento debe ser positivo
- el tipo del movimiento determina si suma o resta en los resúmenes
- un movimiento debe pertenecer a una categoría válida
- una persona puede existir sin movimientos, pero no un movimiento sin persona
- una categoría inactiva no debería usarse en nuevos movimientos
- el resumen mensual debe calcularse a partir de los movimientos registrados

---

## 18. Requerimientos de captura de imagen

## 18.1 Foto desde archivo
Debe poder cargarse una foto desde el sistema de archivos.

## 18.2 Foto desde webcam
Idealmente, en una versión intermedia o posterior, debe poder:

- activar cámara
- previsualizar
- capturar
- guardar como foto de perfil

## 18.3 Validaciones mínimas
- tamaño máximo razonable
- formato permitido
- manejo de errores si no hay cámara

---

## 19. Requerimientos de visualización de datos

## 19.1 Gráficos
Se desean gráficos como:

- barras por mes
- pastel por categoría de gasto
- comparativo ingresos vs gastos

## 19.2 Propósito
Los gráficos no deben ser adorno. Deben responder preguntas como:

- ¿en qué gasto más?
- ¿cómo voy este mes?
- ¿qué categorías dominan?
- ¿mi saldo mejoró o empeoró?

## 19.3 Estilo visual
- sobrio
- claro
- integrados como paneles o pestañas
- no exageradamente modernos

---

## 20. Requerimientos de exportación

La aplicación debería poder exportar, al menos en fases posteriores:

- movimientos en CSV
- resumen mensual en CSV
- imagen de gráfico
- informe simple PDF futuro

---

## 21. Requerimientos de búsqueda y filtros

Debe ser posible:

- buscar personas por nombre
- filtrar movimientos por mes
- filtrar por año
- filtrar por tipo
- filtrar por categoría
- ordenar tabla de movimientos

---

## 22. Requerimientos de navegación

Flujo principal esperado:

1. abrir app
2. ver lista de personas
3. crear o seleccionar persona
4. abrir ficha
5. registrar ingresos y gastos
6. revisar resumen
7. exportar o cerrar

---

## 23. Requerimientos no funcionales

## 23.1 Legibilidad
El proyecto debe ser fácilmente entendible meses después.

## 23.2 Mantenibilidad
La estructura debe permitir añadir módulos sin romper todo.

## 23.3 Reproducibilidad
Debe poder instalarse en un entorno virtual y ejecutarse con pocos pasos.

## 23.4 Trazabilidad
La documentación debe dejar claro:
- qué decisiones se tomaron
- por qué patrón se eligió
- qué quedó fuera del alcance inicial

## 23.5 Robustez básica
La app debe manejar errores previsibles de forma amable:
- archivo de imagen inválido
- monto inválido
- campos vacíos obligatorios
- base no encontrada o no inicializada

---

## 24. Tecnología sugerida

## 24.1 Toolkit de interfaz
**wxPython** como primera opción si se quiere reforzar la estética y sensación de escritorio clásico.

Razones:
- vibra nativa y tradicional
- encaja con software retro-serio
- formularios y tablas se sienten naturales
- buenas capacidades para escritorio clásico

## 24.2 Persistencia
**SQLite**

## 24.3 Gráficos
**Matplotlib** incrustado en la app o solución equivalente sobria.

## 24.4 Cámara
**OpenCV** para captura puntual si se añade webcam.

---

## 25. Reglas de implementación y buenas prácticas

- usar entorno virtual
- fijar dependencias
- documentar instalación
- separar recursos de código
- no mezclar lógica del dominio con widgets
- construir primero el dominio y persistencia
- luego la UI
- luego gráficos y detalles extra
- escribir README y roadmap desde temprano

---

## 26. Roadmap sugerido

## Versión 0.1
- estructura base del proyecto
- SQLite inicial
- CRUD de personas
- CRUD de movimientos
- categorías básicas
- cálculo de saldo simple

## Versión 0.2
- vista maestro-detalle
- pestañas de ficha
- filtros por mes y categoría
- validaciones de formularios

## Versión 0.3
- gráficos de resumen
- carga de foto desde archivo
- mejor organización visual

## Versión 0.4
- webcam opcional
- exportación CSV
- configuración persistente
- pulido de UX clásico

---

## 27. Riesgos a evitar

- convertir la app en contabilidad profesional demasiado pronto
- mezclar tabla, gráficos y lógica financiera en una sola clase
- sobreingeniería de patrones innecesarios
- UI demasiado moderna que rompa la identidad buscada
- tratar la foto o la webcam como si fueran el centro del sistema

---

## 28. Criterios de éxito

El proyecto se considera bien orientado si:

- se puede registrar una persona y sus movimientos
- el saldo y los resúmenes se calculan bien
- la interfaz es clara y agradable
- los módulos del código se entienden
- la arquitectura se percibe clásica pero sana
- el proyecto puede enseñarte sobre software de escritorio serio
- el repositorio queda presentable en GitHub

---

## 29. Frase oficial del proyecto

**Aplicación de escritorio en Python para gestionar finanzas personales básicas, concebida como un monolito modular clásico con interfaz de oficina estilo 2005–2010, centrada en fichas personales, movimientos financieros, gráficos simples y arquitectura limpia para fines de aprendizaje y portafolio.**

---

## 30. Decisiones escritas en piedra

- el proyecto será en Python
- la app será de escritorio
- el estilo será clásico, sobrio y ligeramente nostálgico
- la estructura global será monolítica modular
- el marco arquitectónico será por capas
- la presentación se inspirará en MVP y frontend de formularios típico de 2005–2010
- la interfaz principal será maestro-detalle con ficha tabulada
- el dominio será básico y doméstico, no contabilidad profesional
- la foto del usuario es complemento útil, no núcleo del sistema
- los gráficos deben informar, no adornar

