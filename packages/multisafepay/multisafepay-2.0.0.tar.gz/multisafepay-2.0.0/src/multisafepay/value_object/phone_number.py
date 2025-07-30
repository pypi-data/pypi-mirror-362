# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.model.inmutable_model import InmutableModel


class PhoneNumber(InmutableModel):
    """
    A class to represent a phone number.

    Attributes
    ----------
    phone_number (str): The phone number as a string.

    """

    phone_number: str

    def get(self: "PhoneNumber") -> str:
        """
        Get the phone number.

        Returns
        -------
        str: The phone number.

        """
        return self.phone_number
