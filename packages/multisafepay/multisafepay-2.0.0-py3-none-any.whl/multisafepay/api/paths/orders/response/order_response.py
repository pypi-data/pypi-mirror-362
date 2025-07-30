# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import List, Optional

from multisafepay.api.base.decorator import Decorator
from multisafepay.api.paths.orders.response.components.order_adjustment import (
    OrderAdjustment,
)
from multisafepay.api.paths.orders.response.components.payment_details import (
    PaymentDetails,
)
from multisafepay.api.paths.transactions.response.transaction import (
    Transaction,
)
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.checkout.checkout_options import CheckoutOptions
from multisafepay.api.shared.costs import Costs
from multisafepay.api.shared.custom_info import CustomInfo
from multisafepay.api.shared.customer import Customer
from multisafepay.api.shared.payment_method import PaymentMethod
from multisafepay.model.response_model import ResponseModel


class Order(ResponseModel):
    """
    Represents an order with various attributes such as amount, currency, customer details, etc.

    Attributes
    ----------
    amount (Optional[int]): The amount of the order.
    amount_refunded (Optional[int]): The amount refunded.
    checkout_options (Optional[CheckoutOptions]): The checkout options.
    costs (Optional[List[Costs]]): The costs of the order.
    created (Optional[str]): The creation date of the order.
    modified (Optional[str]): The modification date of the order.
    currency (Optional[str]): The currency of the order.
    custom_info (Optional[CustomInfo]): The custom information of the order.
    customer (Optional[Customer]): The customer details.
    description (Optional[str]): The description of the order.
    fastcheckout (Optional[str]): The fast checkout option.
    financial_status (Optional[str]): The financial status of the order.
    items (Optional[str]): The items of the order.
    order_adjustment (Optional[OrderAdjustment]): The order adjustments.
    order_id (Optional[str]): The ID of the order.
    order_total (Optional[float]): The total amount of the order.
    payment_details (Optional[PaymentDetails]): The payment details.
    payment_method (Optional[List[PaymentMethod]]): The payment methods.
    reason (Optional[str]): The reason for the order.
    reason_code (Optional[str]): The reason code for the order.
    related_transactions (Optional[List[Transaction]]): The related transactions.
    shopping_cart (Optional[ShoppingCart]): The shopping cart.
    status (Optional[str]): The status of the order.
    transaction_id (Optional[str]): The ID of the transaction.
    var1 (Optional[str]): The var1 attribute.
    var2 (Optional[str]): The var2 attribute.
    var3 (Optional[str]): The var3 attribute.
    manual (Optional[bool]): The manual attribute.
    payment_url (Optional[str]): The payment URL.
    cancel_url (Optional[str]): The cancel URL.
    session_id (Optional[str]): The session ID.
    event_token (Optional[str]): The event token.
    event_url (Optional[str]): The event URL.
    event_stream_url (Optional[str]): The event stream URL.

    """

    amount: Optional[int]
    amount_refunded: Optional[int]
    checkout_options: Optional[CheckoutOptions]
    costs: Optional[List[Costs]]
    created: Optional[str]
    modified: Optional[str]
    currency: Optional[str]
    custom_info: Optional[CustomInfo]
    customer: Optional[Customer]
    description: Optional[str]
    fastcheckout: Optional[str]
    financial_status: Optional[str]
    items: Optional[str]
    order_adjustment: Optional[OrderAdjustment]
    order_id: Optional[str]
    order_total: Optional[float]
    payment_details: Optional[PaymentDetails]
    payment_methods: Optional[List[PaymentMethod]]
    reason: Optional[str]
    reason_code: Optional[str]
    related_transactions: Optional[List[Transaction]]
    shopping_cart: Optional[ShoppingCart]
    status: Optional[str]
    transaction_id: Optional[str]
    var1: Optional[str]
    var2: Optional[str]
    var3: Optional[str]
    manual: Optional[bool]

    payment_url: Optional[str]
    cancel_url: Optional[str]
    session_id: Optional[str]
    event_token: Optional[str]
    event_url: Optional[str]
    event_stream_url: Optional[str]

    def get_order_id(self: "Order") -> str:
        """
        Returns the order ID.

        Returns
        -------
        str: The order ID.

        """
        return self.order_id

    @staticmethod
    def from_dict(d: dict) -> Optional["Order"]:
        """
        Creates an Order instance from a dictionary.

        Parameters
        ----------
        d (dict): A dictionary containing the order data.

        Returns
        -------
        Order: An instance of Order with the data from the dictionary.

        """
        if d is None:
            return None
        order_dependency_adapter = Decorator(dependencies=d)
        dependencies = (
            order_dependency_adapter.adapt_order_adjustment(
                d.get("order_adjustment"),
            )
            .adapt_checkout_options(d.get("checkout_options"))
            .adapt_costs(d.get("costs"))
            .adapt_custom_info(d.get("custom_info"))
            .adapt_customer(d.get("customer"))
            .adapt_payment_details(d.get("payment_details"))
            .adapt_payment_methods(d.get("payment_methods"))
            .adapt_related_transactions(d.get("related_transactions"))
            .adapt_shopping_cart(d.get("shopping_cart"))
            .get_dependencies()
        )
        return Order(**dependencies)
