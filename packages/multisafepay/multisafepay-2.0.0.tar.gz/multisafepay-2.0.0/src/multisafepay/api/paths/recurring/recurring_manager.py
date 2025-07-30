# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Any

from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.recurring.customer_reference.token.token import (
    Token,
)
from multisafepay.client.client import Client
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg


class RecurringManager(AbstractManager):
    """
    Manages recurring payment tokens for a customer reference.

    Attributes
    ----------
    CREDIT_CARD_GATEWAY_CODE (str): The code for the credit card gateway.
    CREDIT_CARD_GATEWAYS (list): List of supported credit card gateways.
    tokens (dict): Dictionary to store tokens.

    """

    CREDIT_CARD_GATEWAY_CODE = "CREDITCARD"
    CREDIT_CARD_GATEWAYS = ["VISA", "MASTERCARD", "AMEX", "MAESTRO"]

    def __init__(self: "RecurringManager", client: Client) -> None:
        """
        Initializes the RecurringManager with a client.

        Parameters
        ----------
        client: The client to use for API requests.

        """
        super().__init__(client)
        self.tokens: Any = {}

    def get_list(
        self: "RecurringManager",
        reference: str,
    ) -> CustomApiResponse:
        """
        Retrieves a list of recurring tokens for a given customer reference.

        Parameters
        ----------
        reference (str): The customer reference.
        force_api_call (bool): Whether to force an API call.

        Returns
        -------
        CustomApiResponse: The response containing the list of tokens.

        """
        encoded_reference = self.encode_path_segment(reference)
        response: ApiResponse = self.client.create_get_request(
            f"json/recurring/{encoded_reference}",
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }

        body_data = response.get_body_data()

        if not dict_empty(response.get_body_data()):
            tokens = body_data.copy()
            try:

                args["data"] = [
                    Token.from_dict(token)
                    for token in tokens["tokens"]
                    if tokens["tokens"]
                ]

            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Listing Tokens"),
                )

        return CustomApiResponse(**args)

    def get(
        self: "RecurringManager",
        token: str,
        reference: str,
    ) -> CustomApiResponse:
        """
        Retrieves a specific recurring token for a given customer reference.

        Parameters
        ----------
        token (str): The token to retrieve.
        reference (str): The customer reference.

        Returns
        -------
        CustomApiResponse: The response containing the token data.

        """
        encoded_reference = self.encode_path_segment(reference)
        encoded_token = self.encode_path_segment(token)
        response = self.client.create_get_request(
            f"json/recurring/{encoded_reference}/token/{encoded_token}",
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = Token(**response.get_body_data().copy())
            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Listing Tokens"),
                )

        return CustomApiResponse(**args)

    def delete(
        self: "RecurringManager",
        reference: str,
        token: str,
    ) -> CustomApiResponse:
        """
        Deletes a specific recurring token for a given customer reference.

        Parameters
        ----------
        reference (str): The customer reference.
        token (str): The token to delete.

        Returns
        -------
        CustomApiResponse: The response after deleting the token.

        """
        encoded_reference = self.encode_path_segment(reference)
        encoded_token = self.encode_path_segment(token)
        response = self.client.create_delete_request(
            f"json/recurring/{encoded_reference}/remove/{encoded_token}",
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        return CustomApiResponse(**args)
