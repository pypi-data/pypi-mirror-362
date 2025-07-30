# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.response_model import ResponseModel


class Weight(ResponseModel):
    """
    A class to represent the weight of an item.

    Attributes
    ----------
    unit (str): The unit of measurement for the weight (e.g., kg, lb).
    value (float) :The quantity of the weight.

    """

    unit: Optional[str]
    value: Optional[Union[float, str]]

    def get_unit(self: "Weight") -> str:
        """
        Get the unit of measurement for the weight.

        Returns
        -------
        str: The unit of measurement.

        """
        return self.unit

    def get_value(self: "Weight") -> Union[float, str]:
        """
        Get the value of the weight.

        Returns
        -------
        float: The value of the weight.

        """
        return self.value

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["Weight"]:
        """
        Create a Weight instance from a dictionary.

        Parameters
        ----------
        d (dict): A dictionary containing the weight data.

        Returns
        -------
        Optional[Weight]: The Weight instance.

        """
        if d is None:
            return None

        return Weight(**d)
