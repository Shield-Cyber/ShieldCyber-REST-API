from fastapi import APIRouter, Depends, Response, Body
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
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

@ROUTER.get("/get/configs")
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
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_scan_configs(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details,families=families,preferences=preferences,tasks=tasks)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")


@ROUTER.post("/import/config")
async def import_scan_config(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    config = Body(..., media_type="application/xml")
):
    """Import a scan config from XML

    Args:

        config: Scan Config XML as string to import. This XML must contain a `<get_configs_response>` root element.
    
    Make the entire body the raw xml.

    """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(
            username=current_user.username, password=Auth.get_admin_password()
        )
        try:
            return gmp.import_scan_config(config)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
