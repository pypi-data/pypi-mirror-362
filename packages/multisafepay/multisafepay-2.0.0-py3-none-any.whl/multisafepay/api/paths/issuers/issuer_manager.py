# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.issuers.response.issuer import (
    ALLOWED_GATEWAY_CODES,
    Issuer,
)
from multisafepay.client.client import Client
from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.util.message import MessageList, gen_could_not_created_msg


class IssuerManager(AbstractManager):
    """
    Manager class for handling issuer-related operations.
    """

    def __init__(self: "IssuerManager", client: Client) -> None:
        """
        Initialize the IssuerManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def get_issuers_by_gateway_code(
        self: "IssuerManager",
        gateway_code: str,
    ) -> CustomApiResponse:
        """
        Retrieve issuers by gateway code.

        Parameters
        ----------
        gateway_code (str): The code of the gateway to retrieve issuers for.

        Returns
        -------
        CustomApiResponse: The response containing the list of issuers.

        Raises
        ------
        InvalidArgumentException: If the provided gateway code is not allowed.

        """
        gateway_code = gateway_code.lower()
        if gateway_code not in ALLOWED_GATEWAY_CODES:
            raise InvalidArgumentException("Gateway code is not allowed")

        encoded_gateway_code = self.encode_path_segment(gateway_code)
        response = self.client.create_get_request(
            f"json/issuers/{encoded_gateway_code}",
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if isinstance(response.get_body_data(), list):
            try:
                args["data"] = [
                    Issuer.from_dict(issuer)
                    for issuer in response.get_body_data().copy()
                ]
            except Exception as e:
                print(e)
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("Issuer list"))
                    .get_messages()
                )

        return CustomApiResponse(**args)
