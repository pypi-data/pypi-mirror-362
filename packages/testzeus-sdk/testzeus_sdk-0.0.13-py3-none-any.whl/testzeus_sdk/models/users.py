"""
Model for users collection.
"""

import datetime
from typing import Any, Dict, List, Optional

from .base import BaseModel


class Users(BaseModel):
    """
    Users model for users collection
    """

    def __init__(self, data: Dict[str, Any]):
        """
        Initialize a Users instance

        Args:
            data: Dictionary containing model data
        """
        super().__init__(data)
        self.password = data.get("password")
        self.tokenKey = data.get("tokenKey")
        self.email = data.get("email")
        self.emailVisibility = data.get("emailVisibility")
        self.verified = data.get("verified")
        self.name = data.get("name")
        self.avatar = data.get("avatar")
        self.tenant = data.get("tenant")
        self.oauth2id = data.get("oauth2id")
        self.oauth2username = data.get("oauth2username")
        self.eula_signed = data.get("eula_signed")
        self.profile_updated = data.get("profile_updated")
        self.company = data.get("company")
        self.hmac = data.get("hmac")
        self.admin = data.get("admin")
