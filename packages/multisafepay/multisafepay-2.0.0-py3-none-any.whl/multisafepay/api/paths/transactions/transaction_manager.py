# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.listings.listing_pager import ListingPager
from multisafepay.api.base.listings.pager import Pager
from multisafepay.api.base.response.api_response import ApiResponse
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.transactions.response.transaction import (
    Transaction,
)
from multisafepay.client.client import Client
from multisafepay.util.message import MessageList, gen_could_not_created_msg

ALLOWED_OPTIONS = {
    "site_id": "",
    "financial_status": "",
    "status": "",
    "payment_method": "",
    "type": "",
    "created_until": "",
    "created_from": "",
    "completed_until": "",
    "completed_from": "",
    "debit_credit": "",
    "after": "",
    "before": "",
    "limit": "",
}


class TransactionManager(AbstractManager):
    """
    A class representing the TransactionManager.
    """

    def __init__(self: "TransactionManager", client: Client) -> None:
        """
        Initialize the CaptureManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def get_transactions(
        self: "TransactionManager",
        options: dict = None,
    ) -> CustomApiResponse:
        """
        Retrieve a list of transactions.

        Parameters
        ----------
        options (dict): Additional options for the request. Defaults to None.

        Returns
        -------
        CustomApiResponse: The response containing the list of transactions

        """
        if options is None:
            options = {}
        options = {k: v for k, v in options.items() if k in ALLOWED_OPTIONS}

        response: ApiResponse = self.client.create_get_request(
            "json/transactions",
            options,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }

        try:
            args["data"] = ListingPager(
                data=response.get_body_data().copy(),
                pager=Pager.from_dict(response.get_pager().copy()),
                class_type=Transaction,
            )
        except Exception:
            args["warnings"] = MessageList().add_message(
                gen_could_not_created_msg("Listing Transaction"),
            )

        return CustomApiResponse(**args)
