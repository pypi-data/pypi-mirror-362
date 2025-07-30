# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.exception.invalid_argument import InvalidArgumentException
from pydantic import BaseModel, validator


class Cvc(BaseModel):
    """
    A class to represent a Credit Card CVC.

    Attributes
    ----------
    cvc (str): The credit card CVC as a string.

    """

    cvc: str

    def get(self: "Cvc") -> str:
        """
        Get the credit card CVC.

        Returns
        -------
        str: The credit card CVC.

        """
        return self.cvc

    @validator("cvc")
    def validate(cls: "Cvc", cvc: str) -> str:
        """
        Validate the credit card CVC.

        Parameters
        ----------
        cvc (str): The credit card CVC to validate.

        Returns
        -------
        bool: True if the CVC is valid, raises InvalidArgumentException otherwise.

        Raises
        ------
        InvalidArgumentException: If the CVC does not have 3 digits or is not numeric.

        """
        cvc = cvc.replace(" ", "")
        if len(cvc) != 3:
            raise InvalidArgumentException("CVC must have 3 digits")

        if not cvc.isnumeric():
            raise InvalidArgumentException("CVC must be a number")

        return cvc
