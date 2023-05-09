from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth, PASSWORD
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX

ENDPOINT = "scanner"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/scanners")
async def get_scanners(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    details: Optional[bool] = None,
    ):
    """Request a list of scanners

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scanners instead
            details:  Whether to include extra details like tasks using this scanner

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        try:
            return gmp.get_scanners(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details)
        except Exception as err:
            return ErrorResponse(err)
