"""
Repositorio de Categoria - Infraestructura

Implementa el patrón Repository para la entidad Categoria.
Gestiona las categorías de ingresos y gastos.
"""
from typing import List, Optional
import sqlite3

from ...domain.categoria import Categoria, TipoCategoria


class CategoriaRepository:
    """
    Repositorio para operaciones de Categoría.
    
    Las categorías son compartidas entre todas las personas,
    pero pueden filtrarse por tipo según el contexto.
    """
    
    def __init__(self, connection: sqlite3.Connection):
        """
        Inicializa el repositorio.
        
        Args:
            connection: Conexión activa a SQLite
        """
        self._conn = connection
    
    def save(self, categoria: Categoria) -> Categoria:
        """
        Guarda una categoría (crea o actualiza).
        
        Args:
            categoria: Entidad Categoria a guardar
            
        Returns:
            Categoria con ID asignado
        """
        cursor = self._conn.cursor()
        
        if categoria.id is None:
            cursor.execute("""
                INSERT INTO categoria (nombre, tipo, color, activa, descripcion)
                VALUES (?, ?, ?, ?, ?)
            """, (
                categoria.nombre,
                categoria.tipo.value,
                categoria.color,
                categoria.activa,
                categoria.descripcion
            ))
            categoria.id = cursor.lastrowid
        else:
            cursor.execute("""
                UPDATE categoria 
                SET nombre = ?, tipo = ?, color = ?, activa = ?, descripcion = ?
                WHERE id = ?
            """, (
                categoria.nombre,
                categoria.tipo.value,
                categoria.color,
                categoria.activa,
                categoria.descripcion,
                categoria.id
            ))
        
        self._conn.commit()
        return categoria
    
    def find_by_id(self, id: int) -> Optional[Categoria]:
        """Busca una categoría por ID."""
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM categoria WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_categoria(row) if row else None
    
    def find_all(
        self, 
        tipo: Optional[str] = None, 
        solo_activas: bool = True
    ) -> List[Categoria]:
        """
        Obtiene todas las categorías con filtros opcionales.
        
        Args:
            tipo: 'INGRESO', 'GASTO' o 'AMBOS' (opcional)
            solo_activas: Si True, solo retorna categorías activas
            
        Returns:
            Lista de categorías ordenadas por nombre
        """
        cursor = self._conn.cursor()
        
        where_clauses = []
        params = []
        
        if tipo:
            # Incluir 'AMBOS' si se filtra por tipo específico
            where_clauses.append("(tipo = ? OR tipo = 'AMBOS')")
            params.append(tipo)
        
        if solo_activas:
            where_clauses.append("activa = 1")
        
        where_sql = " AND ".join(where_clauses) if where_clauses else "1=1"
        
        cursor.execute(f"""
            SELECT * FROM categoria 
            WHERE {where_sql}
            ORDER BY tipo, nombre
        """, params)
        
        rows = cursor.fetchall()
        return [self._row_to_categoria(row) for row in rows]
    
    def find_by_tipo_movimiento(self, tipo_movimiento: str) -> List[Categoria]:
        """
        Obtiene categorías compatibles con un tipo de movimiento.
        
        Args:
            tipo_movimiento: 'INGRESO' o 'GASTO'
            
        Returns:
            Lista de categorías activas que pueden usarse
        """
        cursor = self._conn.cursor()
        cursor.execute("""
            SELECT * FROM categoria 
            WHERE activa = 1 
            AND (tipo = ? OR tipo = 'AMBOS')
            ORDER BY nombre
        """, (tipo_movimiento,))
        
        rows = cursor.fetchall()
        return [self._row_to_categoria(row) for row in rows]
    
    def delete(self, id: int) -> bool:
        """
        Elimina una categoría por ID.
        
        Nota: Solo debería eliminarse si no tiene movimientos asociados.
        """
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM categoria WHERE id = ?", (id,))
        self._conn.commit()
        return cursor.rowcount > 0
    
    def tiene_movimientos(self, categoria_id: int) -> bool:
        """
        Verifica si una categoría tiene movimientos asociados.
        
        Returns:
            True si tiene movimientos, False si está libre
        """
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT 1 FROM movimiento WHERE categoria_id = ? LIMIT 1", 
            (categoria_id,)
        )
        return cursor.fetchone() is not None
    
    def _row_to_categoria(self, row: sqlite3.Row) -> Categoria:
        """Convierte una fila de BD en objeto Categoria."""
        return Categoria(
            id=row['id'],
            nombre=row['nombre'],
            tipo=TipoCategoria(row['tipo']),
            color=row['color'],
            activa=bool(row['activa']),
            descripcion=row['descripcion']
        )
