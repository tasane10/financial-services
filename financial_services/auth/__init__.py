"""Authentication package for financial-services.

Provides API key generation, validation, revocation, and middleware
for securing integrations such as Claude for Microsoft 365.

Usage example::

    from financial_services.auth import APIKeyManager, require_api_key, AuthenticationError

    manager = APIKeyManager()
    key_id, secret = manager.generate_key("claude-msft-365", ttl_seconds=86400)

    # Later, validate:
    is_valid = manager.validate_key(key_id, secret)

    # Protect a function:
    @require_api_key
    def fetch_account_data(key_id: str, api_secret: str, account_id: str):
        return {"account_id": account_id, "balance": 0.0}
"""

from financial_services.auth.api_key_manager import APIKey, APIKeyManager
from financial_services.auth.middleware import (
    AuthenticationError,
    extract_credentials_from_header,
    get_manager,
    require_api_key,
)

__all__ = [
    "APIKey",
    "APIKeyManager",
    "AuthenticationError",
    "extract_credentials_from_header",
    "get_manager",
    "require_api_key",
]
