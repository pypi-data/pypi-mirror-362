# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Any, Dict, List, Optional, Union

from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.model.api_model import ApiModel


class TaxRule(ApiModel):
    """
    A class to represent a tax rule.

    Attributes
    ----------
    name (Optional[str]): The name of the tax rule.
    rules (Optional[List[TaxRate]]): A list of tax rates associated with the tax rule.
    standalone (Optional[bool]): Indicates if the tax rule is standalone.

    """

    name: Optional[str]
    rules: Optional[List[TaxRate]]
    standalone: Optional[Any]

    def add_name(self: "TaxRule", name: str) -> "TaxRule":
        """
        Add a name to the tax rule.

        Parameters
        ----------
        name (str): The name to be added.

        Returns
        -------
        TaxRule: The updated TaxRule instance.

        """
        self.name = name
        return self

    def add_rules(self: "TaxRule", rules: List[TaxRate]) -> "TaxRule":
        """
        Add a list of tax rates to the tax rule.

        Parameters
        ----------
        rules (List[TaxRate]): The list of tax rates to be added.

        Returns
        -------
        TaxRule: The updated TaxRule instance.

        """
        self.rules = rules
        return self

    def add_standalone(
        self: "TaxRule",
        standalone: Union[bool, str],
    ) -> "TaxRule":
        """
        Add standalone information to the tax rule.

        Parameters
        ----------
        standalone (bool): Indicates if the tax rule is standalone.

        Returns
        -------
        TaxRule: The updated TaxRule instance.

        """
        self.standalone = standalone
        return self

    def add_rule(self: "TaxRule", rule: TaxRate) -> "TaxRule":
        """
        Add a single tax rate to the tax rule.

        Parameters
        ----------
        rule (TaxRate): The tax rate to be added.

        Returns
        -------
        TaxRule: The updated TaxRule instance.

        """
        if self.rules is None:
            self.rules = []
        self.rules.append(rule)

    @staticmethod
    def from_dict(d: Optional[Dict]) -> Optional["TaxRule"]:
        """
        Create a TaxRule instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the tax rule data, by default None.

        Returns
        -------
        Optional[TaxRule]: A TaxRule instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        rules = None
        if d.get("rules", None) is not None:
            rules = [TaxRate.from_dict(item) for item in d.get("rules", [])]
        d_adapted = {**d, "rules": rules}

        return TaxRule(**d_adapted)
