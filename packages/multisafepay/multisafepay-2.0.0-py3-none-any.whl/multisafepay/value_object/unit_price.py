# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.model.inmutable_model import InmutableModel


class UnitPrice(InmutableModel):
    """
    A class to represent the unit price of an item.

    Attributes
    ----------
    unit_price (float): The unit price of the item.

    """

    unit_price: float

    def get(self: "UnitPrice") -> float:
        """
        Get the unit price of the item.

        Returns
        -------
        float: The unit price of the item.

        """
        return self.unit_price
