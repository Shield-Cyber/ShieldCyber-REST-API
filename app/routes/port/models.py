from dataclasses import dataclass
from gvm.protocols.gmpv208.entities.port_lists import PortRangeType

@dataclass
class PortListBase:
    name: str
    port_range: str
    comment: str | None = None

@dataclass
class PortRangeBase:
    port_list_id: str
    start: int
    end: int
    port_range_type: PortRangeType
    comment: str | None = None