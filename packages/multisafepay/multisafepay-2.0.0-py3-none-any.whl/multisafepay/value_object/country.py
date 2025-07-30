# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from multisafepay.exception.invalid_argument import InvalidArgumentException
from pydantic import BaseModel, validator


class Country(BaseModel):
    """
    A class to represent a Country.

    Attributes
    ----------
    code (str): The country code as a string.

    """

    code: str

    @validator("code")
    def validate_country(cls: "Country", value: str) -> str:
        """
        Validate the country code.

        Parameters
        ----------
        value (str): The country code to validate.

        Returns
        -------
        str: The validated country code.

        Raises
        ------
        InvalidArgumentException: If the country code is not valid.

        """
        if len(value) != 2:
            raise InvalidArgumentException(
                "Country code should be 2 characters (ISO3166 alpha 2)",
            )
        return value

    def get_code(self: "Country") -> str:
        """
        Get the country code in uppercase.

        Returns
        -------
        str: The country code in uppercase.

        """
        code = None
        if self.code is not None:
            code = self.code.upper()
        return code
