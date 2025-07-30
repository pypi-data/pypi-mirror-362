# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from pydantic import validator
from pydantic.main import BaseModel

from ..exception.invalid_api_key import InvalidApiKeyException


class ApiKey(BaseModel):
    """
    A class to represent an API key.

    Attributes
    ----------
    api_key (str): The API key string.

    """

    api_key: str

    @validator("api_key")
    def validate_api_key(cls: "ApiKey", api_key: str) -> str:
        """
        Validate the API key.

        Parameters
        ----------
        api_key (str): The API key to validate.

        Returns
        -------
        str: The validated API key.

        Raises
        ------
        InvalidApiKeyException: If the API key is invalid (less than 5 characters).

        """
        if len(api_key) < 5:
            raise InvalidApiKeyException("Invalid API key")
        return api_key

    def get(self: "ApiKey") -> str:
        """
        Get the API key.

        Returns
        -------
        str: The API key.

        """
        return self.api_key
