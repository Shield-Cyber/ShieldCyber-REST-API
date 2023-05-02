from fastapi import APIRouter, Depends
from app import LOGGING_PREFIX
from app.utils.auth import Auth, PASSWORD
from app.utils.xml import XMLResponse
from gvm.protocols.gmp import Gmp
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmpv208.entities.credentials import CredentialType, SnmpAuthAlgorithm, SnmpPrivacyAlgorithm, CredentialFormat
from typing import Annotated, Optional
import logging

ENDPOINT = "credential"

LOGGER = logging.getLogger(f"{LOGGING_PREFIX}.{ENDPOINT}")

ROUTER = APIRouter(
    prefix=f"/{ENDPOINT}",
    tags=[ENDPOINT],
    default_response_class=XMLResponse
    )

### ROUTES ###

@ROUTER.post("/create/credential")
def create_credential(
        current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
        name: str,
        credential_type: CredentialType,
        comment: Optional[str] = None,
        allow_insecure: Optional[bool] = None,
        certificate: Optional[str] = None,
        key_phrase: Optional[str] = None,
        private_key: Optional[str] = None,
        login: Optional[str] = None,
        password: Optional[str] = None,
        auth_algorithm: Optional[SnmpAuthAlgorithm] = None,
        community: Optional[str] = None,
        privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None,
        privacy_password: Optional[str] = None,
        public_key: Optional[str] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.create_credential(name=name,credential_type=credential_type,comment=comment,allow_insecure=allow_insecure,certificate=certificate,key_phrase=key_phrase,private_key=private_key,login=login,password=password,auth_algorithm=auth_algorithm,community=community,privacy_algorithm=privacy_algorithm,privacy_password=privacy_password,public_key=public_key)
    
@ROUTER.get("/get/credential")
def get_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str,
    scanners: Optional[bool] = None,
    targets: Optional[bool] = None,
    credential_format: Optional[CredentialFormat] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_credential(credential_id=credential_id,scanners=scanners,targets=targets,credential_format=credential_format)
    
@ROUTER.get("/get/credentials")
def get_credentials(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    filter_string: Optional[str] = None,
    filter_id: Optional[str] = None,
    scanners: Optional[bool] = None,
    trash: Optional[bool] = None,
    targets: Optional[bool] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.get_credentials(filter_string=filter_string,filter_id=filter_id,scanners=scanners,trash=trash,targets=targets)
    
@ROUTER.post("/clone/credential")
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.clone_credential(credential_id=credential_id)
    
@ROUTER.delete("/delete/credential")
def delete_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str,
    ultimate: Optional[bool] = False
):
    """Deletes an existing credential

        Arguments:

            credential_id: UUID of the credential to be deleted.
            ultimate: Whether to remove entirely, or to the trashcan.
        """
    with Gmp(connection=UnixSocketConnection()) as gmp:
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.delete_credential(credential_id=credential_id, ultimate=ultimate)
    
@ROUTER.patch("/modify/credential")
def modify_credential(
    current_user: Annotated[Auth.User, Depends(Auth.get_current_active_user)],
    credential_id: str,
    name: Optional[str] = None,
    comment: Optional[str] = None,
    allow_insecure: Optional[bool] = None,
    certificate: Optional[str] = None,
    key_phrase: Optional[str] = None,
    private_key: Optional[str] = None,
    login: Optional[str] = None,
    password: Optional[str] = None,
    auth_algorithm: Optional[SnmpAuthAlgorithm] = None,
    community: Optional[str] = None,
    privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None,
    privacy_password: Optional[str] = None,
    public_key: Optional[str] = None,
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
        gmp.authenticate(username=current_user.username, password=PASSWORD)
        return gmp.modify_credential(name=name,credential_id=credential_id,comment=comment,allow_insecure=allow_insecure,certificate=certificate,key_phrase=key_phrase,private_key=private_key,login=login,password=password,auth_algorithm=auth_algorithm,community=community,privacy_algorithm=privacy_algorithm,privacy_password=privacy_password,public_key=public_key)
    