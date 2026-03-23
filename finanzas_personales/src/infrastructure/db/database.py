"""
Configuración y gestión de la base de datos SQLite.

Este módulo es responsable de:
- Establecer la conexión con SQLite
- Crear el esquema de tablas
- Inicializar datos base mediante seeds desacoplados

Principio: Single Responsibility - Solo gestiona la base de datos,
no contiene lógica de negocio ni datos iniciales hardcodeados.
"""
import sqlite3
import os
from pathlib import Path

from .seeds import get_categorias_seeds


class Database:
    """Gestiona la conexión y esquema de la base de datos."""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            # Ruta por defecto: data/finanzas.db
            base_dir = Path(__file__).parent.parent.parent.parent
            db_path = base_dir / "data" / "finanzas.db"
        
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._connection = None
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos."""
        if self._connection is None:
            self._connection = sqlite3.connect(str(self.db_path))
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
        return self._connection
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if self._connection:
            self._connection.close()
            self._connection = None
    
    def init_schema(self):
        """Inicializa el esquema de la base de datos."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla persona
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS persona (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombres TEXT NOT NULL,
                apellidos TEXT NOT NULL,
                identificacion TEXT UNIQUE,
                telefono TEXT,
                correo TEXT,
                fecha_registro DATE DEFAULT CURRENT_DATE,
                observaciones TEXT,
                foto_path TEXT
            )
        """)
        
        # Tabla categoria
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS categoria (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL UNIQUE,
                tipo TEXT NOT NULL CHECK (tipo IN ('INGRESO', 'GASTO', 'AMBOS')),
                color TEXT DEFAULT '#808080',
                activa BOOLEAN DEFAULT 1,
                descripcion TEXT
            )
        """)
        
        # Tabla movimiento
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimiento (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                persona_id INTEGER NOT NULL,
                fecha DATE NOT NULL,
                tipo TEXT NOT NULL CHECK (tipo IN ('INGRESO', 'GASTO')),
                categoria_id INTEGER NOT NULL,
                monto REAL NOT NULL CHECK (monto > 0),
                descripcion TEXT,
                medio TEXT,
                referencia TEXT,
                FOREIGN KEY (persona_id) REFERENCES persona(id) ON DELETE CASCADE,
                FOREIGN KEY (categoria_id) REFERENCES categoria(id)
            )
        """)
        
        # Índices
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_movimiento_persona 
            ON movimiento(persona_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_movimiento_fecha 
            ON movimiento(fecha)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_movimiento_categoria 
            ON movimiento(categoria_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_persona_nombre 
            ON persona(nombres, apellidos)
        """)
        
        conn.commit()
        self._insert_categorias_seeds(cursor)
        conn.commit()
    
    def _insert_categorias_seeds(self, cursor):
        """
        Inserta categorías iniciales desde el módulo seeds desacoplado.
        
        Este método usa OR IGNORE para no sobrescribir categorías existentes,
        permitiendo que el usuario personalice sin perder sus cambios.
        """
        # Obtener seeds del módulo desacoplado
        categorias_seeds = get_categorias_seeds()
        
        for categoria in categorias_seeds:
            cursor.execute("""
                INSERT OR IGNORE INTO categoria (nombre, tipo, color, descripcion)
                VALUES (?, ?, ?, ?)
            """, (categoria.nombre, categoria.tipo.value, categoria.color, categoria.descripcion))
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
