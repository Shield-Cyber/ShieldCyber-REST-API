from fastapi import APIRouter, Depends
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
import logging
from gvm.connections import UnixSocketConnection
from typing import Annotated, Optional
from app import LOGGING_PREFIX

ENDPOINT = "user"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.get("/get/user")
async def get_user(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    user_id: str
    ):
    """Request a single user

        Arguments:

            user_id: UUID of an existing user

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_user(user_id=user_id)
        except Exception as err:
            return ErrorResponse(err)

@ROUTER.get("/get/user/settings")
async def get_user_settings(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None
    ):
    """Request a list of user settings

        Arguments:

            filter_string: Filter term to use for the query

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_user_settings(filter_string=filter_string)
        except Exception as err:
            return ErrorResponse(err)

@ROUTER.get("/get/user/setting")
async def get_user_setting(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    setting_id: str
    ):
    """Request a single user setting

        Arguments:

            setting_id: UUID of an existing setting

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_user_setting(setting_id=setting_id)
        except Exception as err:
            return ErrorResponse(err)
    
@ROUTER.get("/get/users")
async def get_users(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    ):
    """Request a list of users

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_users(filter_id=filter_id, filter_string=filter_string)
        except Exception as err:
            return ErrorResponse(err)
