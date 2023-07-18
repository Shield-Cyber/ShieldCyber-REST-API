from dataclasses import dataclass
from typing import Optional, List
from gvm.protocols.gmpv208.entities.hosts import HostsOrdering

@dataclass
class CreateTask:
    name: str
    config_id: str
    target_id: str
    scanner_id: str
    alterable: Optional[bool] = None
    hosts_ordering: Optional[HostsOrdering] = None
    schedule_id: Optional[str] = None
    alert_ids: Optional[List[str]] = None
    comment: Optional[str] = None
    schedule_periods: Optional[int] = None
    observers: Optional[List[str]] = None
    preferences: Optional[dict] = None

@dataclass
class ModifyTask:
    task_id: str
    name: Optional[str] = None
    config_id: Optional[str] = None
    target_id: Optional[str] = None
    scanner_id: Optional[str] = None
    alterable: Optional[bool] = None
    hosts_ordering: Optional[HostsOrdering] = None
    schedule_id: Optional[str] = None
    schedule_periods: Optional[int] = None
    comment: Optional[str] = None
    alert_ids: Optional[List[str]] = None
    observers: Optional[List[str]] = None
    preferences: Optional[dict] = None

@dataclass
class MoveTask:
    task_id: str
    slave_id: Optional[str] = None