# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.me.response.me import Me
from multisafepay.client.client import Client
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg


class MeManager(AbstractManager):
    """
    A manager class for handling 'me' related API requests.
    """

    def __init__(self: "MeManager", client: Client) -> None:
        """
        Initialize the MeManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def get(self: "MeManager") -> CustomApiResponse:
        """
        Retrieve the 'me' data.

        This method makes an API request to retrieve the 'me' data and
        returns a CustomApiResponse object containing the response data.

        Returns
        -------
        CustomApiResponse: The response object containing the 'me' data and any warnings.

        """
        response = self.client.create_get_request("json/me")
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = Me(**response.get_body_data().copy())
            except Exception as e:
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("Me"))
                    .get_messages()
                )

        return CustomApiResponse(**args)
