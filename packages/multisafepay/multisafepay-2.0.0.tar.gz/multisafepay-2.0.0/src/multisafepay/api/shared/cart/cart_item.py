# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import copy
import math
from typing import Dict, List, Optional

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.api_model import ApiModel
from multisafepay.value_object.weight import Weight


class CartItem(ApiModel):
    """
    A class to represent a cart item.

    Attributes
    ----------
    cashback: (Optional[str]) The cashback value.
    currency: (Optional[str]) The currency.
    description: (Optional[str]) The description.
    image: (Optional[str]) The image URL.
    merchant_item_id: (Optional[str]) The merchant item ID.
    name: (Optional[str]) The name.
    options: (Optional[List[dict]]) The list of options.
    product_url: (Optional[str]) The product URL.
    quantity: (Optional[int]) The quantity.
    tax_table_selector: (Optional[str]) The tax table selector.
    unit_price: (Optional[float]) The unit price.
    weight: (Optional[Weight]) The weight.

    """

    cashback: Optional[str]
    currency: Optional[str]
    description: Optional[str]
    image: Optional[str]
    merchant_item_id: Optional[str]
    name: Optional[str]
    options: Optional[List[Dict]]
    product_url: Optional[str]
    quantity: Optional[int]
    tax_table_selector: Optional[str]
    unit_price: Optional[float]
    weight: Optional[Weight]

    def add_cashback(self: "CartItem", cashback: str) -> "CartItem":
        """
        Add cashback to the cart item.

        Parameters
        ----------
        cashback: (str) The cashback value to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.cashback = cashback
        return self

    def add_currency(self: "CartItem", currency: str) -> "CartItem":
        """
        Add currency to the cart item.

        Parameters
        ----------
        currency: (str) The currency value to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.currency = currency
        return self

    def add_description(self: "CartItem", description: str) -> "CartItem":
        """
        Add description to the cart item.

        Parameters
        ----------
        description: (str) The description to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.description = description
        return self

    def add_image(self: "CartItem", image: str) -> "CartItem":
        """
        Add image URL to the cart item.

        Parameters
        ----------
        image: (str) The image URL to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.image = image
        return self

    def add_merchant_item_id(
        self: "CartItem",
        merchant_item_id: str,
    ) -> "CartItem":
        """
        Add merchant item ID to the cart item.

        Parameters
        ----------
        merchant_item_id: (str) The merchant item ID to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.merchant_item_id = merchant_item_id
        return self

    def add_name(self: "CartItem", name: str) -> "CartItem":
        """
        Add name to the cart item.

        Parameters
        ----------
        name: (str) The name to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.name = name
        return self

    def add_options(self: "CartItem", options: List[Dict]) -> "CartItem":
        """
        Add options to the cart item.

        Parameters
        ----------
        options: (List[dict]) The list of options to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.options = options
        return self

    def add_product_url(self: "CartItem", product_url: str) -> "CartItem":
        """
        Add product URL to the cart item.

        Parameters
        ----------
        product_url: (str) The product URL to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.product_url = product_url
        return self

    def add_quantity(self: "CartItem", quantity: int) -> "CartItem":
        """
        Add quantity to the cart item.

        Parameters
        ----------
        quantity: (int) The quantity to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.quantity = quantity
        return self

    def add_tax_table_selector(
        self: "CartItem",
        tax_table_selector: str,
    ) -> "CartItem":
        """
        Add tax table selector to the cart item.

        Parameters
        ----------
        tax_table_selector: (str) The tax table selector to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.tax_table_selector = tax_table_selector
        return self

    def add_unit_price(self: "CartItem", unit_price: float) -> "CartItem":
        """
        Add unit price to the cart item.

        Parameters
        ----------
        unit_price: (float) The unit price to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.unit_price = unit_price
        return self

    def add_weight(self: "CartItem", weight: Weight) -> "CartItem":
        """
        Add weight to the cart item.

        Parameters
        ----------
        weight: (Weight) The weight to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        self.weight = weight
        return self

    def add_tax_rate_percentage(
        self: "CartItem",
        tax_rate_percentage: float,
    ) -> "CartItem":
        """
        Add tax rate percentage to the cart item.

        This method sets the tax rate percentage for the cart item. The tax rate should be a non-negative number.

        If the tax rate percentage is negative, an InvalidArgumentException is raised.

        If the tax rate percentage is a special float (NaN or Infinity), an InvalidArgumentException is raised.

        Parameters
        ----------
        tax_rate_percentage: (float) The tax rate percentage to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        if tax_rate_percentage < 0:
            raise InvalidArgumentException(
                "Tax rate percentage cannot be negative.",
            )

        if math.isnan(tax_rate_percentage) or math.isinf(tax_rate_percentage):
            raise InvalidArgumentException(
                "Tax rate percentage cannot be special floats.",
            )

        try:
            self.tax_table_selector = str(tax_rate_percentage / 100)
        except (ValueError, TypeError) as e:
            raise InvalidArgumentException(
                "Tax rate percentage cannot be converted to a string.",
            ) from e

        return self

    def add_tax_rate(self: "CartItem", tax_rate: float) -> "CartItem":
        """
        Add tax rate to the cart item.

        This method sets the tax rate for the cart item. The tax rate should be a non-negative number.

        If the tax rate is negative, an InvalidArgumentException is raised.

        If the tax rate is a special float (NaN or Infinity), an InvalidArgumentException is raised.

        Parameters
        ----------
        tax_rate: (float) The tax rate to be added.

        Returns
        -------
        CartItem: The updated CartItem instance.

        """
        if tax_rate < 0:
            raise InvalidArgumentException("Tax rate cannot be negative.")

        if math.isnan(tax_rate) or math.isinf(tax_rate):
            raise InvalidArgumentException(
                "Tax rate cannot be special floats.",
            )

        try:
            self.tax_table_selector = str(tax_rate)
        except (ValueError, TypeError) as e:
            raise InvalidArgumentException(
                "Tax rate cannot be converted to a string.",
            ) from e

        return self

    def clone(self: "CartItem") -> "CartItem":
        """
        Create a deep copy of the cart item.

        Returns
        -------
        CartItem: A deep copy of the CartItem instance.

        """
        return copy.deepcopy(self)

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["CartItem"]:
        """
        Create a CartItem instance from a dictionary.

        Parameters
        ----------
        d: (Optional[dict]) A dictionary containing the cart item data, by default None.

        Returns
        -------
        Optional[CartItem]: A CartItem instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None

        return CartItem(**d)
