from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from gvm.protocols.gmpv208.entities.credentials import CredentialType, SnmpAuthAlgorithm, SnmpPrivacyAlgorithm

@dataclass
class CreateCredential:
    name: str
    credential_type: CredentialType
    comment: Optional[str] = None
    allow_insecure: Optional[bool] = None
    certificate: Optional[str] = None
    key_phrase: Optional[str] = None
    private_key: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    auth_algorithm: Optional[SnmpAuthAlgorithm] = None
    community: Optional[str] = None
    privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None
    privacy_password: Optional[str] = None
    public_key: Optional[str] = None

@dataclass
class ModifyCredential:
    name: Optional[str] = None
    comment: Optional[str] = None
    allow_insecure: Optional[bool] = None
    certificate: Optional[str] = None
    key_phrase: Optional[str] = None
    private_key: Optional[str] = None
    login: Optional[str] = None
    password: Optional[str] = None
    auth_algorithm: Optional[SnmpAuthAlgorithm] = None
    community: Optional[str] = None
    privacy_algorithm: Optional[SnmpPrivacyAlgorithm] = None
    privacy_password: Optional[str] = None
    public_key: Optional[str] = None