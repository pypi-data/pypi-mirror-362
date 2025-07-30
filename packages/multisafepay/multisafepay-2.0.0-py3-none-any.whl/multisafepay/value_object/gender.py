# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator

ALLOWED_VALUES = ["male", "female", "mr", "mrs", "miss"]


class Gender(InmutableModel):
    """
    A class to represent a Gender.

    Attributes
    ----------
    gender (str): The gender value as a string.

    """

    gender: str

    @validator("gender")
    def validate_ip_address(cls: "Gender", value: str) -> str:
        """
        Validate the gender value.

        Parameters
        ----------
        value (str): The gender value to validate.

        Returns
        -------
        str: The validated gender value.

        Raises
        ------
        InvalidArgumentException: If the gender value is not allowed.

        """
        if value not in ALLOWED_VALUES:
            raise InvalidArgumentException(
                f"Gender is not allowed. Allowed values are: {ALLOWED_VALUES}",
            )

        return value

    def get(self: "Gender") -> str:
        """
        Get the gender value.

        Returns
        -------
        str: The gender value.

        """
        return self.gender
