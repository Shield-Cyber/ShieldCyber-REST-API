from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth, PASSWORD
from app.utils.xml import XMLResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX

ENDPOINT = "scan"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/scan/configs")
async def get_scan_configs(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    trash: Optional[bool] = None,
    details: Optional[bool] = None,
    families: Optional[bool] = None,
    preferences: Optional[bool] = None,
    tasks: Optional[bool] = None
    ):
    """Request a list of scan configs

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            trash: Whether to get the trashcan scan configs instead
            details: Whether to get config families, preferences, nvt selectors and tasks.
            families: Whether to include the families if no details are requested
            preferences: Whether to include the preferences if no details are requested
            tasks: Whether to get tasks using this config

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_scan_configs(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details,families=families,preferences=preferences,tasks=tasks)

@ROUTER.get("/get/scanners", deprecated=True)
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
        return Response(content=gmp.get_scanners(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details), media_type="application/xml")
