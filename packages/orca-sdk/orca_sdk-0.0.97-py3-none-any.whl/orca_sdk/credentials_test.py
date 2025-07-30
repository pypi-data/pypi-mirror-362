from uuid import uuid4

import pytest

from .credentials import OrcaCredentials


def test_list_api_keys():
    api_keys = OrcaCredentials.list_api_keys()
    assert len(api_keys) >= 1
    assert "orca_sdk_test" in [api_key.name for api_key in api_keys]


def test_list_api_keys_unauthenticated(unauthenticated):
    with pytest.raises(ValueError, match="Invalid API key"):
        OrcaCredentials.list_api_keys()


def test_is_authenticated():
    assert OrcaCredentials.is_authenticated()


def test_is_authenticated_false(unauthenticated):
    assert not OrcaCredentials.is_authenticated()


def test_set_api_key(api_key, unauthenticated):
    assert not OrcaCredentials.is_authenticated()
    OrcaCredentials.set_api_key(api_key)
    assert OrcaCredentials.is_authenticated()


def test_set_invalid_api_key(api_key):
    assert OrcaCredentials.is_authenticated()
    with pytest.raises(ValueError, match="Invalid API key"):
        OrcaCredentials.set_api_key(str(uuid4()))
    assert not OrcaCredentials.is_authenticated()
