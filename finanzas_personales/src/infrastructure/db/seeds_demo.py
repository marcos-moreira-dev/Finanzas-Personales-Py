"""
Seeds de Datos de Ejemplo - Para Pruebas y Demo

Este módulo genera datos realistas de personas y movimientos
para facilitar las pruebas y demostración de la aplicación.

Uso:
    python seeds_demo.py

O desde la aplicación:
    from src.infrastructure.db.seeds_demo import cargar_datos_demo
    cargar_datos_demo(connection)
"""
import sqlite3
import random
from datetime import datetime, timedelta
from typing import List, Dict

# Datos de ejemplo realistas
NOMBRES = [
    ("Juan", "Pérez García"),
    ("María", "López Martínez"),
    ("Carlos", "Rodríguez Silva"),
    ("Ana", "Martínez Torres"),
    ("Pedro", "Gómez Sánchez"),
    ("Laura", "Hernández Ruiz"),
    ("Miguel", "Díaz Morales"),
    ("Carmen", "Jiménez Castro"),
    ("José", "Vargas Luna"),
    ("Patricia", "Flores Reyes"),
]

TELEFONOS = [
    "555-0100", "555-0101", "555-0102", "555-0103", "555-0104",
    "555-0105", "555-0106", "555-0107", "555-0108", "555-0109"
]

CORREOS = [
    "juan.perez@email.com",
    "maria.lopez@email.com",
    "carlos.rodriguez@email.com",
    "ana.martinez@email.com",
    "pedro.gomez@email.com",
    "laura.hernandez@email.com",
    "miguel.diaz@email.com",
    "carmen.jimenez@email.com",
    "jose.vargas@email.com",
    "patricia.flores@email.com",
]

IDENTIFICACIONES = [
    "12345678-9", "23456789-0", "34567890-1", "45678901-2", "56789012-3",
    "67890123-4", "78901234-5", "89012345-6", "90123456-7", "01234567-8"
]

DESCRIPCIONES_PERSONA = [
    "Cliente desde 2023. Interesado en ahorro.",
    "Trabajador independiente. Requiere reportes mensuales.",
    "Empleado corporativo. Ingresos estables.",
    "Emprendedora. Freelance en diseño.",
    "Consultor financiero. Necesita categorías detalladas.",
    "Estudiante de posgrado. Presupuesto ajustado.",
    "Profesor universitario. Ingresos regulares.",
    "Dueño de negocio familiar. Variabilidad en ingresos.",
    "Médico especialista. Altos ingresos.",
    "Ingeniera de software. Trabajo remoto.",
]

# Descripciones de movimientos por categoría
MOVIMIENTOS_POR_CATEGORIA = {
    "Sueldo": [
        "Sueldo mensual",
        "Pago de nómina",
        "Salario quincenal",
        "Remuneración mensual",
    ],
    "Freelance": [
        "Proyecto web cliente A",
        "Consultoría marketing",
        "Diseño logo empresa",
        "Desarrollo app móvil",
        "Redacción contenidos",
    ],
    "Inversiones": [
        "Dividendos acciones",
        "Intereses cuenta ahorro",
        "Rendimiento fondo",
        "Criptomonedas",
    ],
    "Ventas": [
        "Venta artículo usado",
        "Productos marketplace",
        "Venta garaje",
        "Artesanías vendidas",
    ],
    "Regalos": [
        "Regalo cumpleaños",
        "Dinero de familia",
        "Bono navideño",
        "Reembolso amigo",
    ],
    "Alimentación": [
        "Supermercado semanal",
        "Comida rápida",
        "Restaurante fin de semana",
        "Cafetería trabajo",
        "Delivery pizza",
    ],
    "Transporte": [
        "Gasolina",
        "Transporte público",
        "Uber/Taxi",
        "Mantenimiento auto",
        "Estacionamiento",
        "Lavado auto",
    ],
    "Vivienda": [
        "Pago de renta",
        "Hipoteca mensual",
        "Servicio eléctrico",
        "Agua potable",
        "Gas doméstico",
        "Internet y cable",
        "Mantenimiento hogar",
    ],
    "Salud": [
        "Consulta médica",
        "Medicamentos",
        "Seguro médico",
        "Exámenes laboratorio",
        "Dentista",
        "Lentes óptica",
    ],
    "Educación": [
        "Mensualidad universidad",
        "Curso online",
        "Libros y materiales",
        "Taller especializado",
        "Suscripción educativa",
    ],
    "Entretenimiento": [
        "Cine",
        "Suscripción Netflix",
        "Spotify Premium",
        "Videojuegos",
        "Salida con amigos",
        "Concierto",
    ],
    "Ropa": [
        "Ropa trabajo",
        "Zapatos",
        "Accesorios",
        "Lavandería",
        "Reparación ropa",
    ],
    "Tecnología": [
        "Celular nuevo",
        "Laptop trabajo",
        "Software licencia",
        "Accesorios",
        "Reparación equipo",
    ],
    "Mascotas": [
        "Alimento perro",
        "Veterinaria",
        "Vacunas",
        "Juguetes",
        "Grooming",
    ],
    "Viajes": [
        "Hotel fin de semana",
        "Vuelos",
        "Gasolina viaje",
        "Comidas viaje",
        "Souvenirs",
    ],
    "Ahorro": [
        "Transferencia ahorro",
        "Fondo emergencia",
        "Inversión mensual",
        "Ahorro vacaciones",
    ],
    "Impuestos": [
        "Pago impuesto renta",
        "IVA declaración",
        "Tasa municipal",
        "Impuesto vehículo",
    ],
    "Seguros": [
        "Seguro auto",
        "Seguro vida",
        "Seguro hogar",
        "Seguro médico",
    ],
    "Otros Gastos": [
        "Donación",
        "Regalo",
        "Gastos varios",
        "Imprevisto",
    ],
}


def generar_fecha_aleatoria(inicio: datetime, fin: datetime) -> datetime:
    """Genera una fecha aleatoria entre dos fechas."""
    delta = fin - inicio
    segundos = random.randint(0, int(delta.total_seconds()))
    return inicio + timedelta(seconds=segundos)


def generar_monto(tipo: str, categoria: str) -> float:
    """Genera un monto realista según tipo y categoría."""
    rangos = {
        "Sueldo": (2000, 5000),
        "Freelance": (300, 2000),
        "Inversiones": (50, 500),
        "Ventas": (50, 800),
        "Regalos": (20, 300),
        "Alimentación": (20, 200),
        "Transporte": (10, 100),
        "Vivienda": (500, 1500),
        "Salud": (30, 300),
        "Educación": (50, 500),
        "Entretenimiento": (10, 100),
        "Ropa": (30, 200),
        "Tecnología": (100, 2000),
        "Mascotas": (20, 150),
        "Viajes": (200, 2000),
        "Ahorro": (100, 1000),
        "Impuestos": (100, 1000),
        "Seguros": (50, 300),
        "Otros Gastos": (10, 200),
        "Otros Ingresos": (20, 500),
    }
    
    min_val, max_val = rangos.get(categoria, (10, 500))
    return round(random.uniform(min_val, max_val), 2)


def obtener_categorias_por_tipo(cursor, tipo: str) -> List[Dict]:
    """Obtiene categorías activas por tipo."""
    cursor.execute("""
        SELECT id, nombre, tipo FROM categoria 
        WHERE activa = 1 AND (tipo = ? OR tipo = 'AMBOS')
    """, (tipo,))
    
    return [
        {"id": row[0], "nombre": row[1], "tipo": row[2]}
        for row in cursor.fetchall()
    ]


def crear_persona_demo(cursor, index: int) -> int:
    """Crea una persona de ejemplo."""
    nombre, apellido = NOMBRES[index]
    telefono = TELEFONOS[index]
    correo = CORREOS[index]
    identificacion = IDENTIFICACIONES[index]
    observaciones = DESCRIPCIONES_PERSONA[index]
    
    # Fecha de registro aleatoria entre 2023 y ahora
    fecha_registro = generar_fecha_aleatoria(
        datetime(2023, 1, 1),
        datetime.now()
    ).strftime('%Y-%m-%d')
    
    cursor.execute("""
        INSERT OR IGNORE INTO persona 
        (nombres, apellidos, identificacion, telefono, correo, fecha_registro, observaciones)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (nombre, apellido, identificacion, telefono, correo, fecha_registro, observaciones))
    
    return cursor.lastrowid


def crear_movimiento_demo(
    cursor,
    persona_id: int,
    categoria_id: int,
    categoria_nombre: str,
    tipo: str,
    fecha: datetime
):
    """Crea un movimiento de ejemplo."""
    # Obtener descripción aleatoria de la categoría
    descripciones = MOVIMIENTOS_POR_CATEGORIA.get(
        categoria_nombre,
        ["Movimiento general"]
    )
    descripcion = random.choice(descripciones)
    
    # Generar monto
    monto = generar_monto(tipo, categoria_nombre)
    
    # Medio de pago aleatorio
    medios = ["EFECTIVO", "TRANSFERENCIA", "TARJETA", "CHEQUE"]
    medio = random.choice(medios)
    
    # Referencia opcional
    referencia = None
    if random.random() > 0.7:  # 30% de probabilidad
        referencia = f"REF-{fecha.year}-{random.randint(100, 999)}"
    
    cursor.execute("""
        INSERT INTO movimiento 
        (persona_id, fecha, tipo, categoria_id, monto, descripcion, medio, referencia)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        persona_id,
        fecha.strftime('%Y-%m-%d'),
        tipo,
        categoria_id,
        monto,
        descripcion,
        medio,
        referencia
    ))


def cargar_datos_demo(connection: sqlite3.Connection):
    """
    Carga datos de ejemplo completos en la base de datos.
    
    Crea:
    - 5 personas con datos realistas
    - 30-50 movimientos por persona (ingresos y gastos)
    - Distribución temporal de los últimos 6 meses
    """
    cursor = connection.cursor()
    
    print("🚀 Cargando datos de ejemplo...")
    print()
    
    # Verificar si ya existen datos
    cursor.execute("SELECT COUNT(*) FROM persona")
    count_personas = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM movimiento")
    count_movimientos = cursor.fetchone()[0]
    
    if count_personas > 0 or count_movimientos > 0:
        print(f"⚠️  Ya existen datos:")
        print(f"   - {count_personas} personas")
        print(f"   - {count_movimientos} movimientos")
        print()
        respuesta = input("¿Desea borrar los datos existentes y crear nuevos? (s/n): ")
        if respuesta.lower() != 's':
            print("❌ Operación cancelada.")
            return
        
        # Borrar datos existentes
        cursor.execute("DELETE FROM movimiento")
        cursor.execute("DELETE FROM persona")
        connection.commit()
        print("🗑️  Datos existentes eliminados.")
        print()
    
    # Crear personas
    personas_creadas = []
    print("👥 Creando personas...")
    
    for i in range(min(5, len(NOMBRES))):
        persona_id = crear_persona_demo(cursor, i)
        if persona_id:
            personas_creadas.append(persona_id)
            nombre_completo = f"{NOMBRES[i][0]} {NOMBRES[i][1]}"
            print(f"   ✅ {nombre_completo}")
    
    connection.commit()
    print(f"   {len(personas_creadas)} personas creadas")
    print()
    
    # Obtener categorías
    categorias_ingreso = obtener_categorias_por_tipo(cursor, "INGRESO")
    categorias_gasto = obtener_categorias_por_tipo(cursor, "GASTO")
    
    # Crear movimientos
    print("💰 Creando movimientos...")
    
    fecha_fin = datetime.now()
    fecha_inicio = fecha_fin - timedelta(days=180)  # Últimos 6 meses
    
    total_movimientos = 0
    
    # Perfiles financieros diferentes para cada persona
    perfiles = [
        {'nombre': 'Ahorrador', 'sueldo': 3500, 'gasto_base': 2000, 'variacion': 0.1},
        {'nombre': 'Gastador', 'sueldo': 4000, 'gasto_base': 3800, 'variacion': 0.3},
        {'nombre': 'Equilibrado', 'sueldo': 3000, 'gasto_base': 2500, 'variacion': 0.2},
        {'nombre': 'Inestable', 'sueldo': 2500, 'gasto_base': 2200, 'variacion': 0.4},
        {'nombre': 'Inversionista', 'sueldo': 5000, 'gasto_base': 3000, 'variacion': 0.15},
    ]
    
    for idx, persona_id in enumerate(personas_creadas):
        perfil = perfiles[idx % len(perfiles)]
        
        # Generar 6 meses de datos
        for mes_offset in range(6):
            fecha_mes = fecha_fin - timedelta(days=30*mes_offset)
            
            # === INGRESOS ===
            # Sueldo fijo a fin de mes (con pequeña variación)
            sueldo_cat = next((c for c in categorias_ingreso if c['nombre'] == 'Sueldo'), None)
            if sueldo_cat:
                sueldo_variado = perfil['sueldo'] * random.uniform(0.95, 1.05)
                fecha_sueldo = fecha_mes - timedelta(days=random.randint(1, 5))
                cursor.execute("""
                    INSERT INTO movimiento 
                    (persona_id, fecha, tipo, categoria_id, monto, descripcion, medio)
                    VALUES (?, ?, 'INGRESO', ?, ?, 'Sueldo mensual', 'TRANSFERENCIA')
                """, (persona_id, fecha_sueldo.strftime('%Y-%m-%d'), 
                     sueldo_cat['id'], round(sueldo_variado, 2)))
                total_movimientos += 1
            
            # Ingresos adicionales aleatorios (freelance, inversiones, etc.)
            if random.random() < 0.4:  # 40% probabilidad
                cat_ing = random.choice([c for c in categorias_ingreso if c['nombre'] != 'Sueldo'])
                monto_extra = random.uniform(100, 800)
                fecha_extra = fecha_mes - timedelta(days=random.randint(10, 25))
                crear_movimiento_demo(
                    cursor, persona_id, cat_ing["id"],
                    cat_ing["nombre"], "INGRESO", fecha_extra
                )
                total_movimientos += 1
            
            # === GASTOS FIJOS MENSUALES ===
            gastos_fijos = [
                ('Vivienda', perfil['gasto_base'] * 0.35),
                ('Alimentación', perfil['gasto_base'] * 0.20),
                ('Transporte', perfil['gasto_base'] * 0.10),
                ('Servicios', perfil['gasto_base'] * 0.08),
                ('Salud', perfil['gasto_base'] * 0.05),
            ]
            
            for cat_nombre, monto_base in gastos_fijos:
                cat_gasto = next((c for c in categorias_gasto if c['nombre'] == cat_nombre), None)
                if cat_gasto:
                    # Variación según perfil
                    variacion = random.uniform(1 - perfil['variacion'], 1 + perfil['variacion'])
                    monto_final = monto_base * variacion
                    
                    # Distribuir gasto en varios días del mes
                    num_pagos = random.randint(1, 3)
                    for _ in range(num_pagos):
                        fecha_gasto = fecha_mes - timedelta(days=random.randint(1, 28))
                        crear_movimiento_demo(
                            cursor, persona_id, cat_gasto["id"],
                            cat_gasto["nombre"], "GASTO", fecha_gasto
                        )
                        total_movimientos += 1
            
            # === GASTOS VARIABLES ===
            # Entretenimiento (varía mucho según perfil)
            if random.random() < perfil['variacion'] * 2:
                cat_ent = next((c for c in categorias_gasto if c['nombre'] == 'Entretenimiento'), None)
                if cat_ent:
                    monto_ent = random.uniform(50, 300)
                    fecha_ent = fecha_mes - timedelta(days=random.randint(1, 28))
                    cursor.execute("""
                        INSERT INTO movimiento 
                        (persona_id, fecha, tipo, categoria_id, monto, descripcion, medio)
                        VALUES (?, ?, 'GASTO', ?, ?, ?, 'TARJETA')
                    """, (persona_id, fecha_ent.strftime('%Y-%m-%d'), 
                         cat_ent['id'], round(monto_ent, 2), 
                         random.choice(['Cine', 'Streaming', 'Salida', 'Juegos'])))
                    total_movimientos += 1
            
            # Educación (ocasional)
            if random.random() < 0.2:
                cat_edu = next((c for c in categorias_gasto if c['nombre'] == 'Educación'), None)
                if cat_edu:
                    fecha_edu = fecha_mes - timedelta(days=random.randint(1, 28))
                    crear_movimiento_demo(
                        cursor, persona_id, cat_edu["id"],
                        cat_edu["nombre"], "GASTO", fecha_edu
                    )
                    total_movimientos += 1
            
            # Compras variadas (ropa, tecnología, etc.)
            num_compras = random.randint(2, 5)
            for _ in range(num_compras):
                cat_comp = random.choice([c for c in categorias_gasto 
                                        if c['nombre'] in ['Ropa', 'Tecnología', 'Mascotas', 'Otros Gastos']])
                fecha_comp = fecha_mes - timedelta(days=random.randint(1, 28))
                crear_movimiento_demo(
                    cursor, persona_id, cat_comp["id"],
                    cat_comp["nombre"], "GASTO", fecha_comp
                )
                total_movimientos += 1
            
            # Ahorro/Inversión (solo perfiles que ahorran)
            if perfil['nombre'] in ['Ahorrador', 'Inversionista']:
                cat_aho = next((c for c in categorias_gasto if c['nombre'] == 'Ahorro'), None)
                if cat_aho:
                    monto_ahorro = perfil['sueldo'] * 0.15  # Ahorra 15%
                    fecha_aho = fecha_mes - timedelta(days=5)
                    cursor.execute("""
                        INSERT INTO movimiento 
                        (persona_id, fecha, tipo, categoria_id, monto, descripcion, medio)
                        VALUES (?, ?, 'GASTO', ?, ?, 'Ahorro mensual', 'TRANSFERENCIA')
                    """, (persona_id, fecha_aho.strftime('%Y-%m-%d'),
                         cat_aho['id'], round(monto_ahorro, 2)))
                    total_movimientos += 1
    
    connection.commit()
    print(f"   ✅ {total_movimientos} movimientos creados")
    print()
    
    # Mostrar resumen
    print("📊 RESUMEN DE DATOS DEMO:")
    print("=" * 50)
    
    for persona_id in personas_creadas:
        cursor.execute("""
            SELECT nombres, apellidos FROM persona WHERE id = ?
        """, (persona_id,))
        nombre, apellido = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                COALESCE(SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE 0 END), 0) as ingresos,
                COALESCE(SUM(CASE WHEN tipo = 'GASTO' THEN monto ELSE 0 END), 0) as gastos,
                COUNT(*) as total
            FROM movimiento 
            WHERE persona_id = ?
        """, (persona_id,))
        
        ingresos, gastos, total = cursor.fetchone()
        saldo = ingresos - gastos
        
        print(f"\n👤 {nombre} {apellido}")
        print(f"   💵 Ingresos: ${ingresos:,.2f}")
        print(f"   💸 Gastos:   ${gastos:,.2f}")
        print(f"   💰 Saldo:    ${saldo:,.2f}")
        print(f"   📋 Movs:     {total}")
    
    print()
    print("=" * 50)
    print("✅ Datos demo cargados exitosamente!")
    print()
    print("💡 Puedes ejecutar la aplicación ahora:")
    print("   python src/main.py")


if __name__ == "__main__":
    import sys
    import os
    
    # Agregar src al path (desde cualquier ubicación)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(script_dir, '..', '..', '..')
    sys.path.insert(0, project_root)
    
    from src.infrastructure.config.settings import Config
    from src.infrastructure.db.database import Database
    
    # Conectar a la base de datos
    db_path = Config.DB_PATH
    
    print(f"📁 Base de datos: {db_path}")
    print()
    
    with Database(str(db_path)) as db:
        cargar_datos_demo(db.get_connection())
