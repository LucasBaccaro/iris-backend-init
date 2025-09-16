# app/utils/timezone_handler.py
# Manejo completo de timezones para IRIS
# Específicamente optimizado para Argentina y expansión a LATAM

import pytz
from datetime import datetime, date, time
from typing import Optional, List, Tuple
from app.config.settings import settings
from app.config.logging import get_logger

logger = get_logger("iris.timezone")

# ============================================
# CONFIGURACIÓN DE TIMEZONES ARGENTINA
# ============================================

# Timezones oficiales de Argentina soportados por IRIS
ARGENTINA_TIMEZONES = {
    # Zona horaria principal (mayor población)
    'Buenos_Aires': 'America/Argentina/Buenos_Aires',
    'CABA': 'America/Argentina/Buenos_Aires',

    # Zonas horarias provinciales
    'Cordoba': 'America/Argentina/Cordoba',
    'Mendoza': 'America/Argentina/Mendoza',
    'Tucuman': 'America/Argentina/Tucuman',
    'Salta': 'America/Argentina/Salta',
    'San_Juan': 'America/Argentina/San_Juan',
    'Catamarca': 'America/Argentina/Catamarca',
    'Jujuy': 'America/Argentina/Jujuy',
    'La_Rioja': 'America/Argentina/La_Rioja',
    'Rio_Gallegos': 'America/Argentina/Rio_Gallegos',  # Santa Cruz
    'Ushuaia': 'America/Argentina/Ushuaia',  # Tierra del Fuego
}

# Mapeo de provincias a timezones (para facilitar setup)
PROVINCIA_TO_TIMEZONE = {
    # Provincia -> Timezone string
    'Buenos Aires': 'America/Argentina/Buenos_Aires',
    'CABA': 'America/Argentina/Buenos_Aires',
    'Ciudad de Buenos Aires': 'America/Argentina/Buenos_Aires',
    'Cordoba': 'America/Argentina/Cordoba',
    'Córdoba': 'America/Argentina/Cordoba',
    'Mendoza': 'America/Argentina/Mendoza',
    'Tucuman': 'America/Argentina/Tucuman',
    'Tucumán': 'America/Argentina/Tucuman',
    'Salta': 'America/Argentina/Salta',
    'San Juan': 'America/Argentina/San_Juan',
    'Catamarca': 'America/Argentina/Catamarca',
    'Jujuy': 'America/Argentina/Jujuy',
    'La Rioja': 'America/Argentina/La_Rioja',
    'Santa Cruz': 'America/Argentina/Rio_Gallegos',
    'Tierra del Fuego': 'America/Argentina/Ushuaia',
    # Provincias que usan Buenos Aires timezone
    'Entre Rios': 'America/Argentina/Buenos_Aires',
    'Entre Ríos': 'America/Argentina/Buenos_Aires',
    'Santa Fe': 'America/Argentina/Buenos_Aires',
    'Corrientes': 'America/Argentina/Buenos_Aires',
    'Misiones': 'America/Argentina/Buenos_Aires',
    'Formosa': 'America/Argentina/Buenos_Aires',
    'Chaco': 'America/Argentina/Buenos_Aires',
    'Santiago del Estero': 'America/Argentina/Buenos_Aires',
    'La Pampa': 'America/Argentina/Buenos_Aires',
    'Neuquen': 'America/Argentina/Buenos_Aires',
    'Neuquén': 'America/Argentina/Buenos_Aires',
    'Rio Negro': 'America/Argentina/Buenos_Aires',
    'Río Negro': 'America/Argentina/Buenos_Aires',
    'Chubut': 'America/Argentina/Buenos_Aires',
}

class TimezoneHandler:
    """
    Clase principal para manejar todas las operaciones de timezone en IRIS

    Funcionalidades:
    - Conversión entre timezones
    - Validación de horarios de negocio
    - Formateo para Argentina
    - Cálculos de disponibilidad
    """

    def __init__(self, business_timezone: str = None):
        """
        Inicializar handler con timezone específico del business

        Args:
            business_timezone: Timezone del salón (ej: 'America/Argentina/Buenos_Aires')
        """
        self.business_timezone = business_timezone or settings.default_timezone

        try:
            self.business_tz = pytz.timezone(self.business_timezone)
        except Exception as e:
            logger.error("timezone_initialization_failed",
                        timezone=self.business_timezone, error=str(e))
            # Fallback a Buenos Aires
            self.business_timezone = 'America/Argentina/Buenos_Aires'
            self.business_tz = pytz.timezone(self.business_timezone)

    def get_current_business_time(self) -> datetime:
        """
        Obtiene la hora actual en el timezone del salón

        Returns:
            datetime: Hora actual en timezone del business
        """
        utc_now = datetime.now(pytz.UTC)
        business_now = utc_now.astimezone(self.business_tz)

        logger.debug("current_business_time_requested",
                    business_timezone=self.business_timezone,
                    utc_time=utc_now.isoformat(),
                    business_time=business_now.isoformat())

        return business_now

    def convert_to_business_timezone(self, dt: datetime) -> datetime:
        """
        Convierte cualquier datetime al timezone del salón

        Args:
            dt: datetime a convertir (puede tener timezone o ser naive)

        Returns:
            datetime: datetime en timezone del salón
        """
        # Si el datetime es naive, asumir que está en UTC
        if dt.tzinfo is None:
            dt = pytz.UTC.localize(dt)

        # Convertir al timezone del business
        business_dt = dt.astimezone(self.business_tz)

        logger.debug("timezone_conversion",
                    original_time=dt.isoformat(),
                    business_time=business_dt.isoformat(),
                    business_timezone=self.business_timezone)

        return business_dt

    def convert_to_utc(self, dt: datetime) -> datetime:
        """
        Convierte datetime del timezone del salón a UTC

        Args:
            dt: datetime en timezone del salón

        Returns:
            datetime: datetime en UTC
        """
        # Si es naive, asumir que está en el timezone del business
        if dt.tzinfo is None:
            dt = self.business_tz.localize(dt)

        utc_dt = dt.astimezone(pytz.UTC)

        logger.debug("utc_conversion",
                    business_time=dt.isoformat(),
                    utc_time=utc_dt.isoformat(),
                    business_timezone=self.business_timezone)

        return utc_dt

    def create_business_datetime(self, date: date, time: time) -> datetime:
        """
        Crea un datetime combinando fecha y hora en el timezone del salón

        Args:
            date: Fecha
            time: Hora

        Returns:
            datetime: datetime en timezone del salón
        """
        # Crear datetime naive
        naive_dt = datetime.combine(date, time)

        # Localizar en el timezone del business
        business_dt = self.business_tz.localize(naive_dt)

        logger.debug("business_datetime_created",
                    date=date.isoformat(),
                    time=time.isoformat(),
                    business_datetime=business_dt.isoformat(),
                    business_timezone=self.business_timezone)

        return business_dt

    def is_same_day(self, dt1: datetime, dt2: datetime) -> bool:
        """
        Verifica si dos datetimes están en el mismo día en el timezone del salón

        Args:
            dt1: Primer datetime
            dt2: Segundo datetime

        Returns:
            bool: True si están en el mismo día
        """
        business_dt1 = self.convert_to_business_timezone(dt1)
        business_dt2 = self.convert_to_business_timezone(dt2)

        return business_dt1.date() == business_dt2.date()

    def get_week_day_number(self, dt: datetime) -> int:
        """
        Obtiene el número del día de la semana en timezone del salón

        Args:
            dt: datetime

        Returns:
            int: 0=Domingo, 1=Lunes, ..., 6=Sábado
        """
        business_dt = self.convert_to_business_timezone(dt)
        # Python usa 0=Lunes, convertir a 0=Domingo para consistency con DB
        weekday = business_dt.weekday()  # 0=Lunes, 6=Domingo
        return (weekday + 1) % 7  # Convertir a 0=Domingo, 6=Sábado

    def format_for_argentina(self, dt: datetime, include_timezone: bool = True) -> str:
        """
        Formatea datetime para mostrar a usuarios argentinos

        Args:
            dt: datetime a formatear
            include_timezone: Si incluir info de timezone

        Returns:
            str: datetime formateado para Argentina
        """
        business_dt = self.convert_to_business_timezone(dt)

        # Formato argentino: DD/MM/YYYY HH:MM
        formatted = business_dt.strftime("%d/%m/%Y %H:%M")

        if include_timezone:
            # Agregar timezone abreviado
            formatted += f" ({business_dt.tzinfo.tzname(business_dt)})"

        return formatted

    def parse_argentina_datetime(self, date_str: str, time_str: str = None) -> datetime:
        """
        Parsea strings de fecha/hora en formato argentino

        Args:
            date_str: Fecha en formato DD/MM/YYYY o YYYY-MM-DD
            time_str: Hora en formato HH:MM o HH:MM:SS (opcional)

        Returns:
            datetime: datetime en timezone del salón
        """
        try:
            # Intentar formato argentino DD/MM/YYYY
            if '/' in date_str:
                date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            # Intentar formato ISO YYYY-MM-DD
            elif '-' in date_str:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            else:
                raise ValueError(f"Formato de fecha no reconocido: {date_str}")

            # Parsear hora si se proporciona
            if time_str:
                if len(time_str.split(':')) == 2:
                    time_obj = datetime.strptime(time_str, "%H:%M").time()
                else:
                    time_obj = datetime.strptime(time_str, "%H:%M:%S").time()
            else:
                time_obj = time(0, 0)  # Medianoche por defecto

            return self.create_business_datetime(date_obj, time_obj)

        except Exception as e:
            logger.error("argentina_datetime_parsing_failed",
                        date_str=date_str,
                        time_str=time_str,
                        error=str(e))
            raise ValueError(f"Error parseando fecha/hora: {e}")

# ============================================
# FUNCIONES AUXILIARES GLOBALES
# ============================================

def get_timezone_for_provincia(provincia: str) -> str:
    """
    Obtiene el timezone correcto para una provincia argentina

    Args:
        provincia: Nombre de la provincia

    Returns:
        str: Timezone string
    """
    # Normalizar nombre de provincia
    provincia_normalized = provincia.strip().title()

    timezone = PROVINCIA_TO_TIMEZONE.get(
        provincia_normalized,
        settings.default_timezone  # Fallback
    )

    logger.info("timezone_for_provincia",
               provincia=provincia,
               timezone=timezone)

    return timezone

def validate_timezone(timezone_str: str) -> bool:
    """
    Valida que un timezone string sea válido y esté soportado

    Args:
        timezone_str: String del timezone a validar

    Returns:
        bool: True si es válido
    """
    try:
        # Verificar que sea un timezone válido de pytz
        pytz.timezone(timezone_str)

        # Verificar que esté en nuestra lista de Argentina
        is_argentina = timezone_str in ARGENTINA_TIMEZONES.values()

        if not is_argentina:
            logger.warning("unsupported_timezone",
                          timezone=timezone_str,
                          message="Timezone válido pero no está en lista de Argentina")

        return True

    except Exception as e:
        logger.error("invalid_timezone",
                    timezone=timezone_str,
                    error=str(e))
        return False

def get_supported_timezones() -> List[Tuple[str, str]]:
    """
    Obtiene lista de timezones soportados para UI

    Returns:
        List[Tuple[str, str]]: [(display_name, timezone_string), ...]
    """
    return [
        ("Buenos Aires / CABA", "America/Argentina/Buenos_Aires"),
        ("Córdoba", "America/Argentina/Cordoba"),
        ("Mendoza", "America/Argentina/Mendoza"),
        ("Tucumán", "America/Argentina/Tucuman"),
        ("Salta", "America/Argentina/Salta"),
        ("San Juan", "America/Argentina/San_Juan"),
        ("Catamarca", "America/Argentina/Catamarca"),
        ("Jujuy", "America/Argentina/Jujuy"),
        ("La Rioja", "America/Argentina/La_Rioja"),
        ("Santa Cruz", "America/Argentina/Rio_Gallegos"),
        ("Tierra del Fuego", "America/Argentina/Ushuaia"),
    ]

def create_timezone_handler(business_timezone: str = None) -> TimezoneHandler:
    """
    Factory function para crear TimezoneHandler

    Args:
        business_timezone: Timezone del salón

    Returns:
        TimezoneHandler: Handler configurado
    """
    return TimezoneHandler(business_timezone)

# ============================================
# FUNCIONES ESPECÍFICAS PARA APPOINTMENTS
# ============================================

def calculate_appointment_end_time(
    start_datetime: datetime,
    duration_minutes: int,
    business_timezone: str = None
) -> datetime:
    """
    Calcula la hora de fin de una cita basada en duración

    Args:
        start_datetime: Hora de inicio
        duration_minutes: Duración en minutos
        business_timezone: Timezone del salón

    Returns:
        datetime: Hora de fin de la cita
    """
    from datetime import timedelta

    handler = TimezoneHandler(business_timezone)

    # Asegurar que el start_datetime está en el timezone correcto
    start_business = handler.convert_to_business_timezone(start_datetime)

    # Calcular end time
    end_business = start_business + timedelta(minutes=duration_minutes)

    logger.debug("appointment_end_time_calculated",
                start_time=start_business.isoformat(),
                duration_minutes=duration_minutes,
                end_time=end_business.isoformat(),
                business_timezone=business_timezone)

    return end_business

def is_appointment_in_future(
    appointment_datetime: datetime,
    business_timezone: str = None,
    buffer_minutes: int = 0
) -> bool:
    """
    Verifica si una cita está en el futuro

    Args:
        appointment_datetime: Datetime de la cita
        business_timezone: Timezone del salón
        buffer_minutes: Buffer en minutos (para permitir citas "casi pasadas")

    Returns:
        bool: True si está en el futuro
    """
    from datetime import timedelta

    handler = TimezoneHandler(business_timezone)

    current_time = handler.get_current_business_time()
    appointment_time = handler.convert_to_business_timezone(appointment_datetime)

    # Aplicar buffer si se especifica
    if buffer_minutes > 0:
        current_time = current_time - timedelta(minutes=buffer_minutes)

    is_future = appointment_time > current_time

    logger.debug("appointment_future_check",
                current_time=current_time.isoformat(),
                appointment_time=appointment_time.isoformat(),
                buffer_minutes=buffer_minutes,
                is_future=is_future)

    return is_future