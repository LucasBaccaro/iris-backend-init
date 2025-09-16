-- schema.sql - Modelo de datos completo para IRIS
-- Sistema de Gestión para Salones de Belleza
-- Basado exactamente en planification.md

-- ============================================
-- CONFIGURACIÓN INICIAL
-- ============================================

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "btree_gist";

-- ============================================
-- TABLA: BUSINESSES (Salones)
-- ============================================

CREATE TABLE businesses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(20),
    timezone VARCHAR(50) NOT NULL DEFAULT 'America/Argentina/Buenos_Aires',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Comentarios explicativos
COMMENT ON TABLE businesses IS 'Tabla principal de salones de belleza';
COMMENT ON COLUMN businesses.timezone IS 'Timezone del salón para manejo correcto de horarios';
COMMENT ON COLUMN businesses.is_active IS 'ON/OFF del salón - el dueño puede cerrar temporalmente';

-- ============================================
-- TABLA: BUSINESS_HOURS (Horarios del salón)
-- ============================================

CREATE TABLE business_hours (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
    open_time TIME,
    close_time TIME,
    is_closed BOOLEAN NOT NULL DEFAULT false,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices para performance
CREATE INDEX idx_business_hours_business_id ON business_hours(business_id);
CREATE UNIQUE INDEX idx_business_hours_unique ON business_hours(business_id, day_of_week);

-- Comentarios
COMMENT ON TABLE business_hours IS 'Horarios de funcionamiento de cada salón';
COMMENT ON COLUMN business_hours.day_of_week IS '0=Domingo, 1=Lunes, 2=Martes, ..., 6=Sábado';
COMMENT ON COLUMN business_hours.is_closed IS 'true si el salón está cerrado ese día';

-- ============================================
-- TABLA: SERVICES (Servicios del salón)
-- ============================================

CREATE TABLE services (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
    duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
    points_awarded INTEGER NOT NULL DEFAULT 0 CHECK (points_awarded >= 0),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_services_business_id ON services(business_id);
CREATE INDEX idx_services_active ON services(business_id, is_active);

-- Comentarios
COMMENT ON TABLE services IS 'Catálogo de servicios de cada salón con precios y puntos';
COMMENT ON COLUMN services.points_awarded IS 'Puntos de fidelización que otorga este servicio';

-- ============================================
-- TABLA: EMPLOYEES (Empleados)
-- ============================================

CREATE TABLE employees (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    user_id UUID REFERENCES auth.users(id),  -- Referencia a Supabase Auth
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'inactive')),
    is_available BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_employees_business_id ON employees(business_id);
CREATE INDEX idx_employees_user_id ON employees(user_id);
CREATE INDEX idx_employees_available ON employees(business_id, is_available, status);

-- Comentarios
COMMENT ON TABLE employees IS 'Empleados de cada salón';
COMMENT ON COLUMN employees.user_id IS 'Opcional: si el empleado tiene cuenta puede loguearse';
COMMENT ON COLUMN employees.is_available IS 'ON/OFF del empleado - puede pausar su calendario';

-- ============================================
-- TABLA: EMPLOYEE_HOURS (Horarios de empleados)
-- ============================================

CREATE TABLE employee_hours (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
    day_of_week INTEGER NOT NULL CHECK (day_of_week >= 0 AND day_of_week <= 6),
    start_time TIME,
    end_time TIME,
    is_working BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_employee_hours_employee_id ON employee_hours(employee_id);
CREATE UNIQUE INDEX idx_employee_hours_unique ON employee_hours(employee_id, day_of_week);

-- Comentarios
COMMENT ON TABLE employee_hours IS 'Horarios de trabajo de cada empleado';
COMMENT ON COLUMN employee_hours.is_working IS 'false si el empleado no trabaja ese día';

-- ============================================
-- TABLA: APPOINTMENTS (Reservas)
-- ============================================

CREATE TABLE appointments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES auth.users(id),  -- Cliente (puede ser null para walk-ins)
    employee_id UUID NOT NULL REFERENCES employees(id),
    service_id UUID NOT NULL REFERENCES services(id),
    start_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    end_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'confirmed' CHECK (
        status IN ('confirmed', 'completed', 'cancelled', 'no_show')
    ),
    is_override BOOLEAN NOT NULL DEFAULT false,
    customer_name VARCHAR(255),  -- Para walk-ins sin cuenta
    customer_phone VARCHAR(20),  -- Para walk-ins sin cuenta
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices críticos para performance
CREATE INDEX idx_appointments_business_id ON appointments(business_id);
CREATE INDEX idx_appointments_employee_id ON appointments(employee_id);
CREATE INDEX idx_appointments_customer_id ON appointments(customer_id);
CREATE INDEX idx_appointments_datetime ON appointments(start_datetime, end_datetime);
CREATE INDEX idx_appointments_status ON appointments(status);

-- Comentarios
COMMENT ON TABLE appointments IS 'Reservas del sistema - core de IRIS';
COMMENT ON COLUMN appointments.is_override IS 'true para sobreturnos creados por el dueño';
COMMENT ON COLUMN appointments.customer_name IS 'Para clientes sin cuenta (walk-ins)';

-- ============================================
-- TABLA: SPECIAL_OPENINGS (Sobreturnos)
-- ============================================

CREATE TABLE special_openings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    start_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    end_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    max_extra_appointments INTEGER NOT NULL DEFAULT 1,
    description TEXT,
    created_by UUID NOT NULL REFERENCES auth.users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_special_openings_business_id ON special_openings(business_id);
CREATE INDEX idx_special_openings_datetime ON special_openings(start_datetime, end_datetime);

-- Comentarios
COMMENT ON TABLE special_openings IS 'Sobreturnos especiales creados por el dueño';
COMMENT ON COLUMN special_openings.max_extra_appointments IS 'Cuántas citas extra permite';

-- ============================================
-- TABLA: LOYALTY_POINTS (Sistema de puntos)
-- ============================================

CREATE TABLE loyalty_points (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    customer_id UUID NOT NULL REFERENCES auth.users(id),
    appointment_id UUID REFERENCES appointments(id),
    points_earned INTEGER NOT NULL CHECK (points_earned != 0),
    transaction_date TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    transaction_type VARCHAR(20) NOT NULL CHECK (
        transaction_type IN ('earned', 'redeemed', 'expired', 'adjustment')
    ),
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_loyalty_points_business_customer ON loyalty_points(business_id, customer_id);
CREATE INDEX idx_loyalty_points_appointment ON loyalty_points(appointment_id);
CREATE INDEX idx_loyalty_points_date ON loyalty_points(transaction_date);

-- Comentarios
COMMENT ON TABLE loyalty_points IS 'Historial completo de puntos de fidelización';
COMMENT ON COLUMN loyalty_points.points_earned IS 'Positivo para earned, negativo para redeemed';

-- ============================================
-- TABLA: LOYALTY_REWARDS (Recompensas canjeables)
-- ============================================

CREATE TABLE loyalty_rewards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    points_required INTEGER NOT NULL CHECK (points_required > 0),
    reward_type VARCHAR(20) NOT NULL CHECK (
        reward_type IN ('discount', 'free_service', 'gift')
    ),
    discount_percentage DECIMAL(5,2) CHECK (discount_percentage >= 0 AND discount_percentage <= 100),
    free_service_id UUID REFERENCES services(id),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_loyalty_rewards_business_id ON loyalty_rewards(business_id);
CREATE INDEX idx_loyalty_rewards_active ON loyalty_rewards(business_id, is_active);

-- Comentarios
COMMENT ON TABLE loyalty_rewards IS 'Catálogo de recompensas configurables por el dueño';

-- ============================================
-- TABLA: LOYALTY_REDEMPTIONS (Historial de canjes)
-- ============================================

CREATE TABLE loyalty_redemptions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    customer_id UUID NOT NULL REFERENCES auth.users(id),
    reward_id UUID NOT NULL REFERENCES loyalty_rewards(id),
    points_used INTEGER NOT NULL CHECK (points_used > 0),
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (
        status IN ('pending', 'approved', 'used', 'expired', 'cancelled')
    ),
    redeemed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    used_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_loyalty_redemptions_business_customer ON loyalty_redemptions(business_id, customer_id);
CREATE INDEX idx_loyalty_redemptions_reward ON loyalty_redemptions(reward_id);
CREATE INDEX idx_loyalty_redemptions_status ON loyalty_redemptions(status);

-- Comentarios
COMMENT ON TABLE loyalty_redemptions IS 'Historial de canjes de recompensas';

-- ============================================
-- TABLA: PROMOTIONS (Promociones informativas)
-- ============================================

CREATE TABLE promotions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    valid_from DATE NOT NULL,
    valid_until DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active' CHECK (
        status IN ('active', 'inactive', 'expired')
    ),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_promotions_business_id ON promotions(business_id);
CREATE INDEX idx_promotions_validity ON promotions(valid_from, valid_until, status);

-- Comentarios
COMMENT ON TABLE promotions IS 'Promociones informativas sin lógica de redención';

-- ============================================
-- TABLA: BUSINESS_FAQS (FAQs básicas)
-- ============================================

CREATE TABLE business_faqs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    category VARCHAR(100),
    display_order INTEGER DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_business_faqs_business_id ON business_faqs(business_id);
CREATE INDEX idx_business_faqs_category ON business_faqs(business_id, category, is_active);
CREATE INDEX idx_business_faqs_order ON business_faqs(business_id, display_order);

-- Comentarios
COMMENT ON TABLE business_faqs IS 'FAQs básicas por salón - preparación para IA futura';

-- ============================================
-- TABLA: BUSINESS_OWNERS (Relación propietarios)
-- ============================================

CREATE TABLE business_owners (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES auth.users(id),
    business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL DEFAULT 'owner' CHECK (role IN ('owner', 'admin')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_business_owners_user_id ON business_owners(user_id);
CREATE INDEX idx_business_owners_business_id ON business_owners(business_id);
CREATE UNIQUE INDEX idx_business_owners_unique ON business_owners(user_id, business_id);

-- Comentarios
COMMENT ON TABLE business_owners IS 'Relación muchos-a-muchos: un usuario puede ser dueño de múltiples salones';

-- ============================================
-- FUNCIONES AUXILIARES
-- ============================================

-- Función para actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger de updated_at a las tablas necesarias
CREATE TRIGGER update_businesses_updated_at BEFORE UPDATE ON businesses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_loyalty_rewards_updated_at BEFORE UPDATE ON loyalty_rewards FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_loyalty_redemptions_updated_at BEFORE UPDATE ON loyalty_redemptions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_promotions_updated_at BEFORE UPDATE ON promotions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
CREATE TRIGGER update_business_faqs_updated_at BEFORE UPDATE ON business_faqs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- VISTAS ÚTILES PARA CONSULTAS COMUNES
-- ============================================

-- Vista para obtener el balance de puntos de cada cliente por salón
CREATE VIEW loyalty_balances AS
SELECT
    business_id,
    customer_id,
    SUM(points_earned) as total_points
FROM loyalty_points
GROUP BY business_id, customer_id;

-- Vista para citas con información completa
CREATE VIEW appointments_full AS
SELECT
    a.*,
    b.name as business_name,
    e.name as employee_name,
    s.name as service_name,
    s.price as service_price,
    s.duration_minutes as service_duration,
    s.points_awarded as service_points
FROM appointments a
JOIN businesses b ON a.business_id = b.id
JOIN employees e ON a.employee_id = e.id
JOIN services s ON a.service_id = s.id;

-- Comentarios finales
COMMENT ON SCHEMA public IS 'Schema principal de IRIS - Sistema de Gestión para Salones de Belleza';