from typing import NamedTuple, get_args

from pandas import DatetimeIndex, NaT, Timedelta, Timestamp, date_range

from ..types import DatetimeIterable, ExpandLimits, Schedule, TimedeltaTypes
from ._limits import LimitsTuple
from ._process_available import ProcessAvailableResult, process_available

NO_LIMITS: LimitsTuple = NaT, NaT


class MaterializedSchedule(NamedTuple):
    """An explicit schedule."""

    schedule: DatetimeIndex
    available_metadata: ProcessAvailableResult


def materialize_schedule(
    schedule: Schedule, expand_limits: ExpandLimits, *, available: DatetimeIterable | None = None
) -> MaterializedSchedule:
    """Materialize user schedule based on available data."""
    if available is None:
        try:
            return MaterializedSchedule(
                DatetimeIndex(schedule),
                available_metadata=ProcessAvailableResult(None, NO_LIMITS, NO_LIMITS),
            )
        except TypeError as e:
            raise ValueError("Schedule must be explicit when not bounded by an available range.") from e

    available_metadata = process_available(available, expand_limits=expand_limits)
    min_dt, max_dt = available_metadata.expanded_limits

    if isinstance(schedule, str) and _cron_like(schedule):
        schedule = _handle_cron(schedule, min_dt, max_dt)
    elif isinstance(schedule, get_args(TimedeltaTypes)):
        schedule = _from_timedelta(schedule, available_metadata.expanded_limits)
    else:
        if not isinstance(schedule, DatetimeIndex):
            schedule = DatetimeIndex(schedule)

        schedule = schedule.tz_localize(min_dt.tz) if schedule.tz is None else schedule.tz_convert(min_dt.tz)
        schedule = schedule[(min_dt <= schedule) & (schedule <= max_dt)]
    return MaterializedSchedule(schedule, available_metadata=available_metadata)


def _cron_like(schedule: str) -> bool:
    # CroniterBadCronError: Exactly 5 or 6 columns has to be specified for iterator expression.
    return len(schedule.split()) > 4 or schedule[0] == "@"  # noqa: PLR2004


def _from_timedelta(schedule: TimedeltaTypes, limits: LimitsTuple) -> DatetimeIndex:
    timedelta = Timedelta(schedule)
    if timedelta <= Timedelta(0):
        raise ValueError(f"unbounded {schedule=} must be greater than zero.")
    return date_range(*limits, freq=timedelta, inclusive="both")


def _handle_cron(expr: str, min_dt: Timestamp, max_dt: Timestamp) -> DatetimeIndex:
    try:
        from croniter import croniter_range

        return DatetimeIndex(croniter_range(min_dt, max_dt, expr))
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(f"Install 'croniter' to parse cron expressions such such as '{expr}'.") from e
