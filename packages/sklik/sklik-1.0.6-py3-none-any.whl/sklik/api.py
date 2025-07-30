from typing import Any, Dict, List, Optional, Union

import requests

from sklik.exception import SklikException
from sklik.util import SKLIK_API_URL


def _handle_response(response: requests.Response) -> Dict[str, Any]:
    """
    Process and validate the Sklik API response.

    Checks the HTTP status and the Sklik-specific status code in the response.
    If either indicates an error, appropriate exceptions are raised.

    Args:
        response: Response object from the requests library containing
            the API response data.

    Returns:
        Dict containing the parsed JSON response from the API.

    Raises:
        requests.exceptions.HTTPError: If the HTTP request was unsuccessful.
        SklikException: If the API response indicates an error (status != 200).
    """

    response.raise_for_status()

    response_content = response.json()
    response_status = response_content.get("status")
    if response_status != 200:
        raise SklikException(
            msg=f"Could not request {response.url}: status code {response_status}",
            status_code=response_status,
            additional_information=response_content.get("statusMessage")
        )
    return response_content


def sklik_request(api_url: str, service: str, method: str, args: Union[str, List]) -> Dict[str, Any]:
    """
    Makes a POST request to the Sklik API and handles the response.

    This function constructs the API endpoint URL from the given parameters, sends a POST
    request with the provided arguments, and processes the response through _handle_response.

    Args:
        api_url: Base URL of the Sklik API (e.g., 'https://api.sklik.cz/drak/json')
        service: Name of the Sklik service to call (e.g., 'campaigns', 'ads')
        method: Specific API method to invoke on the service (e.g., 'list', 'create')
        args: Request payload that will be serialized to JSON. Can be either a string
            or a list containing the API method arguments.

    Returns:
        Dict containing the processed API response.

    Raises:
        Exceptions from _handle_response may be raised based on API response.
    """

    request_url = f"{api_url}/{service}.{method}"
    response = requests.post(url=request_url, json=args)
    return _handle_response(response)


class SklikApi:
    """
    Client for interacting with the Sklik advertising platform API.

    This class manages authentication and provides methods for making API calls
    to the Sklik platform. It handles session management and token-based authentication.

    Attributes:
        session (str): Current session token used for API authentication.
        _default_api (SklikApi | None): Class-level reference to the default API instance.

    Example:
        >>> api = SklikApi.init("your_api_token")
        >>> response = api.call("campaigns", "list", [{"userId": 123}])
    """

    _default_api = None

    def __init__(self, session: str) -> None:
        """
        Initialize a new SklikApi instance. Do not use this constructor directly.

        Args:
            session: Authentication session token for API access.
        """

        self.session = session

    @classmethod
    def init(cls, token: str) -> "SklikApi":
        """
        Create and initialize a new SklikApi instance using an API token.

        Creates a new API instance by authenticating with the provided token,
        sets it as the default instance, and returns it.

        Args:
            token: API token for authentication.

        Returns:
            New authenticated SklikApi instance.
        """

        response = sklik_request(SKLIK_API_URL, service="client", method="loginByToken", args=token)
        api = cls(response["session"])
        cls.set_default_api(api)
        return api

    @classmethod
    def set_default_api(cls, api: "SklikApi") -> None:
        """
        Set the default API instance.

        Args:
            api: SklikApi instance to set as default.
        """

        cls._default_api = api

    @classmethod
    def get_default_api(cls) -> "SklikApi":
        """
        Retrieve the default API instance.

        Returns:
            The default SklikApi instance.
        """

        return cls._default_api

    def _update_session(self, response: Dict) -> None:
        """
        Update the current session token from an API response.

        Args:
            response: API response dictionary containing a new session token.
        """

        self.session = response.get("session", self.session)

    def _preprocess_call(self, args: Optional[List]) -> List[Dict[str, Any]]:
        """
        Prepare arguments for an API call by injecting session information.

        Ensures the session token is properly included in the API call arguments.
        If args contains a userId, the session is added to that dictionary,
        otherwise, it's prepended to the arguments list.

        Args:
            args: List of arguments for the API call. Maybe None.

        Returns:
            List of processed arguments with session information included.
        """

        session_args = [{"session": self.session}]
        if not args:
            return session_args

        if isinstance(args[0], dict) and args[0].get("userId"):
            args[0]["session"] = self.session
        else:
            args = session_args + args
        return args

    def call(self, service: str, method: str, args: Optional[List] = None) -> Dict[str, Any]:
        """
        Make a request to the Sklik API with automatic session management.

        This method handles the complete API call workflow including:
        - Preprocessing the arguments to include session information
        - Making the actual API request
        - Updating the session token from the response
        - Returning the processed response

        Args:
            service: Name of the Sklik API service (e.g., 'campaigns', 'ads', 'client')
            method: Name of the API method to call (e.g., 'list', 'create', 'update')
            args: Optional list of arguments for the API call. If provided, session
                information will be automatically included according to the API requirements.

        Returns:
            Dictionary containing the API response data.

        Example:
            >>> api.call('campaigns', 'list', [{'userId': 123}])
            {'status': 200, 'session': 'new_session_token', '...': ...}
        """

        payload = self._preprocess_call(args)
        response = sklik_request(SKLIK_API_URL, service, method, payload)
        self._update_session(response)
        return response
