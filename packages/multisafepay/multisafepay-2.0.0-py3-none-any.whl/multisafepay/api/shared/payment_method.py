# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.api_model import ApiModel


class PaymentMethod(ApiModel):
    """
    A class to represent a payment method, inheriting from ApiModel.

    Attributes
    ----------
    account_id (Optional[str]): The account ID associated with the payment method.
    amount (Optional[float]): The amount for the payment.
    currency (Optional[str]): The currency for the payment.
    description (Optional[str]): The description of the payment method.
    external_transaction_id (Optional[str]): The external transaction ID.
    payment_description (Optional[str]): The description of the payment.
    status (Optional[str]): The status of the payment method.
    type (Optional[str]): The type of the payment method.

    """

    account_id: Optional[str]
    amount: Optional[float]
    currency: Optional[str]
    description: Optional[str]
    external_transaction_id: Optional[str]
    payment_description: Optional[str]
    status: Optional[str]
    type: Optional[str]

    def add_account_id(
        self: "PaymentMethod",
        account_id: Optional[str],
    ) -> "PaymentMethod":
        """
        Add an account ID to the PaymentMethod instance.

        Parameters
        ----------
        account_id (Optional[str]): The account ID to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.account_id = account_id
        return self

    def add_amount(
        self: "PaymentMethod",
        amount: Optional[str],
    ) -> "PaymentMethod":
        """
        Add an amount to the PaymentMethod instance.

        Parameters
        ----------
        amount (Optional[str]): The amount to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.amount = amount
        return self

    def add_currency(
        self: "PaymentMethod",
        currency: Optional[str],
    ) -> "PaymentMethod":
        """
        Add a currency to the PaymentMethod instance.

        Parameters
        ----------
        currency (Optional[str]): The currency to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.currency = currency
        return self

    def add_description(
        self: "PaymentMethod",
        description: Optional[str],
    ) -> "PaymentMethod":
        """
        Add a description to the PaymentMethod instance.

        Parameters
        ----------
        description (Optional[str]): The description to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.description = description
        return self

    def add_external_transaction_id(
        self: "PaymentMethod",
        external_transaction_id: Optional[str],
    ) -> "PaymentMethod":
        """
        Add an external transaction ID to the PaymentMethod instance.

        Parameters
        ----------
        external_transaction_id (Optional[str]): The external transaction ID to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.external_transaction_id = external_transaction_id
        return self

    def add_payment_description(
        self: "PaymentMethod",
        payment_description: Optional[str],
    ) -> "PaymentMethod":
        """
        Add a payment description to the PaymentMethod instance.

        Parameters
        ----------
        payment_description (Optional[str]): The payment description to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.payment_description = payment_description
        return self

    def add_status(
        self: "PaymentMethod",
        status: Optional[str],
    ) -> "PaymentMethod":
        """
        Add a status to the PaymentMethod instance.

        Parameters
        ----------
        status (Optional[str]): The status to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.status = status
        return self

    def add_type(
        self: "PaymentMethod",
        type_: Optional[str],
    ) -> "PaymentMethod":
        """
        Add a type to the PaymentMethod instance.

        Parameters
        ----------
        type_ (Optional[str]): The type to add.

        Returns
        -------
        PaymentMethod: The updated PaymentMethod instance.

        """
        self.type = type_
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["PaymentMethod"]:
        """
        Create a PaymentMethod instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): The dictionary containing payment method data.

        Returns
        -------
        Optional[PaymentMethod]:
                A new PaymentMethod instance with the provided data, or None if the dictionary
                is None.

        """
        if d is None:
            return None
        return PaymentMethod(**d)
