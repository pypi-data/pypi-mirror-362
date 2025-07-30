# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator


class Currency(InmutableModel):
    """
    A class to represent a Currency.

    Attributes
    ----------
    currency (str):The currency code as a string.

    """

    currency: str

    @validator("currency")
    def validate_currency(cls: "Currency", value: str) -> str:
        """
        Validate the currency code.

        Parameters
        ----------
        value (str):The currency code to validate.

        Returns
        -------
        str: The validated currency code.

        Raises
        ------
        InvalidArgumentException: If the currency code is not valid.

        """
        if len(value) != 3 or not value.isalpha():
            raise InvalidArgumentException(
                f'Value "{value}" is not a valid currency code',
            )

        return value

    def get(self: "Currency") -> str:
        """
        Get the currency code.

        Returns
        -------
        str: The currency code.

        """
        return self.currency
