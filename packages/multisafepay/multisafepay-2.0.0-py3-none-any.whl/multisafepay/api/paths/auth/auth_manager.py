# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.auth.api_token.response.api_token import ApiToken
from multisafepay.client.client import Client
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg


class AuthManager(AbstractManager):
    """
    A manager class for handling authentication-related operations.
    """

    def __init__(self: "AuthManager", client: Client) -> None:
        """
        Initialize the CaptureManager with a client.

        Parameters
        ----------
            client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def get_api_token(self: "AuthManager") -> CustomApiResponse:
        """
        Retrieve the API token.

        This method sends a GET request to the 'json/auth/api_token' endpoint
        and attempts to create an ApiToken object from the response data.

        Returns
        -------
        CustomApiResponse
            A custom API response containing the ApiToken object or warnings if the token could not be created.

        """
        response: ApiResponse = self.client.create_get_request(
            "json/auth/api_token",
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }

        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = ApiToken(**response.get_body_data().copy())
            except Exception as e:
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("ApiToken"))
                    .get_messages()
                )

        return CustomApiResponse(**args)
