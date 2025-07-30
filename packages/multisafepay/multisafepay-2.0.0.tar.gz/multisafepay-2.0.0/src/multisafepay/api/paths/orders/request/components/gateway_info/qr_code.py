# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class QrCode(RequestModel):
    """
    Represents a QR Code in the MultiSafepay API.

    Attributes
    ----------
    qr_size (Optional[int]): The size of the QR code.
    allow_multiple (Optional[bool]): Whether multiple QR codes are allowed.
    allow_change_amount (Optional[bool]): Whether changing the amount is allowed.
    min_amount (Optional[int]): The minimum amount.
    max_amount (Optional[int]): The maximum amount

    """

    qr_size: Optional[int]
    allow_multiple: Optional[bool]
    allow_change_amount: Optional[bool]
    min_amount: Optional[int]
    max_amount: Optional[int]

    def add_qr_size(self: "QrCode", qr_size: int) -> "QrCode":
        """
        Adds a size to the QR code.

        Parameters
        ----------
        qr_size (int): The size of the QR code to be added.

        Returns
        -------
        QrCode: The updated QrCode object.

        """
        self.qr_size = qr_size
        return self

    def add_allow_multiple(self: "QrCode", allow_multiple: bool) -> "QrCode":
        """
        Sets whether multiple QR codes are allowed.

        Parameters
        ----------
        allow_multiple (bool): Whether multiple QR codes are allowed.

        Returns
        -------
        QrCode: The updated QrCode object.

        """
        self.allow_multiple = allow_multiple
        return self

    def add_allow_change_amount(
        self: "QrCode",
        allow_change_amount: bool,
    ) -> "QrCode":
        """
        Sets whether changing the amount is allowed.

        Parameters
        ----------
        allow_change_amount (bool): Whether changing the amount is allowed.

        Returns
        -------
        QrCode: The updated QrCode object.

        """
        self.allow_change_amount = allow_change_amount
        return self

    def add_min_amount(self: "QrCode", min_amount: int) -> "QrCode":
        """
        Adds a minimum amount to the QR code.

        Parameters
        ----------
        min_amount (int): The minimum amount to be added.

        Returns
        -------
        QrCode: The updated QrCode object.

        """
        self.min_amount = min_amount
        return self

    def add_max_amount(self: "QrCode", max_amount: int) -> "QrCode":
        """
        Adds a maximum amount to the QR code.

        Parameters
        ----------
        max_amount (int): The maximum amount to be added.

        Returns
        -------
        QrCode: The updated QrCode object.

        """
        self.max_amount = max_amount
        return self
