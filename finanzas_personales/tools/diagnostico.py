"""
Diagnostico rapido de la base de datos local.

Este script no forma parte del flujo normal de la aplicacion. Se deja en
`tools/` como apoyo de estudio y soporte tecnico para revisar:
- si la base existe;
- que tablas fueron creadas;
- cuantas personas, categorias y movimientos hay cargados.

Uso:
    python tools/diagnostico.py
"""

import os
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.infrastructure.config.settings import Config
from src.infrastructure.db.database import Database


def main():
    """Ejecuta el diagnostico y muestra un resumen de estado."""
    print("=" * 60)
    print("DIAGNOSTICO DE BASE DE DATOS")
    print("=" * 60)
    print()

    print(f"Ruta de BD: {Config.DB_PATH}")
    print(f"Directorio de datos: {Config.DATA_DIR}")
    print()

    if os.path.exists(Config.DB_PATH):
        print("[OK] Base de datos encontrada")
        print(f"     Tamano: {os.path.getsize(Config.DB_PATH)} bytes")
    else:
        print("[ERROR] La base de datos todavia no existe")
        print()
        sys.exit(1)

    print()

    with Database(str(Config.DB_PATH)) as db:
        conn = db.get_connection()
        cursor = conn.cursor()

        print("TABLAS EN LA BASE DE DATOS:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        for table_name, in cursor.fetchall():
            print(f"  - {table_name}")
        print()

        print("PERSONAS:")
        cursor.execute("SELECT COUNT(*) FROM persona")
        personas = cursor.fetchone()[0]
        print(f"  Total: {personas}")

        if personas > 0:
            print("\n  Lista de personas:")
            cursor.execute("SELECT id, nombres, apellidos FROM persona ORDER BY apellidos")
            for persona_id, nombres, apellidos in cursor.fetchall():
                print(f"  - {persona_id}: {apellidos}, {nombres}")
        else:
            print("\n  No hay personas registradas")
            print("  Puede cargar datos demo con:")
            print("  python src/infrastructure/db/seeds_demo.py")
        print()

        print("CATEGORIAS:")
        cursor.execute("SELECT COUNT(*) FROM categoria")
        categorias = cursor.fetchone()[0]
        print(f"  Total: {categorias}")

        if categorias > 0:
            cursor.execute("SELECT tipo, COUNT(*) FROM categoria GROUP BY tipo")
            for tipo, cantidad in cursor.fetchall():
                print(f"  - {tipo}: {cantidad}")
        print()

        print("MOVIMIENTOS:")
        cursor.execute("SELECT COUNT(*) FROM movimiento")
        movimientos = cursor.fetchone()[0]
        print(f"  Total: {movimientos}")

        if movimientos > 0:
            cursor.execute(
                """
                SELECT p.nombres || ' ' || p.apellidos, COUNT(*)
                FROM movimiento m
                JOIN persona p ON m.persona_id = p.id
                GROUP BY p.id
                ORDER BY COUNT(*) DESC
                """
            )
            print("\n  Por persona:")
            for nombre, cantidad in cursor.fetchall():
                print(f"  - {nombre}: {cantidad} movimientos")
        print()

    print("=" * 60)
    print("FIN DEL DIAGNOSTICO")
    print("=" * 60)


if __name__ == "__main__":
    main()
