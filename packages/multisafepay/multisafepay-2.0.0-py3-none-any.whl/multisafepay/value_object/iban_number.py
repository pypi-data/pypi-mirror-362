# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import re

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator


class IbanNumber(InmutableModel):
    """
    A class to represent an IBAN number.

    Attributes
    ----------
    iban_number (str): The IBAN number as a string.

    """

    iban_number: str

    @validator("iban_number")
    def validate(cls: "IbanNumber", value: str) -> str:
        """
        Validate the IBAN number.

        Parameters
        ----------
        value (str): The IBAN number to validate.

        Returns
        -------
        str: The validated IBAN number.

        Raises
        ------
        InvalidArgumentException: If the IBAN number is not valid.

        """
        if not IbanNumber.validate_iban_number(value):
            raise InvalidArgumentException(
                f'Value "{value}" is not a valid IP address',
            )

        return value

    def get(self: "IbanNumber") -> str:
        """
        Get the IBAN number.

        Returns
        -------
        str: The IBAN number.

        """
        return self.iban_number

    @staticmethod
    def validate_iban_number(iban_number: str) -> bool:
        """
        Validate the format of an IBAN number.

        Parameters
        ----------
        iban_number (str): The IBAN number to validate.

        Returns
        -------
        bool: True if the IBAN number is valid, False otherwise.

        Raises
        ------
        InvalidArgumentException: If the IBAN number is not valid.

        """
        message = f'Value "{iban_number}" is not a valid IBAN number'

        if len(iban_number) < 8:
            raise InvalidArgumentException(message)

        if not re.match(r"^([a-z]{2})([0-9]{2})", iban_number.lower()):
            raise InvalidArgumentException(message)

        return True
