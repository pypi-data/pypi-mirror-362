# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Any, Dict, List, Optional


class Decorator:
    """
    A class to represent a decorator for response models.

    Attributes
    ----------
    dependencies (Optional[Dict]): A dictionary of dependencies to be used by the decorator.

    """

    dependencies: Optional[Dict]

    def __init__(self: "Decorator", dependencies: Dict = None) -> None:
        """
        Initialize the Decorator with optional dependencies.

        Parameters
        ----------
        dependencies (dict): A dictionary of dependencies to be used by the decorator, by default {}.

        """
        self.dependencies = dependencies if dependencies is not None else {}

    def adapt_checkout_options(
        self: "Decorator",
        checkout_options: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the checkout options and update the dependencies.

        Parameters
        ----------
        checkout_options (Optional[dict]): A dictionary containing checkout options, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if checkout_options is not None:
            from multisafepay.api.shared.checkout.checkout_options import (
                CheckoutOptions,
            )

            self.dependencies["checkout_options"] = CheckoutOptions.from_dict(
                checkout_options,
            )
        return self

    def adapt_costs(self: "Decorator", costs: Optional[Dict]) -> "Decorator":
        """
        Adapt the costs and update the dependencies.

        Parameters
        ----------
        costs (Optional[dict]): A dictionary containing costs, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if costs is not None:
            from multisafepay.api.shared.costs import Costs

            self.dependencies["costs"] = [
                Costs.from_dict(cost) for cost in costs
            ]
        return self

    def adapt_custom_info(
        self: "Decorator",
        custom_info: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the custom information and update the dependencies.

        Parameters
        ----------
        custom_info (Optional[dict]): A dictionary containing custom information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if custom_info is not None:
            from multisafepay.api.shared.custom_info import CustomInfo

            self.dependencies["custom_info"] = CustomInfo.from_dict(
                custom_info,
            )

        return self

    def adapt_customer(
        self: "Decorator",
        customer: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the customer information and update the dependencies.

        Parameters
        ----------
        customer (Optional[dict]): A dictionary containing customer information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if customer is not None:
            from multisafepay.api.shared.customer import Customer

            self.dependencies["customer"] = Customer.from_dict(customer)

        return self

    def adapt_order_adjustment(
        self: "Decorator",
        order_adjustment: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the order adjustment and update the dependencies.

        Parameters
        ----------
        order_adjustment (Optional[dict]): A dictionary containing order adjustment information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if order_adjustment is not None:
            from multisafepay.api.paths.orders.response.components.order_adjustment import (
                OrderAdjustment,
            )

            self.dependencies["order_adjustment"] = OrderAdjustment.from_dict(
                order_adjustment,
            )

        return self

    def adapt_payment_details(
        self: "Decorator",
        payment_details: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the payment details and update the dependencies.

        Parameters
        ----------
        payment_details (Optional[dict]): A dictionary containing payment details, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if payment_details is not None:
            from multisafepay.api.paths.orders.response.components.payment_details import (
                PaymentDetails,
            )

            self.dependencies["payment_details"] = PaymentDetails.from_dict(
                payment_details,
            )

        return self

    def adapt_payment_methods(
        self: "Decorator",
        payment_methods: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the payment methods and update the dependencies.

        Parameters
        ----------
        payment_methods (Optional[dict]): A dictionary containing payment methods, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if payment_methods is not None:
            from multisafepay.api.shared.payment_method import PaymentMethod

            self.dependencies["payment_methods"] = [
                PaymentMethod.from_dict(payment_method)
                for payment_method in payment_methods
            ]
        return self

    def adapt_shopping_cart(
        self: "Decorator",
        shopping_cart: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the shopping cart and update the dependencies.

        Parameters
        ----------
        shopping_cart (Optional[dict]): A dictionary containing shopping cart information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if shopping_cart is not None:
            from multisafepay.api.shared.cart.shopping_cart import ShoppingCart

            self.dependencies["shopping_cart"] = ShoppingCart.from_dict(
                shopping_cart,
            )
        return self

    def adapt_related_transactions(
        self: "Decorator",
        related_transactions: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the related transactions and update the dependencies.

        Parameters
        ----------
        related_transactions (Optional[dict]): A dictionary containing related transactions, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if related_transactions is not None:
            from multisafepay.api.paths.transactions.response.transaction import (
                Transaction,
            )

            self.dependencies["related_transactions"] = [
                Transaction.from_dict(related_transaction)
                for related_transaction in related_transactions
            ]
        return self

    def adapt_apps(self: "Decorator", apps: Optional[Dict]) -> "Decorator":
        """
        Adapt the apps and update the dependencies.

        Parameters
        ----------
        apps (Optional[dict]): A dictionary containing app information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if apps is not None:
            from multisafepay.api.paths.payment_methods.response.components.apps import (
                Apps,
            )

            self.dependencies["apps"] = Apps.from_dict(apps)

        return self

    def adapt_brands(
        self: "Decorator",
        brands: Optional[List[Optional[Dict]]],
    ) -> "Decorator":
        """
        Adapt the brands and update the dependencies.

        Parameters
        ----------
        brands (Optional[List[Optional[dict]]]): A list of dictionaries containing brand information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if brands is not None:
            from multisafepay.api.paths.payment_methods.response.components.brand import (
                Brand,
            )

            self.dependencies["brands"] = [
                Brand.from_dict(brand) for brand in brands
            ]
        return self

    def adapt_icon_urls(
        self: "Decorator",
        icon_urls: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the icon URLs and update the dependencies.

        Parameters
        ----------
        icon_urls (Optional[dict]): A dictionary containing icon URL information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if icon_urls is not None:
            from multisafepay.api.paths.payment_methods.response.components.icon_urls import (
                IconUrls,
            )

            self.dependencies["icon_urls"] = IconUrls.from_dict(icon_urls)

        return self

    def adapt_tokenization(
        self: "Decorator",
        tokenization: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the tokenization and update the dependencies.

        Parameters
        ----------
        tokenization: (dict, optional) A dictionary containing tokenization information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if tokenization is not None:
            from multisafepay.api.paths.payment_methods.response.components.tokenization import (
                Tokenization,
            )

            self.dependencies["tokenization"] = Tokenization.from_dict(
                tokenization,
            )

        return self

    def adapt_allowed_amount(
        self: "Decorator",
        allowed_amount: Optional[Dict],
    ) -> "Decorator":
        """
        Adapt the allowed amount and update the dependencies.

        Parameters
        ----------
        allowed_amount (Optional[dict]): A dictionary containing allowed amount information, by default None.

        Returns
        -------
        Decorator: The updated Decorator instance.

        """
        if allowed_amount is not None:
            from multisafepay.api.paths.payment_methods.response.components.allowed_amount import (
                AllowedAmount,
            )

            self.dependencies["allowed_amount"] = AllowedAmount.from_dict(
                allowed_amount,
            )
        return self

    def get_dependencies(self: "Decorator") -> Dict[str, Any]:
        """
        Get the current dependencies.

        Returns
        -------
        dict: A dictionary of the current dependencies.

        """
        return self.dependencies
