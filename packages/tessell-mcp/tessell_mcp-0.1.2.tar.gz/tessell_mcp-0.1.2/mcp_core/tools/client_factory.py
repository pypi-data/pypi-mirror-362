from mcp_core.context import auth_config_var
from mcp_core.auth_config import TessellAuthConfig
from api_client.tessell_api_client import TessellApiClient

def get_tessell_api_client():
    """
    Returns a TessellApiClient using auth config from HTTP headers (contextvars),
    or falls back to environment-based config if not set or missing jwt_token.
    """
    try:
        header_cfg = auth_config_var.get()
    except LookupError:
        header_cfg = None
    if header_cfg and header_cfg.jwt_token:
        return TessellApiClient(
            base_url=header_cfg.api_base,
            tenant_id=header_cfg.tenant_id,
            jwt_token=header_cfg.jwt_token
        )
    env_cfg = TessellAuthConfig()
    return TessellApiClient(
        base_url=env_cfg.api_base,
        api_key=env_cfg.api_key,
        tenant_id=env_cfg.tenant_id
    )