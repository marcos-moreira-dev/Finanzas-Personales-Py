"""
Seeds de Categorías - Datos Iniciales Robustos

Este módulo contiene los datos iniciales (seeds) para las categorías.
Está desacoplado del sistema de base de datos para permitir:
- Fácil modificación sin tocar código de infraestructura
- Personalización por el usuario final
- Testing independiente
- Versionado de datos iniciales
- Ejecución transaccional y segura
"""
import logging
import sqlite3
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

# Configurar logger
logger = logging.getLogger(__name__)


class TipoCategoriaSeed(str, Enum):
    """Tipos válidos para categorías en seeds."""
    INGRESO = "INGRESO"
    GASTO = "GASTO"
    AMBOS = "AMBOS"


@dataclass(frozen=True)
class CategoriaSeed:
    """
    Representa una categoría seed inmutable.
    
    frozen=True hace que la instancia sea inmutable (como una tupla)
    pero con acceso por nombre de atributo.
    
    Attributes:
        nombre: Nombre único de la categoría
        tipo: TipoCategoriaSeed (INGRESO, GASTO o AMBOS)
        color: Código hexadecimar del color (ej: #FF5733)
        descripcion: Descripción detallada de la categoría
        icono: Nombre del icono opcional (ej: "money", "food")
        orden: Orden de visualización (menor = primero)
    """
    nombre: str
    tipo: TipoCategoriaSeed
    color: str
    descripcion: str
    icono: Optional[str] = None
    orden: int = 999
    
    def __post_init__(self):
        """Valida los datos después de la creación."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError(f"El nombre no puede estar vacío")
        
        if not isinstance(self.tipo, TipoCategoriaSeed):
            raise ValueError(f"Tipo inválido: {self.tipo}")
        
        # Validar formato de color hex
        if not self.color.startswith('#') or len(self.color) != 7:
            raise ValueError(f"Color debe ser formato hex (#RRGGBB): {self.color}")


# =============================================================================
# SEEDS DE CATEGORÍAS - VERSIÓN 1.0
# =============================================================================
# Versión para control de migraciones de seeds
SEEDS_VERSION = "1.0.0"

# Categorías de Ingresos (ordenados por frecuencia de uso estimada)
CATEGORIAS_INGRESOS: List[CategoriaSeed] = [
    CategoriaSeed(
        nombre="Sueldo",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#27ae60",
        descripcion="Ingresos fijos por trabajo dependiente",
        icono="money",
        orden=1
    ),
    CategoriaSeed(
        nombre="Freelance",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#2ecc71",
        descripcion="Trabajos independientes y proyectos personales",
        icono="briefcase",
        orden=2
    ),
    CategoriaSeed(
        nombre="Inversiones",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#16a085",
        descripcion="Dividendos, intereses y rendimientos financieros",
        icono="chart-line",
        orden=3
    ),
    CategoriaSeed(
        nombre="Ventas",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#1abc9c",
        descripcion="Ingresos por venta de productos o bienes",
        icono="shopping-cart",
        orden=4
    ),
    CategoriaSeed(
        nombre="Regalos",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#3498db",
        descripcion="Dinero recibido como regalo o herencia",
        icono="gift",
        orden=5
    ),
    CategoriaSeed(
        nombre="Reembolsos",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#9b59b6",
        descripcion="Devoluciones de dinero o reembolsos",
        icono="undo",
        orden=6
    ),
    CategoriaSeed(
        nombre="Otros Ingresos",
        tipo=TipoCategoriaSeed.INGRESO,
        color="#34495e",
        descripcion="Otros tipos de ingresos varios",
        icono="coins",
        orden=99
    ),
]

# Categorías de Gastos (ordenados por frecuencia de uso estimada)
CATEGORIAS_GASTOS: List[CategoriaSeed] = [
    CategoriaSeed(
        nombre="Alimentación",
        tipo=TipoCategoriaSeed.GASTO,
        color="#e74c3c",
        descripcion="Supermercado, restaurantes y comida",
        icono="utensils",
        orden=1
    ),
    CategoriaSeed(
        nombre="Transporte",
        tipo=TipoCategoriaSeed.GASTO,
        color="#e67e22",
        descripcion="Gasolina, transporte público, mantenimiento vehicular",
        icono="car",
        orden=2
    ),
    CategoriaSeed(
        nombre="Vivienda",
        tipo=TipoCategoriaSeed.GASTO,
        color="#d35400",
        descripcion="Renta, hipoteca, servicios (agua, luz, gas)",
        icono="home",
        orden=3
    ),
    CategoriaSeed(
        nombre="Salud",
        tipo=TipoCategoriaSeed.GASTO,
        color="#c0392b",
        descripcion="Doctores, medicinas, seguros médicos",
        icono="medkit",
        orden=4
    ),
    CategoriaSeed(
        nombre="Educación",
        tipo=TipoCategoriaSeed.GASTO,
        color="#8e44ad",
        descripcion="Cursos, libros, colegiaturas, material escolar",
        icono="graduation-cap",
        orden=5
    ),
    CategoriaSeed(
        nombre="Entretenimiento",
        tipo=TipoCategoriaSeed.GASTO,
        color="#f39c12",
        descripcion="Cine, juegos, hobbies, suscripciones streaming",
        icono="film",
        orden=6
    ),
    CategoriaSeed(
        nombre="Ropa",
        tipo=TipoCategoriaSeed.GASTO,
        color="#e91e63",
        descripcion="Vestimenta, calzado y accesorios personales",
        icono="tshirt",
        orden=7
    ),
    CategoriaSeed(
        nombre="Tecnología",
        tipo=TipoCategoriaSeed.GASTO,
        color="#00bcd4",
        descripcion="Computadoras, celulares, software, gadgets",
        icono="laptop",
        orden=8
    ),
    CategoriaSeed(
        nombre="Mascotas",
        tipo=TipoCategoriaSeed.GASTO,
        color="#795548",
        descripcion="Alimento, veterinaria, cuidado de mascotas",
        icono="paw",
        orden=9
    ),
    CategoriaSeed(
        nombre="Viajes",
        tipo=TipoCategoriaSeed.GASTO,
        color="#3f51b5",
        descripcion="Hoteles, vuelos, tours, vacaciones",
        icono="plane",
        orden=10
    ),
    CategoriaSeed(
        nombre="Ahorro",
        tipo=TipoCategoriaSeed.GASTO,
        color="#009688",
        descripcion="Dinero destinado a ahorro o fondos de emergencia",
        icono="piggy-bank",
        orden=11
    ),
    CategoriaSeed(
        nombre="Impuestos",
        tipo=TipoCategoriaSeed.GASTO,
        color="#ff5722",
        descripcion="Pagos de impuestos y tasas gubernamentales",
        icono="file-invoice-dollar",
        orden=12
    ),
    CategoriaSeed(
        nombre="Seguros",
        tipo=TipoCategoriaSeed.GASTO,
        color="#607d8b",
        descripcion="Seguros de vida, auto, hogar, etc.",
        icono="shield-alt",
        orden=13
    ),
    CategoriaSeed(
        nombre="Otros Gastos",
        tipo=TipoCategoriaSeed.GASTO,
        color="#95a5a6",
        descripcion="Gastos misceláneos no clasificados",
        icono="receipt",
        orden=99
    ),
]

# Categorías que sirven para ambos tipos
CATEGORIAS_AMBOS: List[CategoriaSeed] = [
    CategoriaSeed(
        nombre="Transferencias",
        tipo=TipoCategoriaSeed.AMBOS,
        color="#607d8b",
        descripcion="Transferencias entre cuentas propias",
        icono="exchange-alt",
        orden=50
    ),
]

# Todas las categorías combinadas y ordenadas
TODAS_CATEGORIAS: List[CategoriaSeed] = (
    sorted(CATEGORIAS_INGRESOS, key=lambda x: x.orden) +
    sorted(CATEGORIAS_GASTOS, key=lambda x: x.orden) +
    sorted(CATEGORIAS_AMBOS, key=lambda x: x.orden)
)


def get_categorias_seeds() -> List[CategoriaSeed]:
    """
    Retorna todas las categorías seeds ordenadas.
    
    Returns:
        Lista de CategoriaSeed ordenadas por tipo y orden
    """
    return TODAS_CATEGORIAS.copy()


def get_categorias_por_tipo(tipo: TipoCategoriaSeed) -> List[CategoriaSeed]:
    """
    Filtra categorías por tipo.
    
    Args:
        tipo: TipoCategoriaSeed a filtrar
        
    Returns:
        Lista filtrada y ordenada de categorías
    """
    return sorted(
        [c for c in TODAS_CATEGORIAS if c.tipo == tipo],
        key=lambda x: x.orden
    )


def validar_seeds() -> List[str]:
    """
    Valida que todos los seeds sean correctos.
    
    Returns:
        Lista de errores encontrados (vacía si todo OK)
    """
    errores = []
    nombres_vistos = set()
    
    for categoria in TODAS_CATEGORIAS:
        # Verificar nombres únicos
        if categoria.nombre in nombres_vistos:
            errores.append(f"Nombre duplicado: {categoria.nombre}")
        nombres_vistos.add(categoria.nombre)
        
        # Verificar color válido
        if not categoria.color.startswith('#'):
            errores.append(f"Color inválido en {categoria.nombre}: {categoria.color}")
        elif len(categoria.color) != 7:
            errores.append(f"Longitud de color inválida en {categoria.nombre}")
    
    return errores


class SeedRunner:
    """
    Ejecutor de seeds con soporte para transacciones y logging.
    
    Esta clase encapsula la lógica de ejecución de seeds,
    permitiendo ejecución segura y recuperable.
    """
    
    def __init__(self, connection: sqlite3.Connection):
        """
        Inicializa el ejecutor de seeds.
        
        Args:
            connection: Conexión activa a SQLite
        """
        self._conn = connection
        self._ejecutados = 0
        self._omitidos = 0
        self._errores = []
    
    def ejecutar(self, force: bool = False) -> dict:
        """
        Ejecuta todos los seeds de categorías.
        
        Args:
            force: Si True, fuerza la recreación de categorías existentes
            
        Returns:
            Diccionario con estadísticas de ejecución
        """
        logger.info(f"Iniciando ejecución de seeds v{SEEDS_VERSION}")
        
        # Validar seeds antes de ejecutar
        errores_validacion = validar_seeds()
        if errores_validacion:
            logger.error(f"Validación fallida: {errores_validacion}")
            raise ValueError(f"Seeds inválidos: {errores_validacion}")
        
        cursor = self._conn.cursor()
        
        try:
            for categoria in TODAS_CATEGORIAS:
                self._procesar_categoria(cursor, categoria, force)
            
            self._conn.commit()
            logger.info(f"Seeds completados: {self._ejecutados} insertados, "
                       f"{self._omitidos} omitidos")
            
            return {
                'version': SEEDS_VERSION,
                'ejecutados': self._ejecutados,
                'omitidos': self._omitidos,
                'errores': self._errores,
                'total': len(TODAS_CATEGORIAS)
            }
            
        except Exception as e:
            self._conn.rollback()
            logger.error(f"Error ejecutando seeds: {e}")
            raise
    
    def _procesar_categoria(self, cursor, categoria: CategoriaSeed, force: bool):
        """
        Procesa una categoría individual.
        
        Args:
            cursor: Cursor de SQLite
            categoria: CategoriaSeed a procesar
            force: Si True, actualiza categorías existentes
        """
        try:
            # Verificar si ya existe
            cursor.execute(
                "SELECT id FROM categoria WHERE nombre = ?",
                (categoria.nombre,)
            )
            existe = cursor.fetchone()
            
            if existe and not force:
                logger.debug(f"Categoría ya existe, omitiendo: {categoria.nombre}")
                self._omitidos += 1
                return
            
            if existe and force:
                # Actualizar categoría existente
                cursor.execute("""
                    UPDATE categoria 
                    SET tipo = ?, color = ?, descripcion = ?, activa = 1
                    WHERE nombre = ?
                """, (
                    categoria.tipo.value,
                    categoria.color,
                    categoria.descripcion,
                    categoria.nombre
                ))
                logger.info(f"Categoría actualizada: {categoria.nombre}")
            else:
                # Insertar nueva categoría
                cursor.execute("""
                    INSERT INTO categoria (nombre, tipo, color, activa, descripcion)
                    VALUES (?, ?, ?, 1, ?)
                """, (
                    categoria.nombre,
                    categoria.tipo.value,
                    categoria.color,
                    categoria.descripcion
                ))
                logger.info(f"Categoría creada: {categoria.nombre}")
            
            self._ejecutados += 1
            
        except Exception as e:
            error_msg = f"Error procesando {categoria.nombre}: {e}"
            logger.error(error_msg)
            self._errores.append(error_msg)
            raise


def ejecutar_seeds(connection: sqlite3.Connection, force: bool = False) -> dict:
    """
    Función de conveniencia para ejecutar seeds.
    
    Args:
        connection: Conexión a base de datos
        force: Forzar actualización de existentes
        
    Returns:
        Estadísticas de ejecución
        
    Example:
        >>> from src.infrastructure.db.database import Database
        >>> with Database() as db:
        ...     resultados = ejecutar_seeds(db.get_connection())
        ...     print(f"Creadas: {resultados['ejecutados']}")
    """
    runner = SeedRunner(connection)
    return runner.ejecutar(force=force)


# Validar seeds al cargar el módulo
_errores_iniciales = validar_seeds()
if _errores_iniciales:
    raise ImportError(
        f"Seeds inválidos detectados al cargar módulo: {_errores_iniciales}"
    )
