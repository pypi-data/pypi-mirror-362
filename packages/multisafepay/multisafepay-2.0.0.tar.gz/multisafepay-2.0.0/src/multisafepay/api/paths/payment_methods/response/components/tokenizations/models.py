# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Models(ResponseModel):
    """
    A class representing the models associated with tokenization.

    Attributes
    ----------
    cardonfile (Optional[bool]): Whether the card is on file.
    subscription (Optional[bool]): Whether the tokenization is for a subscription.
    unscheduled (Optional[bool]): Whether the tokenization is unscheduled.

    """

    cardonfile: Optional[bool]
    subscription: Optional[bool]
    unscheduled: Optional[bool]

    @staticmethod
    def from_dict(d: dict) -> Optional["Models"]:
        """
        Create a Models instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the models data.

        Returns
        -------
        Optional[Models]: The Models instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return Models(**d)
