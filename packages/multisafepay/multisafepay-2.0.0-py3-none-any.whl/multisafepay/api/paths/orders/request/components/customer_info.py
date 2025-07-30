# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class CustomInfo(RequestModel):
    """
    Represents custom information with three optional custom fields.

    Attributes
    ----------
    custom1 (Optional[str]): The first custom field.
    custom2 (Optional[str]): The second custom field.
    custom3 (Optional[str]): The third custom field.

    """

    custom1: Optional[str]
    custom2: Optional[str]
    custom3: Optional[str]

    def add_custom1(self: "CustomInfo", custom1: str) -> "CustomInfo":
        """
        Adds the first custom field to the CustomInfo object.

        Parameters
        ----------
        custom1 (str): The value for the first custom field.

        Returns
        -------
        CustomInfo: The updated CustomInfo object.

        """
        self.custom1 = custom1
        return self

    def add_custom2(self: "CustomInfo", custom2: str) -> "CustomInfo":
        """
        Adds the second custom field to the CustomInfo object.

        Parameters
        ----------
        custom2 (str): The value for the second custom field.

        Returns
        -------
        CustomInfo: The updated CustomInfo object.

        """
        self.custom2 = custom2
        return self

    def add_custom3(self: "CustomInfo", custom3: str) -> "CustomInfo":
        """
        Adds the third custom field to the CustomInfo object.

        Parameters
        ----------
        custom3 (str): The value for the third custom field.

        Returns
        -------
        CustomInfo: The updated CustomInfo object.

        """
        self.custom3 = custom3
        return self
