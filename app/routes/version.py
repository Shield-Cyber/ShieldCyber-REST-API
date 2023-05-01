from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated
from app import LOGGING_PREFIX, VERSION

ENDPOINT = "version"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/version")
async def get_version(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
):
    """Get the Greenbone Vulnerability Manager Protocol version used by the remote gvmd.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        return gmp.get_version()
    
@ROUTER.get("/get/protocol/version")
async def get_protocol_version(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
):
    """Determine the Greenbone Management Protocol (gmp) version used by python-gvm version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        content = str(gmp.get_protocol_version())
        return Response(content=content, media_type="application/xml")
    
@ROUTER.get("/get/api/version")
async def get_api_version(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
):
    """Determine the current API version.

        Returns:
            str: Version of the API
        """
    content = f"<version>{VERSION}</version>"
    return Response(content=content, media_type="application/xml")