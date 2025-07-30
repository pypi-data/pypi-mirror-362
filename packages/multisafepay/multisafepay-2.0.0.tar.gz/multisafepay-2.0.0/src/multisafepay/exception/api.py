# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import json
from typing import Dict, List, Optional, Union


class ApiException(Exception):
    """
    Base exception class for API-related errors.

    Attributes
    ----------
    message (str): The error message.
    context (dict): Additional context for the error.

    """

    def __init__(
        self: "ApiException",
        message: str,
        context: dict = None,
    ) -> None:
        """
        Initialize the ApiException.

        Parameters
        ----------
        message (str): The error message.
        context (dict, optional): Additional context for the error. Defaults to an empty dictionary.

        """
        self.message = message
        self.context = context if context else {}

    def add_message(self: "ApiException", message: str) -> "ApiException":
        """
        Add a message to the exception.

        Parameters
        ----------
        message (str): The message to add.

        Returns
        -------
        ApiException: The updated exception instance.

        """
        self.message = message
        return self

    def add_context(self: "ApiException", context: dict) -> "ApiException":
        """
        Add additional context to the exception.

        Parameters
        ----------
        context (dict): Additional context to add.

        Returns
        -------
        ApiException: The updated exception instance.

        """
        self.context.update(context)
        return self

    def get_details(self: "ApiException") -> str:
        """
        Get a detailed string representation of the exception.

        Returns
        -------
        str: A detailed string representation of the exception, including the message and context.

        """
        lines = [f"{self.__class__.__name__}: {self.get_message()}"]
        lines.extend(self.get_context_as_array())
        return "\n".join(lines)

    def get_message(self: "ApiException") -> str:
        """
        Get the error message.

        Returns
        -------
        str: The error message.

        """
        return self.message

    def get_context_as_array(self: "ApiException") -> list:
        """
        Get the context as an array of strings.

        Returns
        -------
        list: The context as an array of strings, with each key-value pair formatted as a string.

        """
        lines = []
        for context_name, context_value in self.context.items():
            debug_value = context_value
            if not isinstance(debug_value, str):
                debug_value = json.dumps(
                    context_value,
                    indent=4,
                    separators=(",", ": "),
                )
            lines.append(f"{context_name}: {debug_value}")
        return lines

    def get_context_value(
        self: "ApiException",
        name: str,
    ) -> Optional[Union[str, int, float, bool, Dict, List]]:
        """
        Get a specific context value by name.

        Parameters
        ----------
        name (str): The name of the context value to retrieve.

        Returns
        -------
        Optional[Union[str, int, float, bool, Dict, List]]: The value associated with the given name,
            or None if the name is not found.

        """
        return self.context.get(name)
