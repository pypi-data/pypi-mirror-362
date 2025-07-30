# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.api_model import ApiModel


class CustomInfo(ApiModel):
    """
    A class to represent custom information associated with a transaction.

    Attributes
    ----------
    custom_1 (Optional[str]): The first custom information field.
    custom_2 (Optional[str]): The second custom information field.
    custom_3 (Optional[str]): The third custom information field.

    """

    custom_1: Optional[str]
    custom_2: Optional[str]
    custom_3: Optional[str]

    def add_custom_1(self: "CustomInfo", custom_1: str) -> "CustomInfo":
        """
        Add custom information to the first field.

        Parameters
        ----------
        custom_1 (str): The custom information to add.

        Returns
        -------
        CustomInfo: The updated CustomInfo instance.

        """
        self.custom_1 = custom_1
        return self

    def add_custom_2(self: "CustomInfo", custom_2: str) -> "CustomInfo":
        """
        Add custom information to the second field.

        Parameters
        ----------
        custom_2 (str): The custom information to add.

        Returns
        -------
        CustomInfo: The updated CustomInfo instance.

        """
        self.custom_2 = custom_2
        return self

    def add_custom_3(self: "CustomInfo", custom_3: str) -> "CustomInfo":
        """
        Add custom information to the third field.

        Parameters
        ----------
        custom_3 (str): The custom information to add.

        Returns
        -------
        CustomInfo: The updated CustomInfo instance.

        """
        self.custom_3 = custom_3
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["CustomInfo"]:
        """
        Create a CustomInfo instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the custom information details.

        Returns
        -------
        Optional[CustomInfo]: A CustomInfo instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return CustomInfo(**d)
