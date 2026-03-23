"""
Decoradores de Utilidad - Capa Compartida

Proporciona decoradores reutilizables para:
- Manejo de excepciones
- Logging automático
- Validación de parámetros
- Medición de performance
"""
import functools
import logging
import time
from typing import Any, Callable

from .logging_config import get_logger

logger = get_logger(__name__)


def handle_errors(
    default_return: Any = None,
    reraise: bool = False,
    log_level: int = logging.ERROR
):
    """
    Decorador que captura excepciones y las maneja gracefulmente.
    
    Args:
        default_return: Valor a retornar si hay error
        reraise: Si True, relanza la excepción después de loggear
        log_level: Nivel de logging para el error
        
    Example:
        >>> @handle_errors(default_return=[])
        ... def get_personas():
        ...     return repo.find_all()
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.log(
                    log_level,
                    f"Error en {func.__name__}: {e}",
                    exc_info=True
                )
                
                if reraise:
                    raise
                
                return default_return
        
        return wrapper
    return decorator


def log_execution(level: int = logging.DEBUG, log_args: bool = False):
    """Decorador que loggea la ejecución de funciones."""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_logger = get_logger(func.__module__)
            
            if log_args:
                func_logger.log(
                    level,
                    f"Ejecutando {func.__name__}"
                )
            
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            func_logger.log(level, f"{func.__name__} completado en {elapsed:.3f}s")
            
            return result
        
        return wrapper
    return decorator


def singleton(cls):
    """Decorador que implementa el patrón Singleton."""
    instances = {}
    
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return wrapper
