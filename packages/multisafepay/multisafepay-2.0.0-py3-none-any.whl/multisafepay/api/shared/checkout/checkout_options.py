# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import List, Optional

from multisafepay.api.shared.checkout.default_tax_rate import DefaultTaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule
from multisafepay.model.api_model import ApiModel


class CheckoutOptions(ApiModel):
    """
    A class to represent the checkout options.

    Attributes
    ----------
    default (Optional[DefaultTaxRate]): The default tax rate.
    alternate (Optional[List[TaxRate]]): A list of alternate tax rates.

    """

    default: Optional[DefaultTaxRate]
    alternate: Optional[List[TaxRule]]

    def add_default(
        self: "CheckoutOptions",
        default: DefaultTaxRate,
    ) -> "CheckoutOptions":
        """
        Add a default tax rate to the checkout options.

        Parameters
        ----------
        default (DefaultTaxRate): The default tax rate to be added.

        Returns
        -------
        CheckoutOptions: The updated CheckoutOptions instance.

        """
        self.default = default
        return self

    def add_alternate(
        self: "CheckoutOptions",
        alternate: List[TaxRule],
    ) -> "CheckoutOptions":
        """
        Add alternate tax rates to the checkout options.

        Parameters
        ----------
        alternate (List[TaxRule]): The list of alternate tax rates to be added.

        Returns
        -------
        CheckoutOptions: The updated CheckoutOptions instance.

        """
        self.alternate = alternate
        return self

    def add_tax_rule(
        self: "CheckoutOptions",
        tax_rule: TaxRule,
    ) -> "CheckoutOptions":
        """
        Add a tax rule to the checkout options.

        Parameters
        ----------
        tax_rule (TaxRule): The tax rule to be added.

        Returns
        -------
        CheckoutOptions: The updated CheckoutOptions instance.

        """
        if self.alternate is None:
            self.alternate = []
        self.alternate.append(tax_rule)
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["CheckoutOptions"]:
        """
        Create a CheckoutOptions instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the checkout options data, by default None.

        Returns
        -------
        Optional["CheckoutOptions"]: A CheckoutOptions instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        alternate = (
            [TaxRule.from_dict(item) for item in d.get("alternate", [])]
            if d.get("alternate") is not None
            else None
        )

        return CheckoutOptions(
            default=DefaultTaxRate.from_dict(d=d.get("default", None)),
            alternate=alternate,
        )
