# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.api.paths.orders.request.components.checkout_options import (
    CheckoutOptions,
)
from multisafepay.api.paths.orders.request.components.customer_info import (
    CustomInfo,
)
from multisafepay.api.paths.orders.request.components.google_analytics import (
    GoogleAnalytics,
)
from multisafepay.api.paths.orders.request.components.payment_options import (
    PaymentOptions,
)
from multisafepay.api.paths.orders.request.components.plugin import (
    Plugin,
)
from multisafepay.api.paths.orders.request.components.second_chance import (
    SecondChance,
)
from multisafepay.api.shared.cart.shopping_cart import ShoppingCart
from multisafepay.api.shared.customer import Customer
from multisafepay.api.shared.delivery import Delivery
from multisafepay.api.shared.description import Description
from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.request_model import RequestModel
from multisafepay.util.total_amount import validate_total_amount
from multisafepay.value_object.amount import Amount
from multisafepay.value_object.currency import Currency

DIRECT_TYPE = "direct"
REDIRECT_TYPE = "redirect"
PAYMENT_LINK_TYPE = "paymentlink"
ALLOWED_TYPES = [DIRECT_TYPE, REDIRECT_TYPE, PAYMENT_LINK_TYPE]

CARD_ON_FILE_MODEL = "cardOnFile"
SUBSCRIPTION_MODEL = "subscription"
UNSCHEDULED_MODEL = "unscheduled"
ALLOWED_RECURRING_MODELS = [
    CARD_ON_FILE_MODEL,
    SUBSCRIPTION_MODEL,
    UNSCHEDULED_MODEL,
]


class OrderRequest(RequestModel):
    """
    Represents an order request with various attributes and methods to add details to the request.

    Attributes
    ----------
    type (Optional[str]): The type of the order request.
    gateway (Optional[str]): The gateway of the order request.
    order_id (Optional[str]): The order ID.
    currency (Optional[str]): The currency of the order.
    amount (Optional[str]): The amount of the order.
    payment_options (Optional[PaymentOptions]): The payment options.
    customer (Optional[Customer]): The customer.
    delivery (Optional[Delivery]): The delivery information.
    gateway_info (Optional[dict]): The gateway information.
    description (Optional[str]): The description of the order.
    recurring_id (Optional[str]): The recurring ID.
    google_analytics (Optional[GoogleAnalytics]): The Google Analytics information.
    shopping_cart (Optional[ShoppingCart]): The shopping cart.
    checkout_options (Optional[CheckoutOptions]): The checkout options.
    seconds_active (Optional[int]): The number of seconds the order is active.
    days_active (Optional[int]): The number of days the order is active.
    plugin (Optional[Plugin]): The plugin details.
    recurring_model (Optional[str]): The recurring model of the order.
    custom_info (Optional[CustomInfo]): The custom information.
    second_chance (Optional[SecondChance]): The second chance information.
    var1 (Optional[str]): The first custom variable.
    var2 (Optional[str]): The second custom variable.
    var3 (Optional[str]): The third custom variable

    """

    type: Optional[str]
    gateway: Optional[str]
    order_id: Optional[str]
    currency: Optional[str]
    amount: Optional[int]
    capture: Optional[str]
    payment_options: Optional[PaymentOptions]
    customer: Optional[Customer]
    delivery: Optional[Delivery]
    gateway_info: Optional[dict]
    description: Optional[str]
    recurring_id: Optional[str]
    recurring_model: Optional[str]
    google_analytics: Optional[GoogleAnalytics]
    shopping_cart: Optional[ShoppingCart]
    checkout_options: Optional[CheckoutOptions]
    seconds_active: Optional[int]
    days_active: Optional[int]
    plugin: Optional[Plugin]
    custom_info: Optional[CustomInfo]
    second_chance: Optional[SecondChance]
    var1: Optional[str]
    var2: Optional[str]
    var3: Optional[str]

    def add_type(self: "OrderRequest", order_type: str) -> "OrderRequest":
        """
        Adds the type of the order request.

        Parameters
        ----------
        order_type (str): The type of the order request. Must be one of the allowed types.

        Raises
        ------
        InvalidArgumentException: If the type is not a known type.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        if order_type not in ALLOWED_TYPES:
            msg = f'Type "{order_type}" is not a known type. Available types: {", ".join(ALLOWED_TYPES)}'
            raise InvalidArgumentException(msg)
        self.type = order_type
        return self

    def add_recurring_model(
        self: "OrderRequest",
        recurring_model: str,
    ) -> "OrderRequest":
        """
        Adds the recurring model of the order request.

        Parameters
        ----------
        recurring_model (str): The recurring model of the order request. Must be one of the allowed recurring models.

        Raises
        ------
        InvalidArgumentException: If the recurring model is not a known type.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        if recurring_model not in ALLOWED_RECURRING_MODELS:
            msg = f'Type "{recurring_model}" is not a known type. Available types: {", ".join(ALLOWED_RECURRING_MODELS)}'
            raise InvalidArgumentException(msg)
        self.recurring_model = recurring_model
        return self

    def add_order_id(self: "OrderRequest", order_id: str) -> "OrderRequest":
        """
        Adds the order ID to the order request.

        Parameters
        ----------
        order_id (str): The order ID.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.order_id = order_id
        return self

    def add_currency(
        self: "OrderRequest",
        currency: Union[Currency, str],
    ) -> "OrderRequest":
        """
        Adds the currency to the order request.

        Parameters
        ----------
        currency (Currency | str): The currency as a Currency object or a string.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        if isinstance(currency, str):
            currency = Currency(currency=currency)
        self.currency = currency.get()
        return self

    def add_amount(
        self: "OrderRequest",
        amount: Union[Amount, int],
    ) -> "OrderRequest":
        """
        Adds the amount to the order request.

        Parameters
        ----------
        amount (Amount | int): The amount as an Amount object or an integer.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        if isinstance(amount, int):
            amount = Amount(amount=amount)
        self.amount = amount.get()
        return self

    def add_capture(self: "OrderRequest", capture: str) -> "OrderRequest":
        """
        Adds the capture type to the order request.

        Parameters
        ----------
        capture (str): The capture type.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.capture = capture
        return self

    def add_payment_options(
        self: "OrderRequest",
        payment_options: PaymentOptions,
    ) -> "OrderRequest":
        """
        Adds the payment options to the order request.

        Parameters
        ----------
        payment_options (PaymentOptions): The payment options.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.payment_options = payment_options
        return self

    def add_customer(
        self: "OrderRequest",
        customer: Customer,
    ) -> "OrderRequest":
        """
        Adds the customer to the order request.

        Parameters
        ----------
        customer (Customer): The customer.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.customer = customer
        return self

    def add_gateway(self: "OrderRequest", gateway: str) -> "OrderRequest":
        """
        Adds the gateway to the order request.

        Parameters
        ----------
        gateway (str): The gateway.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.gateway = gateway
        return self

    def add_gateway_info(
        self: "OrderRequest",
        gateway_info: dict,
    ) -> "OrderRequest":
        """
        Adds the gateway information to the order request.

        Parameters
        ----------
        gateway_info (dict): The gateway information as a dictionary.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.gateway_info = gateway_info
        return self

    def add_description(
        self: "OrderRequest",
        description: Union[Description, str],
    ) -> "OrderRequest":
        """
        Adds the description to the order request.

        Parameters
        ----------
        description (Description | str): The description as a Description object or a string.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        if isinstance(description, str):
            description = Description(description=description)
        self.description = description.get()
        return self

    def add_plugin(
        self: "OrderRequest",
        plugin: Plugin,
    ) -> "OrderRequest":
        """
        Adds the plugin details to the order request.

        Parameters
        ----------
        plugin (Plugin): The plugin details.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.plugin = plugin
        return self

    def add_recurring_id(
        self: "OrderRequest",
        recurring_id: str,
    ) -> "OrderRequest":
        """
        Adds the recurring ID to the order request.

        Parameters
        ----------
        recurring_id (str): The recurring ID.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.recurring_id = recurring_id
        return self

    def add_second_chance(
        self: "OrderRequest",
        second_chance: SecondChance,
    ) -> "OrderRequest":
        """
        Adds the second chance information to the order request.

        Parameters
        ----------
        second_chance (SecondChance): The second chance information.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.second_chance = second_chance
        return self

    def add_google_analytics(
        self: "OrderRequest",
        google_analytics: GoogleAnalytics,
    ) -> "OrderRequest":
        """
        Adds the Google Analytics information to the order request.

        Parameters
        ----------
        google_analytics (GoogleAnalytics): The Google Analytics information.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.google_analytics = google_analytics
        return self

    def add_shopping_cart(
        self: "OrderRequest",
        shopping_cart: ShoppingCart,
    ) -> "OrderRequest":
        """
        Adds the shopping cart to the order request.

        Parameters
        ----------
        shopping_cart (ShoppingCart): The shopping cart.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.shopping_cart = shopping_cart
        return self

    def add_delivery(
        self: "OrderRequest",
        delivery: Delivery,
    ) -> "OrderRequest":
        """
        Adds the delivery information to the order request.

        Parameters
        ----------
        delivery (Delivery): The delivery information.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.delivery = delivery
        return self

    def add_checkout_options(
        self: "OrderRequest",
        checkout_options: CheckoutOptions,
    ) -> "OrderRequest":
        """
        Adds the checkout options to the order request.

        Parameters
        ----------
        checkout_options (CheckoutOptions): The checkout options.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.checkout_options = checkout_options
        return self

    def add_seconds_active(
        self: "OrderRequest",
        seconds: int,
    ) -> "OrderRequest":
        """
        Adds the seconds active to the order request.

        Parameters
        ----------
        seconds (int): The number of seconds the order is active.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.seconds_active = seconds
        return self

    def add_days_active(self: "OrderRequest", days: int) -> "OrderRequest":
        """
        Adds the days active to the order request.

        Parameters
        ----------
        days (int): The number of days the order is active.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.days_active = days
        return self

    def add_custom_info(
        self: "OrderRequest",
        custom_info: CustomInfo,
    ) -> "OrderRequest":
        """
        Adds the custom information to the order request.

        Parameters
        ----------
        custom_info (CustomInfo): The custom information.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.custom_info = custom_info
        return self

    def add_var1(self: "OrderRequest", var1: str) -> "OrderRequest":
        """
        Adds the first custom variable to the order request.

        Parameters
        ----------
        var1 (str): The first custom variable.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.var1 = var1
        return self

    def add_var2(self: "OrderRequest", var2: str) -> "OrderRequest":
        """
        Adds the second custom variable to the order request.

        Parameters
        ----------
        var2 (str): The second custom variable.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.var2 = var2
        return self

    def add_var3(self: "OrderRequest", var3: str) -> "OrderRequest":
        """
        Adds the third custom variable to the order request.

        Parameters
        ----------
        var3 (str): The third custom variable.

        Returns
        -------
        OrderRequest: The updated OrderRequest object.

        """
        self.var3 = var3
        return self

    def validate_amount(self: "OrderRequest") -> "OrderRequest":
        """
        Validates the total amount of the order request and the shopping cart.

        Returns
        -------
        OrderRequest: The validated OrderRequest object.

        """
        validate = validate_total_amount(self.dict())
        return self
