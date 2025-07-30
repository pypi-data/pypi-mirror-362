# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.api.base.listings.cursor import Cursor
from multisafepay.model.response_model import ResponseModel


class Pager(ResponseModel):
    """
    A class to represent a pager for pagination.

    Attributes
    ----------
    after (Optional[str]): The cursor pointing to the next page.
    before (Optional[str]): The cursor pointing to the previous page.
    limit (Optional[int]): The limit on the number of items per page.
    cursor (Optional[Cursor]): The cursor object for pagination.

    """

    after: Optional[str]
    before: Optional[str]
    limit: Optional[int]
    cursor: Optional[Cursor]

    @staticmethod
    def from_dict(d: dict) -> Optional["Pager"]:
        """
        Create a Pager object from a dictionary.

        Parameters
        ----------
        d (dict): A dictionary containing the data to initialize the Pager object.

        Returns
        -------
        Optional[Pager]: An instance of Pager if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Pager(**d)
