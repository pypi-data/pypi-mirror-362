# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class OrderAdjustment(ResponseModel):
    """
    Represents an adjustment to an order, including total adjustment and total tax.

    Attributes
    ----------
    total_adjustment (Optional[float]): The total adjustment to the order.
    total_tax (Optional[float]): The total tax for the order.

    """

    total_adjustment: Optional[float]
    total_tax: Optional[float]

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["OrderAdjustment"]:
        """
        Creates an OrderAdjustment instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the order adjustment data.

        Returns
        -------
        OrderAdjustment: An instance of OrderAdjustment with the data from the dictionary.

        """
        if d is None:
            return None
        return OrderAdjustment(**d)
