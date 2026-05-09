"""API Key management for financial services authentication."""

import hashlib
import hmac
import os
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class APIKey:
    """Represents an API key with metadata."""

    key_id: str
    hashed_secret: str
    service_name: str
    created_at: float = field(default_factory=time.time)
    expires_at: Optional[float] = None
    is_active: bool = True

    def is_expired(self) -> bool:
        """Check if the API key has expired."""
        if self.expires_at is None:
            return False
        return time.time() > self.expires_at

    def is_valid(self) -> bool:
        """Check if the API key is valid (active and not expired)."""
        return self.is_active and not self.is_expired()


class APIKeyManager:
    """Manages API keys for financial service integrations."""

    def __init__(self) -> None:
        self._keys: dict[str, APIKey] = {}

    def generate_key(self, service_name: str, ttl_seconds: Optional[int] = None) -> tuple[str, str]:
        """Generate a new API key pair (key_id, secret).

        Returns:
            Tuple of (key_id, raw_secret). The raw_secret is only returned once.
        """
        key_id = hashlib.sha256(os.urandom(32)).hexdigest()[:16]
        raw_secret = hashlib.sha256(os.urandom(64)).hexdigest()
        hashed_secret = self._hash_secret(raw_secret)

        expires_at = time.time() + ttl_seconds if ttl_seconds else None

        self._keys[key_id] = APIKey(
            key_id=key_id,
            hashed_secret=hashed_secret,
            service_name=service_name,
            expires_at=expires_at,
        )
        return key_id, raw_secret

    def validate_key(self, key_id: str, raw_secret: str) -> bool:
        """Validate an API key against stored credentials."""
        api_key = self._keys.get(key_id)
        if api_key is None or not api_key.is_valid():
            return False
        expected = self._hash_secret(raw_secret)
        return hmac.compare_digest(api_key.hashed_secret, expected)

    def revoke_key(self, key_id: str) -> bool:
        """Revoke an API key by marking it inactive."""
        api_key = self._keys.get(key_id)
        if api_key is None:
            return False
        api_key.is_active = False
        return True

    def get_key_info(self, key_id: str) -> Optional[APIKey]:
        """Retrieve metadata for a given key ID."""
        return self._keys.get(key_id)

    @staticmethod
    def _hash_secret(secret: str) -> str:
        return hashlib.sha256(secret.encode()).hexdigest()
