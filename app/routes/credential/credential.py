from fastapi import APIRouter, Depends, Body
from app import LOGGING_PREFIX
from app.utils.auth import Auth
from app.utils.xml import XMLResponse
from app.utils.error import ErrorResponse
from gvm.protocols.gmp import Gmp
from gvm.connections import UnixSocketConnection
from gvm.errors import RequiredArgument
from gvm.protocols.gmp.requests.v224 import (
    CredentialFormat,
    CredentialType,
    SnmpPrivacyAlgorithm,
    SnmpAuthAlgorithm,
)
from typing import Annotated, Optional
import logging

from . import models as Models

ENDPOINT = "credential"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.post("/create")
def create_credential(
        current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
        Base: Models.CreateCredential
):
    """Create a new credential

        Create a new credential e.g. to be used in the method of an alert.

        Currently the following credential types are supported:

            - Username + Password
            - Username + SSH-Key
            - Client Certificates
            - SNMPv1 or SNMPv2c protocol
            - S/MIME Certificate
            - OpenPGP Key
            - Password only

        Arguments:

            name: Name of the new credential
            credential_type: The credential type.
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential. Required for client-certificate and smime credential types.
            key_phrase: Key passphrase for the private key. Used for the username+ssh-key credential type.
            private_key: Private key to use for login. Required for usk credential type. Also used for the cc credential type. The supported key types (dsa, rsa, ecdsa, ...) and formats (PEM, PKC#12, OpenSSL, ...) depend on your installed GnuTLS version.
            login: Username for the credential. Required for username+password, username+ssh-key and snmp credential type.
            password: Password for the credential. Used for username+password and snmp credential types.
            community: The SNMP community
            auth_algorithm: The SNMP authentication algorithm. Required for snmp credential type.
            privacy_algorithm: The SNMP privacy algorithm
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format. Required for pgp credential type.

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.create_credential(name=Base.name,credential_type=Base.credential_type,comment=Base.comment,allow_insecure=Base.allow_insecure,certificate=Base.certificate,key_phrase=Base.key_phrase,private_key=Base.private_key,login=Base.login,password=Base.password,auth_algorithm=Base.auth_algorithm,community=Base.community,privacy_algorithm=Base.privacy_algorithm,privacy_password=Base.privacy_password,public_key=Base.public_key)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/{credential_id}")
def get_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str,
    scanners: bool = None,
    targets: bool = None,
    credential_format: CredentialFormat = None,
):
    """Request a single credential

        Arguments:

            credential_id: UUID of an existing credential
            scanners: Whether to include a list of scanners using the credentials
            targets: Whether to include a list of targets using the credentials
            credential_format: One of "key", "rpm", "deb", "exe" or "pem"

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_credential(credential_id=credential_id,scanners=scanners,targets=targets,credential_format=credential_format)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.get("/get/credentials")
def get_credentials(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: str = None,
    filter_id: str = None,
    scanners: bool = None,
    trash: bool = None,
    targets: bool = None,
):
    """Request a list of credentials

        Arguments:

            filter_string: Filter term to use for the query
            filter_id: UUID of an existing filter to use for the query
            scanners: Whether to include a list of scanners using the credentials
            trash: Whether to get the trashcan credentials instead
            targets: Whether to include a list of targets using the credentials

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.get_credentials(filter_string=filter_string,filter_id=filter_id,scanners=scanners,trash=trash,targets=targets)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.post("/clone/{credential_id}")
def clone_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str
):
    """Clone an existing credential

        Arguments:

            credential_id: UUID of an existing credential to clone from

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.clone_credential(credential_id=credential_id)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.delete("/delete/{credential_id}")
def delete_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str,
    ultimate: bool = False
):
    """Deletes an existing credential

        Arguments:

            credential_id: UUID of the credential to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.delete_credential(credential_id=credential_id, ultimate=ultimate)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")

@ROUTER.patch("/modify/{credential_id}")
def modify_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str,
    Base: Models.ModifyCredential
):
    """Modifies an existing credential.

        Arguments:

            credential_id: UUID of the credential
            name: Name of the credential
            comment: Comment for the credential
            allow_insecure: Whether to allow insecure use of the credential
            certificate: Certificate for the credential
            key_phrase: Key passphrase for the private key
            private_key: Private key to use for login
            login: Username for the credential
            password: Password for the credential
            auth_algorithm: The authentication algorithm for SNMP
            community: The SNMP community
            privacy_algorithm: The privacy algorithm for SNMP
            privacy_password: The SNMP privacy password
            public_key: PGP public key in *armor* plain text format

        Returns:
            The response.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=Auth.get_admin_password())
        try:
            return gmp.modify_credential(credential_id=credential_id,name=Base.name,credential_type=Base.credential_type,comment=Base.comment,allow_insecure=Base.allow_insecure,certificate=Base.certificate,key_phrase=Base.key_phrase,private_key=Base.private_key,login=Base.login,password=Base.password,auth_algorithm=Base.auth_algorithm,community=Base.community,privacy_algorithm=Base.privacy_algorithm,privacy_password=Base.privacy_password,public_key=Base.public_key)
        except Exception as err:
            LOGGER.error(f"GMP Error: {err}")
            return ErrorResponse("Internal Server Error")
