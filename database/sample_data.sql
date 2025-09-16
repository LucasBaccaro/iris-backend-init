-- sample_data.sql - Datos de ejemplo para testing de IRIS
-- SOLO PARA DESARROLLO - NO usar en producción

-- ============================================
-- DATOS DE EJEMPLO: BUSINESSES
-- ============================================

INSERT INTO businesses (id, name, address, phone, timezone, is_active) VALUES
(
    '550e8400-e29b-41d4-a716-446655440001',
    'Salón Elegance',
    'Av. Santa Fe 1234, CABA',
    '+541145678901',
    'America/Argentina/Buenos_Aires',
    true
),
(
    '550e8400-e29b-41d4-a716-446655440002',
    'Beauty Center',
    'Av. Córdoba 5678, Córdoba',
    '+543514567890',
    'America/Argentina/Cordoba',
    true
);

-- ============================================
-- DATOS DE EJEMPLO: BUSINESS HOURS
-- ============================================

-- Horarios para Salón Elegance (Lun-Vie 9-18, Sab 9-15, Dom cerrado)
INSERT INTO business_hours (business_id, day_of_week, open_time, close_time, is_closed) VALUES
('550e8400-e29b-41d4-a716-446655440001', 0, NULL, NULL, true),     -- Domingo cerrado
('550e8400-e29b-41d4-a716-446655440001', 1, '09:00', '18:00', false), -- Lunes
('550e8400-e29b-41d4-a716-446655440001', 2, '09:00', '18:00', false), -- Martes
('550e8400-e29b-41d4-a716-446655440001', 3, '09:00', '18:00', false), -- Miércoles
('550e8400-e29b-41d4-a716-446655440001', 4, '09:00', '18:00', false), -- Jueves
('550e8400-e29b-41d4-a716-446655440001', 5, '09:00', '18:00', false), -- Viernes
('550e8400-e29b-41d4-a716-446655440001', 6, '09:00', '15:00', false); -- Sábado

-- Horarios para Beauty Center (Mar-Sab 14-20, Lun/Dom cerrado)
INSERT INTO business_hours (business_id, day_of_week, open_time, close_time, is_closed) VALUES
('550e8400-e29b-41d4-a716-446655440002', 0, NULL, NULL, true),     -- Domingo cerrado
('550e8400-e29b-41d4-a716-446655440002', 1, NULL, NULL, true),     -- Lunes cerrado
('550e8400-e29b-41d4-a716-446655440002', 2, '14:00', '20:00', false), -- Martes
('550e8400-e29b-41d4-a716-446655440002', 3, '14:00', '20:00', false), -- Miércoles
('550e8400-e29b-41d4-a716-446655440002', 4, '14:00', '20:00', false), -- Jueves
('550e8400-e29b-41d4-a716-446655440002', 5, '14:00', '20:00', false), -- Viernes
('550e8400-e29b-41d4-a716-446655440002', 6, '14:00', '20:00', false); -- Sábado

-- ============================================
-- DATOS DE EJEMPLO: SERVICES
-- ============================================

-- Servicios para Salón Elegance
INSERT INTO services (id, business_id, name, price, duration_minutes, points_awarded) VALUES
('660e8400-e29b-41d4-a716-446655440001', '550e8400-e29b-41d4-a716-446655440001', 'Corte Dama', 1500.00, 30, 15),
('660e8400-e29b-41d4-a716-446655440002', '550e8400-e29b-41d4-a716-446655440001', 'Corte Caballero', 1200.00, 20, 12),
('660e8400-e29b-41d4-a716-446655440003', '550e8400-e29b-41d4-a716-446655440001', 'Tintura', 3000.00, 90, 30),
('660e8400-e29b-41d4-a716-446655440004', '550e8400-e29b-41d4-a716-446655440001', 'Manicura', 800.00, 45, 8),
('660e8400-e29b-41d4-a716-446655440005', '550e8400-e29b-41d4-a716-446655440001', 'Pedicura', 1000.00, 60, 10);

-- Servicios para Beauty Center
INSERT INTO services (id, business_id, name, price, duration_minutes, points_awarded) VALUES
('660e8400-e29b-41d4-a716-446655440006', '550e8400-e29b-41d4-a716-446655440002', 'Corte y Peinado', 2000.00, 60, 20),
('660e8400-e29b-41d4-a716-446655440007', '550e8400-e29b-41d4-a716-446655440002', 'Tratamiento Capilar', 2500.00, 120, 25),
('660e8400-e29b-41d4-a716-446655440008', '550e8400-e29b-41d4-a716-446655440002', 'Maquillaje Social', 1800.00, 45, 18);

-- ============================================
-- DATOS DE EJEMPLO: EMPLOYEES
-- ============================================

-- Empleados para Salón Elegance
INSERT INTO employees (id, business_id, user_id, name, phone, status, is_available) VALUES
(
    '770e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    NULL, -- Sin user_id por ahora
    'María Pérez',
    '+541156789012',
    'active',
    true
),
(
    '770e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    NULL,
    'Ana García',
    '+541167890123',
    'active',
    true
);

-- Empleados para Beauty Center
INSERT INTO employees (id, business_id, user_id, name, phone, status, is_available) VALUES
(
    '770e8400-e29b-41d4-a716-446655440003',
    '550e8400-e29b-41d4-a716-446655440002',
    NULL,
    'Lucía Morales',
    '+543515678901',
    'active',
    true
);

-- ============================================
-- DATOS DE EJEMPLO: EMPLOYEE HOURS
-- ============================================

-- Horarios de María Pérez (Lun-Vie 9-17)
INSERT INTO employee_hours (employee_id, day_of_week, start_time, end_time, is_working) VALUES
('770e8400-e29b-41d4-a716-446655440001', 0, NULL, NULL, false), -- Domingo
('770e8400-e29b-41d4-a716-446655440001', 1, '09:00', '17:00', true), -- Lunes
('770e8400-e29b-41d4-a716-446655440001', 2, '09:00', '17:00', true), -- Martes
('770e8400-e29b-41d4-a716-446655440001', 3, '09:00', '17:00', true), -- Miércoles
('770e8400-e29b-41d4-a716-446655440001', 4, '09:00', '17:00', true), -- Jueves
('770e8400-e29b-41d4-a716-446655440001', 5, '09:00', '17:00', true), -- Viernes
('770e8400-e29b-41d4-a716-446655440001', 6, NULL, NULL, false); -- Sábado

-- Horarios de Ana García (Mar-Sab 14-20)
INSERT INTO employee_hours (employee_id, day_of_week, start_time, end_time, is_working) VALUES
('770e8400-e29b-41d4-a716-446655440002', 0, NULL, NULL, false), -- Domingo
('770e8400-e29b-41d4-a716-446655440002', 1, NULL, NULL, false), -- Lunes
('770e8400-e29b-41d4-a716-446655440002', 2, '14:00', '20:00', true), -- Martes
('770e8400-e29b-41d4-a716-446655440002', 3, '14:00', '20:00', true), -- Miércoles
('770e8400-e29b-41d4-a716-446655440002', 4, '14:00', '20:00', true), -- Jueves
('770e8400-e29b-41d4-a716-446655440002', 5, '14:00', '20:00', true), -- Viernes
('770e8400-e29b-41d4-a716-446655440002', 6, '14:00', '20:00', true); -- Sábado

-- ============================================
-- DATOS DE EJEMPLO: LOYALTY REWARDS
-- ============================================

-- Recompensas para Salón Elegance
INSERT INTO loyalty_rewards (id, business_id, name, description, points_required, reward_type, discount_percentage) VALUES
(
    '880e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    '10% de descuento',
    'Descuento del 10% en cualquier servicio',
    100,
    'discount',
    10.00
),
(
    '880e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    'Corte gratis',
    'Corte de cabello completamente gratis',
    200,
    'free_service',
    NULL
);

-- ============================================
-- DATOS DE EJEMPLO: PROMOTIONS
-- ============================================

-- Promociones para Salón Elegance
INSERT INTO promotions (id, business_id, title, description, valid_from, valid_until, status) VALUES
(
    '990e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    '20% off en tinturas',
    'Descuento especial del 20% en todos los servicios de tintura durante enero',
    '2024-01-01',
    '2024-01-31',
    'active'
),
(
    '990e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    'Manicura + Pedicura',
    'Combo especial: Manicura + Pedicura por $1500 (precio normal $1800)',
    '2024-01-15',
    '2024-02-15',
    'active'
);

-- ============================================
-- DATOS DE EJEMPLO: BUSINESS FAQS
-- ============================================

-- FAQs para Salón Elegance
INSERT INTO business_faqs (id, business_id, question, answer, category, display_order) VALUES
(
    'aa0e8400-e29b-41d4-a716-446655440001',
    '550e8400-e29b-41d4-a716-446655440001',
    '¿Aceptan tarjetas de crédito?',
    'Sí, aceptamos todas las tarjetas de crédito y débito.',
    'pagos',
    1
),
(
    'aa0e8400-e29b-41d4-a716-446655440002',
    '550e8400-e29b-41d4-a716-446655440001',
    '¿Tienen estacionamiento?',
    'Sí, tenemos estacionamiento gratuito para nuestros clientes.',
    'servicios',
    2
),
(
    'aa0e8400-e29b-41d4-a716-446655440003',
    '550e8400-e29b-41d4-a716-446655440001',
    '¿Cómo puedo cancelar una cita?',
    'Podés cancelar llamando al salón o desde la aplicación móvil con al menos 2 horas de anticipación.',
    'reservas',
    3
),
(
    'aa0e8400-e29b-41d4-a716-446655440004',
    '550e8400-e29b-41d4-a716-446655440001',
    '¿Qué productos usan?',
    'Trabajamos con productos de primera calidad: LOréal, Schwarzkopf y OPI.',
    'productos',
    4
);

-- ============================================
-- COMENTARIOS Y NOTAS
-- ============================================

-- Notas importantes para development:
/*
1. Los user_id en employees están como NULL porque aún no tenemos usuarios reales de Supabase Auth
2. No incluimos appointments de ejemplo porque necesitamos user_id reales para customer_id
3. Los IDs están hardcoded para facilitar testing - en producción serán UUID automáticos
4. Los datos están en español porque el sistema es para Argentina
5. Los precios están en pesos argentinos (ARS)
6. Los teléfonos siguen formato argentino
7. Los horarios están en formato 24hs
*/

-- Para testing del constraint de overlapping appointments:
/*
-- Este INSERT debería FALLAR por constraint:
INSERT INTO appointments (
    business_id, employee_id, service_id, customer_id,
    start_datetime, end_datetime, status
) VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    '770e8400-e29b-41d4-a716-446655440001',
    '660e8400-e29b-41d4-a716-446655440001',
    NULL,
    '2024-01-15 14:00:00+00',
    '2024-01-15 14:30:00+00',
    'confirmed'
);

-- Y este también debería FALLAR (overlapping):
INSERT INTO appointments (
    business_id, employee_id, service_id, customer_id,
    start_datetime, end_datetime, status
) VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    '770e8400-e29b-41d4-a716-446655440001', -- Mismo empleado
    '660e8400-e29b-41d4-a716-446655440002',
    NULL,
    '2024-01-15 14:15:00+00', -- Se superpone con la anterior
    '2024-01-15 14:35:00+00',
    'confirmed'
);
*/