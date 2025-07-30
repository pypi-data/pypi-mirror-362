# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.checkout.checkout_options import (
    CheckoutOptions as CheckoutOptionsApiModel,
)
from multisafepay.api.shared.checkout.tax_rate import TaxRate
from multisafepay.api.shared.checkout.tax_rule import TaxRule
from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.request_model import RequestModel


class CheckoutOptions(RequestModel):
    """
    A class to represent the checkout options.

    Attributes
    ----------
    tax_tables (Optional[CheckoutOptionsApiModel]): The tax tables.

    """

    tax_tables: Optional[CheckoutOptionsApiModel]
    validate_cart: Optional[bool]

    def add_tax_tables(
        self: "CheckoutOptions",
        tax_tables: CheckoutOptionsApiModel,
    ) -> "CheckoutOptions":
        """
        Add tax tables to the checkout options.

        Parameters
        ----------
        tax_tables (CheckoutOptionsApiModel): The tax tables to be added.

        Returns
        -------
        CheckoutOptions: The updated CheckoutOptions instance.

        """
        self.tax_tables = tax_tables
        return self

    def add_validate_cart(
        self: "CheckoutOptions",
        validate_cart: bool,
    ) -> "CheckoutOptions":
        """
        Add validate cart information to the checkout options.

        Parameters
        ----------
        validate_cart (bool): Indicates if the cart should be validated.

        Returns
        -------
        CheckoutOptions: The updated CheckoutOptions instance.

        """
        self.validate_cart = validate_cart
        return self

    @staticmethod
    def generate_from_shopping_cart(
        shopping_cart: ShoppingCart,
    ) -> Optional["CheckoutOptions"]:
        """
        Generate checkout options from a shopping cart.

        This method creates a CheckoutOptions instance based on the items in the shopping cart.

        Parameters
        ----------
        shopping_cart (ShoppingCart): The shopping cart containing items.

        Returns
        -------
        Optional[CheckoutOptions]: The generated CheckoutOptions instance or None if no items are present.

        """
        if shopping_cart.items:
            if not isinstance(shopping_cart.items, list):
                raise InvalidArgumentException(
                    "Expected shopping_cart.items to be a list.",
                )

            items_with_tax_table_selector = [
                item
                for item in shopping_cart.items
                if item.tax_table_selector is not None
                and (
                    isinstance(item.tax_table_selector, float)
                    or (
                        isinstance(item.tax_table_selector, str)
                        and item.tax_table_selector.replace(
                            ".",
                            "",
                            1,
                        ).isdigit()
                    )
                )
            ]

            tax_rules = [
                TaxRule(
                    name=str(item.tax_table_selector),
                    rules=[TaxRate(rate=item.tax_table_selector)],
                )
                for item in items_with_tax_table_selector
            ]
            return CheckoutOptions(
                tax_tables=CheckoutOptionsApiModel(
                    alternate=tax_rules,
                ),
            )
        return None
