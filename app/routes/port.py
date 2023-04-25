from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth, PASSWORD
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX

ENDPOINT = "port"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT]
    )

### ROUTES ###

@ROUTER.get("/get/port/lists")
async def get_port_lists(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    details: Optional[bool] = None,
    targets: Optional[bool] = None,
    trash: Optional[bool] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return Response(content=gmp.get_port_lists(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details,targets=targets), media_type="application/xml")
