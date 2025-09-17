-- ==============================================
-- TABLA FALTANTE: user_profiles
-- ==============================================

-- Perfiles de usuario, vinculados a la autenticación de Supabase
CREATE TABLE public.user_profiles (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL DEFAULT 'customer' CHECK (role IN ('owner', 'employee', 'customer')),
    business_id UUID REFERENCES public.businesses(id) ON DELETE SET NULL,
    first_name TEXT,
    last_name TEXT,
    phone_number TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- Trigger para updated_at en user_profiles
-- (Asume que la función update_updated_at_column ya existe por tu script anterior)
CREATE TRIGGER update_user_profiles_updated_at BEFORE UPDATE ON user_profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Habilitar RLS para user_profiles
ALTER TABLE public.user_profiles ENABLE ROW LEVEL SECURITY;


-- ==============================================
-- POLÍTICAS RLS (Row Level Security) INICIALES
-- ==============================================

-- --- Políticas para `businesses` ---

-- Los dueños pueden hacer todo en su propio negocio.
CREATE POLICY "business_owners_full_access"
ON public.businesses
FOR ALL
TO authenticated
USING (
    id IN (
        SELECT business_id FROM public.user_profiles
        WHERE user_profiles.id = auth.uid() AND user_profiles.role = 'owner'
    )
)
WITH CHECK (
    id IN (
        SELECT business_id FROM public.user_profiles
        WHERE user_profiles.id = auth.uid() AND user_profiles.role = 'owner'
    )
);

-- Los empleados pueden ver el negocio al que pertenecen.
CREATE POLICY "employees_read_access"
ON public.businesses
FOR SELECT
TO authenticated
USING (
    id IN (
        SELECT business_id FROM public.user_profiles
        WHERE user_profiles.id = auth.uid() AND user_profiles.role = 'employee'
    )
);

-- Todos los usuarios autenticados pueden ver todos los negocios (para buscar y unirse).
CREATE POLICY "authenticated_users_read_all"
ON public.businesses
FOR SELECT
TO authenticated
USING (true);


-- --- Políticas para `user_profiles` ---

-- Los usuarios pueden ver y modificar su propio perfil.
CREATE POLICY "users_manage_own_profile"
ON public.user_profiles
FOR ALL
TO authenticated
USING (id = auth.uid())
WITH CHECK (id = auth.uid());

-- Los dueños de negocios pueden ver los perfiles de los empleados y clientes de su negocio.
CREATE POLICY "business_owners_view_profiles"
ON public.user_profiles
FOR SELECT
TO authenticated
USING (
    business_id IN (
        SELECT business_id FROM public.user_profiles
        WHERE user_profiles.id = auth.uid() AND user_profiles.role = 'owner'
    )
);
