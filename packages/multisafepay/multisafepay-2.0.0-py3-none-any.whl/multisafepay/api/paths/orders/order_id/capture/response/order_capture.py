# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.api.paths.orders.response.components.payment_details import (
    PaymentDetails,
)
from multisafepay.model.response_model import ResponseModel


class OrderCapture(ResponseModel):
    """
    Represents the capture of an order.

    Attributes
    ----------
    transaction_id (Optional[str]): The ID of the transaction.
    order_id (Optional[str]): The ID of the order.
    payment_details (Optional[PaymentDetails]): The payment details of the order.

    """

    transaction_id: Optional[str]
    order_id: Optional[str]
    payment_details: Optional[PaymentDetails]

    @staticmethod
    def from_dict(d: dict) -> Optional["OrderCapture"]:
        """
        Creates an OrderCapture object from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing order capture data.

        Returns
        -------
        Optional[OrderCapture]: The OrderCapture object or None if the input dictionary is None.

        """
        if d is None:
            return None
        return OrderCapture(**d)
