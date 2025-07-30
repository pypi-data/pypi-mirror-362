# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import List, Optional

from multisafepay.api.shared.cart.cart_item import CartItem
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.request_model import RequestModel


class CheckoutData(RequestModel):
    """
    Represents the checkout data for an order.

    Attributes
    ----------
    items (Optional[List[CartItem]]): The list of cart items.

    """

    items: Optional[List[CartItem]]

    def add_items(
        self: "CheckoutData",
        items: List[CartItem] = (),
    ) -> "CheckoutData":
        """
        Adds multiple items to the checkout data.

        Parameters
        ----------
        items (List[CartItem]): The list of items to add.

        Returns
        -------
        CheckoutData: The updated checkout data.

        """
        if self.items is None:
            self.items = []
        for item in items:
            self.add_item(item)
        return self

    def add_item(self: "CheckoutData", item: CartItem) -> "CheckoutData":
        """
        Adds a single item to the checkout data.

        Parameters
        ----------
        item (CartItem): The item to add.

        Returns
        -------
        CheckoutData: The updated checkout data.

        """
        if self.items is None:
            self.items = []
        self.items.append(item)
        return self

    def get_items(self: "CheckoutData") -> List[CartItem]:
        """
        Retrieves all items from the checkout data.

        Returns
        -------
        List[CartItem]: The list of items.

        """
        return self.items

    def get_item(self: "CheckoutData", index: int) -> CartItem:
        """
        Retrieves an item by its index from the checkout data.

        Parameters
        ----------
        index (int): The index of the item to retrieve.

        Returns
        -------
        CartItem: The retrieved item.

        """
        return self.items[index]

    def generate_from_shopping_cart(
        self: "CheckoutData",
        shopping_cart: ShoppingCart,
        tax_table_selector: str = "",
    ) -> None:
        """
        Generates checkout data from a shopping cart.

        Parameters
        ----------
        shopping_cart (ShoppingCart): The shopping cart to generate data from.
        tax_table_selector (str): The tax table selector to use.

        """
        if shopping_cart is None:
            return
        for shopping_cart_item in shopping_cart.get_items():
            if tax_table_selector:
                shopping_cart_item.add_tax_table_selector(tax_table_selector)
            self.add_item(shopping_cart_item)

    def refund_by_merchant_item_id(
        self: "CheckoutData",
        merchant_item_id: str,
        quantity: int = 0,
    ) -> None:
        """
        Processes a refund by merchant item ID.

        Parameters
        ----------
        merchant_item_id (str): The merchant item ID to refund.
        quantity (int): The quantity to refund.

        Raises
        ------
        InvalidArgumentException: If no items are provided or the item is not found.

        """
        if len(self.items) < 1:
            raise InvalidArgumentException(
                "No items provided in checkout data",
            )

        found_item = self.get_item_by_merchant_item_id(merchant_item_id)
        if quantity < 1 or quantity > found_item.quantity:
            quantity = found_item.get_quantity()

        refund_item = found_item.clone()
        refund_item.add_quantity(quantity)
        refund_item.add_unit_price(found_item.unit_price * -1.0)

        self.add_item(refund_item)

    def get_item_by_merchant_item_id(
        self: "CheckoutData",
        merchant_item_id: str,
    ) -> CartItem:
        """
        Retrieves an item by its merchant item ID.

        Parameters
        ----------
        merchant_item_id (str): The merchant item ID to search for.

        Returns
        -------
        CartItem: The found item.

        Raises
        ------
        InvalidArgumentException: If no item is found with the given merchant item ID.

        """
        for item in self.items:
            if item.merchant_item_id == merchant_item_id:
                return item

        raise InvalidArgumentException(
            f'No item found with merchant_item_id "{merchant_item_id}"',
        )
