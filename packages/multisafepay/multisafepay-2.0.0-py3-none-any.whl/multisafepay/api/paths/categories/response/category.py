# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Category(ResponseModel):
    """
    A class representing a category in the response model.

    Attributes
    ----------
    code (Optional[str]): The category code.

    """

    code: Optional[str]
    description: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Category"]:
        """
        Create a Category instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the category data.

        Returns
        -------
        Optional[ResponseModel]: A Category instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Category(**d)
