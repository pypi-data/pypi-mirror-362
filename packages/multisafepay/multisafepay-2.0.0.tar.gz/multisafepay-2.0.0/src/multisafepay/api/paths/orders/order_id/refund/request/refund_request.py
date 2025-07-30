# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.api.paths.orders.order_id.refund.request.components.checkout_data import (
    CheckoutData,
)
from multisafepay.api.shared.description import Description
from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.currency import Currency


class RefundOrderRequest(RequestModel):
    """
    Represents a request to refund an order.

    Attributes
    ----------
        currency (Optional[str]): The currency of the order.
        amount (Optional[int]): The amount to refund.
        description (Optional[str]): The description of the refund.
        checkout_data (Optional[CheckoutData]): The checkout data of the refund.

    """

    currency: Optional[str]
    amount: Optional[int]
    description: Optional[str]
    checkout_data: Optional[CheckoutData]

    def add_currency(
        self: "RefundOrderRequest",
        currency: Union[Currency, str],
    ) -> "RefundOrderRequest":
        """
        Adds the currency to the refund request.

        Parameters
        ----------
        currency (Currency | str): The currency to add.

        Returns
        -------
        RefundOrderRequest: The updated refund request.

        """
        if isinstance(currency, str):
            currency = Currency(currency=currency)
        self.currency = currency.get()
        return self

    def add_amount(
        self: "RefundOrderRequest",
        amount: Union[Amount, int],
    ) -> "RefundOrderRequest":
        """
        Adds the amount to the refund request.

        Parameters
        ----------
        amount (Amount | int): The amount to add.

        Returns
        -------
        RefundOrderRequest: The updated refund request.

        """
        if isinstance(amount, int):
            amount = Amount(amount=amount)
        self.amount = amount.get()
        return self

    def add_description(
        self: "RefundOrderRequest",
        description: Union[Description, str],
    ) -> "RefundOrderRequest":
        """
        Adds the description to the refund request.

        Parameters
        ----------
        description (Description | str): The description to add.

        Returns
        -------
        RefundOrderRequest: The updated refund request.

        """
        if isinstance(description, str):
            description = Description(description=description)
        self.description = description.get()
        return self

    def add_checkout_data(
        self: "RefundOrderRequest",
        checkout_data: CheckoutData,
    ) -> "RefundOrderRequest":
        """
        Adds the checkout data to the refund request.

        Parameters
        ----------
        checkout_data (CheckoutData): The checkout data to add.

        Returns
        -------
        RefundOrderRequest: The updated refund request.

        """
        self.checkout_data = checkout_data
        return self
