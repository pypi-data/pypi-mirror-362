"""This module contains internal utils for managing api keys in tests"""

import logging
import os
from typing import List

from dotenv import load_dotenv

from .._generated_api_client.api import (
    check_authentication,
    create_api_key,
    delete_api_key,
    delete_org,
    list_api_keys,
)
from .._generated_api_client.client import headers_context, set_base_url, set_headers
from .._generated_api_client.models import (
    CreateApiKeyRequest,
    CreateApiKeyRequestScopeItem,
)
from .._generated_api_client.models.api_key_metadata import ApiKeyMetadata
from .common import DropMode

load_dotenv()  # this needs to be here to ensure env is populated before accessing it

# the defaults here must match nautilus and lighthouse config defaults
_ORCA_ROOT_ACCESS_API_KEY = os.environ.get("ORCA_ROOT_ACCESS_API_KEY", "00000000-0000-0000-0000-000000000000")
_DEFAULT_ORG_ID = os.environ.get("DEFAULT_ORG_ID", "10e50000-0000-4000-a000-a78dca14af3a")


def _create_api_key(org_id: str, name: str, scopes: list[str] = ["ADMINISTER"]) -> str:
    """Creates an API key for the given organization"""
    with headers_context({"Api-Key": _ORCA_ROOT_ACCESS_API_KEY, "Org-Id": org_id}):
        res = create_api_key(
            body=CreateApiKeyRequest(name=name, scope=[CreateApiKeyRequestScopeItem(scope) for scope in scopes])
        )
        return res.api_key


def _list_api_keys(org_id: str) -> List[ApiKeyMetadata]:
    """Lists all API keys for the given organization"""
    with headers_context({"Api-Key": _ORCA_ROOT_ACCESS_API_KEY, "Org-Id": org_id}):
        return list_api_keys()


def _delete_api_key(org_id: str, name: str, if_not_exists: DropMode = "error") -> None:
    """Deletes the API key with the given name from the organization"""
    with headers_context({"Api-Key": _ORCA_ROOT_ACCESS_API_KEY, "Org-Id": org_id}):
        try:
            delete_api_key(name_or_id=name)
        except LookupError:
            if if_not_exists == "error":
                raise


def _delete_org(org_id: str) -> None:
    """Deletes the organization"""
    with headers_context({"Api-Key": _ORCA_ROOT_ACCESS_API_KEY, "Org-Id": org_id}):
        delete_org()


def _authenticate_local_api(org_id: str = _DEFAULT_ORG_ID, api_key_name: str = "local") -> None:
    """Connect to the local API at http://localhost:1584/ and authenticate with a new API key"""
    set_base_url("http://localhost:1584/")
    _delete_api_key(org_id, api_key_name, if_not_exists="ignore")
    set_headers({"Api-Key": _create_api_key(org_id, api_key_name)})
    check_authentication()
    logging.info(f"Authenticated against local API at 'http://localhost:1584' with '{api_key_name}' API key")


__all__ = ["_create_api_key", "_delete_api_key", "_delete_org", "_list_api_keys", "_authenticate_local_api"]
