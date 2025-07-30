# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.api_model import ApiModel


class DefaultTaxRate(ApiModel):
    """
    A class to represent the default tax rate.

    Attributes
    ----------
    rate (Optional[str]): The tax rate as a string.
    shipping_taxed (Optional[bool]): Indicates if shipping is taxed.

    """

    rate: Optional[float]
    shipping_taxed: Optional[bool]

    def add_rate(self: "DefaultTaxRate", rate: float) -> "DefaultTaxRate":
        """
        Add a tax rate.

        Parameters
        ----------
        rate (str): The tax rate to be added.

        Returns
        -------
        DefaultTaxRate: The updated DefaultTaxRate instance.

        """
        self.rate = rate
        return self

    def add_shipping_taxed(
        self: "DefaultTaxRate",
        shipping_taxed: bool,
    ) -> "DefaultTaxRate":
        """
        Add shipping taxed information.

        Parameters
        ----------
        shipping_taxed (bool): Indicates if shipping is taxed.

        Returns
        -------
        DefaultTaxRate: The updated DefaultTaxRate instance.

        """
        self.shipping_taxed = shipping_taxed
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["DefaultTaxRate"]:
        """
        Create a DefaultTaxRate instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the default tax rate data, by default None.

        Returns
        -------
        Optional[DefaultTaxRate]: A DefaultTaxRate instance if the dictionary is not None, otherwise None.

        """
        if d is None or not isinstance(d, dict):
            return None
        return DefaultTaxRate(**d)
