# app/utils/business_hours_validator.py
# Validador de horarios de negocio para IRIS
# Verifica si appointments están dentro de horarios permitidos

from datetime import datetime, time, date
from typing import Optional, Dict, List, Tuple
from app.utils.timezone_handler import TimezoneHandler
from app.config.logging import get_logger

logger = get_logger("iris.business_hours")

class BusinessHoursValidator:
    """
    Validador de horarios de negocio para IRIS

    Funcionalidades:
    - Verificar si una cita está dentro del horario del salón
    - Verificar si un empleado está trabajando
    - Calcular slots disponibles
    - Manejar excepciones y sobreturnos
    """

    def __init__(self, business_timezone: str = None):
        """
        Inicializar validador

        Args:
            business_timezone: Timezone del salón
        """
        self.timezone_handler = TimezoneHandler(business_timezone)

    async def is_within_business_hours(
        self,
        appointment_datetime: datetime,
        business_hours: Dict[int, Dict]  # {day_of_week: {open_time, close_time, is_closed}}
    ) -> bool:
        """
        Verifica si una cita está dentro del horario del salón

        Args:
            appointment_datetime: Datetime de la cita
            business_hours: Horarios del salón por día de semana

        Returns:
            bool: True si está dentro del horario
        """

        # Convertir a timezone del business
        business_dt = self.timezone_handler.convert_to_business_timezone(appointment_datetime)
        day_of_week = self.timezone_handler.get_week_day_number(business_dt)
        appointment_time = business_dt.time()

        # Obtener horarios para ese día
        day_hours = business_hours.get(day_of_week)

        if not day_hours:
            logger.warning("no_business_hours_defined",
                          day_of_week=day_of_week,
                          appointment_datetime=business_dt.isoformat())
            return False

        # Verificar si el salón está cerrado ese día
        if day_hours.get('is_closed', False):
            logger.info("business_closed_on_day",
                       day_of_week=day_of_week,
                       appointment_datetime=business_dt.isoformat())
            return False

        open_time = day_hours.get('open_time')
        close_time = day_hours.get('close_time')

        if not open_time or not close_time:
            logger.warning("incomplete_business_hours",
                          day_of_week=day_of_week,
                          open_time=open_time,
                          close_time=close_time)
            return False

        # Verificar si está dentro del horario
        is_within = open_time <= appointment_time <= close_time

        logger.debug("business_hours_validation",
                    appointment_datetime=business_dt.isoformat(),
                    day_of_week=day_of_week,
                    appointment_time=appointment_time.isoformat(),
                    open_time=open_time.isoformat(),
                    close_time=close_time.isoformat(),
                    is_within=is_within)

        return is_within

    async def is_employee_working(
        self,
        appointment_datetime: datetime,
        employee_hours: Dict[int, Dict]  # {day_of_week: {start_time, end_time, is_working}}
    ) -> bool:
        """
        Verifica si un empleado está trabajando en el horario solicitado

        Args:
            appointment_datetime: Datetime de la cita
            employee_hours: Horarios del empleado por día de semana

        Returns:
            bool: True si el empleado está trabajando
        """

        # Convertir a timezone del business
        business_dt = self.timezone_handler.convert_to_business_timezone(appointment_datetime)
        day_of_week = self.timezone_handler.get_week_day_number(business_dt)
        appointment_time = business_dt.time()

        # Obtener horarios del empleado para ese día
        day_schedule = employee_hours.get(day_of_week)

        if not day_schedule:
            logger.warning("no_employee_hours_defined",
                          day_of_week=day_of_week,
                          appointment_datetime=business_dt.isoformat())
            return False

        # Verificar si el empleado trabaja ese día
        if not day_schedule.get('is_working', False):
            logger.info("employee_not_working_on_day",
                       day_of_week=day_of_week,
                       appointment_datetime=business_dt.isoformat())
            return False

        start_time = day_schedule.get('start_time')
        end_time = day_schedule.get('end_time')

        if not start_time or not end_time:
            logger.warning("incomplete_employee_hours",
                          day_of_week=day_of_week,
                          start_time=start_time,
                          end_time=end_time)
            return False

        # Verificar si está dentro del horario del empleado
        is_working = start_time <= appointment_time <= end_time

        logger.debug("employee_hours_validation",
                    appointment_datetime=business_dt.isoformat(),
                    day_of_week=day_of_week,
                    appointment_time=appointment_time.isoformat(),
                    start_time=start_time.isoformat(),
                    end_time=end_time.isoformat(),
                    is_working=is_working)

        return is_working

    async def validate_appointment_timing(
        self,
        appointment_datetime: datetime,
        duration_minutes: int,
        business_hours: Dict[int, Dict],
        employee_hours: Dict[int, Dict],
        check_future: bool = True
    ) -> Tuple[bool, List[str]]:
        """
        Validación completa de timing para una cita

        Args:
            appointment_datetime: Datetime de inicio de la cita
            duration_minutes: Duración de la cita en minutos
            business_hours: Horarios del salón
            employee_hours: Horarios del empleado
            check_future: Si verificar que la cita esté en el futuro

        Returns:
            Tuple[bool, List[str]]: (is_valid, list_of_errors)
        """
        from app.utils.timezone_handler import calculate_appointment_end_time, is_appointment_in_future

        errors = []

        # 1. Verificar que esté en el futuro
        if check_future and not is_appointment_in_future(
            appointment_datetime,
            self.timezone_handler.business_timezone,
            buffer_minutes=15  # Permitir citas hasta 15 min en el pasado
        ):
            errors.append("La cita debe estar en el futuro")

        # 2. Calcular hora de fin
        end_datetime = calculate_appointment_end_time(
            appointment_datetime,
            duration_minutes,
            self.timezone_handler.business_timezone
        )

        # 3. Verificar horario del salón (inicio y fin)
        if not await self.is_within_business_hours(appointment_datetime, business_hours):
            errors.append("La hora de inicio está fuera del horario del salón")

        if not await self.is_within_business_hours(end_datetime, business_hours):
            errors.append("La hora de fin está fuera del horario del salón")

        # 4. Verificar horario del empleado (inicio y fin)
        if not await self.is_employee_working(appointment_datetime, employee_hours):
            errors.append("El empleado no está trabajando a la hora de inicio")

        if not await self.is_employee_working(end_datetime, employee_hours):
            errors.append("El empleado no está trabajando a la hora de fin")

        # 5. Verificar que inicio y fin estén en el mismo día
        if not self.timezone_handler.is_same_day(appointment_datetime, end_datetime):
            errors.append("La cita no puede extenderse a otro día")

        is_valid = len(errors) == 0

        logger.info("appointment_timing_validation",
                   appointment_datetime=appointment_datetime.isoformat(),
                   duration_minutes=duration_minutes,
                   end_datetime=end_datetime.isoformat(),
                   is_valid=is_valid,
                   errors=errors)

        return is_valid, errors

    async def get_available_slots(
        self,
        target_date: date,
        duration_minutes: int,
        business_hours: Dict[int, Dict],
        employee_hours: Dict[int, Dict],
        existing_appointments: List[Tuple[datetime, datetime]],  # [(start, end), ...]
        slot_interval_minutes: int = 15
    ) -> List[datetime]:
        """
        Calcula slots disponibles para una fecha específica

        Args:
            target_date: Fecha objetivo
            duration_minutes: Duración del servicio
            business_hours: Horarios del salón
            employee_hours: Horarios del empleado
            existing_appointments: Lista de citas existentes
            slot_interval_minutes: Intervalo entre slots

        Returns:
            List[datetime]: Lista de slots disponibles
        """
        from datetime import timedelta

        available_slots = []

        # Obtener día de la semana
        temp_dt = self.timezone_handler.create_business_datetime(target_date, time(12, 0))
        day_of_week = self.timezone_handler.get_week_day_number(temp_dt)

        # Verificar que el salón y empleado trabajen ese día
        business_day = business_hours.get(day_of_week)
        employee_day = employee_hours.get(day_of_week)

        if not business_day or business_day.get('is_closed', False):
            logger.info("business_closed_no_slots",
                       date=target_date.isoformat(),
                       day_of_week=day_of_week)
            return []

        if not employee_day or not employee_day.get('is_working', False):
            logger.info("employee_not_working_no_slots",
                       date=target_date.isoformat(),
                       day_of_week=day_of_week)
            return []

        # Determinar ventana de trabajo (intersección de horarios)
        work_start = max(
            business_day.get('open_time', time(0, 0)),
            employee_day.get('start_time', time(0, 0))
        )
        work_end = min(
            business_day.get('close_time', time(23, 59)),
            employee_day.get('end_time', time(23, 59))
        )

        if work_start >= work_end:
            logger.warning("invalid_work_window",
                          date=target_date.isoformat(),
                          work_start=work_start.isoformat(),
                          work_end=work_end.isoformat())
            return []

        # Generar slots candidatos
        current_slot = self.timezone_handler.create_business_datetime(target_date, work_start)
        work_end_dt = self.timezone_handler.create_business_datetime(target_date, work_end)

        while current_slot + timedelta(minutes=duration_minutes) <= work_end_dt:
            slot_end = current_slot + timedelta(minutes=duration_minutes)

            # Verificar que no se superponga con citas existentes
            is_available = True
            for existing_start, existing_end in existing_appointments:
                # Convertir a timezone del business para comparar
                existing_start = self.timezone_handler.convert_to_business_timezone(existing_start)
                existing_end = self.timezone_handler.convert_to_business_timezone(existing_end)

                # Verificar superposición
                if (current_slot < existing_end and slot_end > existing_start):
                    is_available = False
                    break

            if is_available:
                available_slots.append(current_slot)

            # Próximo slot
            current_slot += timedelta(minutes=slot_interval_minutes)

        logger.info("available_slots_calculated",
                   date=target_date.isoformat(),
                   duration_minutes=duration_minutes,
                   total_slots=len(available_slots),
                   work_start=work_start.isoformat(),
                   work_end=work_end.isoformat())

        return available_slots

# ============================================
# FUNCIONES HELPER
# ============================================

def create_business_hours_validator(business_timezone: str = None) -> BusinessHoursValidator:
    """
    Factory function para crear BusinessHoursValidator

    Args:
        business_timezone: Timezone del salón

    Returns:
        BusinessHoursValidator: Validador configurado
    """
    return BusinessHoursValidator(business_timezone)

async def quick_validate_appointment_time(
    appointment_datetime: datetime,
    duration_minutes: int,
    business_timezone: str,
    business_hours: Dict[int, Dict],
    employee_hours: Dict[int, Dict]
) -> bool:
    """
    Validación rápida de una cita (solo True/False)

    Args:
        appointment_datetime: Datetime de la cita
        duration_minutes: Duración en minutos
        business_timezone: Timezone del salón
        business_hours: Horarios del salón
        employee_hours: Horarios del empleado

    Returns:
        bool: True si es válida
    """
    validator = BusinessHoursValidator(business_timezone)

    is_valid, _ = await validator.validate_appointment_timing(
        appointment_datetime,
        duration_minutes,
        business_hours,
        employee_hours
    )

    return is_valid