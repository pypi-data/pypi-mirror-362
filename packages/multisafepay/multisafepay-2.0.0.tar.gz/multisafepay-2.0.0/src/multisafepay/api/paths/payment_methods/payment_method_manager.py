# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.payment_methods.response.payment_method import (
    PaymentMethod,
)
from multisafepay.client.client import ApiResponse, Client
from multisafepay.util.dict_utils import dict_empty
from multisafepay.util.message import MessageList, gen_could_not_created_msg

ALLOWED_OPTIONS = {
    "country": "",
    "currency": "",
    "amount": "",
    "include": "",
}


class PaymentMethodManager(AbstractManager):
    """
    A class representing the PaymentMethodManager.
    """

    def __init__(self: "PaymentMethodManager", client: Client) -> None:
        """
        Initialize the CaptureManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def get_payment_methods_request(
        self: "PaymentMethodManager",
        include_coupons: bool = True,
        options: dict = None,
    ) -> ApiResponse:
        """
        Create a request to retrieve payment methods.

        Parameters
        ----------
        include_coupons (bool): Whether to include coupons in the request. Defaults to True.
        options (dict): Additional options for the request. Defaults to None.

        Returns
        -------
        ApiResponse: The API response containing the payment methods data.

        """
        if options is None:
            options = {}
        options = {k: v for k, v in options.items() if k in ALLOWED_OPTIONS}
        if include_coupons:
            options["include_coupons"] = "1"

        return self.client.create_get_request("json/payment-methods", options)

    def get_payment_methods(
        self: "PaymentMethodManager",
        include_coupons: bool = True,
        options: dict = None,
    ) -> CustomApiResponse:
        """
        Retrieve payment methods.

        Parameters
        ----------
        include_coupons (bool): Whether to include coupons in the request. Defaults to True.
        options (dict): Additional options for the request. Defaults to None.

        Returns
        -------
        CustomApiResponse: The custom API response containing the payment methods data.

        """
        response = self.get_payment_methods_request(include_coupons, options)

        args: dict = {
            **response.dict(),
            "data": None,
        }

        if isinstance(response.get_body_data(), list):
            try:
                args["data"] = [
                    PaymentMethod.from_dict(payment_method)
                    for payment_method in response.get_body_data().copy()
                ]
            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Listing Payment Method"),
                )

        return CustomApiResponse(**args)

    def get_by_gateway_code(
        self: "PaymentMethodManager",
        gateway_code: str,
        options: dict = None,
    ) -> CustomApiResponse:
        """
        Retrieve a payment method by its gateway code.

        Parameters
        ----------
        gateway_code (str): The gateway code of the payment method.
        options (dict): Additional options for the request. Defaults to None.

        Returns
        -------
        CustomApiResponse: The custom API response containing the payment method data.

        """
        if options is None:
            options = {}
        options = {k: v for k, v in options.items() if k in ALLOWED_OPTIONS}
        encoded_gateway_code = self.encode_path_segment(gateway_code)
        response = self.client.create_get_request(
            f"json/payment-methods/{encoded_gateway_code}",
            options,
        )
        args: dict = {
            **response.dict(),
            "data": None,
        }
        if not dict_empty(response.get_body_data()):
            try:
                args["data"] = PaymentMethod.from_dict(
                    d=response.get_body_data().copy(),
                )
            except Exception:
                args["warnings"] = MessageList().add_message(
                    gen_could_not_created_msg("Payment Method"),
                )

        return CustomApiResponse(**args)
