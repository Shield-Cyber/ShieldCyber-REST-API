from fastapi import APIRouter, Depends, HTTPException, status, Response
from app.utils.auth import Auth, users_db, ACCESS_TOKEN_EXPIRE_MINUTES
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
from gvm.connections import UnixSocketConnection
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import logging
from datetime import timedelta
from app import LOGGING_PREFIX

ENDPOINT = "authenticate"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT]
    )

### ROUTES ###

@ROUTER.post("", response_model=Auth.Token)
async def authenticate(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = Auth.authenticate_user(users_db, form_data.username, form_data.password)
    if not user:
        LOGGER.warning(f"User '{form_data.username}' has failed authentication.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = Auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    LOGGER.info(f"User '{form_data.username}' has passed authentication.")
    return {"access_token": access_token, "token_type": "bearer"}

@ROUTER.get("/describe_auth", response_class=XMLResponse)
async def describe_auth(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
):
    """Describe authentication methods

        Returns a list of all used authentication methods if such a list is available.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return XMLResponse(gmp.describe_auth())
        except Exception as err:
            return ErrorResponse(err)

@ROUTER.get("/is_authenticated", response_class=XMLResponse)
async def is_authenticated(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)]
):
    """Checks if the user is authenticated

        If the user is authenticated privileged GMP commands like get_tasks
        may be send to gvmd.

        Returns:
            bool: True if an authenticated connection to gvmd has been
            established.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            response = str(gmp.is_authenticated())
            return XMLResponse(f'<is_authenticated_response status="200" status_text="{response}"/>')
        except Exception as err:
            return ErrorResponse(err)

@ROUTER.patch("/modify_auth", response_class=XMLResponse)
async def modify_auth(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    group_name: str,
    auth_conf_settings: dict
):
    """Modifies an existing auth.

        Arguments:

            group_name: Name of the group to be modified.
            auth_conf_settings: The new auth config.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return XMLResponse(gmp.modify_auth(group_name=group_name, auth_conf_settings=auth_conf_settings))
        except Exception as err:
            return ErrorResponse(err)
