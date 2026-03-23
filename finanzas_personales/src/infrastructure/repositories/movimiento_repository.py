"""
Repositorio de Movimiento - Infraestructura

Implementa el patrón Repository para la entidad Movimiento.
Proporciona métodos especializados para consultas financieras como
saldos, resúmenes mensuales y agrupaciones por categoría.
"""
from typing import List, Optional, Tuple
import sqlite3
from datetime import date

from ...domain.movimiento import Movimiento, TipoMovimiento
from ...domain.resumen import ResumenMensual, ResumenCategoria


class MovimientoRepository:
    """
    Repositorio para operaciones de Movimiento financiero.
    
    Además del CRUD básico, incluye métodos analíticos para:
    - Calcular saldos y totales
    - Generar resúmenes mensuales
    - Agrupar gastos por categoría
    """
    
    def __init__(self, connection: sqlite3.Connection):
        """
        Inicializa el repositorio.
        
        Args:
            connection: Conexión activa a SQLite
        """
        self._conn = connection
        self._allowed_order_by = {
            "fecha desc": "fecha DESC, id DESC",
            "fecha asc": "fecha ASC, id ASC",
            "monto desc": "monto DESC, fecha DESC, id DESC",
            "monto asc": "monto ASC, fecha ASC, id ASC",
        }
    
    def save(self, movimiento: Movimiento) -> Movimiento:
        """
        Guarda un movimiento (crea o actualiza).
        
        Args:
            movimiento: Entidad Movimiento a guardar
            
        Returns:
            Movimiento con ID asignado
        """
        cursor = self._conn.cursor()
        
        if movimiento.id is None:
            cursor.execute("""
                INSERT INTO movimiento (persona_id, fecha, tipo, categoria_id, 
                                      monto, descripcion, medio, referencia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                movimiento.persona_id,
                movimiento.fecha.isoformat(),
                movimiento.tipo.value,
                movimiento.categoria_id,
                movimiento.monto,
                movimiento.descripcion,
                movimiento.medio,
                movimiento.referencia
            ))
            movimiento.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE movimiento 
                SET fecha = ?, tipo = ?, categoria_id = ?, monto = ?,
                    descripcion = ?, medio = ?, referencia = ?
                WHERE id = ? AND persona_id = ?
            """, (
                movimiento.fecha.isoformat(),
                movimiento.tipo.value,
                movimiento.categoria_id,
                movimiento.monto,
                movimiento.descripcion,
                movimiento.medio,
                movimiento.referencia,
                movimiento.id,
                movimiento.persona_id
            ))
        
        self._conn.commit()
        return movimiento
    
    def find_by_id(self, id: int) -> Optional[Movimiento]:
        """Busca un movimiento por ID."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM movimiento WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_movimiento(row) if row else None
    
    def find_by_persona(
        self, 
        persona_id: int,
        tipo: Optional[str] = None,
        categoria_id: Optional[int] = None,
        fecha_desde: Optional[date] = None,
        fecha_hasta: Optional[date] = None,
        order_by: str = "fecha DESC"
    ) -> List[Movimiento]:
        """
        Busca movimientos de una persona con filtros opcionales.
        
        Args:
            persona_id: ID de la persona
            tipo: 'INGRESO' o 'GASTO' (opcional)
            categoria_id: Filtrar por categoría (opcional)
            fecha_desde: Fecha inicial inclusive (opcional)
            fecha_hasta: Fecha final inclusive (opcional)
            order_by: Ordenamiento SQL (default: fecha DESC)
            
        Returns:
            Lista de movimientos filtrados
        """
        cursor = self._conn.cursor()
        
        # Construir query dinámicamente según filtros
        where_clauses = ["persona_id = ?"]
        params = [persona_id]
        
        if tipo:
            where_clauses.append("tipo = ?")
            params.append(tipo)
        
        if categoria_id:
            where_clauses.append("categoria_id = ?")
            params.append(categoria_id)
        
        if fecha_desde:
            where_clauses.append("fecha >= ?")
            params.append(fecha_desde.isoformat())
        
        if fecha_hasta:
            where_clauses.append("fecha <= ?")
            params.append(fecha_hasta.isoformat())
        
        where_sql = " AND ".join(where_clauses)
        order_sql = self._resolve_order_by(order_by)
        query = f"SELECT * FROM movimiento WHERE {where_sql} ORDER BY {order_sql}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        return [self._row_to_movimiento(row) for row in rows]
    
    def delete(self, id: int) -> bool:
        """Elimina un movimiento por ID."""
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM movimiento WHERE id = ?", (id,))
        self._conn.commit()
        return cursor.rowcount > 0
    
    def get_saldo_total(self, persona_id: int) -> float:
        """
        Calcula el saldo total de una persona.
        
        Returns:
            Saldo (ingresos - gastos)
        """
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE 0 END), 0) as ingresos,
                COALESCE(SUM(CASE WHEN tipo = 'GASTO' THEN monto ELSE 0 END), 0) as gastos
            FROM movimiento
            WHERE persona_id = ?
        """, (persona_id,))
        row = cursor.fetchone()
        return row['ingresos'] - row['gastos']
    
    def get_totales(self, persona_id: int) -> Tuple[float, float]:
        """
        Obtiene los totales de ingresos y gastos.
        
        Returns:
            Tupla (total_ingresos, total_gastos)
        """
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE 0 END), 0) as ingresos,
                COALESCE(SUM(CASE WHEN tipo = 'GASTO' THEN monto ELSE 0 END), 0) as gastos
            FROM movimiento
            WHERE persona_id = ?
        """, (persona_id,))
        row = cursor.fetchone()
        return row['ingresos'], row['gastos']
    
    def get_resumen_mensual(
        self, 
        persona_id: int, 
        anio: int, 
        mes: int
    ) -> ResumenMensual:
        """
        Obtiene el resumen de un mes específico.
        
        Args:
            persona_id: ID de la persona
            anio: Año (ej: 2024)
            mes: Mes (1-12)
            
        Returns:
            ResumenMensual con los totales del mes
        """
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE 0 END), 0) as ingresos,
                COALESCE(SUM(CASE WHEN tipo = 'GASTO' THEN monto ELSE 0 END), 0) as gastos
            FROM movimiento
            WHERE persona_id = ? 
            AND strftime('%Y', fecha) = ?
            AND strftime('%m', fecha) = ?
        """, (persona_id, str(anio), f"{mes:02d}"))
        
        row = cursor.fetchone()
        return ResumenMensual(
            anio=anio,
            mes=mes,
            total_ingresos=row['ingresos'],
            total_gastos=row['gastos']
        )
    
    def get_gastos_por_categoria(
        self, 
        persona_id: int,
        anio: Optional[int] = None,
        mes: Optional[int] = None
    ) -> List[ResumenCategoria]:
        """
        Obtiene el resumen de gastos agrupados por categoría.
        
        Args:
            persona_id: ID de la persona
            anio: Filtrar por año (opcional)
            mes: Filtrar por mes (opcional)
            
        Returns:
            Lista de ResumenCategoria ordenada por total descendente
        """
        cursor = self._conn.cursor()
        
        where_clause = "m.persona_id = ? AND m.tipo = 'GASTO'"
        params = [persona_id]
        
        if anio:
            where_clause += " AND strftime('%Y', m.fecha) = ?"
            params.append(str(anio))
        
        if mes:
            where_clause += " AND strftime('%m', m.fecha) = ?"
            params.append(f"{mes:02d}")
        
        cursor.execute(f"""
            SELECT 
                c.id as categoria_id,
                c.nombre as categoria_nombre,
                c.color,
                COALESCE(SUM(m.monto), 0) as total,
                COUNT(m.id) as cantidad
            FROM categoria c
            LEFT JOIN movimiento m ON m.categoria_id = c.id AND {where_clause}
            WHERE c.tipo IN ('GASTO', 'AMBOS')
            GROUP BY c.id, c.nombre, c.color
            HAVING total > 0
            ORDER BY total DESC
        """, params)
        
        rows = cursor.fetchall()
        
        # Calcular total para porcentajes
        total_gastos = sum(row['total'] for row in rows)
        
        resultados = []
        for row in rows:
            porcentaje = (row['total'] / total_gastos * 100) if total_gastos > 0 else 0
            resultados.append(ResumenCategoria(
                categoria_id=row['categoria_id'],
                categoria_nombre=row['categoria_nombre'],
                color=row['color'],
                total=row['total'],
                cantidad=row['cantidad'],
                porcentaje=porcentaje
            ))
        
        return resultados
    
    def get_historial_mensual(
        self, 
        persona_id: int, 
        meses: int = 12
    ) -> List[ResumenMensual]:
        """
        Obtiene el historial de los últimos N meses.
        
        Args:
            persona_id: ID de la persona
            meses: Cantidad de meses hacia atrás (default: 12)
            
        Returns:
            Lista de ResumenMensual ordenada cronológicamente
        """
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT 
                CAST(strftime('%Y', fecha) AS INTEGER) as anio,
                CAST(strftime('%m', fecha) AS INTEGER) as mes,
                COALESCE(SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE 0 END), 0) as ingresos,
                COALESCE(SUM(CASE WHEN tipo = 'GASTO' THEN monto ELSE 0 END), 0) as gastos
            FROM movimiento
            WHERE persona_id = ?
            AND fecha >= date('now', ?)
            GROUP BY anio, mes
            ORDER BY anio, mes
        """, (persona_id, f'-{meses} months'))
        
        rows = cursor.fetchall()
        return [
            ResumenMensual(
                anio=row['anio'],
                mes=row['mes'],
                total_ingresos=row['ingresos'],
                total_gastos=row['gastos']
            )
            for row in rows
        ]
    
    def _row_to_movimiento(self, row: sqlite3.Row) -> Movimiento:
        """Convierte una fila de BD en objeto Movimiento."""
        return Movimiento(
            id=row['id'],
            persona_id=row['persona_id'],
            fecha=date.fromisoformat(row['fecha']),
            tipo=TipoMovimiento(row['tipo']),
            categoria_id=row['categoria_id'],
            monto=row['monto'],
            descripcion=row['descripcion'],
            medio=row['medio'],
            referencia=row['referencia']
        )

    def _resolve_order_by(self, order_by: str) -> str:
        """Restringe el ORDER BY a opciones conocidas y seguras."""
        order_key = " ".join(order_by.strip().lower().split())
        if order_key not in self._allowed_order_by:
            raise ValueError(f"Ordenamiento no soportado: {order_by}")
        return self._allowed_order_by[order_key]
