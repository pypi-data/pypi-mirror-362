# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import List, Optional

from multisafepay.api.base.decorator import Decorator
from multisafepay.api.shared.costs import Costs
from multisafepay.api.shared.custom_info import CustomInfo
from multisafepay.api.shared.customer import Customer
from multisafepay.api.shared.payment_method import PaymentMethod
from multisafepay.model.response_model import ResponseModel


class Transaction(ResponseModel):
    """
    Transaction model class.

    Attributes
    ----------
    amount (Optional[int]): The amount of the transaction.
    completed (Optional[str]): The completion date of the transaction.
    costs (Optional[List[Costs]]): The costs of the transaction.
    created (Optional[str]): The creation date of the transaction.
    modified (Optional[str]): The modification date of the transaction.
    currency (Optional[str]): The currency of the transaction.
    customer (Optional[Customer]): The customer details.
    custom_info (Optional[CustomInfo]): The custom information of the transaction.
    debit_credit (Optional[str]): The debit or credit status of the transaction.
    description (Optional[str]): The description of the transaction.
    financial_status (Optional[str]): The financial status of the transaction.
    invoice_id (Optional[str]): The invoice ID of the transaction.
    net (Optional[int]): The net amount of the transaction.
    order_id (Optional[str]): The order ID of the transaction.
    payment_method (Optional[str]): The payment method of the transaction.
    payment_methods (Optional[List[PaymentMethod]]): The payment methods of the transaction.
    reason (Optional[str]): The reason for the transaction.
    reason_code (Optional[str]): The reason code for the transaction.
    site_id (Optional[str]): The site ID of the transaction.
    status (Optional[str]): The status of the transaction.
    transaction_id (Optional[str]): The ID of the transaction.
    type (Optional[str]): The type of the transaction.
    var1 (Optional[str]): The var1 attribute.
    var2 (Optional[str]): The var2 attribute.
    var3 (Optional[str]): The var3 attribute.
    fastcheckout (Optional[str]): The fast checkout option.
    items (Optional[str]): The items of the transaction.

    """

    amount: Optional[int]
    completed: Optional[str]
    costs: Optional[List[Costs]]
    created: Optional[str]
    modified: Optional[str]
    currency: Optional[str]
    customer: Optional[Customer]
    custom_info: Optional[CustomInfo]
    debit_credit: Optional[str]
    description: Optional[str]
    financial_status: Optional[str]
    invoice_id: Optional[str]
    net: Optional[int]
    order_id: Optional[str]
    payment_method: Optional[str]
    payment_methods: Optional[List[PaymentMethod]]
    reason: Optional[str]
    reason_code: Optional[str]
    site_id: Optional[str]
    status: Optional[str]
    transaction_id: Optional[str]
    type: Optional[str]
    var1: Optional[str]
    var2: Optional[str]
    var3: Optional[str]
    fastcheckout: Optional[str]
    items: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Transaction"]:
        """
        Create a Transaction instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the transaction data.

        Returns
        -------
        Transaction: The Transaction instance.

        """
        if d is None:
            return None
        transaction_dependency_adapter = Decorator(dependencies=d)
        dependencies = (
            transaction_dependency_adapter.adapt_costs(d.get("costs"))
            .adapt_customer(d.get("customer"))
            .adapt_payment_methods(d.get("payment_methods"))
            .get_dependencies()
        )
        return Transaction(**dependencies)
