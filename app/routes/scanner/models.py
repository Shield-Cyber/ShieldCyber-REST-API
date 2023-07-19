from dataclasses import dataclass
from typing import Optional
from gvm.protocols.gmpv208.entities.scanners import ScannerType

@dataclass
class CreateScanner:
    name: str
    host: str
    port: int
    scanner_type: ScannerType
    credential_id: str
    ca_pub: Optional[str] = None
    comment: Optional[str] = None

@dataclass
class ModifyScanner:
    scanner_type: Optional[ScannerType] = None
    host: Optional[str] = None
    port: Optional[int] = None
    comment: Optional[str] = None
    name: Optional[str] = None
    ca_pub: Optional[str] = None
    credential_id: Optional[str] = None