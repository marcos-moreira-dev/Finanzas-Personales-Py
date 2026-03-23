"""
Entidad Movimiento - Dominio
Representa una transacción financiera (ingreso o gasto).
"""
from dataclasses import dataclass, field, replace
from datetime import date
from enum import Enum
from typing import Any, Optional


class TipoMovimiento(Enum):
    """Tipos de movimiento financiero."""
    INGRESO = "INGRESO"
    GASTO = "GASTO"


@dataclass
class Movimiento:
    """Entidad que representa un movimiento financiero."""
    
    persona_id: int
    fecha: date
    tipo: TipoMovimiento
    categoria_id: int
    monto: float
    id: Optional[int] = None
    descripcion: Optional[str] = None
    medio: Optional[str] = None
    referencia: Optional[str] = None
    
    def __post_init__(self):
        """Validaciones iniciales."""
        if self.monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if not isinstance(self.tipo, TipoMovimiento):
            raise ValueError("El tipo de movimiento no es válido")
        if self.fecha > date.today():
            raise ValueError("La fecha no puede ser futura")
    
    @property
    def monto_efectivo(self) -> float:
        """
        Retorna el monto con signo según el tipo.
        Positivo para ingresos, negativo para gastos.
        """
        if self.tipo == TipoMovimiento.INGRESO:
            return self.monto
        else:
            return -self.monto
    
    @property
    def es_ingreso(self) -> bool:
        """Retorna True si es un ingreso."""
        return self.tipo == TipoMovimiento.INGRESO
    
    @property
    def es_gasto(self) -> bool:
        """Retorna True si es un gasto."""
        return self.tipo == TipoMovimiento.GASTO

    def actualizado(self, **cambios: Any) -> "Movimiento":
        """Retorna una copia validada con los cambios aplicados."""
        return replace(self, **cambios)
    
    def __str__(self) -> str:
        signo = "+" if self.es_ingreso else "-"
        return f"{signo}${self.monto:.2f} - {self.descripcion or 'Sin descripción'}"
    
    def __repr__(self) -> str:
        return f"Movimiento(id={self.id}, tipo={self.tipo.value}, monto={self.monto})"
