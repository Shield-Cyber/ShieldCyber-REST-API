from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated
from app import LOGGING_PREFIX

ENDPOINT = "version"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT]
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
        return Response(content=gmp.get_version(), media_type="application/xml")
    
@ROUTER.get("/get/protocol/version")
async def get_protocol_version(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
):
    """Determine the Greenbone Management Protocol (gmp) version used by python-gvm version.

        Returns:
            tuple: Implemented version of the Greenbone Management Protocol
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        return gmp.get_protocol_version()