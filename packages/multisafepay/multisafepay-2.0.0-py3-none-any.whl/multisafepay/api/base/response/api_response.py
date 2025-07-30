# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.api.base.listings.pager import Pager
from multisafepay.model.extra_model import ExtraModel


class ApiResponse(ExtraModel):
    """
    A class to represent an API response.

    Attributes
    ----------
    headers (dict): The headers of the response.
    status_code (int): The status code of the response.
    body (dict): The body of the response.
    context (Optional[dict]): The context of the response.
    raw (Optional[str]): The raw response data as a string.

    """

    headers: dict
    status_code: int
    body: dict
    context: Optional[dict]
    raw: Optional[str]

    @staticmethod
    def with_json(
        status_code: int,
        json_data: dict,
        headers: dict,
        context: dict = None,
    ) -> "ApiResponse":
        """
        Create an ApiResponse object with JSON data.

        Parameters
        ----------
        status_code (int): The status code of the response.
        json_data (dict): The JSON data of the response.
        headers (dict): The headers of the response.
        context (dict, optional): The context of the response. Defaults to None.

        Returns
        -------
        ApiResponse: An instance of ApiResponse.

        """
        if context is None:
            context = {}
        data = json_data if json_data else {}
        return ApiResponse(
            status_code=status_code,
            body=data,
            context=context,
            headers=headers,
            raw=json_data.__str__(),
        )

    def get_body_data(self: "ApiResponse") -> Optional[Union[dict, list]]:
        """
        Get the data from the body of the response.

        Returns
        -------
        dict | list: The data from the body of the response.

        """
        return self.body.get("data", None)

    def get_body_success(self: "ApiResponse") -> Optional[bool]:
        """
        Get the success status from the body of the response.

        Returns
        -------
        bool | None: The success status from the body of the response.

        """
        return self.body.get("success", None)

    def get_body_error_code(self: "ApiResponse") -> Optional[int]:
        """
        Get the error code from the body of the response.

        Returns
        -------
        int | None: The error code from the body of the response.

        """
        return self.body.get("error_code", None)

    def get_body_error_info(self: "ApiResponse") -> Optional[str]:
        """
        Get the error information from the body of the response.

        Returns
        -------
        str | None: The error information from the body of the response.

        """
        return self.body.get("error_info", None)

    def get_context(self: "ApiResponse") -> dict:
        """
        Get the context of the response.

        Returns
        -------
        dict: The context of the response.

        """
        return self.context

    def get_headers(self: "ApiResponse") -> dict:
        """
        Get the headers of the response.

        Returns
        -------
        dict: The headers of the response.

        """
        return self.headers

    def get_status_code(self: "ApiResponse") -> int:
        """
        Get the status code of the response.

        Returns
        -------
        int: The status code of the response.

        """
        return self.status_code

    def get_raw(self: "ApiResponse") -> str:
        """
        Get the raw response data as a string.

        Returns
        -------
        str: The raw response data as a string.

        """
        return self.raw

    def get_pager(self: "ApiResponse") -> Optional[Pager]:
        """
        Get the pager object from the body of the response.

        Returns
        -------
        Optional[Pager]: The pager object from the body of the response.

        """
        return self.body.get("pager", None)
