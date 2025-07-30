from typing import Any, Dict, Optional

from pydantic import BaseModel
from pydantic.alias_generators import to_camel

from sklik.api import SklikApi
from sklik.exception import SklikException


class AccountModel(BaseModel):
    class Config:
        title = "client"
        alias_generator = to_camel
        populate_by_name = True

    user_id: int
    username: str
    wallet_credit: Optional[int] = None
    wallet_credit_with_vat: Optional[int] = None
    wallet_verified: Optional[bool] = None
    day_budget_sum: Optional[int] = None
    account_limit: Optional[int] = None


class Account:
    """
    Represents a Sklik advertising account with API interaction capabilities.

    Provides an interface for interacting with a specific Sklik account, managing
    authentication, and making API calls. The class automatically fetches and maintains
    account data through the API.

    Attributes:
        account_id: Unique identifier of the Sklik account.
        api: API client instance used for making requests. If not provided,
            uses the default API client.

    Dynamic Attributes:
        All account properties (like username, access_level, etc.) are dynamically
        accessible through the underlying account model.

    Examples:
        >>> # Create account instance
        >>> account = Account(account_id=123456)
        >>>
        >>> # Access account properties
        >>> print(account.username)
        >>> print(account.access_level)
        # >>>
        # >>> # Make API calls
        # >>> response = account.call(
        # ...     service="campaigns",
        # ...     method="list",
        # ...     args=[{"includeDeleted": False}]
        # ... )

    Raises:
        SklikException: If account data cannot be fetched from the API or
            if the account is not found.
        AttributeError: When accessing a non-existent account property.
    """

    def __init__(self, account_id: int, api: Optional[SklikApi] = None) -> None:
        self.account_id = account_id
        self.api = api or SklikApi.get_default_api()
        self._model = self._build_model()

    def __getattr__(self, item) -> Any:
        if hasattr(self._model, item):
            return getattr(self._model, item)
        else:
            raise AttributeError(
                f"{self.__class__.__name__} nor {self._model.__class__.__name__} object has no attribute '{item}'")

    def _build_model(self) -> AccountModel:
        """
        Fetch and build the account data model.

        Retrieves account data from the API and constructs the corresponding
            model object.

            Returns:
                Validated account model instance.

            Raises:
                SklikException: If account data cannot be retrieved.
        """

        response = self.api.call("client", "get")
        account_data = self._find_account_data(response)
        if not account_data:
            raise SklikException(
                msg="Unable to fetch account data from the API.",
                status_code=404,
                additional_information=None
            )
        return AccountModel.model_validate(account_data)

    def _find_account_data(self, response: dict) -> Optional[Dict]:
        """
        Fetch and build the account data model.

        Retrieves account data from the API and constructs the corresponding
         model object.

        Returns:
            Validated account model instance.

        Raises:
            SklikException: If account data cannot be retrieved.
        """

        if response["user"]["userId"] == self.account_id:
            return response["user"]
        for foreign_account in response["foreignAccounts"]:
            if foreign_account["userId"] == self.account_id:
                return foreign_account
        return None

    def call(self, service: str, method: str, args: list) -> Dict[str, Any]:
        """
        Execute an API call in the context of this account.

        Automatically includes account authentication and context in the request.

        Args:
            service: Name of the Sklik API service to call.
            method: Name of the method to execute.
            args: List of additional arguments for the API call.

        Returns:
            API response data.
        """

        payload = [{"userId": self._model.user_id}] + args
        return self.api.call(service, method, payload)
