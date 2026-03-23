# 📚 Guía del Sistema de Logging Profesional

Esta guía te enseña cómo funciona un sistema de logging empresarial paso a paso.

## 🎯 ¿Por qué es importante el logging?

Imagina que tu aplicación es como un restaurante:

- **Sin logs**: No sabes qué pasó cuando algo falla
- **Con logs básicos**: Sabes que algo falló, pero no cuándo ni por qué
- **Con logs profesionales**: Sabes exactamente qué pasó, cuándo, quién lo hizo y cómo solucionarlo

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    APLICACIÓN                                │
├─────────────────────────────────────────────────────────────┤
│  Código fuente                                              │
│  ├── logger.debug("Detalles internos")                      │
│  ├── logger.info("Usuario inició sesión")                   │
│  ├── logger.warning("Conexión lenta")                       │
│  ├── logger.error("Error al guardar")                       │
│  └── logger.critical("Base de datos no disponible")         │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              LOGGER (logging.getLogger)                     │
│  - Recibe mensajes de log                                   │
│  - Determina nivel de severidad                             │
│  - Los pasa a los handlers                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
           ┌───────────┴───────────┐
           │                       │
           ▼                       ▼
┌──────────────────┐    ┌──────────────────┐
│  HANDLER CONSOLA │    │  HANDLER ARCHIVO │
│  - Muestra en    │    │  - Guarda en     │
│    terminal      │    │    finanzas.log  │
│  - Formato color │    │  - Rota por      │
│  - Para desarrollo│   │    tamaño        │
└──────────────────┘    └──────────────────┘
           │                       │
           └───────────┬───────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              FORMATTER                                      │
│  Convierte el log en formato legible:                       │
│  "2024-03-21 10:30:45 | app.module | INFO | Mensaje"        │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Niveles de Log (Más comunes → Más graves)

```
DEBUG      ────────► Información detallada para desarrollo
    ↑                 Ej: "Variable x = 42"
    │
INFO       ────────► Eventos normales de la aplicación
    ↑                 Ej: "Usuario creado exitosamente"
    │
WARNING    ────────► Situaciones inesperadas pero manejables
    ↑                 Ej: "Conexión lenta detectada"
    │
ERROR      ────────► Errores que impiden una operación
    ↑                 Ej: "Error al guardar en base de datos"
    │
CRITICAL   ────────► Errores graves que requieren atención
                    Ej: "Base de datos no disponible"
```

## 🔧 Componentes Principales

### 1. Logger

El objeto que usas en tu código para enviar mensajes.

```python
from src.shared.logging_config import get_logger

# Obtener logger para este módulo
logger = get_logger(__name__)

# Usar diferentes niveles
logger.debug("Esto es para desarrollo")
logger.info("Esto es información normal")
logger.warning("Esto es una advertencia")
logger.error("Esto es un error")
logger.critical("Esto es crítico!")
```

### 2. Handlers

Deciden **dónde** van los logs.

**Tipos de Handlers:**

- `StreamHandler` → Consola/terminal
- `FileHandler` → Archivo único
- `RotatingFileHandler` → Archivo que rota por tamaño
- `TimedRotatingFileHandler` → Archivo que rota por tiempo

**Ejemplo de configuración:**

```python
# Handler de consola (para ver en tiempo real)
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)  # Solo INFO y superior

# Handler de archivo (guarda todo)
file_handler = logging.handlers.RotatingFileHandler(
    'app.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5            # Mantener 5 archivos
)
file_handler.setLevel(logging.DEBUG)  # Guarda todo
```

### 3. Formatters

Deciden **cómo** se ven los logs.

**Formato Simple:**

```
2024-03-21 10:30:45 | INFO | Mensaje
```

**Formato Detallado:**

```
2024-03-21 10:30:45,123 | app.module | INFO | [archivo.py:42] | Mensaje
```

**Formato JSON (para análisis automático):**

```json
{
  "timestamp": "2024-03-21T10:30:45",
  "level": "INFO",
  "logger": "app.module",
  "message": "Mensaje",
  "file": "archivo.py",
  "line": 42
}
```

### 4. Filters

Permiten **filtrar** qué logs se procesan.

```python
# Solo logs de ERROR o superior
error_filter = LevelFilter(min_level=logging.ERROR)
handler.addFilter(error_filter)

# Agregar contexto automático
context_filter = ContextFilter()
handler.addFilter(context_filter)
```

## 🎨 Funcionalidades Avanzadas

### Contexto de Log (LogContext)

Agrega información adicional a todos los logs dentro de un bloque:

```python
from src.shared.logging_config import LogContext, get_logger

logger = get_logger(__name__)

# Sin contexto
logger.info("Procesando pago")  # Output: Procesando pago

# Con contexto
with LogContext(user_id=123, transaction_id='abc'):
    logger.info("Procesando pago")
    # Output: [user_id: 123] [transaction_id: abc] Procesando pago

    logger.info("Validando tarjeta")
    # Output: [user_id: 123] [transaction_id: abc] Validando tarjeta
```

**¿Para qué sirve?**

- Rastrear operaciones de un usuario específico
- Seguir una transacción a través de múltiples módulos
- Debugging de operaciones complejas

### Colores en Consola

Los logs en consola usan colores para diferenciar niveles:

```
[GRIS]    10:30:45 TRACE Detalle muy específico
[CIAN]    10:30:46 DEBUG Información de desarrollo
[VERDE]   10:30:47 INFO  Evento normal
[AMARILLO]10:30:48 WARN  Advertencia
[ROJO]    10:30:49 ERROR Error!
[ROJO+]   10:30:50 CRIT  ¡Crítico!
```

### Rotación de Archivos

Para no tener un archivo de log gigante:

```
finanzas.log          ← Archivo actual (hasta 10MB)
finanzas.log.1        ← Backup más reciente
finanzas.log.2
finanzas.log.3
finanzas.log.4
finanzas.log.5        ← Backup más antiguo (se elimina el 6°)
```

Cuando `finanzas.log` llega a 10MB:

1. `finanzas.log.5` se elimina
2. `finanzas.log.4` → `finanzas.log.5`
3. `finanzas.log.3` → `finanzas.log.4`
4. ...así sucesivamente...
5. `finanzas.log` → `finanzas.log.1`
6. Se crea nuevo `finanzas.log` vacío

## 📝 Ejemplos Prácticos

### Ejemplo 1: Login de Usuario

```python
from src.shared.logging_config import get_logger, LogContext

logger = get_logger(__name__)

def login(username, password):
    with LogContext(username=username, action='login'):
        logger.info(f"Intento de login para usuario: {username}")

        user = find_user(username)
        if not user:
            logger.warning(f"Usuario no encontrado: {username}")
            return False

        if not verify_password(password, user.password_hash):
            logger.warning(f"Contraseña incorrecta para: {username}")
            return False

        logger.info(f"Login exitoso: {username}")
        return True
```

**Output:**

```
10:30:45 | auth | INFO | [username: juan] [action: login] Intento de login para usuario: juan
10:30:45 | auth | INFO | [username: juan] [action: login] Login exitoso: juan
```

### Ejemplo 2: Manejo de Errores

```python
def save_to_database(data):
    try:
        logger.debug(f"Guardando datos: {data}")
        db.execute("INSERT INTO ...", data)
        logger.info("Datos guardados exitosamente")
    except DatabaseError as e:
        logger.error("Error al guardar en base de datos", exc_info=True)
        # exc_info=True incluye el stack trace completo
        raise
```

**Output:**

```
10:30:45 | db | DEBUG | Guardando datos: {'nombre': 'Juan'}
10:30:45 | db | ERROR | Error al guardar en base de datos
Traceback (most recent call last):
  File "database.py", line 42, in save_to_database
    db.execute("INSERT INTO ...", data)
DatabaseError: duplicate key value violates unique constraint
```

### Ejemplo 3: Rendimiento

```python
import time
from src.shared.logging_config import log_execution

@log_execution(level=logging.INFO)
def procesar_archivo_grande(ruta):
    """Esta función loggeará automáticamente el tiempo de ejecución"""
    with open(ruta, 'r') as f:
        return f.read()

# Output:
# 10:30:45 | app | INFO | Ejecutando procesar_archivo_grande
# 10:30:47 | app | INFO | procesar_archivo_grande completado en 2.145s
```

## 🔍 Cómo leer los logs

### Archivos generados:

```
logs/
├── finanzas.log          # Todos los logs
├── finanzas_errors.log   # Solo ERROR y CRITICAL
└── finanzas.log.1        # Backup rotado
```

### Buscar errores:

```bash
# Linux/Mac
grep "ERROR" logs/finanzas.log

# Windows
findstr "ERROR" logs\finanzas.log
```

### Ver logs en tiempo real:

```bash
# Linux/Mac
tail -f logs/finanzas.log

# Windows (PowerShell)
Get-Content logs\finanzas.log -Wait
```

### Buscar por contexto:

```bash
# Buscar logs de un usuario específico
grep "user_id: 123" logs/finanzas.log
```

## 🎓 Mejores Prácticas

### ✅ HACER:

- Usar niveles apropiados (DEBUG para desarrollo, INFO para producción)
- Incluir contexto (IDs de usuario, transacción)
- Loggear al inicio y fin de operaciones importantes
- Usar `exc_info=True` en bloques except
- Ser descriptivo pero conciso

```python
# ✅ Bien
logger.info("Usuario %s creado exitosamente con ID %d", username, user_id)

with LogContext(operation='payment', amount=100.50):
    logger.info("Procesando pago")
    process_payment()
    logger.info("Pago completado")
```

### ❌ NO HACER:

- Loggear información sensible (contraseñas, tarjetas)
- Usar print() en código de producción
- Loggear demasiado (nivel DEBUG en producción)
- Loggear muy poco (sin contexto)

```python
# ❌ Mal
logger.debug("x = %s, y = %s, z = %s", x, y, z)  # Demasiado detalle
print("Error!")  # Usar logger.error()
logger.info(password)  # ¡NUNCA loggear contraseñas!
```

## 🔧 Configuración para Diferentes Entornos

### Desarrollo:

```python
configure_logging(
    level='DEBUG',        # Ver todo
    console_output=True,  # Mostrar en terminal
    json_format=False     # Formato legible
)
```

### Producción:

```python
configure_logging(
    level='INFO',         # Solo INFO y superior
    console_output=False, # No mostrar en terminal
    json_format=True      # Formato JSON para análisis
)
```

### Testing:

```python
configure_logging(
    level='ERROR',        # Solo errores
    console_output=True
)
```

## 📚 Recursos Adicionales

- **Python Logging HOWTO**: https://docs.python.org/3/howto/logging.html
- **Logging Cookbook**: https://docs.python.org/3/howto/logging-cookbook.html
- **12 Factor App (Logs)**: https://12factor.net/logs

---

**💡 Tip**: Los logs son la herramienta más importante para debugging en producción. ¡Úsalos sabiamente!
