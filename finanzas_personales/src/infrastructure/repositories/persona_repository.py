"""
Repositorio de Persona - Infraestructura

Este módulo implementa el patrón Repository para la entidad Persona.
El patrón Repository encapsula la lógica de acceso a datos, permitiendo
que la capa de dominio no dependa de detalles de implementación de base de datos.

Patrón: Repository Pattern
- Abstrae el acceso a datos
- Permite cambiar la base de datos sin afectar el dominio
- Facilita el testing mediante mocks
"""
from typing import List, Optional
import sqlite3
from datetime import date

from ...domain.persona import Persona


class PersonaRepository:
    """
    Repositorio para operaciones CRUD de Persona.
    
    Responsabilidades:
    - Crear, leer, actualizar y eliminar personas
    - Buscar personas por diferentes criterios
    - Mapear entre la base de datos y objetos de dominio
    
    Nota: No contiene lógica de negocio, solo persistencia.
    """
    
    def __init__(self, connection: sqlite3.Connection):
        """
        Inicializa el repositorio con una conexión a la base de datos.
        
        Args:
            connection: Conexión activa a SQLite
        """
        self._conn = connection
    
    def save(self, persona: Persona) -> Persona:
        """
        Guarda una persona (crea o actualiza).
        
        Si persona.id es None, crea un nuevo registro.
        Si persona.id existe, actualiza el registro existente.
        
        Args:
            persona: Entidad Persona a guardar
            
        Returns:
            Persona con el ID asignado (en caso de creación)
        """
        cursor = self._conn.cursor()
        
        if persona.id is None:
            # INSERT: Crear nueva persona
            cursor.execute("""
                INSERT INTO persona (nombres, apellidos, identificacion, 
                                   telefono, correo, fecha_registro, 
                                   observaciones, foto_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                persona.nombres,
                persona.apellidos,
                persona.identificacion,
                persona.telefono,
                persona.correo,
                persona.fecha_registro.isoformat(),
                persona.observaciones,
                persona.foto_path
            ))
            persona.id = cursor.lastrowid
        else:
            # UPDATE: Actualizar persona existente
            cursor.execute("""
                UPDATE persona 
                SET nombres = ?, apellidos = ?, identificacion = ?,
                    telefono = ?, correo = ?, observaciones = ?, foto_path = ?
                WHERE id = ?
            """, (
                persona.nombres,
                persona.apellidos,
                persona.identificacion,
                persona.telefono,
                persona.correo,
                persona.observaciones,
                persona.foto_path,
                persona.id
            ))
        
        self._conn.commit()
        return persona
    
    def find_by_id(self, id: int) -> Optional[Persona]:
        """
        Busca una persona por su ID.
        
        Args:
            id: Identificador único de la persona
            
        Returns:
            Persona si existe, None si no se encuentra
        """
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM persona WHERE id = ?", (id,))
        row = cursor.fetchone()
        
        if row:
            return self._row_to_persona(row)
        return None
    
    def find_all(self, search_term: str = None) -> List[Persona]:
        """
        Obtiene todas las personas, opcionalmente filtradas.
        
        Args:
            search_term: Término de búsqueda para nombres/apellidos (opcional)
            
        Returns:
            Lista de personas ordenadas alfabéticamente
        """
        cursor = self._conn.cursor()
        
        if search_term:
            # Búsqueda con filtro (LIKE para búsqueda parcial)
            search_pattern = f"%{search_term}%"
            cursor.execute("""
                SELECT * FROM persona 
                WHERE nombres LIKE ? OR apellidos LIKE ?
                ORDER BY apellidos, nombres
            """, (search_pattern, search_pattern))
        else:
            # Sin filtro: traer todas
            cursor.execute("SELECT * FROM persona ORDER BY apellidos, nombres")
        
        rows = cursor.fetchall()
        return [self._row_to_persona(row) for row in rows]
    
    def delete(self, id: int) -> bool:
        """
        Elimina una persona por su ID.
        
        Args:
            id: Identificador de la persona a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM persona WHERE id = ?", (id,))
        self._conn.commit()
        return cursor.rowcount > 0
    
    def exists(self, id: int) -> bool:
        """
        Verifica si existe una persona con el ID dado.
        
        Args:
            id: Identificador a verificar
            
        Returns:
            True si existe, False en caso contrario
        """
        cursor = self._conn.cursor()
        cursor.execute("SELECT 1 FROM persona WHERE id = ?", (id,))
        return cursor.fetchone() is not None
    
    def _row_to_persona(self, row: sqlite3.Row) -> Persona:
        """
        Convierte una fila de la base de datos en un objeto Persona.
        
        Este método es privado (underscore) porque es un detalle interno
        de implementación. Realiza el mapeo entre el esquema de la BD
        y los atributos de la entidad de dominio.
        
        Args:
            row: Fila de la base de datos (sqlite3.Row)
            
        Returns:
            Instancia de Persona poblada con los datos
        """
        # Convertir fecha de string a objeto date de Python
        fecha_registro = date.fromisoformat(row['fecha_registro']) if row['fecha_registro'] else date.today()
        
        return Persona(
            id=row['id'],
            nombres=row['nombres'],
            apellidos=row['apellidos'],
            identificacion=row['identificacion'],
            telefono=row['telefono'],
            correo=row['correo'],
            fecha_registro=fecha_registro,
            observaciones=row['observaciones'],
            foto_path=row['foto_path']
        )
