# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.amount import Amount


class CaptureOrderRequest(RequestModel):
    """
    Represents a request to capture an order.

    Attributes
    ----------
    amount (Optional[int]): The amount to capture.
    new_order_id (Optional[str]): The new order ID.
    new_order_status (Optional[str]): The new status of the order.
    invoice_id (Optional[str]): The invoice ID.
    carrier (Optional[str]): The carrier information.
    reason (Optional[str]): The reason for the capture.
    tracktrace_code (Optional[str]): The tracking code.
    description (Optional[str]): The description of the capture request.

    """

    amount: Optional[int]
    new_order_id: Optional[str]
    new_order_status: Optional[str]
    invoice_id: Optional[str]
    carrier: Optional[str]
    reason: Optional[str]
    tracktrace_code: Optional[str]
    description: Optional[str]

    def add_amount(
        self: "CaptureOrderRequest",
        amount: Union[Amount, int],
    ) -> "CaptureOrderRequest":
        """
        Adds the amount to the capture request.

        Parameters
        ----------
        amount (Amount | int): The amount to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        if isinstance(amount, int):
            amount = Amount(amount=amount)
        self.amount = amount.get()
        return self

    def add_new_order_id(
        self: "CaptureOrderRequest",
        new_order_id: str,
    ) -> "CaptureOrderRequest":
        """
        Adds the new order ID to the capture request.

        Parameters
        ----------
        new_order_id (str): The new order ID to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.new_order_id = new_order_id
        return self

    def add_new_order_status(
        self: "CaptureOrderRequest",
        new_order_status: str,
    ) -> "CaptureOrderRequest":
        """
        Adds the new order status to the capture request.

        Parameters
        ----------
        new_order_status (str): The new order status to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.new_order_status = new_order_status
        return self

    def add_invoice_id(
        self: "CaptureOrderRequest",
        invoice_id: str,
    ) -> "CaptureOrderRequest":
        """
        Adds the invoice ID to the capture request.

        Parameters
        ----------
            invoice_id (str): The invoice ID to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.invoice_id = invoice_id
        return self

    def add_carrier(
        self: "CaptureOrderRequest",
        carrier: str,
    ) -> "CaptureOrderRequest":
        """
        Adds the carrier information to the capture request.

        Parameters
        ----------
        carrier (str): The carrier information to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.carrier = carrier
        return self

    def add_reason(
        self: "CaptureOrderRequest",
        reason: str,
    ) -> "CaptureOrderRequest":
        """
        Adds the reason for the capture to the capture request.

        Parameters
        ----------
        reason (str): The reason to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.reason = reason
        return self

    def add_tracktrace_code(
        self: "CaptureOrderRequest",
        tracktrace_code: str,
    ) -> "CaptureOrderRequest":
        """
        Adds the tracktrace code to the capture request.

        Parameters
        ----------
        tracktrace_code (str): The tracktrace code to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.tracktrace_code = tracktrace_code
        return self

    def add_description(
        self: "CaptureOrderRequest",
        description: str,
    ) -> "CaptureOrderRequest":
        """
        Adds a description to the capture request.

        Parameters
        ----------
        description (str): The description to add.

        Returns
        -------
        CaptureOrderRequest: The updated capture request.

        """
        self.description = description
        return self
