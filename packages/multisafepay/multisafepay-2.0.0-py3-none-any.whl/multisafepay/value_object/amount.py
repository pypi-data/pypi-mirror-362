# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.model.inmutable_model import InmutableModel


class Amount(InmutableModel):
    """
    A class to represent an Amount.

    Attributes
    ----------
    amount (int): The amount value as an integer.

    """

    amount: int

    def get(self: "Amount") -> int:
        """
        Get the amount value.

        Returns
        -------
        int: The amount value.

        """
        return self.amount
