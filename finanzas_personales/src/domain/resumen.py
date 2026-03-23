"""
Entidad Resumen - Dominio
Representa el resumen financiero de una persona.
"""
from dataclasses import dataclass
from datetime import date
from typing import Dict, List, Optional


@dataclass
class ResumenMensual:
    """Resumen financiero de un mes específico."""
    
    anio: int
    mes: int
    total_ingresos: float = 0.0
    total_gastos: float = 0.0
    
    @property
    def saldo_neto(self) -> float:
        """Calcula el saldo neto del mes."""
        return self.total_ingresos - self.total_gastos
    
    @property
    def nombre_mes(self) -> str:
        """Retorna el nombre del mes en español."""
        meses = [
            "Enero", "Febrero", "Marzo", "Abril",
            "Mayo", "Junio", "Julio", "Agosto",
            "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return meses[self.mes - 1]
    
    def __str__(self) -> str:
        return f"{self.nombre_mes} {self.anio}: ${self.saldo_neto:,.2f}"


@dataclass
class ResumenCategoria:
    """Resumen por categoría."""
    
    categoria_id: int
    categoria_nombre: str
    color: str
    total: float
    cantidad: int
    porcentaje: float = 0.0
    
    def __str__(self) -> str:
        return f"{self.categoria_nombre}: ${self.total:,.2f} ({self.porcentaje:.1f}%)"


@dataclass
class ResumenPersona:
    """Resumen completo de una persona."""
    
    persona_id: int
    persona_nombre: str
    saldo_total: float = 0.0
    total_ingresos: float = 0.0
    total_gastos: float = 0.0
    cantidad_movimientos: int = 0
    resumen_mensual: Optional[ResumenMensual] = None
    gastos_por_categoria: List[ResumenCategoria] = None
    
    def __post_init__(self):
        if self.gastos_por_categoria is None:
            self.gastos_por_categoria = []
    
    @property
    def promedio_movimiento(self) -> float:
        """Calcula el promedio por movimiento."""
        if self.cantidad_movimientos == 0:
            return 0.0
        return (self.total_ingresos + self.total_gastos) / self.cantidad_movimientos
    
    def __str__(self) -> str:
        return f"Resumen de {self.persona_nombre}: Saldo ${self.saldo_total:,.2f}"
