"""
Sistema de Logging Profesional - Finanzas Personales

Este módulo implementa un sistema de logging empresarial con:
- Múltiples handlers (consola, archivo, rotación)
- Niveles de log configurables
- Formato JSON para análisis
- Rotación de archivos por tamaño/fecha
- Filtros personalizados
- Contexto de correlación

Arquitectura de Logging en Aplicaciones Profesionales:
======================================================

Niveles de Log (de menor a mayor severidad):
├── DEBUG    (10) - Información detallada para desarrollo
├── INFO     (20) - Eventos normales de la aplicación  
├── WARNING  (30) - Situaciones inesperadas pero manejables
├── ERROR    (40) - Errores que impiden una operación
└── CRITICAL (50) - Errores graves que requieren atención inmediata

Handlers Comunes:
├── StreamHandler    → Consola/terminal
├── FileHandler      → Archivo único
├── RotatingFileHandler → Rotación por tamaño
├── TimedRotatingFileHandler → Rotación por tiempo
├── SMTPHandler      → Envío por email (alertas críticas)
└── SocketHandler    → Envío a servidor centralizado

Formatos:
├── Simple: "2024-03-21 10:30:45 - INFO - Mensaje"
├── Detallado: "2024-03-21 10:30:45,123 - app.module - INFO - [request_id: abc123] - Mensaje"
└── JSON: {"timestamp": "...", "level": "INFO", "module": "...", "message": "..."}

Uso en el código:
================

Básico:
    from src.shared.logging_config import get_logger
    logger = get_logger(__name__)
    logger.info("Usuario creado exitosamente")
    logger.error("Error al guardar en BD", exc_info=True)

Con contexto:
    from src.shared.logging_config import LogContext
    with LogContext(user_id=123, action="create"):
        logger.info("Procesando operación")
        # Output: [user_id: 123] [action: create] Procesando operación

Ejemplo Completo:
    from src.shared.logging_config import configure_logging, get_logger
    
    # Configurar al inicio de la app
    configure_logging(
        level='INFO',
        log_dir='logs',
        max_bytes=10*1024*1024,  # 10MB
        backup_count=5
    )
    
    # Usar en cualquier módulo
    logger = get_logger('mi_modulo')
    logger.info("Aplicación iniciada")
    logger.debug("Valor de configuración: %s", config_value)
"""
import logging
import logging.handlers
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any
from contextvars import ContextVar
from functools import wraps

# ============================================================================
# CONFIGURACIÓN GLOBAL
# ============================================================================

# Contexto para almacenar información de correlación (request_id, user_id, etc.)
log_context: ContextVar[Dict[str, Any]] = ContextVar('log_context', default={})

# Niveles de log personalizados
TRACE_LEVEL = 5
logging.addLevelName(TRACE_LEVEL, 'TRACE')


def trace(self, message, *args, **kwargs):
    """Método de log TRACE (más detallado que DEBUG)."""
    if self.isEnabledFor(TRACE_LEVEL):
        self._log(TRACE_LEVEL, message, args, **kwargs)


# Agregar método trace a la clase Logger
logging.Logger.trace = trace


# ============================================================================
# FORMATTERS PERSONALIZADOS
# ============================================================================

class ColoredFormatter(logging.Formatter):
    """
    Formateador con colores para consola.
    
    Muestra diferentes colores según el nivel de log:
    - TRACE: Gris
    - DEBUG: Cyan
    - INFO: Verde
    - WARNING: Amarillo
    - ERROR: Rojo
    - CRITICAL: Rojo brillante + negrita
    """
    
    # Códigos de color ANSI
    COLORS = {
        'TRACE': '\033[90m',      # Gris
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Amarillo
        'ERROR': '\033[31m',      # Rojo
        'CRITICAL': '\033[1;91m', # Rojo brillante + negrita
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        # Guardar el nivel original
        levelname = record.levelname
        
        # Aplicar color si estamos en terminal
        if sys.stdout.isatty():
            color = self.COLORS.get(levelname, self.COLORS['RESET'])
            reset = self.COLORS['RESET']
            record.levelname = f"{color}{levelname}{reset}"
        
        # Agregar contexto si existe
        context = log_context.get()
        if context:
            context_str = ' '.join([f"[{k}: {v}]" for k, v in context.items()])
            record.msg = f"{context_str} {record.msg}"
        
        result = super().format(record)
        record.levelname = levelname  # Restaurar
        return result


class JSONFormatter(logging.Formatter):
    """
    Formateador JSON para logs estructurados.
    
    Útil para:
    - Análisis automatizado
    - Importación en ELK Stack
    - Procesamiento con herramientas de log
    """
    
    def format(self, record):
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'thread': record.thread,
            'process': record.process,
        }
        
        # Agregar información de excepción si existe
        if record.exc_info:
            log_data['exception'] = {
                'type': record.exc_info[0].__name__ if record.exc_info[0] else None,
                'message': str(record.exc_info[1]) if record.exc_info[1] else None,
            }
        
        # Agregar contexto adicional
        context = log_context.get()
        if context:
            log_data['context'] = context
        
        # Agregar atributos extra del record
        for key, value in record.__dict__.items():
            if key not in log_data and not key.startswith('_'):
                log_data[key] = value
        
        return json.dumps(log_data, ensure_ascii=False, default=str)


class DetailedFormatter(logging.Formatter):
    """
    Formateador detallado con información de contexto.
    
    Formato: 2024-03-21 10:30:45,123 | app.module | INFO | [ctx] Mensaje
    """
    
    def format(self, record):
        # Agregar contexto al mensaje
        context = log_context.get()
        if context:
            context_str = ' '.join([f"[{k}={v}]" for k, v in context.items()])
            record.msg = f"{context_str} {record.msg}"
        
        return super().format(record)


# ============================================================================
# FILTROS PERSONALIZADOS
# ============================================================================

class ContextFilter(logging.Filter):
    """Filtro que agrega información de contexto a cada log."""
    
    def filter(self, record):
        context = log_context.get()
        for key, value in context.items():
            setattr(record, key, value)
        return True


class LevelFilter(logging.Filter):
    """Filtro por nivel de log (útil para separar logs por severidad)."""
    
    def __init__(self, min_level=None, max_level=None):
        super().__init__()
        self.min_level = min_level
        self.max_level = max_level
    
    def filter(self, record):
        if self.min_level and record.levelno < self.min_level:
            return False
        if self.max_level and record.levelno > self.max_level:
            return False
        return True


# ============================================================================
# CLASE PRINCIPAL DE CONFIGURACIÓN
# ============================================================================

class LoggingManager:
    """
    Gestor centralizado de logging.
    
    Implementa el patrón Singleton para mantener una única
    configuración de logging en toda la aplicación.
    
    Example:
        >>> manager = LoggingManager()
        >>> manager.configure(
        ...     level='INFO',
        ...     log_dir='/var/log/app',
        ...     max_bytes=10*1024*1024
        ... )
    """
    
    _instance = None
    _configured = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def configure(
        self,
        level: str = 'INFO',
        log_dir: Optional[str] = None,
        app_name: str = 'finanzas_personales',
        max_bytes: int = 10 * 1024 * 1024,  # 10MB
        backup_count: int = 5,
        console_output: bool = True,
        json_format: bool = False
    ):
        """
        Configura el sistema de logging.
        
        Args:
            level: Nivel de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_dir: Directorio para archivos de log
            app_name: Nombre de la aplicación (para nombrar archivos)
            max_bytes: Tamaño máximo antes de rotar archivo
            backup_count: Número de archivos de backup a mantener
            console_output: Si True, muestra logs en consola
            json_format: Si True, usa formato JSON para archivo
        """
        if self._configured:
            return
        
        # Crear directorio de logs
        if log_dir:
            log_path = Path(log_dir)
        else:
            from ..infrastructure.config.settings import Config
            log_path = Config.DATA_DIR / 'logs'
        
        log_path.mkdir(parents=True, exist_ok=True)
        
        # Configurar logger raíz
        root_logger = logging.getLogger()
        root_logger.setLevel(getattr(logging, level.upper()))
        
        # Limpiar handlers existentes
        root_logger.handlers = []
        
        # Filtro de contexto (para todos los handlers)
        context_filter = ContextFilter()
        
        # Handler de consola
        if console_output:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(getattr(logging, level.upper()))
            
            # Usar formato con colores
            console_format = '%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s'
            console_formatter = ColoredFormatter(
                console_format,
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
            console_handler.addFilter(context_filter)
            root_logger.addHandler(console_handler)
        
        # Handler de archivo con rotación
        log_file = log_path / f'{app_name}.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Archivo guarda todo
        
        # Formato para archivo
        if json_format:
            file_formatter = JSONFormatter()
        else:
            file_format = '%(asctime)s | %(name)-30s | %(levelname)-8s | [%(filename)s:%(lineno)d] | %(message)s'
            file_formatter = DetailedFormatter(file_format)
        
        file_handler.setFormatter(file_formatter)
        file_handler.addFilter(context_filter)
        root_logger.addHandler(file_handler)
        
        # Handler de errores (solo ERROR y CRITICAL)
        error_file = log_path / f'{app_name}_errors.log'
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.addFilter(LevelFilter(min_level=logging.ERROR))
        error_handler.setFormatter(file_formatter)
        root_logger.addHandler(error_handler)
        
        # Reducir ruido de librerías externas
        logging.getLogger('matplotlib').setLevel(logging.WARNING)
        logging.getLogger('PIL').setLevel(logging.WARNING)
        logging.getLogger('urllib3').setLevel(logging.WARNING)
        
        self._configured = True
        
        # Log de inicio
        logger = logging.getLogger(__name__)
        logger.info(f"Sistema de logging configurado")
        logger.info(f"Nivel: {level}")
        logger.info(f"Archivo de log: {log_file}")
        logger.info(f"Archivo de errores: {error_file}")


# ============================================================================
# FUNCIONES DE CONVENIENCIA
# ============================================================================

def configure_logging(**kwargs):
    """
    Configura el logging de la aplicación.
    
    Función de conveniencia para no instanciar LoggingManager directamente.
    
    Args:
        **kwargs: Ver LoggingManager.configure()
    
    Example:
        >>> from src.shared.logging_config import configure_logging
        >>> configure_logging(level='DEBUG', log_dir='./logs')
    """
    manager = LoggingManager()
    manager.configure(**kwargs)


def get_logger(name: str) -> logging.Logger:
    """
    Obtiene un logger configurado.
    
    Args:
        name: Nombre del logger (generalmente __name__)
        
    Returns:
        Logger configurado
        
    Example:
        >>> from src.shared.logging_config import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Mensaje de información")
    """
    return logging.getLogger(name)


# ============================================================================
# CONTEXTO DE LOG
# ============================================================================

class LogContext:
    """
    Contexto para agregar información adicional a los logs.
    
    Útil para agregar IDs de usuario, request, transacción, etc.
    
    Example:
        >>> from src.shared.logging_config import LogContext, get_logger
        >>> logger = get_logger(__name__)
        >>> 
        >>> with LogContext(user_id=123, request_id='abc'):
        ...     logger.info("Procesando...")  # [user_id: 123] [request_id: abc] Procesando...
    """
    
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.token = None
    
    def __enter__(self):
        # Obtener contexto actual o crear nuevo
        current = log_context.get().copy()
        current.update(self.kwargs)
        self.token = log_context.set(current)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restaurar contexto anterior
        log_context.reset(self.token)


def log_context_decorator(**context_kwargs):
    """
    Decorador para agregar contexto a funciones.
    
    Example:
        >>> @log_context_decorator(operation='save', entity='persona')
        ... def guardar_persona(datos):
        ...     logger.info("Guardando...")  # [operation: save] [entity: persona] Guardando...
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with LogContext(**context_kwargs):
                return func(*args, **kwargs)
        return wrapper
    return decorator


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

if __name__ == '__main__':
    # Configurar logging
    configure_logging(
        level='DEBUG',
        console_output=True,
        json_format=False
    )
    
    logger = get_logger('ejemplo')
    
    # Diferentes niveles de log
    logger.trace("Mensaje TRACE (muy detallado)")
    logger.debug("Mensaje DEBUG")
    logger.info("Mensaje INFO")
    logger.warning("Mensaje WARNING")
    logger.error("Mensaje ERROR")
    logger.critical("Mensaje CRITICAL")
    
    # Con contexto
    with LogContext(user_id=123, action='test'):
        logger.info("Operación con contexto")
    
    # Formato con variables
    logger.info("Usuario %s creado con ID %d", "Juan", 456)
    
    # Log de excepción
    try:
        1 / 0
    except ZeroDivisionError:
        logger.error("Error en cálculo", exc_info=True)
    
    print("\nRevisa el directorio de logs para ver los archivos generados")
