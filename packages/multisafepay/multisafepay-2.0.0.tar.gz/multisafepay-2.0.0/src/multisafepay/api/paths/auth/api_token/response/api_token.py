# Copyright (c) MultiSafepay, Inc. All rights reserved.
from typing import Optional

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.
# See the DISCLAIMER.md file for disclaimer details.
from multisafepay.model.response_model import ResponseModel


class ApiToken(ResponseModel):
    """
    A class to represent an API token.

    Attributes
    ----------
    api_token (Optional[str]): The API token.

    """

    api_token: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["ApiToken"]:
        """
        Create an ApiToken object from a dictionary.

        Parameters
        ----------
        d (dict): A dictionary containing the API token data.

        Returns
        -------
        Optional[ApiToken]: An ApiToken object if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return ApiToken(**d)
