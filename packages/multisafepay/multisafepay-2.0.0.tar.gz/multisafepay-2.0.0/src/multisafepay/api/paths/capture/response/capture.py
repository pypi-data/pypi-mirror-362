# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class CancelReservation(ResponseModel):
    """
    A class to represent a cancel reservation response.

    Attributes
    ----------
    order_id (Optional[str]): The order ID.
    success (Optional[bool]): A boolean indicating whether the reservation was successfully canceled.
    transaction_id (Optional[str]): The transaction ID.

    """

    order_id: Optional[str]
    success: Optional[bool]
    transaction_id: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["CancelReservation"]:
        """
        Create a CancelReservation object from a dictionary.

        Parameters
        ----------
        d (dict): A dictionary containing the data to initialize the CancelReservation object.

        Returns
        -------
        Optional[CancelReservation]: An instance of CancelReservation if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return CancelReservation(**d)
