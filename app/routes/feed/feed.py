from fastapi import APIRouter, Depends
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
# from gvm.protocols.gmpv208.system.feed import FeedType
from gvm.protocols.gmp.requests.v224 import FeedType
from app import LOGGING_PREFIX

ENDPOINT = "feed"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/feeds")
async def get_feeds(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
    ):
    """Request the list of feeds

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_feeds()
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/{feed_type}")
async def get_feed(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    feed_type: FeedType
    ):
    """Request a single feed

        Arguments:
        
            feed_type: Type of single feed to get: NVT, CERT or SCAP

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_feed(feed_type=feed_type)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
