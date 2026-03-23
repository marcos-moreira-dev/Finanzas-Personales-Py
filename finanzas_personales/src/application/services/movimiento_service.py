"""
Servicio de Movimientos - Capa de Aplicación

Implementa los casos de uso relacionados con movimientos financieros
y consultas analíticas (saldos, resúmenes, gráficos).
"""
from datetime import date
from typing import List, Optional, Tuple, Union

from ...domain.movimiento import Movimiento, TipoMovimiento
from ...domain.resumen import ResumenMensual, ResumenCategoria, ResumenPersona
from ...infrastructure.repositories.movimiento_repository import MovimientoRepository


class MovimientoService:
    """
    Servicio para operaciones de movimientos financieros.
    
    Proporciona métodos para:
    - CRUD de movimientos
    - Consultas analíticas (saldos, totales)
    - Generación de resúmenes y reportes
    """
    
    def __init__(self, movimiento_repo: MovimientoRepository):
        """
        Inicializa el servicio.
        
        Args:
            movimiento_repo: Repositorio de movimientos inyectado
        """
        self._repo = movimiento_repo

    def crear_movimiento(
        self,
        persona_id: int,
        fecha: date,
        tipo: Union[TipoMovimiento, str],
        categoria_id: int,
        monto: float,
        descripcion: str = None,
        medio: str = None,
        referencia: str = None,
        es_recurrente: bool = False
    ) -> Movimiento:
        """
        Crea un movimiento segÃºn el tipo recibido.

        Mantiene compatibilidad con la capa de presentaciÃ³n, que envÃ­a
        el tipo del movimiento como parte del formulario.
        """
        if es_recurrente:
            raise ValueError("Los movimientos recurrentes aÃºn no estÃ¡n implementados.")

        tipo_normalizado = self._normalizar_tipo(tipo)
        if tipo_normalizado == TipoMovimiento.INGRESO:
            return self.registrar_ingreso(
                persona_id=persona_id,
                fecha=fecha,
                categoria_id=categoria_id,
                monto=monto,
                descripcion=descripcion,
                medio=medio,
                referencia=referencia
            )

        return self.registrar_gasto(
            persona_id=persona_id,
            fecha=fecha,
            categoria_id=categoria_id,
            monto=monto,
            descripcion=descripcion,
            medio=medio,
            referencia=referencia
        )
    
    def registrar_ingreso(
        self,
        persona_id: int,
        fecha: date,
        categoria_id: int,
        monto: float,
        descripcion: str = None,
        medio: str = None,
        referencia: str = None
    ) -> Movimiento:
        """
        Caso de uso: Registrar un ingreso.
        
        Args:
            persona_id: ID de la persona
            fecha: Fecha del ingreso
            categoria_id: ID de la categoría
            monto: Monto positivo
            descripcion: Descripción opcional
            medio: Medio de pago
            referencia: Referencia externa
            
        Returns:
            Movimiento creado
        """
        movimiento = Movimiento(
            persona_id=persona_id,
            fecha=fecha,
            tipo=TipoMovimiento.INGRESO,
            categoria_id=categoria_id,
            monto=monto,
            descripcion=descripcion,
            medio=medio,
            referencia=referencia
        )
        return self._repo.save(movimiento)
    
    def registrar_gasto(
        self,
        persona_id: int,
        fecha: date,
        categoria_id: int,
        monto: float,
        descripcion: str = None,
        medio: str = None,
        referencia: str = None
    ) -> Movimiento:
        """
        Caso de uso: Registrar un gasto.
        
        Args:
            persona_id: ID de la persona
            fecha: Fecha del gasto
            categoria_id: ID de la categoría
            monto: Monto positivo
            descripcion: Descripción opcional
            medio: Medio de pago
            referencia: Referencia externa
            
        Returns:
            Movimiento creado
        """
        movimiento = Movimiento(
            persona_id=persona_id,
            fecha=fecha,
            tipo=TipoMovimiento.GASTO,
            categoria_id=categoria_id,
            monto=monto,
            descripcion=descripcion,
            medio=medio,
            referencia=referencia
        )
        return self._repo.save(movimiento)
    
    def obtener_movimiento(self, movimiento_id: int) -> Optional[Movimiento]:
        """Obtiene un movimiento por ID."""
        return self._repo.find_by_id(movimiento_id)
    
    def listar_movimientos(
        self,
        persona_id: int,
        tipo: str = None,
        categoria_id: int = None,
        fecha_desde: date = None,
        fecha_hasta: date = None
    ) -> List[Movimiento]:
        """
        Lista movimientos con filtros.
        
        Args:
            persona_id: ID de la persona
            tipo: 'INGRESO' o 'GASTO' (opcional)
            categoria_id: Filtrar por categoría (opcional)
            fecha_desde: Fecha inicial (opcional)
            fecha_hasta: Fecha final (opcional)
            
        Returns:
            Lista de movimientos filtrados
        """
        return self._repo.find_by_persona(
            persona_id=persona_id,
            tipo=tipo,
            categoria_id=categoria_id,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta
        )
    
    def actualizar_movimiento(
        self,
        movimiento_id: int,
        fecha: date = None,
        tipo: Union[TipoMovimiento, str] = None,
        categoria_id: int = None,
        monto: float = None,
        descripcion: str = None,
        medio: str = None,
        referencia: str = None,
        es_recurrente: bool = False
    ) -> Movimiento:
        """
        Actualiza un movimiento existente.
        
        Args:
            movimiento_id: ID del movimiento
            ...campos a actualizar
            
        Returns:
            Movimiento actualizado
        """
        movimiento = self._repo.find_by_id(movimiento_id)
        if not movimiento:
            raise ValueError(f"No existe movimiento con ID {movimiento_id}")

        if es_recurrente:
            raise ValueError("Los movimientos recurrentes aÃºn no estÃ¡n implementados.")

        cambios = {}
        if fecha is not None:
            cambios["fecha"] = fecha
        if tipo is not None:
            cambios["tipo"] = self._normalizar_tipo(tipo)
        if categoria_id is not None:
            cambios["categoria_id"] = categoria_id
        if monto is not None:
            cambios["monto"] = monto
        if descripcion is not None:
            cambios["descripcion"] = descripcion
        if medio is not None:
            cambios["medio"] = medio
        if referencia is not None:
            cambios["referencia"] = referencia

        movimiento_actualizado = movimiento.actualizado(**cambios) if cambios else movimiento
        return self._repo.save(movimiento_actualizado)
    
    def eliminar_movimiento(self, movimiento_id: int) -> bool:
        """Elimina un movimiento."""
        return self._repo.delete(movimiento_id)
    
    # ===== MÉTODOS ANALÍTICOS =====
    
    def obtener_saldo(self, persona_id: int) -> float:
        """
        Obtiene el saldo total de una persona.
        
        Returns:
            Saldo (ingresos - gastos)
        """
        return self._repo.get_saldo_total(persona_id)
    
    def obtener_totales(self, persona_id: int) -> Tuple[float, float]:
        """
        Obtiene totales de ingresos y gastos.
        
        Returns:
            Tupla (ingresos, gastos)
        """
        return self._repo.get_totales(persona_id)
    
    def obtener_resumen_mensual(
        self, 
        persona_id: int, 
        anio: int = None, 
        mes: int = None
    ) -> ResumenMensual:
        """
        Obtiene resumen del mes especificado o mes actual.
        
        Args:
            persona_id: ID de la persona
            anio: Año (default: año actual)
            mes: Mes (default: mes actual)
            
        Returns:
            ResumenMensual con totales
        """
        if anio is None:
            anio = date.today().year
        if mes is None:
            mes = date.today().month
            
        return self._repo.get_resumen_mensual(persona_id, anio, mes)
    
    def obtener_gastos_por_categoria(
        self,
        persona_id: int,
        anio: int = None,
        mes: int = None
    ) -> List[ResumenCategoria]:
        """
        Obtiene gastos agrupados por categoría.
        
        Args:
            persona_id: ID de la persona
            anio: Filtrar por año (opcional)
            mes: Filtrar por mes (opcional)
            
        Returns:
            Lista de resúmenes por categoría
        """
        return self._repo.get_gastos_por_categoria(persona_id, anio, mes)
    
    def obtener_historial_mensual(
        self, 
        persona_id: int, 
        meses: int = 12
    ) -> List[ResumenMensual]:
        """
        Obtiene historial de los últimos N meses.
        
        Args:
            persona_id: ID de la persona
            meses: Cantidad de meses (default: 12)
            
        Returns:
            Lista de resúmenes mensuales
        """
        return self._repo.get_historial_mensual(persona_id, meses)
    
    def generar_resumen_completo(
        self,
        persona_id: int,
        persona_nombre: str
    ) -> ResumenPersona:
        """
        Genera un resumen completo de la situación financiera.
        
        Args:
            persona_id: ID de la persona
            persona_nombre: Nombre para mostrar
            
        Returns:
            ResumenPersona con toda la información
        """
        ingresos, gastos = self._repo.get_totales(persona_id)
        saldo = ingresos - gastos
        
        # Contar movimientos
        movimientos = self._repo.find_by_persona(persona_id)
        cantidad = len(movimientos)
        
        # Resumen del mes actual
        resumen_mensual = self._repo.get_resumen_mensual(
            persona_id, 
            date.today().year, 
            date.today().month
        )
        
        # Gastos por categoría del mes actual
        gastos_categoria = self._repo.get_gastos_por_categoria(
            persona_id,
            date.today().year,
            date.today().month
        )
        
        return ResumenPersona(
            persona_id=persona_id,
            persona_nombre=persona_nombre,
            saldo_total=saldo,
            total_ingresos=ingresos,
            total_gastos=gastos,
            cantidad_movimientos=cantidad,
            resumen_mensual=resumen_mensual,
            gastos_por_categoria=gastos_categoria
        )

    def _normalizar_tipo(self, tipo: Union[TipoMovimiento, str]) -> TipoMovimiento:
        """Convierte cadenas y enums al tipo de dominio."""
        if isinstance(tipo, TipoMovimiento):
            return tipo

        if isinstance(tipo, str):
            try:
                return TipoMovimiento(tipo.strip().upper())
            except ValueError as exc:
                raise ValueError(f"Tipo de movimiento no vÃ¡lido: {tipo}") from exc

        raise ValueError(f"Tipo de movimiento no soportado: {tipo!r}")
