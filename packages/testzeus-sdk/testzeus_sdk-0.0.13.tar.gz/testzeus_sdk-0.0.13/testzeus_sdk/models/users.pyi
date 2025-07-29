"""
Type stubs for the Users model.
"""

from typing import Any, Dict, Optional

from testzeus_sdk.models.base import BaseModel

class Users(BaseModel):
    """
    Users model for users collection
    """

    password: Optional[str]
    tokenKey: Optional[str]
    email: Optional[str]
    emailVisibility: Optional[bool]
    verified: Optional[bool]
    name: Optional[str]
    avatar: Optional[str]
    tenant: Optional[str]
    oauth2id: Optional[str]
    oauth2username: Optional[str]
    eula_signed: Optional[bool]
    profile_updated: Optional[bool]
    company: Optional[str]
    hmac: Optional[str]
    admin: Optional[bool]

    def __init__(self, data: Dict[str, Any]) -> None: ...
