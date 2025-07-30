# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import json

from multisafepay.exception.invalid_total_amount import (
    InvalidTotalAmountException,
)


def validate_total_amount(data: dict) -> bool:
    """
    Validate the total amount in the provided data dictionary.

    Parameters
    ----------
    data (dict): The data dictionary containing the amount and shopping cart details.

    Returns
    -------
    bool: True if the total amount is valid, False otherwise.

    Raises
    ------
    InvalidTotalAmountException: If the total unit price does not match the amount in the data.

    """
    if "amount" not in data:
        raise InvalidTotalAmountException("Amount is required")

    if not data.get("shopping_cart") or not data["shopping_cart"].get("items"):
        return False

    amount = data["amount"]
    total_unit_price = __calculate_totals(data)

    if (total_unit_price * 100) != amount:
        msg = f"Total of unit_price ({total_unit_price}) does not match amount ({amount})"
        msg += "\n" + json.dumps(data, indent=4)
        raise InvalidTotalAmountException(msg)

    return True


def __calculate_totals(data: dict) -> float:
    """
    Calculate the total unit price of items in the shopping cart.

    Parameters
    ----------
    data (dict): The data dictionary containing the shopping cart details.

    Returns
    -------
    float: The total unit price of all items in the shopping cart.

    """
    total_unit_price = 0
    for item in data["shopping_cart"]["items"]:
        tax_rate = __get_tax_rate_by_item(item, data)
        item_price = item["unit_price"] * item["quantity"]
        item_price += tax_rate * item_price
        total_unit_price += item_price

    return round(total_unit_price, 2)


def __get_tax_rate_by_item(
    item: dict,
    data: dict,
) -> object:
    """
    Get the tax rate for a specific item in the shopping cart.

    Parameters
    ----------
    item (dict): The item dictionary containing the tax table selector.
    data (dict): The data dictionary containing the checkout options and tax tables.

    Returns
    -------
    object: The tax rate for the item, or 0 if no tax rate is found.

    """
    if "tax_table_selector" not in item or not item["tax_table_selector"]:
        return 0

    if (
        "checkout_options" not in data
        or "tax_tables" not in data["checkout_options"]
        or "default" not in data["checkout_options"]["tax_tables"]
    ):
        return 0

    for tax_table in data["checkout_options"]["tax_tables"]["alternate"]:
        if tax_table["name"] != item["tax_table_selector"]:
            continue

        tax_rule = tax_table["rules"][0]
        return tax_rule["rate"]
    return (
        data["checkout_options"]["tax_tables"]["default"]["rate"]
        if "default" in data["checkout_options"]["tax_tables"]
        and "rate" in data["checkout_options"]["tax_tables"]["default"]
        else 0
    )
