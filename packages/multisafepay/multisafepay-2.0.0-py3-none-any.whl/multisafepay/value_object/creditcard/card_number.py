# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from pydantic import BaseModel


class CardNumber(BaseModel):
    """
    A class to represent a Credit Card Number.

    Attributes
    ----------
    card_number (str): The credit card number as a string.

    """

    card_number: str

    def get_card_number(self: "CardNumber") -> str:
        """
        Get the credit card number.

        Returns
        -------
        str: The credit card number.

        """
        return self.card_number
