from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth, PASSWORD
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional, List
from gvm.protocols.gmpv208.entities.targets import AliveTest
from app import LOGGING_PREFIX

ENDPOINT = "target"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT]
    )

### ROUTES ###

@ROUTER.post("/create/target")
async def create_target(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
        name: str,
        asset_hosts_filter: Optional[str] = None,
        hosts: Optional[List[str]] = None,
        comment: Optional[str] = None,
        exclude_hosts: Optional[List[str]] = None,
        ssh_credential_id: Optional[str] = None,
        ssh_credential_port: Optional[int] = None,
        smb_credential_id: Optional[str] = None,
        esxi_credential_id: Optional[str] = None,
        snmp_credential_id: Optional[str] = None,
        alive_test: Optional[AliveTest] = None,
        reverse_lookup_only: Optional[bool] = None,
        reverse_lookup_unify: Optional[bool] = None,
        port_range: Optional[str] = None,
        port_list_id: Optional[str] = None,
    ):
    """Create a new target

        Arguments:

            name: Name of the target
            asset_hosts_filter: Filter to select target host from assets hosts
            hosts: List of hosts addresses to scan
            exclude_hosts: List of hosts addresses to exclude from scan
            comment: Comment for the target
            ssh_credential_id: UUID of a ssh credential to use on target
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of a smb credential to use on target
            snmp_credential_id: UUID of a snmp credential to use on target
            esxi_credential_id: UUID of a esxi credential to use on target
            alive_test: Which alive test to use
            reverse_lookup_only: Whether to scan only hosts that have names
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs have the same name.
            port_range: Port range for the target
            port_list_id: UUID of the port list to use on target

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.create_target(name=name,asset_hosts_filter=asset_hosts_filter,hosts=hosts,comment=comment,exclude_hosts=exclude_hosts,ssh_credential_id=ssh_credential_id,ssh_credential_port=ssh_credential_port,smb_credential_id=smb_credential_id,esxi_credential_id=esxi_credential_id,snmp_credential_id=snmp_credential_id,alive_test=alive_test,reverse_lookup_only=reverse_lookup_only,reverse_lookup_unify=reverse_lookup_unify,port_range=port_range,port_list_id=port_list_id), media_type="application/xml")
