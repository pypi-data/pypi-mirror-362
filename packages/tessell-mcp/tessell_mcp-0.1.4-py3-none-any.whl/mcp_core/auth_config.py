"""
Environment configuration for the Tessell API server.

This module handles all environment variable configuration with sensible defaults
and type conversion.

Initialization:
- You must provide either:
    1. TESSELL_API_BASE, TESSELL_API_KEY, and TESSELL_TENANT_ID (via env or constructor),
  OR
    2. jwt_token and tenant_id directly to the constructor.
- If jwt_token and tenant_id are provided, environment variable validation is skipped.
"""

from dotenv import load_dotenv
from dataclasses import dataclass
import os
from typing import Optional

@dataclass
class TessellAuthConfig:
    _api_base: Optional[str] = None
    _api_key: Optional[str] = None
    _tenant_id: Optional[str] = None
    _jwt_token: Optional[str] = None

    def __init__(self, api_base: Optional[str] = None, api_key: Optional[str] = None, tenant_id: Optional[str] = None, jwt_token: Optional[str] = None):
        load_dotenv()
        if api_base is not None:
            self._api_base = api_base
        if api_key is not None:
            self._api_key = api_key
        if tenant_id is not None:
            self._tenant_id = tenant_id
        if jwt_token is not None:
            self._jwt_token = jwt_token
        # Only validate required vars if not using JWT/tenant direct init
        if jwt_token is None and tenant_id is None:
            self._validate_required_vars()

    @property
    def api_base(self) -> str:
        """Get the Tessell API Base URL."""
        return self._api_base or os.getenv("TESSELL_API_BASE")

    @property
    def api_key(self) -> str:
        """Get the Tessell API Key."""
        return self._api_key or os.getenv("TESSELL_API_KEY")

    @property
    def tenant_id(self) -> str:
        """Get the Tessell Tenant ID."""
        return self._tenant_id or os.getenv("TESSELL_TENANT_ID")

    @property
    def jwt_token(self) -> Optional[str]:
        """Get the JWT token if set."""
        return self._jwt_token

    def get_client_config(self) -> dict:
        """Get the configuration dictionary for Tessell API client."""
        return {
            "api_base": self.api_base,
            "api_key": self.api_key,
            "tenant_id": self.tenant_id,
            "jwt_token": self.jwt_token,
        }

    def _validate_required_vars(self) -> None:
        """Validate that all required environment variables are set."""
        missing_vars = []
        for var in ["TESSELL_API_BASE", "TESSELL_API_KEY", "TESSELL_TENANT_ID"]:
            if not os.getenv(var):
                missing_vars.append(var)
        if missing_vars:
            raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")