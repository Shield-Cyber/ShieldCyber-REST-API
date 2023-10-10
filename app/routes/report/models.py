from dataclasses import dataclass
from typing import Optional

@dataclass
class ImportReport:
    report: str
    task_id: Optional[str] = None
    in_assets: Optional[bool] = None

@dataclass
class ImportFormat:
    report_format: str

@dataclass
class ModifyFormat:
    active: Optional[bool] = None
    name: Optional[str] = None
    summary: Optional[str] = None
    param_name: Optional[str] = None
    param_value: Optional[str] = None