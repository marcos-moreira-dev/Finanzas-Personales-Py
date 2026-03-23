"""
Entidad Categoria - Dominio
Clasifica los movimientos financieros.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TipoCategoria(Enum):
    """Tipos de categoría permitidos."""
    INGRESO = "INGRESO"
    GASTO = "GASTO"
    AMBOS = "AMBOS"


@dataclass
class Categoria:
    """Entidad que representa una categoría de movimiento."""
    
    nombre: str
    tipo: TipoCategoria
    id: Optional[int] = None
    color: str = "#808080"  # Gris por defecto
    activa: bool = True
    descripcion: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones iniciales."""
        if not self.nombre or not self.nombre.strip():
            raise ValueError("El nombre de la categoría es obligatorio")
        if not isinstance(self.tipo, TipoCategoria):
            raise ValueError("El tipo de categoría no es válido")
    
    def puede_usar_para(self, tipo: str) -> bool:
        """
        Verifica si la categoría puede usarse para un tipo de movimiento.
        
        Args:
            tipo: 'INGRESO' o 'GASTO'
        
        Returns:
            True si la categoría es compatible con el tipo
        """
        if not self.activa:
            return False
        if self.tipo == TipoCategoria.AMBOS:
            return True
        return self.tipo.value == tipo
    
    def desactivar(self) -> None:
        """Desactiva la categoría para nuevos movimientos."""
        self.activa = False
    
    def activar(self) -> None:
        """Activa la categoría."""
        self.activa = True
    
    def __str__(self) -> str:
        estado = "Activa" if self.activa else "Inactiva"
        return f"{self.nombre} ({self.tipo.value}) - {estado}"
    
    def __repr__(self) -> str:
        return f"Categoria(id={self.id}, nombre='{self.nombre}', tipo={self.tipo.value})"
