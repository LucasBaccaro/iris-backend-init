-- ==============================================
  -- IRIS - Esquema Completo de Base de Datos
  -- SaaS de Gestión para Salones de Belleza
  -- ==============================================

  -- Extensiones necesarias
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
  CREATE EXTENSION IF NOT EXISTS btree_gist;

  -- ==============================================
  -- TABLAS PRINCIPALES
  -- ==============================================

  -- Salones de belleza (multi-tenant)
  CREATE TABLE businesses (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      name VARCHAR(255) NOT NULL,
      address TEXT NOT NULL,
      phone VARCHAR(20),
      timezone VARCHAR(50) DEFAULT 'America/Argentina/Buenos_Aires'
          CHECK (timezone IN (
              'America/Argentina/Buenos_Aires',
              'America/Argentina/Cordoba',
              'America/Argentina/Mendoza',
              'America/Argentina/Tucuman'
          )),
      is_active BOOLEAN DEFAULT true,
      access_code VARCHAR(8) UNIQUE NOT NULL DEFAULT UPPER(SUBSTRING(REPLACE(uuid_generate_v4()::text, '-', '') FROM 1 FOR 8)),
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- Horarios del salón
  CREATE TABLE business_hours (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6), -- 0=Domingo, 6=Sábado
      open_time TIME,
      close_time TIME,
      is_closed BOOLEAN DEFAULT false,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      UNIQUE(business_id, day_of_week)
  );

  -- Servicios del salón
  CREATE TABLE services (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      name VARCHAR(255) NOT NULL,
      description TEXT,
      price DECIMAL(10,2) NOT NULL CHECK (price >= 0),
      duration_minutes INTEGER NOT NULL CHECK (duration_minutes > 0),
      points_awarded INTEGER DEFAULT 0 CHECK (points_awarded >= 0),
      is_active BOOLEAN DEFAULT true,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- Empleados del salón
  CREATE TABLE employees (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      user_id UUID, -- Referencia a auth.users de Supabase
      name VARCHAR(255) NOT NULL,
      phone VARCHAR(20),
      email VARCHAR(255),
      status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
      is_available BOOLEAN DEFAULT true,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- Horarios de empleados
  CREATE TABLE employee_hours (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
      day_of_week INTEGER NOT NULL CHECK (day_of_week BETWEEN 0 AND 6),
      start_time TIME,
      end_time TIME,
      is_available BOOLEAN DEFAULT true,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      UNIQUE(employee_id, day_of_week)
  );

  -- Servicios que puede realizar cada empleado
  CREATE TABLE employee_services (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      employee_id UUID NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
      service_id UUID NOT NULL REFERENCES services(id) ON DELETE CASCADE,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      UNIQUE(employee_id, service_id)
  );

  -- Clientes adheridos a salones
  CREATE TABLE customer_businesses (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      customer_id UUID NOT NULL, -- Referencia a auth.users de Supabase
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      customer_name VARCHAR(255) NOT NULL,
      customer_phone VARCHAR(20),
      customer_email VARCHAR(255),
      joined_at TIMESTAMPTZ DEFAULT NOW(),
      UNIQUE(customer_id, business_id)
  );

  -- Reservas/Citas
  CREATE TABLE appointments (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      customer_id UUID NOT NULL,
      employee_id UUID NOT NULL REFERENCES employees(id),
      service_id UUID NOT NULL REFERENCES services(id),
      start_datetime TIMESTAMPTZ NOT NULL,
      end_datetime TIMESTAMPTZ NOT NULL,
      status VARCHAR(20) DEFAULT 'scheduled' CHECK (status IN ('scheduled', 'confirmed', 'in_progress', 'completed', 'cancelled', 'no_show')),
      is_override BOOLEAN DEFAULT false, -- Para sobreturnos
      notes TEXT,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW(),

      -- Validaciones
      CHECK (end_datetime > start_datetime),

      -- Constraint para evitar overlapping appointments (excepto canceladas y sobreturnos)
      EXCLUDE USING gist (
          employee_id WITH =,
          tstzrange(start_datetime, end_datetime) WITH &&
      ) WHERE (status != 'cancelled' AND is_override = false)
  );

  -- Sobreturnos especiales
  CREATE TABLE special_openings (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      start_datetime TIMESTAMPTZ NOT NULL,
      end_datetime TIMESTAMPTZ NOT NULL,
      max_extra_appointments INTEGER DEFAULT 1,
      description TEXT,
      created_by UUID NOT NULL, -- employee_id que lo creó
      created_at TIMESTAMPTZ DEFAULT NOW(),

      CHECK (end_datetime > start_datetime),
      CHECK (max_extra_appointments > 0)
  );

  -- Sistema de puntos de fidelización
  CREATE TABLE loyalty_points (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      customer_id UUID NOT NULL,
      appointment_id UUID REFERENCES appointments(id),
      points_earned INTEGER NOT NULL,
      transaction_date TIMESTAMPTZ DEFAULT NOW(),
      transaction_type VARCHAR(20) DEFAULT 'earned' CHECK (transaction_type IN ('earned', 'redeemed', 'expired', 'adjusted')),
      description TEXT,
      created_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- Recompensas configurables
  CREATE TABLE loyalty_rewards (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      name VARCHAR(255) NOT NULL,
      description TEXT,
      points_required INTEGER NOT NULL CHECK (points_required > 0),
      reward_type VARCHAR(20) NOT NULL CHECK (reward_type IN ('discount_percentage', 'discount_fixed', 'free_service')),
      discount_percentage DECIMAL(5,2) CHECK (discount_percentage BETWEEN 0 AND 100),
      discount_fixed DECIMAL(10,2) CHECK (discount_fixed >= 0),
      free_service_id UUID REFERENCES services(id),
      is_active BOOLEAN DEFAULT true,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW(),

      -- Al menos uno de los campos de descuento debe estar definido según el tipo
      CHECK (
          (reward_type = 'discount_percentage' AND discount_percentage IS NOT NULL) OR
          (reward_type = 'discount_fixed' AND discount_fixed IS NOT NULL) OR
          (reward_type = 'free_service' AND free_service_id IS NOT NULL)
      )
  );

  -- Historial de canjes de recompensas
  CREATE TABLE loyalty_redemptions (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      customer_id UUID NOT NULL,
      reward_id UUID NOT NULL REFERENCES loyalty_rewards(id),
      appointment_id UUID REFERENCES appointments(id), -- Cita donde se usó
      points_used INTEGER NOT NULL CHECK (points_used > 0),
      status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'used', 'expired', 'cancelled')),
      redeemed_at TIMESTAMPTZ DEFAULT NOW(),
      used_at TIMESTAMPTZ,
      expires_at TIMESTAMPTZ,
      created_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- Promociones
  CREATE TABLE promotions (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      title VARCHAR(255) NOT NULL,
      description TEXT,
      valid_from TIMESTAMPTZ NOT NULL,
      valid_until TIMESTAMPTZ NOT NULL,
      status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'expired')),
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW(),

      CHECK (valid_until > valid_from)
  );

  -- FAQs del negocio (preparación para IA)
  CREATE TABLE business_faqs (
      id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
      business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
      question TEXT NOT NULL,
      answer TEXT NOT NULL,
      category VARCHAR(100),
      is_active BOOLEAN DEFAULT true,
      created_at TIMESTAMPTZ DEFAULT NOW(),
      updated_at TIMESTAMPTZ DEFAULT NOW()
  );

  -- ==============================================
  -- ÍNDICES PARA PERFORMANCE
  -- ==============================================

  -- Índices principales para consultas frecuentes
  CREATE INDEX idx_appointments_business_datetime ON appointments(business_id, start_datetime);
  CREATE INDEX idx_appointments_employee_datetime ON appointments(employee_id, start_datetime);
  CREATE INDEX idx_appointments_customer ON appointments(customer_id);
  CREATE INDEX idx_loyalty_points_customer_business ON loyalty_points(customer_id, business_id);
  CREATE INDEX idx_customer_businesses_customer ON customer_businesses(customer_id);
  CREATE INDEX idx_employee_services_employee ON employee_services(employee_id);
  CREATE INDEX idx_services_business_active ON services(business_id, is_active);
  CREATE INDEX idx_employees_business_active ON employees(business_id, status);

  -- ==============================================
  -- TRIGGERS PARA UPDATED_AT
  -- ==============================================

  -- Función para actualizar updated_at
  CREATE OR REPLACE FUNCTION update_updated_at_column()
  RETURNS TRIGGER AS $$
  BEGIN
      NEW.updated_at = NOW();
      RETURN NEW;
  END;
  $$ language 'plpgsql';

  -- Triggers para todas las tablas que tienen updated_at
  CREATE TRIGGER update_businesses_updated_at BEFORE UPDATE ON businesses FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  CREATE TRIGGER update_services_updated_at BEFORE UPDATE ON services FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  CREATE TRIGGER update_employees_updated_at BEFORE UPDATE ON employees FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  CREATE TRIGGER update_appointments_updated_at BEFORE UPDATE ON appointments FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  CREATE TRIGGER update_loyalty_rewards_updated_at BEFORE UPDATE ON loyalty_rewards FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  CREATE TRIGGER update_promotions_updated_at BEFORE UPDATE ON promotions FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
  CREATE TRIGGER update_business_faqs_updated_at BEFORE UPDATE ON business_faqs FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

  -- ==============================================
  -- FUNCIONES AUXILIARES
  -- ==============================================

  -- Función para obtener puntos totales de un cliente en un negocio
  CREATE OR REPLACE FUNCTION get_customer_total_points(p_customer_id UUID, p_business_id UUID)
  RETURNS INTEGER AS $$
  BEGIN
      RETURN COALESCE(
          (SELECT SUM(
              CASE
                  WHEN transaction_type = 'earned' THEN points_earned
                  WHEN transaction_type = 'redeemed' THEN -points_earned
                  WHEN transaction_type = 'adjusted' THEN points_earned
                  ELSE 0
              END
          )
          FROM loyalty_points
          WHERE customer_id = p_customer_id
          AND business_id = p_business_id
          AND transaction_type IN ('earned', 'redeemed', 'adjusted')),
          0
      );
  END;
  $$ LANGUAGE plpgsql;

  -- Función para verificar disponibilidad de empleado
  CREATE OR REPLACE FUNCTION check_employee_availability(
      p_employee_id UUID,
      p_start_datetime TIMESTAMPTZ,
      p_end_datetime TIMESTAMPTZ
  ) RETURNS BOOLEAN AS $$
  DECLARE
      conflict_count INTEGER;
  BEGIN
      -- Verificar si hay conflictos de horario
      SELECT COUNT(*)
      INTO conflict_count
      FROM appointments
      WHERE employee_id = p_employee_id
      AND status NOT IN ('cancelled', 'no_show')
      AND tstzrange(start_datetime, end_datetime) && tstzrange(p_start_datetime, p_end_datetime);

      RETURN conflict_count = 0;
  END;
  $$ LANGUAGE plpgsql;

  -- ==============================================
  -- POLÍTICAS RLS (Row Level Security)
  -- ==============================================

  -- Habilitar RLS en todas las tablas principales
  ALTER TABLE businesses ENABLE ROW LEVEL SECURITY;
  ALTER TABLE business_hours ENABLE ROW LEVEL SECURITY;
  ALTER TABLE services ENABLE ROW LEVEL SECURITY;
  ALTER TABLE employees ENABLE ROW LEVEL SECURITY;
  ALTER TABLE employee_hours ENABLE ROW LEVEL SECURITY;
  ALTER TABLE employee_services ENABLE ROW LEVEL SECURITY;
  ALTER TABLE customer_businesses ENABLE ROW LEVEL SECURITY;
  ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
  ALTER TABLE special_openings ENABLE ROW LEVEL SECURITY;
  ALTER TABLE loyalty_points ENABLE ROW LEVEL SECURITY;
  ALTER TABLE loyalty_rewards ENABLE ROW LEVEL SECURITY;
  ALTER TABLE loyalty_redemptions ENABLE ROW LEVEL SECURITY;
  ALTER TABLE promotions ENABLE ROW LEVEL SECURITY;
  ALTER TABLE business_faqs ENABLE ROW LEVEL SECURITY;

  -- Política base: Los usuarios pueden ver/modificar solo datos de sus negocios
  -- (Las políticas específicas se configurarán según los roles en el backend)