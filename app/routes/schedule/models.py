from dataclasses import dataclass
from typing import Optional

@dataclass
class CreateSchedule:
    name: str
    icalendar: str
    timezone: str
    comment: Optional[str] = None

@dataclass
class ModifySchedule:
    name: Optional[str] = None
    icalendar: Optional[str] = None
    timezone: Optional[str] = None
    comment: Optional[str] = None