from fastapi import APIRouter, Depends, Response, Body
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX
from gvm.protocols.gmpv208.entities.port_lists import PortRangeType

from . import models as Models

ENDPOINT = "port"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/lists")
async def get_port_lists(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: str = None,
    filter_id: str = None,
    details: bool = None,
    targets: bool = None,
    trash: bool = None,
    ):
    """Request a list of port lists

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            details: Whether to include full port list details
            targets: Whether to include targets using this port list
            trash: Whether to get port lists in the trashcan instead

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_port_lists(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details,targets=targets)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/list/{port_list_id}")
async def get_port_list(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    port_list_id: str
    ):
    """Request a single port list

        Arguments:

            port_list_id: UUID of an existing port list

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_port_list(port_list_id=port_list_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/clone/list/{port_list_id}")
async def clone_port_list(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    port_list_id: str
    ):
    """Clone an existing port list

        Arguments:

            port_list_id: UUID of an existing port list to clone from

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.clone_port_list(port_list_id=port_list_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/create/list")
async def create_port_list(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.CreatePortList
    ):
    """Create a new port list

        Arguments:

            name: Name of the new port list
            port_range: Port list ranges e.g. `"T: 1-1234"` for tcp port 1 - 1234
            comment: Comment for the port list

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_port_list(name=Base.name, port_range=Base.port_range, comment=Base.comment)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/create/range")
async def create_port_range(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.CreatePortRange
    ):
    """Create new port range

        Arguments:

            port_list_id: UUID of the port list to which to add the range
            start: The first port in the range
            end: The last port in the range
            port_range_type: The type of the ports: TCP, UDP, ...
            comment: Comment for the port range

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_port_range(port_list_id=Base.port_list_id,start=Base.start,end=Base.end,port_range_type=Base.port_range_type,comment=Base.comment)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.delete("/delete/list/{port_list_id}")
async def delete_port_list(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    port_list_id: str,
    ultimate: Optional[bool] = False
    ):
    """Deletes an existing port list

        Arguments:

            port_list_id: UUID of the port list to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_port_list(port_list_id=port_list_id, ultimate=ultimate)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.delete("/delete/range/{port_range_id}")
async def delete_port_range(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    port_range_id: str
    ):
    """Deletes an existing port range

        Arguments:

            port_range_id: UUID of the port range to be deleted.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_port_range(port_range_id=port_range_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.patch("/modify/list/{port_list_id}")
async def modify_port_list(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    port_list_id: str,
    Base: Models.ModifyPortList
    ):
    """Modifies an existing port list.

        Arguments:

            port_list_id: UUID of port list to modify.
            name: Name of port list.
            comment: Comment on port list.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.modify_port_list(port_list_id=port_list_id, comment=comment, name=name)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")