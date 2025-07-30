# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class IconUrls(ResponseModel):
    """
    A class representing icon URLs with optional attributes for large, medium, and vector icons.

    Attributes
    ----------
    large (Optional[str]): The URL for the large icon.
    medium (Optional[str]): The URL for the medium icon.
    vector (Optional[str]): The URL for the vector icon.

    """

    large: Optional[str]
    medium: Optional[str]
    vector: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["IconUrls"]:
        """
        Create an IconUrls instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the icon URLs data.

        Returns
        -------
        Optional[IconUrls]: The IconUrls instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return IconUrls(**d)
