from dataclasses import dataclass
from typing import Optional, List
from gvm.protocols.gmpv208.entities.targets import AliveTest

@dataclass
class CreateTarget:
    name: str
    asset_hosts_filter: Optional[str] = None
    hosts: Optional[List[str]] = None
    comment: Optional[str] = None
    exclude_hosts: Optional[List[str]] = None
    ssh_credential_id: Optional[str] = None
    ssh_credential_port: Optional[int] = None
    smb_credential_id: Optional[str] = None
    esxi_credential_id: Optional[str] = None
    snmp_credential_id: Optional[str] = None
    alive_test: Optional[AliveTest] = None
    reverse_lookup_only: Optional[bool] = False
    reverse_lookup_unify: Optional[bool] = False
    port_range: Optional[str] = None
    port_list_id: Optional[str] = None

@dataclass
class ModifyTarget:
    name: Optional[str] = None
    comment: Optional[str] = None
    hosts: Optional[List[str]] = None
    exclude_hosts: Optional[List[str]] = None
    ssh_credential_id: Optional[str] = None
    ssh_credential_port: Optional[bool] = None
    smb_credential_id: Optional[str] = None
    esxi_credential_id: Optional[str] = None
    snmp_credential_id: Optional[str] = None
    alive_test: Optional[AliveTest] = None
    allow_simultaneous_ips: Optional[bool] = None
    reverse_lookup_only: Optional[bool] = None
    reverse_lookup_unify: Optional[bool] = None
    port_list_id: Optional[str] = None