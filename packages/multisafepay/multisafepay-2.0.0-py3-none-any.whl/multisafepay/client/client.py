# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Any, Dict, Optional

from multisafepay.api.base.response.api_response import ApiResponse
from requests import Request, Session
from requests.exceptions import RequestException

from ..exception.api import ApiException
from .api_key import ApiKey


class Client:
    """
    Client for interacting with the MultiSafepay API.

    Attributes
    ----------
    LIVE_URL (str): The live API URL.
    TEST_URL (str): The test API URL.
    METHOD_POST (str): HTTP POST method.
    METHOD_GET (str): HTTP GET method.
    METHOD_PATCH (str): HTTP PATCH method.
    METHOD_DELETE (str): HTTP DELETE method.

    """

    LIVE_URL = "https://api.multisafepay.com/v1/"
    TEST_URL = "https://testapi.multisafepay.com/v1/"

    METHOD_POST = "POST"
    METHOD_GET = "GET"
    METHOD_PATCH = "PATCH"
    METHOD_DELETE = "DELETE"

    def __init__(
        self: "Client",
        api_key: str,
        is_production: bool,
        http_client: Optional[Session] = None,
        locale: str = "en_US",
    ) -> None:
        """
        Initialize the Client.

        Parameters
        ----------
        api_key (str): The API key for authentication.
        is_production (bool): Flag indicating if the client is in production mode.
        http_client (Optional[Session], optional): Custom HTTP client session. Defaults to None.
        request_factory (Optional[Any], optional): Factory for creating requests. Defaults to None.
        stream_factory (Optional[Any], optional): Factory for creating streams. Defaults to None.
        locale (str, optional): Locale for the requests. Defaults to "en_US".
        strict_mode (bool, optional): Flag indicating if strict mode is enabled. Defaults to False.

        """
        self.api_key = ApiKey(api_key=api_key)
        self.url = self.LIVE_URL if is_production else self.TEST_URL
        self.http_client = http_client or Session()
        self.locale = locale

    def create_get_request(
        self: "Client",
        endpoint: str,
        params: Dict[str, Any] = None,
        context: Dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a GET request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(
            self.METHOD_GET,
            url,
            params=params,
            context=context,
        )

    def create_post_request(
        self: "Client",
        endpoint: str,
        params: Dict[str, Any] = None,
        request_body: str = None,
        context: Dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a POST request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        request_body (str, optional): The request body. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(
            self.METHOD_POST,
            url,
            request_body=request_body,
            context=context,
        )

    def create_patch_request(
        self: "Client",
        endpoint: str,
        params: Dict[str, Any] = None,
        request_body: str = None,
        context: Dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a PATCH request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        request_body (Optional[RequestBodyInterface], optional): The request body. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(
            self.METHOD_PATCH,
            url,
            request_body=request_body,
            context=context,
        )

    def create_delete_request(
        self: "Client",
        endpoint: str,
        params: Dict[str, Any] = None,
        context: Dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create a DELETE request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Dict[str, Any], optional): Query parameters. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        url = self._build_url(endpoint, params)
        return self._create_request(self.METHOD_DELETE, url, context=context)

    def _build_url(
        self: "Client",
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Build the full URL for the request.

        Parameters
        ----------
        endpoint (str): The API endpoint.
        params (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.

        Returns
        -------
        str: The full URL.

        """
        if params is None:
            params = {}
        if "locale" not in params:
            params["locale"] = self.locale
        query_string = "&".join(
            f"{key}={value}" for key, value in params.items()
        )
        return f"{self.url}{endpoint}?{query_string}"

    def _create_request(
        self: "Client",
        method: str,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        request_body: Optional[Dict[str, Any]] = None,
        context: Dict[str, Any] = None,
    ) -> ApiResponse:
        """
        Create and send an HTTP request.

        Parameters
        ----------
        method (str): The HTTP method.
        url (str): The full URL.
        params (Optional[Dict[str, Any]], optional): Query parameters. Defaults to None.
        request_body (Optional[Dict[str, Any]], optional): The request body. Defaults to None.
        context (Dict[str, Any], optional): Additional context for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response.

        """
        headers = {
            "Authorization": "Bearer " + self.api_key.get(),
            "accept-encoding": "application/json",
            "Content-Type": "application/json",
        }
        request = Request(
            method,
            url,
            params=params,
            data=request_body,
            headers=headers,
        )
        prepared_request = self.http_client.prepare_request(request)

        try:
            response = self.http_client.send(prepared_request)
            response.raise_for_status()
        except RequestException as e:
            if 500 <= response.status_code < 600:
                raise ApiException(f"Request failed: {e}") from e

        context = context or {}
        context.update(
            {
                "headers": request.headers,
                "request_body": request_body,
            },
        )
        return ApiResponse.with_json(
            status_code=response.status_code,
            json_data=response.json(),
            headers=response.headers,
            context=context,
        )
