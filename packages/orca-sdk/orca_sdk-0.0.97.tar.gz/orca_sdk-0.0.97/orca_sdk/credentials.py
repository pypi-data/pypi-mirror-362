from datetime import datetime
from typing import Literal, NamedTuple

from ._generated_api_client.api import (
    check_authentication,
    create_api_key,
    delete_api_key,
    list_api_keys,
)
from ._generated_api_client.client import get_base_url, get_headers, set_headers
from ._generated_api_client.models import (
    CreateApiKeyRequest,
    CreateApiKeyRequestScopeItem,
)

Scope = Literal["ADMINISTER", "PREDICT"]
"""
The scopes of an API key.

- `ADMINISTER`: Can do anything, including creating and deleting organizations, models, and API keys.
- `PREDICT`: Can only call model.predict and perform CRUD operations on predictions.
"""


class ApiKeyInfo(NamedTuple):
    """
    Named tuple containing information about an API key

    Attributes:
        name: Unique name of the API key
        created_at: When the API key was created
    """

    name: str
    created_at: datetime
    scopes: set[Scope]


class OrcaCredentials:
    """
    Class for managing Orca API credentials
    """

    @staticmethod
    def get_api_url() -> str:
        """
        Get the Orca API base URL that is currently being used
        """
        return get_base_url()

    @staticmethod
    def list_api_keys() -> list[ApiKeyInfo]:
        """
        List all API keys that have been created for your org

        Returns:
            A list of named tuples, with the name and creation date time of the API key
        """
        return [
            ApiKeyInfo(name=api_key.name, created_at=api_key.created_at, scopes=set(s.value for s in api_key.scope))
            for api_key in list_api_keys()
        ]

    @staticmethod
    def is_authenticated() -> bool:
        """
        Check if you are authenticated to interact with the Orca API

        Returns:
            True if you are authenticated, False otherwise
        """
        try:
            return check_authentication()
        except ValueError as e:
            if "Invalid API key" in str(e):
                return False
            raise e

    @staticmethod
    def create_api_key(name: str, scopes: set[Scope] = {"ADMINISTER"}) -> str:
        """
        Create a new API key with the given name and scopes

        Params:
            name: The name of the API key
            scopes: The scopes of the API key

        Returns:
            The secret value of the API key. Make sure to save this value as it will not be shown again.
        """
        res = create_api_key(
            body=CreateApiKeyRequest(name=name, scope=[CreateApiKeyRequestScopeItem(scope) for scope in scopes])
        )
        return res.api_key

    @staticmethod
    def revoke_api_key(name: str) -> None:
        """
        Delete an API key

        Params:
            name: The name of the API key to delete

        Raises:
            ValueError: if the API key is not found
        """
        delete_api_key(name_or_id=name)

    @staticmethod
    def set_headers(headers: dict[str, str]):
        """
        Add or override default HTTP headers for all Orca API requests.

        Args:
            **kwargs: Header names with their string values

        Notes:
            New keys are merged into the existing headers, this will overwrite headers with the
            same name, but leave other headers untouched.
        """
        set_headers(get_headers() | headers)

    @staticmethod
    def set_api_key(api_key: str, check_validity: bool = True):
        """
        Set the API key to use for authenticating with the Orca API

        Note:
            The API key can also be provided by setting the `ORCA_API_KEY` environment variable

        Params:
            api_key: The API key to set
            check_validity: Whether to check if the API key is valid and raise an error otherwise

        Raises:
            ValueError: if the API key is invalid and `check_validity` is True
        """
        OrcaCredentials.set_headers({"Api-Key": api_key})
        if check_validity:
            check_authentication()
