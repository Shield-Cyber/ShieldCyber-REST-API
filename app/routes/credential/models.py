from dataclasses import dataclass
from pydantic import BaseModel
from gvm.protocols.gmpv208.entities.credentials import CredentialType, SnmpAuthAlgorithm, SnmpPrivacyAlgorithm

@dataclass
class CredentialBase:
    name: str
    credential_type: CredentialType
    comment: str | None = None
    allow_insecure: bool | None = False
    certificate: str | None = None
    key_phrase: str | None = None
    private_key: str | None = None
    login: str | None = None
    password: str | None = None
    auth_algorithm: SnmpAuthAlgorithm | None = None
    community: str | None = None
    privacy_algorithm: SnmpPrivacyAlgorithm | None = None
    privacy_password: str | None = None
    public_key: str | None = None