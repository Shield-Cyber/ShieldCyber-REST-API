from fastapi import APIRouter, Depends, Response
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX

from . import models as Models

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
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_scanners(filter_string=filter_string,filter_id=filter_id,trash=trash,details=details)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/{scanner_id}")
async def get_scanner(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    scanner_id: str
    ):
    """Request a single scanner

        Arguments:

            scanner_id: UUID of an existing scanner

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_scanner(scanner_id=scanner_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
        
@ROUTER.post("/create")
async def create_scanner(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    Base: Models.CreateScanner
    ):
    """Create a new scanner

        Arguments:

            name: Name of the scanner
            host: The host of the scanner
            port: The port of the scanner
            scanner_type: Type of the scanner.
            credential_id: UUID of client certificate credential for the scanner
            ca_pub: Certificate of CA to verify scanner certificate
            comment: Comment for the scanner

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_scanner(name=Base.name,host=Base.host,port=Base.port,scanner_type=Base.scanner_type,credential_id=Base.credential_id,ca_pub=Base.ca_pub,comment=Base.comment)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
        
@ROUTER.patch("/modify/{scanner_id}")
async def modify_scanner(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    scanner_id: str,
    Base: Models.ModifyScanner
    ):
    """Modifies an existing scanner.

        Arguments:

            scanner_id: UUID of scanner to modify.
            scanner_type: New type of the Scanner.
            host: Host of the scanner.
            port: Port of the scanner.
            comment: Comment on scanner.
            name: Name of scanner.
            ca_pub: Certificate of CA to verify scanner's certificate.
            credential_id: UUID of the client certificate credential for the Scanner.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.modify_scanner(scanner_id=scanner_id,scanner_type=Base.scanner_type,host=Base.host,port=Base.port,comment=Base.comment,name=Base.name,ca_pub=Base.ca_pub,credential_id=Base.credential_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
        
@ROUTER.post("/clone/{scanner_id}")
async def clone_scanner(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    scanner_id: str
    ):
    """Clone an existing scanner

        Arguments:

            scanner_id: UUID of an existing scanner to clone from

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.clone_scanner(scanner_id=scanner_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
        
@ROUTER.delete("/delete/{scanner_id}")
async def delete_scanner(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    scanner_id: str,
    ultimate: Optional[bool] = False
    ):
    """Deletes an existing scanner

        Arguments:

            scanner_id: UUID of the scanner to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_scanner(scanner_id=scanner_id,ultimate=ultimate)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
        
@ROUTER.get("/verify/{scanner_id}")
async def verify_scanner(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    scanner_id: str
    ):
    """Verify an existing scanner

        Verifies if it is possible to connect to an existing scanner. It is *not* verified if the scanner works as expected by the user.

        Arguments:

            scanner_id: UUID of the scanner to be verified

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.verify_scanner(scanner_id=scanner_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")