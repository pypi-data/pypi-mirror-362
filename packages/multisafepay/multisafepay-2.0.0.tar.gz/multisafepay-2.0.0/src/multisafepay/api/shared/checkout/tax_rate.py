# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.api_model import ApiModel


class TaxRate(ApiModel):
    """
    A class to represent the default tax rate.

    Attributes
    ----------
    rate (Optional[str]): The tax rate as a string.
    country (Optional[bool]): Indicates if shipping is taxed.

    """

    rate: Optional[float]
    country: Optional[str] = ""

    def add_rate(self: "TaxRate", rate: float) -> "TaxRate":
        """
        Add a tax rate.

        Parameters
        ----------
        rate (str): The tax rate to be added.

        Returns
        -------
        TaxRate: The updated TaxRate instance.

        """
        self.rate = rate
        return self

    def add_country(self: "TaxRate", country: str) -> "TaxRate":
        """
        Add shipping taxed information.

        Parameters
        ----------
        country (bool): Indicates if shipping is taxed.

        Returns
        -------
        TaxRate: The updated TaxRate instance.

        """
        self.country = country
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["TaxRate"]:
        """
        Create a TaxRate instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the default tax rate data, by default None.

        Returns
        -------
        Optional[TaxRate]: A TaxRate instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return TaxRate(**d)
