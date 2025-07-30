# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

import urllib.parse

from multisafepay.client.client import Client


class AbstractManager:
    """
    A class to represent an abstract manager.

    Attributes
    ----------
    client (Client): An instance of the Client class to be used by the manager.

    """

    def __init__(self: "AbstractManager", client: Client) -> None:
        """
        Initialize the AbstractManager with a Client instance.

        Parameters
        ----------
        client (Client): An instance of the Client class to be used by the manager.

        """
        self.client = client

    @staticmethod
    def encode_path_segment(segment: str) -> str:
        """
        URL encode a path segment to be safely included in a URL.

        Parameters
        ----------
        segment (str): The path segment to encode

        Returns
        -------
        str: The URL encoded path segment

        """
        return urllib.parse.quote(str(segment), safe="")
