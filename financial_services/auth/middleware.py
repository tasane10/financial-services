"""Authentication middleware for financial services API endpoints."""

from functools import wraps
from typing import Callable

from financial_services.auth.api_key_manager import APIKeyManager

_manager: APIKeyManager = APIKeyManager()


def get_manager() -> APIKeyManager:
    """Return the shared APIKeyManager instance."""
    return _manager


def require_api_key(f: Callable) -> Callable:
    """Decorator to enforce API key authentication on a function/route.

    Expects the wrapped function to receive `key_id` and `api_secret`
    as keyword arguments, or raises AuthenticationError.
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        key_id = kwargs.get("key_id")
        api_secret = kwargs.get("api_secret")

        if not key_id or not api_secret:
            raise AuthenticationError("Missing API credentials.")

        if not _manager.validate_key(key_id, api_secret):
            raise AuthenticationError("Invalid or expired API key.")

        return f(*args, **kwargs)

    return wrapper


class AuthenticationError(Exception):
    """Raised when API key authentication fails."""

    def __init__(self, message: str = "Authentication failed.") -> None:
        super().__init__(message)
        self.message = message

    def to_dict(self) -> dict:
        return {"error": "authentication_error", "message": self.message}


def extract_credentials_from_header(auth_header: str) -> tuple[str, str]:
    """Parse 'ApiKey key_id:secret' Authorization header format.

    Returns:
        Tuple of (key_id, secret)

    Raises:
        ValueError: If header format is invalid.
    """
    if not auth_header or not auth_header.startswith("ApiKey "):
        raise ValueError("Authorization header must use 'ApiKey' scheme.")

    credentials = auth_header[len("ApiKey "):].strip()
    parts = credentials.split(":", 1)

    if len(parts) != 2 or not parts[0] or not parts[1]:
        raise ValueError("Credentials must be in 'key_id:secret' format.")

    return parts[0], parts[1]
