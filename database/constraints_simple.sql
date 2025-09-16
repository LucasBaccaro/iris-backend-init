-- constraints_simple.sql - Solo los constraints más críticos para IRIS
-- Usar este archivo si constraints.sql da errores

-- ============================================
-- CONSTRAINT CRÍTICO: PREVENIR OVERLAPPING APPOINTMENTS
-- ============================================

-- Este es EL constraint más importante de IRIS
ALTER TABLE appointments ADD CONSTRAINT prevent_overlapping_appointments
EXCLUDE USING gist (
    employee_id WITH =,
    tstzrange(start_datetime, end_datetime) WITH &&
) WHERE (status != 'cancelled' AND is_override = false);

-- ============================================
-- CONSTRAINT: APPOINTMENTS DATETIME LOGIC
-- ============================================

-- Las citas deben tener end_datetime posterior a start_datetime
ALTER TABLE appointments ADD CONSTRAINT appointments_datetime_logic
CHECK (end_datetime > start_datetime);

-- ============================================
-- CONSTRAINT: TIMEZONE CONSISTENCY (SIMPLIFICADO)
-- ============================================

-- Validar que los salones usen timezones válidos de Argentina
ALTER TABLE businesses ADD CONSTRAINT valid_timezone CHECK (
    timezone LIKE 'America/Argentina/%'
);

-- ============================================
-- CONSTRAINT: LOYALTY SYSTEM VALIDATION
-- ============================================

-- Los puntos no pueden ser cero en loyalty_points
ALTER TABLE loyalty_points ADD CONSTRAINT loyalty_points_not_zero
CHECK (points_earned != 0);

-- Los descuentos no pueden ser mayores al 100%
ALTER TABLE loyalty_rewards ADD CONSTRAINT valid_discount_percentage
CHECK (
    reward_type != 'discount' OR
    (discount_percentage >= 0 AND discount_percentage <= 100)
);

-- ============================================
-- SUCCESS MESSAGE
-- ============================================

SELECT 'Constraints críticos aplicados correctamente ✅' as result;