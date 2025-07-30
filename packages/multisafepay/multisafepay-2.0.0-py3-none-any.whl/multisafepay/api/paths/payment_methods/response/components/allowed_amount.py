# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class AllowedAmount(ResponseModel):
    """
    A class representing the allowed amount with minimum and maximum values.

    Attributes
    ----------
    min (Optional[int]): The minimum allowed amount.
    max (Optional[int]): The maximum allowed amount.

    """

    min: Optional[int]
    max: Optional[int]

    @staticmethod
    def from_dict(d: dict) -> Optional["AllowedAmount"]:
        """
        Create an AllowedAmount instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the allowed amount data.

        Returns
        -------
        Optional[AllowedAmount]: The AllowedAmount instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return AllowedAmount(**d)
