from dataclasses import dataclass
from datetime import time, timedelta


@dataclass
class Schedule:
    id: int
    barber_id: int
    day_of_week: int
    start_time: time
    end_time: time
    break_start: time | None
    break_end: time | None
    tolerance: timedelta