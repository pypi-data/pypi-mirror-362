# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Cursor(ResponseModel):
    """
    A class to represent a cursor for pagination.

    Attributes
    ----------
    after (Optional[str]): The cursor pointing to the next page.
    before (Optional[str]): The cursor pointing to the previous page.

    """

    after: Optional[str]
    before: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Cursor"]:
        """
        Create a Cursor object from a dictionary.

        Parameters
        ----------
        obj (dict): A dictionary containing the data to initialize the Cursor object.

        Returns
        -------
        Optional[Cursor]: An instance of Cursor if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Cursor(**d)
