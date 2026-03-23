-- ========================================================
-- SEEDS DE CATEGORIAS - FINANZAS PERSONALES
-- Versión: 1.0.0
-- Fecha: 2024-03-21
-- ========================================================

-- Insertar categorías de INGRESOS
-- Orden: 1-7 (más usadas primero)
INSERT OR IGNORE INTO categoria (nombre, tipo, color, descripcion, icono, orden) VALUES
('Sueldo', 'INGRESO', '#27ae60', 'Ingresos fijos por trabajo dependiente', 'money', 1),
('Freelance', 'INGRESO', '#2ecc71', 'Trabajos independientes y proyectos personales', 'briefcase', 2),
('Inversiones', 'INGRESO', '#16a085', 'Dividendos, intereses y rendimientos financieros', 'chart-line', 3),
('Ventas', 'INGRESO', '#1abc9c', 'Ingresos por venta de productos o bienes', 'shopping-cart', 4),
('Regalos', 'INGRESO', '#3498db', 'Dinero recibido como regalo o herencia', 'gift', 5),
('Reembolsos', 'INGRESO', '#9b59b6', 'Devoluciones de dinero o reembolsos', 'undo', 6),
('Otros Ingresos', 'INGRESO', '#34495e', 'Otros tipos de ingresos varios', 'coins', 99);

-- Insertar categorías de GASTOS
-- Orden: 1-14 (más usadas primero)
INSERT OR IGNORE INTO categoria (nombre, tipo, color, descripcion, icono, orden) VALUES
('Alimentación', 'GASTO', '#e74c3c', 'Supermercado, restaurantes y comida', 'utensils', 1),
('Transporte', 'GASTO', '#e67e22', 'Gasolina, transporte público, mantenimiento vehicular', 'car', 2),
('Vivienda', 'GASTO', '#d35400', 'Renta, hipoteca, servicios (agua, luz, gas)', 'home', 3),
('Salud', 'GASTO', '#c0392b', 'Doctores, medicinas, seguros médicos', 'medkit', 4),
('Educación', 'GASTO', '#8e44ad', 'Cursos, libros, colegiaturas, material escolar', 'graduation-cap', 5),
('Entretenimiento', 'GASTO', '#f39c12', 'Cine, juegos, hobbies, suscripciones streaming', 'film', 6),
('Ropa', 'GASTO', '#e91e63', 'Vestimenta, calzado y accesorios personales', 'tshirt', 7),
('Tecnología', 'GASTO', '#00bcd4', 'Computadoras, celulares, software, gadgets', 'laptop', 8),
('Mascotas', 'GASTO', '#795548', 'Alimento, veterinaria, cuidado de mascotas', 'paw', 9),
('Viajes', 'GASTO', '#3f51b5', 'Hoteles, vuelos, tours, vacaciones', 'plane', 10),
('Ahorro', 'GASTO', '#009688', 'Dinero destinado a ahorro o fondos de emergencia', 'piggy-bank', 11),
('Impuestos', 'GASTO', '#ff5722', 'Pagos de impuestos y tasas gubernamentales', 'file-invoice-dollar', 12),
('Seguros', 'GASTO', '#607d8b', 'Seguros de vida, auto, hogar, etc.', 'shield-alt', 13),
('Otros Gastos', 'GASTO', '#95a5a6', 'Gastos misceláneos no clasificados', 'receipt', 99);

-- Insertar categorías AMBOS (sirven para ingresos y gastos)
INSERT OR IGNORE INTO categoria (nombre, tipo, color, descripcion, icono, orden) VALUES
('Transferencias', 'AMBOS', '#607d8b', 'Transferencias entre cuentas propias', 'exchange-alt', 50);

-- ========================================================
-- DATOS DE EJEMPLO (Opcional - solo para desarrollo/testing)
-- Descomenta las líneas siguientes si quieres datos de prueba
-- ========================================================

/*
-- Persona de ejemplo
INSERT OR IGNORE INTO persona (nombres, apellidos, identificacion, telefono, correo, observaciones) 
VALUES ('Juan', 'Pérez García', '12345678', '555-0100', 'juan@email.com', 'Usuario de prueba');

-- Movimientos de ejemplo (asumiendo que la persona tiene id=1)
INSERT INTO movimiento (persona_id, fecha, tipo, categoria_id, monto, descripcion, medio) VALUES
(1, date('now', '-30 days'), 'INGRESO', 1, 2500.00, 'Sueldo mensual', 'TRANSFERENCIA'),
(1, date('now', '-25 days'), 'GASTO', 8, 150.00, 'Compra supermercado', 'TARJETA'),
(1, date('now', '-20 days'), 'GASTO', 9, 50.00, 'Gasolina', 'EFECTIVO'),
(1, date('now', '-15 days'), 'GASTO', 10, 800.00, 'Pago de renta', 'TRANSFERENCIA'),
(1, date('now', '-10 days'), 'INGRESO', 2, 500.00, 'Proyecto freelance', 'TRANSFERENCIA'),
(1, date('now', '-5 days'), 'GASTO', 14, 120.00, 'Cena restaurante', 'TARJETA');
*/

-- ========================================================
-- CONFIGURACIÓN INICIAL
-- ========================================================

INSERT OR IGNORE INTO config (key, value, description) VALUES
('db_version', '1.0.0', 'Versión del esquema de base de datos'),
('app_name', 'Finanzas Personales', 'Nombre de la aplicación'),
('seeds_version', '1.0.0', 'Versión de los seeds de categorías'),
('currency', 'USD', 'Moneda por defecto'),
('date_format', 'DD/MM/YYYY', 'Formato de fechas');

-- ========================================================
-- FIN DE SEEDS
-- ========================================================
