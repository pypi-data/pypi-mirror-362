import contextvars

# Context variable to hold the per-request TessellAuthConfig
auth_config_var = contextvars.ContextVar("auth_config")
