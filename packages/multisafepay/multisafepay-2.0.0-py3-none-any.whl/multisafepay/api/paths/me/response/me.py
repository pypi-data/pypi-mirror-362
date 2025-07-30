# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Me(ResponseModel):
    """
    A class representing the 'Me' response model.

    Attributes
    ----------
    account_id (Optional[int]): The account ID.
    role (Optional[str]): The role.
    site_id (Optional[int]): The site

    """

    account_id: Optional[int]
    role: Optional[str]
    site_id: Optional[int]

    @staticmethod
    def from_dict(d: dict) -> Optional["Me"]:
        """
        Create a 'Me' instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the 'Me' data.

        Returns
        -------
        Optional[Me]: The 'Me' instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return Me(**d)
