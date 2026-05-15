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

Notes (personal fork):
    - Default TTL for generated keys is 86400s (24h). For local dev/testing,
      consider passing ttl_seconds=3600 (1h) to generate_key() to limit
      exposure if a key is accidentally logged.
    - To list all active keys and their expiry times, iterate over
      manager.list_keys() and check the `expires_at` field on each APIKey.
      Handy for debugging expired-key errors locally.
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
