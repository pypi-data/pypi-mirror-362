# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import re

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator


class EmailAddress(InmutableModel):
    """
    A class to represent an Email Address.

    Attributes
    ----------
    email_address (str): The email address value as a string.

    """

    email_address: str

    @validator("email_address")
    def validate_email_address(cls: "EmailAddress", value: str) -> str:
        """
        Validate the email address value.

        Parameters
        ----------
        value (str): The email address value to validate.

        Returns
        -------
        str: The validated email address value.

        Raises
        ------
        InvalidArgumentException: If the email address value is not valid.

        """
        if EmailAddress.is_valid_email(value) is False:
            raise InvalidArgumentException(
                f'Value "{value}" is not a valid email address',
            )
        return value

    def get(self: "EmailAddress") -> str:
        """
        Get the email address value.

        Returns
        -------
        str: The email address value.

        """
        return self.email_address

    @staticmethod
    def is_valid_email(email: str) -> bool:
        """
        Check if the provided email address is valid.

        Parameters
        ----------
        email (str): The email address to validate.

        Returns
        -------
        bool: True if the email address is valid, False otherwise.

        """
        pattern = re.compile(
            r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        )
        return bool(pattern.match(email))
