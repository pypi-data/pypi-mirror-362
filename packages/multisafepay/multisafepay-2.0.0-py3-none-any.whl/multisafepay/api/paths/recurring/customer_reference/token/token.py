# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Token(ResponseModel):
    """
    A class to represent a Token.

    Attributes
    ----------
    token (Optional[str]): The token.
    code (Optional[str]): The code.
    display (Optional[str]): The display.
    bin (Optional[str]): The BIN.
    name_holder (Optional[str]): The name holder.
    expiry_date (Optional[str]): The expiry date.
    is_expired (Optional[bool]): Whether the token is expired.
    last_four (Optional[str]): The last four digits.
    model (Optional[str]): The model.

    """

    token: Optional[str]
    code: Optional[str]
    display: Optional[str]
    bin: Optional[str]
    name_holder: Optional[str]
    expiry_date: Optional[str]
    is_expired: Optional[bool]
    last_four: Optional[str]
    model: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Token"]:
        """
        Create a Token instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the data to initialize the Token instance.

        Returns
        -------
        Optional[Token]:
            An instance of the Token class initialized with the data from the dictionary,
            or None if the input dictionary is None.

        """
        if d is None:
            return None
        return Token(**d)
