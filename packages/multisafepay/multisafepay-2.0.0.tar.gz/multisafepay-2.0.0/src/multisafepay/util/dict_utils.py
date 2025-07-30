# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Optional


def merge_recursive(dict1: dict, dict2: dict) -> dict:
    """
    Recursively merge two dictionaries.

    Parameters
    ----------
    dict1 (dict): The first dictionary to merge.
    dict2 (dict): The second dictionary to merge.

    Returns
    -------
    dict: The merged dictionary.

    """
    for key, value in dict2.items():
        if (
            key in dict1
            and isinstance(dict1[key], dict)
            and isinstance(value, dict)
        ):
            dict1[key] = merge_recursive(dict1[key], value)
        else:
            dict1[key] = value
    return dict1


def remove_null(data: dict) -> dict:
    """
    Remove key-value pairs with None values from a dictionary.

    Parameters
    ----------
    data (dict): The dictionary to process.

    Returns
    -------
    dict: The dictionary with None values removed.

    """
    return {k: v for k, v in data.items() if v is not None}


def remove_null_recursive(input_data: dict) -> dict:
    """
    Recursively remove key-value pairs with None values from a dictionary.

    This function processes nested dictionaries and lists, removing any.

    Parameters
    ----------
    input_data (dict): The dictionary to process.

    Returns
    -------
    dict: The dictionary with None values removed recursively.

    """

    def process_value(value: object) -> Optional[object]:
        if isinstance(value, dict):
            processed_dict = remove_null_recursive(value)
            return processed_dict if processed_dict else None
        if isinstance(value, list):
            return [
                processed_item
                for item in value
                if (processed_item := process_value(item)) is not None
            ]
        return value

    return {
        k: process_value(v)
        for k, v in input_data.items()
        if process_value(v) is not None
    }


def dict_empty(value: object) -> bool:
    """
    Check if the given value is an empty dictionary.

    Parameters
    ----------
    value (any): The value to check.

    Returns
    -------
    bool: True if the value is an empty dictionary, False otherwise.

    """
    return isinstance(value, dict) and len(value) == 0
