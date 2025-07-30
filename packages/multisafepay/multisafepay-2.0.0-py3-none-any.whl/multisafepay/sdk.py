# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.api.paths.auth.auth_manager import AuthManager
from multisafepay.api.paths.categories.category_manager import CategoryManager
from multisafepay.api.paths.gateways.gateway_manager import GatewayManager
from multisafepay.api.paths.issuers.issuer_manager import IssuerManager
from multisafepay.api.paths.orders.order_manager import OrderManager
from multisafepay.api.paths.payment_methods.payment_method_manager import (
    PaymentMethodManager,
)
from multisafepay.api.paths.transactions.transaction_manager import (
    TransactionManager,
)

from .api.paths.capture.capture_manager import CaptureManager
from .api.paths.me.me_manager import MeManager
from .api.paths.recurring.recurring_manager import RecurringManager
from .client.client import Client


class Sdk:
    """
    SDK class for interacting with the MultiSafePay API.

    This class provides methods to manage various resources such as transactions,
    gateways, payment methods, issuers, orders, and more.
    """

    def __init__(
        self: "Sdk",
        api_key: str,
        is_production: bool,
        http_client: Optional[Client] = None,
        locale: str = "en_US",
    ) -> None:
        """
        Initialize the SDK with the provided configuration.

        Parameters
        ----------
        api_key : str
            The API key for authenticating with the MultiSafePay API.
        is_production : bool
            Flag indicating whether to use the production environment.
        http_client : Optional[Client], optional
            The HTTP client to use for making requests, by default None.
        locale : str, optional
            The locale to use for requests, by default "en_US".

        """
        self.client = Client(
            api_key.strip(),
            is_production,
            http_client,
            locale,
        )
        self.recurring_manager = RecurringManager(self.client)

    def get_transaction_manager(self: "Sdk") -> TransactionManager:
        """
        Get the transaction manager.

        Returns
        -------
        TransactionManager
            The transaction manager instance.

        """
        return TransactionManager(self.client)

    def get_gateway_manager(self: "Sdk") -> GatewayManager:
        """
        Get the gateway manager.

        Returns
        -------
        GatewayManager
            The gateway manager instance.

        """
        return GatewayManager(self.client)

    def get_payment_method_manager(self: "Sdk") -> PaymentMethodManager:
        """
        Get the payment method manager.

        Returns
        -------
        PaymentMethodManager
            The payment method manager instance.

        """
        return PaymentMethodManager(self.client)

    def get_issuer_manager(self: "Sdk") -> IssuerManager:
        """
        Get the issuer manager.

        Returns
        -------
        IssuerManager
            The issuer manager instance.

        """
        return IssuerManager(self.client)

    def get_recurring_manager(self: "Sdk") -> RecurringManager:
        """
        Get the recurring manager.

        Returns
        -------
        RecurringManager
            The recurring manager instance.

        """
        return self.recurring_manager

    def get_auth_manager(self: "Sdk") -> AuthManager:
        """
        Get the auth manager.

        Returns
        -------
        AuthManager
            The auth manager instance.

        """
        return AuthManager(self.client)

    def get_me_manager(self: "Sdk") -> MeManager:
        """
        Get the me manager.

        Returns
        -------
        MeManager
            The me manager instance.

        """
        return MeManager(self.client)

    def get_category_manager(self: "Sdk") -> CategoryManager:
        """
        Get the category manager.

        Returns
        -------
        CategoryManager
            The category manager instance.

        """
        return CategoryManager(self.client)

    def get_order_manager(self: "Sdk") -> OrderManager:
        """
        Get the order manager.

        Returns
        -------
        OrderManager
            The order manager instance.

        """
        return OrderManager(self.client)

    def get_capture_manager(self: "Sdk") -> CaptureManager:
        """
        Get the capture manager.

        Returns
        -------
        CaptureManager
            The capture manager instance.

        """
        return CaptureManager(self.client)

    def get_client(self: "Sdk") -> Client:
        """
        Get the client instance.

        Returns
        -------
        Client
            The client instance.

        """
        return self.client
