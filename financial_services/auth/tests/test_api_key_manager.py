"""Tests for the APIKeyManager module."""

import time
import pytest
from financial_services.auth.api_key_manager import APIKey, APIKeyManager


@pytest.fixture
def manager() -> APIKeyManager:
    return APIKeyManager()


class TestAPIKeyGeneration:
    def test_generate_returns_key_id_and_secret(self, manager):
        key_id, secret = manager.generate_key("claude-msft-365")
        assert key_id is not None
        assert secret is not None
        assert len(key_id) == 16

    def test_generated_keys_are_unique(self, manager):
        key_id1, _ = manager.generate_key("service-a")
        key_id2, _ = manager.generate_key("service-a")
        assert key_id1 != key_id2

    def test_generate_with_ttl_sets_expiry(self, manager):
        key_id, _ = manager.generate_key("service-b", ttl_seconds=3600)
        info = manager.get_key_info(key_id)
        assert info.expires_at is not None
        assert info.expires_at > time.time()

    def test_generate_without_ttl_no_expiry(self, manager):
        key_id, _ = manager.generate_key("service-c")
        info = manager.get_key_info(key_id)
        assert info.expires_at is None

    def test_generate_with_zero_ttl_expires_immediately(self, manager):
        # Edge case: ttl_seconds=0 should result in an already-expired key
        key_id, secret = manager.generate_key("service-z", ttl_seconds=0)
        assert manager.validate_key(key_id, secret) is False


class TestAPIKeyValidation:
    def test_valid_key_passes_validation(self, manager):
        key_id, secret = manager.generate_key("service-d")
        assert manager.validate_key(key_id, secret) is True

    def test_wrong_secret_fails_validation(self, manager):
        key_id, _ = manager.generate_key("service-e")
        assert manager.validate_key(key_id, "wrong-secret") is False

    def test_unknown_key_id_fails_validation(self, manager):
        assert manager.validate_key("nonexistent", "any-secret") is False

    def test_expired_key_fails_validation(self, manager):
        key_id, secret = manager.generate_key("service-f", ttl_seconds=-1)
        assert manager.validate_key(key_id, secret) is False


class TestAPIKeyRevocation:
    def test_revoked_key_fails_validation(self, manager):
        key_id, secret = manager.generate_key("service-g")
        manager.revoke_key(key_id)
        assert manager.validate_key(key_id, secret) is False

    def test_revoke_nonexistent_key_returns_false(self, manager):
        assert manager.revoke_key("does-not-exist") is False

    def test_revoke_marks_key_inactive(self, manager):
        key_id, _ = manager.generate_key("service-h")
        manager.revoke_key(key_id)
        info = manager.get_key_info(key_id)
        assert info.is_active is False


class TestAPIKeyModel:
    def test_key_is_valid_when_active_and_not_expired(self):
        key = APIKey(key_id="abc", hashed_secret="xyz", service_name="svc")
        assert key.is_valid() is True

    def test_key_is_invalid_when_expired(self):
        key = APIKey(
            key_id="abc", hashed_secret="xyz", service_name="svc",
            expires_at=time.time() - 1
        )
        assert key.is_valid() is False

    def test_key_is_invalid_when_inactive(self):
        # Explicitly check that is_active=False alone invalidates the key
        key = APIKey(
            key_id="abc", hashed_secret="xyz", service_name="svc",
            is_active=False
        )
        assert key.is_valid() is False
