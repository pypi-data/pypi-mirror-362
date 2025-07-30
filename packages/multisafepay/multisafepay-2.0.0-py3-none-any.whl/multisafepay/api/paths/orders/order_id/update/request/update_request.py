# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class UpdateOrderRequest(RequestModel):
    """
    Represents an update order request.

    Attributes
    ----------
    tracktrace_code (Optional[str]): The tracking code.
    tracktrace_url (Optional[str]): The tracking URL.
    carrier (Optional[str]): The carrier.
    ship_date (Optional[str]): The shipping date.
    reason (Optional[str]): The reason for the update.
    invoice_id (Optional[str]): The invoice ID.
    invoice_url (Optional[str]): The invoice URL.
    po_number (Optional[str]): The purchase order number.
    status (Optional[str]): The status of the order.
    exclude_order (Optional[bool]): Exclude the order from the update.
    extend_expiration (Optional[bool]): Extend the expiration date of the order.

    """

    tracktrace_code: Optional[str]
    tracktrace_url: Optional[str]
    carrier: Optional[str]
    ship_date: Optional[str]
    reason: Optional[str]
    invoice_id: Optional[str]
    invoice_url: Optional[str]
    po_number: Optional[str]
    status: Optional[str]
    exclude_order: Optional[bool]
    extend_expiration: Optional[bool]

    def add_tracktrace_code(
        self: "UpdateOrderRequest",
        tracktrace_code: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a tracking code to the order request.

        Parameters
        ----------
        tracktrace_code (str): The tracking code to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.tracktrace_code = tracktrace_code
        return self

    def add_tracktrace_url(
        self: "UpdateOrderRequest",
        tracktrace_url: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a tracking URL to the order request.

        Parameters
        ----------
        tracktrace_url (str): The tracking URL to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.tracktrace_url = tracktrace_url
        return self

    def add_carrier(
        self: "UpdateOrderRequest",
        carrier: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a carrier to the order request.

        Parameters
        ----------
        carrier (str): The carrier to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.carrier = carrier
        return self

    def add_ship_date(
        self: "UpdateOrderRequest",
        ship_date: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a shipping date to the order request.

        Parameters
        ----------
        ship_date (str): The shipping date to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.ship_date = ship_date
        return self

    def add_reason(
        self: "UpdateOrderRequest",
        reason: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a reason for updating the order request.

        Parameters
        ----------
        reason (str): The reason to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.reason = reason
        return self

    def add_invoice_id(
        self: "UpdateOrderRequest",
        invoice_id: str,
    ) -> "UpdateOrderRequest":
        """
        Adds an invoice ID to the order request.

        Parameters
        ----------
        invoice_id (str): The invoice ID to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.invoice_id = invoice_id
        return self

    def add_invoice_url(
        self: "UpdateOrderRequest",
        invoice_url: str,
    ) -> "UpdateOrderRequest":
        """
        Adds an invoice URL to the order request.

        Parameters
        ----------
        invoice_url (str): The invoice URL to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.invoice_url = invoice_url
        return self

    def add_po_number(
        self: "UpdateOrderRequest",
        po_number: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a purchase order number to the order request.

        Parameters
        ----------
        po_number (str): The purchase order number to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.po_number = po_number
        return self

    def add_status(
        self: "UpdateOrderRequest",
        status: str,
    ) -> "UpdateOrderRequest":
        """
        Adds a status to the order request.

        Parameters
        ----------
        status (str): The status to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.status = status
        return self

    def add_exclude_order(
        self: "UpdateOrderRequest",
        exclude_order: bool,
    ) -> "UpdateOrderRequest":
        """
        Adds an exclusion for the order request.

        Parameters
        ----------
        exclude_order (bool): The exclusion to add.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.exclude_order = exclude_order
        return self

    def add_extend_expiration(
        self: "UpdateOrderRequest",
        extend_expiration: bool,
    ) -> "UpdateOrderRequest":
        """
        Adds an expiration extension to the order request.

        Parameters
        ----------
        extend_expiration (bool): Indicates whether to extend the expiration.

        Returns
        -------
        UpdateOrderRequest: The updated order request.

        """
        self.extend_expiration = extend_expiration
        return self
