# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import List, Optional

from multisafepay.api.base.decorator import Decorator
from multisafepay.api.paths.payment_methods.response.components.allowed_amount import (
    AllowedAmount,
)
from multisafepay.api.paths.payment_methods.response.components.apps import (
    Apps,
)
from multisafepay.api.paths.payment_methods.response.components.brand import (
    Brand,
)
from multisafepay.api.paths.payment_methods.response.components.icon_urls import (
    IconUrls,
)
from multisafepay.api.paths.payment_methods.response.components.tokenization import (
    Tokenization,
)
from multisafepay.model.response_model import ResponseModel


class PaymentMethod(ResponseModel):
    """
    A class representing a payment method.

    Attributes
    ----------
    additional_data (Optional[dict]): Additional data for the payment method.
    allowed_amount (Optional[AllowedAmount]): The allowed amount for the payment method.
    allowed_countries (Optional[List[str]]): The allowed countries for the payment method.
    allowed_currencies (OptionalList[str]]): The allowed currencies for the payment method.
    apps (Optional[Apps]): The apps associated with the payment method.
    brands (Optional[List[Brand]]): The brands associated with the payment method.
    description (Optional[str]): The description of the payment method.
    icon_urls (Optional[IconUrls]): The icon URLs for the payment method.
    id (Optional[str]): The ID of the payment method.
    label (Optional[str]): The label of the payment method.
    name (Optional[str]): The name of the payment method.
    preferred_countries (Optional[List[str]]): The preferred countries for the payment method.
    required_customer_data (Optional[List[str]]): The required customer data for the payment method.
    tokenization (Optional[Tokenization]): The tokenization support information for the payment method.
    type (Optional[str]): The type of the payment method.
    shopping_cart_required (Optional[bool]): Whether a shopping cart is required for the payment method.

    """

    additional_data: Optional[dict]
    allowed_amount: Optional[AllowedAmount]
    allowed_countries: Optional[List[str]]
    allowed_currencies: Optional[List[str]]
    apps: Optional[Apps]
    brands: Optional[List[Brand]]
    description: Optional[str]
    icon_urls: Optional[IconUrls]
    id: Optional[str]
    label: Optional[str]
    name: Optional[str]
    preferred_countries: Optional[List[str]]
    required_customer_data: Optional[List[str]]
    tokenization: Optional[Tokenization]
    type: Optional[str]
    shopping_cart_required: Optional[bool]

    @staticmethod
    def from_dict(d: dict) -> "PaymentMethod":
        """
        Create a PaymentMethod instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the payment method data.

        Returns
        -------
        PaymentMethod: The PaymentMethod instance.

        """
        payment_method_dependency_adapter = Decorator(dependencies=d)
        dependencies = (
            payment_method_dependency_adapter.adapt_allowed_amount(
                d.get("allowed_amount"),
            )
            .adapt_apps(d.get("apps"))
            .adapt_brands(d.get("brands"))
            .adapt_icon_urls(d.get("icon_urls"))
            .adapt_tokenization(d.get("tokenization"))
            .get_dependencies()
        )
        return PaymentMethod(**dependencies)
