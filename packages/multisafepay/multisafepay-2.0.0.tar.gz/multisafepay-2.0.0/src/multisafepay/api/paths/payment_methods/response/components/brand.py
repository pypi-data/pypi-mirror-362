# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import List, Optional

from multisafepay.api.paths.payment_methods.response.components.icon_urls import (
    IconUrls,
)
from multisafepay.model.response_model import ResponseModel


class Brand(ResponseModel):
    """
    A class representing a brand with optional attributes for allowed countries, icon URLs, ID, and name.

    Attributes
    ----------
    allowed_countries (Optional[List[str]]): The allowed countries for the brand.
    icon_urls (Optional[IconUrls]): The icon URLs for the brand.
    id (Optional[str]): The ID of the brand.
    name (Optional[str]): The name of the brand.

    """

    allowed_countries: Optional[List[str]]
    icon_urls: Optional[IconUrls]
    id: Optional[str]
    name: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Brand"]:
        """
        Create a Brand instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the brand data.

        Returns
        -------
        Optional[Brand]: The Brand instance or None if the dictionary is None.

        """
        if d is None:
            return None
        d_adapted = {
            **d,
            "icon_urls": IconUrls.from_dict(d.get("icon_urls")),
        }
        return Brand(**d_adapted)
