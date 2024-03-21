from fastapi import APIRouter, Depends
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional, List
from gvm.protocols.gmpv208.entities.targets import AliveTest
from gvm.errors import RequiredArgument
from app import LOGGING_PREFIX

from . import models as Models

ENDPOINT = "target"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.post("/create")
async def create_target(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.CreateTarget
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
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_target(name=Base.name,asset_hosts_filter=Base.asset_hosts_filter,hosts=Base.hosts,comment=Base.comment,exclude_hosts=Base.exclude_hosts,ssh_credential_id=Base.ssh_credential_id,ssh_credential_port=Base.ssh_credential_port,smb_credential_id=Base.smb_credential_id,esxi_credential_id=Base.esxi_credential_id,snmp_credential_id=Base.snmp_credential_id,alive_test=Base.alive_test,reverse_lookup_only=Base.reverse_lookup_only,reverse_lookup_unify=Base.reverse_lookup_unify,port_range=Base.port_range,port_list_id=Base.port_list_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/targets")
async def get_targets(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    tasks: Optional[bool] = None,
):
    """Request a list of targets

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan targets instead
            tasks: Whether to include list of tasks that use the target

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_targets(filter_string=filter_string,filter_id=filter_id,trash=trash,tasks=tasks)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/{target_id}")
async def get_target(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    target_id: str,
    tasks: Optional[bool] = None
):
    """Request a single target

        Arguments:

            target_id: UUID of an existing target
            tasks: Whether to include list of tasks that use the target

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_target(target_id=target_id, tasks=tasks)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
    
@ROUTER.post("/clone/{target_id}")
async def clone_target(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    target_id: str
):
    """Clone an existing target

        Arguments:

            target_id: UUID of an existing target to clone from

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.clone_target(target_id=target_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
    
@ROUTER.delete("/delete/{target_id}")
async def delete_target(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    target_id: str,
    ultimate: Optional[bool] = False
):
    """Deletes an existing target

        Arguments:

            target_id: UUID of the target to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_target(target_id=target_id, ultimate=ultimate)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
    
@ROUTER.patch("/modify/{target_id}")
async def modify_target(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    target_id: str,
    Base: Models.ModifyTarget
):
    """Modifies an existing target.

        Arguments:

            target_id: ID of target to modify.
            comment: Comment on target.
            name: Name of target.
            hosts: List of target hosts.
            exclude_hosts: A list of hosts to exclude.
            ssh_credential_id: UUID of SSH credential to use on target.
            ssh_credential_port: The port to use for ssh credential
            smb_credential_id: UUID of SMB credential to use on target.
            esxi_credential_id: UUID of ESXi credential to use on target.
            snmp_credential_id: UUID of SNMP credential to use on target.
            port_list_id: UUID of port list describing ports to scan.
            alive_test: Which alive tests to use.
            allow_simultaneous_ips: Whether to scan multiple IPs of the same host simultaneously
            reverse_lookup_only: Whether to scan only hosts that have names.
            reverse_lookup_unify: Whether to scan only one IP when multiple IPs have the same name.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.modify_target(target_id=target_id,name=Base.name,comment=Base.comment,hosts=Base.hosts,exclude_hosts=Base.exclude_hosts,ssh_credential_id=Base.ssh_credential_id,ssh_credential_port=Base.ssh_credential_port,smb_credential_id=Base.smb_credential_id,esxi_credential_id=Base.esxi_credential_id,snmp_credential_id=Base.snmp_credential_id,alive_test=Base.alive_test,allow_simultaneous_ips=Base.allow_simultaneous_ips,reverse_lookup_only=Base.reverse_lookup_only,reverse_lookup_unify=Base.reverse_lookup_unify,port_list_id=Base.port_list_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")