-- ========================================================
-- ESQUEMA DE BASE DE DATOS - FINANZAS PERSONALES
-- Versión: 1.0.0
-- Fecha: 2024-03-21
-- ========================================================

-- Eliminar tablas si existen (para recreación limpia)
DROP TABLE IF EXISTS movimiento;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS persona;

-- ========================================================
-- TABLA: persona
-- Almacena la información de las personas/usuarios
-- ========================================================
CREATE TABLE persona (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombres TEXT NOT NULL,
    apellidos TEXT NOT NULL,
    identificacion TEXT UNIQUE,
    telefono TEXT,
    correo TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    observaciones TEXT,
    foto_path TEXT,
    
    -- Constraints
    CONSTRAINT chk_nombres_no_vacios CHECK (length(trim(nombres)) > 0),
    CONSTRAINT chk_apellidos_no_vacios CHECK (length(trim(apellidos)) > 0)
);

-- Comentarios de tabla y columnas (SQLite no soporta COMMENT directamente,
-- pero documentamos aquí para referencia)
-- Tabla persona: Entidad principal del sistema
--   id: Identificador único autoincremental
--   nombres: Nombre(s) de la persona
--   apellidos: Apellido(s) de la persona
--   identificacion: Documento de identidad (opcional, único)
--   telefono: Número de contacto
--   correo: Email de contacto
--   fecha_registro: Fecha de alta en el sistema
--   observaciones: Notas adicionales
--   foto_path: Ruta al archivo de imagen de perfil

-- ========================================================
-- TABLA: categoria
-- Clasificación de ingresos y gastos
-- ========================================================
CREATE TABLE categoria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    tipo TEXT NOT NULL CHECK (tipo IN ('INGRESO', 'GASTO', 'AMBOS')),
    color TEXT DEFAULT '#808080' CHECK (color LIKE '#______'),
    activa BOOLEAN DEFAULT 1 CHECK (activa IN (0, 1)),
    descripcion TEXT,
    icono TEXT,
    orden INTEGER DEFAULT 999,
    
    -- Constraints
    CONSTRAINT chk_nombre_categoria CHECK (length(trim(nombre)) > 0),
    CONSTRAINT chk_tipo_valido CHECK (tipo IN ('INGRESO', 'GASTO', 'AMBOS'))
);

-- Comentarios:
-- Tabla categoria: Categorías para clasificar movimientos
--   id: Identificador único
--   nombre: Nombre descriptivo de la categoría
--   tipo: INGRESO, GASTO o AMBOS
--   color: Código hexadecimal para gráficos
--   activa: 1 si está disponible para nuevos movimientos
--   descripcion: Explicación de la categoría
--   icono: Nombre del icono asociado
--   orden: Orden de visualización (menor = primero)

-- ========================================================
-- TABLA: movimiento
-- Registro de todas las transacciones financieras
-- ========================================================
CREATE TABLE movimiento (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    tipo TEXT NOT NULL CHECK (tipo IN ('INGRESO', 'GASTO')),
    categoria_id INTEGER NOT NULL,
    monto REAL NOT NULL CHECK (monto > 0),
    descripcion TEXT,
    medio TEXT CHECK (medio IN ('EFECTIVO', 'TRANSFERENCIA', 'TARJETA', 'CHEQUE', 'OTRO')),
    referencia TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Foreign Keys
    FOREIGN KEY (persona_id) 
        REFERENCES persona(id) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    
    FOREIGN KEY (categoria_id) 
        REFERENCES categoria(id) 
        ON DELETE RESTRICT 
        ON UPDATE CASCADE,
    
    -- Constraints
    CONSTRAINT chk_monto_positivo CHECK (monto > 0),
    CONSTRAINT chk_tipo_movimiento CHECK (tipo IN ('INGRESO', 'GASTO')),
    CONSTRAINT chk_fecha_no_futura CHECK (fecha <= date('now'))
);

-- Comentarios:
-- Tabla movimiento: Transacciones financieras
--   id: Identificador único
--   persona_id: Referencia a la persona (FK)
--   fecha: Fecha de la transacción
--   tipo: INGRESO o GASTO
--   categoria_id: Categoría de clasificación (FK)
--   monto: Valor positivo de la transacción
--   descripcion: Detalle de la transacción
--   medio: Forma de pago (EFECTIVO, TRANSFERENCIA, etc.)
--   referencia: Número de comprobante, factura, etc.
--   created_at: Fecha de creación del registro
--   updated_at: Fecha de última modificación

-- ========================================================
-- ÍNDICES
-- Mejoran el rendimiento de consultas frecuentes
-- ========================================================

-- Índice para búsquedas por nombre/apellido
CREATE INDEX idx_persona_nombre 
    ON persona(nombres, apellidos);

-- Índice para búsquedas por identificación
CREATE INDEX idx_persona_identificacion 
    ON persona(identificacion);

-- Índice para filtrar movimientos por persona
CREATE INDEX idx_movimiento_persona 
    ON movimiento(persona_id);

-- Índice para filtrar movimientos por fecha
CREATE INDEX idx_movimiento_fecha 
    ON movimiento(fecha);

-- Índice compuesto para consultas por persona y fecha
CREATE INDEX idx_movimiento_persona_fecha 
    ON movimiento(persona_id, fecha);

-- Índice para filtrar movimientos por categoría
CREATE INDEX idx_movimiento_categoria 
    ON movimiento(categoria_id);

-- Índice para filtrar movimientos por tipo
CREATE INDEX idx_movimiento_tipo 
    ON movimiento(tipo);

-- Índice para categorías activas
CREATE INDEX idx_categoria_activa_tipo 
    ON categoria(activa, tipo);

-- ========================================================
-- VISTAS (Views)
-- Facilitan consultas complejas frecuentes
-- ========================================================

-- Vista: Resumen de persona con totales
CREATE VIEW v_persona_resumen AS
SELECT 
    p.id,
    p.nombres,
    p.apellidos,
    p.nombre_completo,
    p.identificacion,
    p.telefono,
    p.correo,
    p.fecha_registro,
    COALESCE(SUM(CASE WHEN m.tipo = 'INGRESO' THEN m.monto ELSE 0 END), 0) as total_ingresos,
    COALESCE(SUM(CASE WHEN m.tipo = 'GASTO' THEN m.monto ELSE 0 END), 0) as total_gastos,
    COALESCE(SUM(CASE WHEN m.tipo = 'INGRESO' THEN m.monto ELSE -m.monto END), 0) as saldo,
    COUNT(m.id) as cantidad_movimientos
FROM persona p
LEFT JOIN movimiento m ON p.id = m.persona_id
GROUP BY p.id, p.nombres, p.apellidos, p.identificacion, p.telefono, p.correo, p.fecha_registro;

-- Vista: Movimientos con información completa
CREATE VIEW v_movimientos_completos AS
SELECT 
    m.id,
    m.persona_id,
    p.nombres || ' ' || p.apellidos as persona_nombre,
    m.fecha,
    m.tipo,
    m.categoria_id,
    c.nombre as categoria_nombre,
    c.color as categoria_color,
    m.monto,
    CASE 
        WHEN m.tipo = 'INGRESO' THEN m.monto 
        ELSE -m.monto 
    END as monto_efectivo,
    m.descripcion,
    m.medio,
    m.referencia,
    m.created_at
FROM movimiento m
JOIN persona p ON m.persona_id = p.id
JOIN categoria c ON m.categoria_id = c.id;

-- Vista: Resumen mensual por persona
CREATE VIEW v_resumen_mensual AS
SELECT 
    persona_id,
    strftime('%Y', fecha) as anio,
    strftime('%m', fecha) as mes,
    SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE 0 END) as ingresos,
    SUM(CASE WHEN tipo = 'GASTO' THEN monto ELSE 0 END) as gastos,
    SUM(CASE WHEN tipo = 'INGRESO' THEN monto ELSE -monto END) as saldo,
    COUNT(*) as cantidad_movimientos
FROM movimiento
GROUP BY persona_id, strftime('%Y', fecha), strftime('%m', fecha);

-- Vista: Gastos por categoría
CREATE VIEW v_gastos_por_categoria AS
SELECT 
    m.persona_id,
    m.categoria_id,
    c.nombre as categoria_nombre,
    c.color as categoria_color,
    SUM(m.monto) as total,
    COUNT(*) as cantidad,
    AVG(m.monto) as promedio,
    MIN(m.fecha) as primera_fecha,
    MAX(m.fecha) as ultima_fecha
FROM movimiento m
JOIN categoria c ON m.categoria_id = c.id
WHERE m.tipo = 'GASTO'
GROUP BY m.persona_id, m.categoria_id, c.nombre, c.color;

-- ========================================================
-- TRIGGERS
-- Automatizan tareas al modificar datos
-- ========================================================

-- Trigger: Actualizar updated_at automáticamente
CREATE TRIGGER trg_movimiento_updated_at
AFTER UPDATE ON movimiento
BEGIN
    UPDATE movimiento 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;

-- Trigger: Prevenir eliminación de categorías en uso
CREATE TRIGGER trg_prevent_delete_categoria_en_uso
BEFORE DELETE ON categoria
BEGIN
    SELECT CASE
        WHEN EXISTS (SELECT 1 FROM movimiento WHERE categoria_id = OLD.id) THEN
            RAISE(ABORT, 'No se puede eliminar la categoría porque tiene movimientos asociados')
    END;
END;

-- ========================================================
-- DATOS DE CONFIGURACIÓN
-- ========================================================

-- Tabla de configuración del sistema
CREATE TABLE IF NOT EXISTS config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Configuraciones por defecto
INSERT OR IGNORE INTO config (key, value, description) VALUES
('db_version', '1.0.0', 'Versión del esquema de base de datos'),
('app_name', 'Finanzas Personales', 'Nombre de la aplicación'),
('seeds_version', '1.0.0', 'Versión de los seeds de categorías'),
('currency', 'USD', 'Moneda por defecto'),
('date_format', 'DD/MM/YYYY', 'Formato de fechas');

-- ========================================================
-- FIN DEL ESQUEMA
-- ========================================================
