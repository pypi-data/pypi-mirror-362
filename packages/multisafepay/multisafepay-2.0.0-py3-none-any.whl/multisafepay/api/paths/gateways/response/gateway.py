# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Gateway(ResponseModel):
    """
    A class representing a gateway in the response model.

    Attributes
    ----------
    id (Optional[str]): The gateway ID.
    description (Optional[str]): The gateway description.
    type (Optional[str]): The gateway type.

    """

    id: Optional[str]
    description: Optional[str]
    type: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Gateway"]:
        """
        Create a Gateway instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the gateway data.

        Returns
        -------
        Optional[ResponseModel]: A Gateway instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Gateway(**d)
