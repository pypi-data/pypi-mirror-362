# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


import re

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.inmutable_model import InmutableModel
from pydantic import validator


class IpAddress(InmutableModel):
    """
    A class to represent an IP address.

    Attributes
    ----------
    ip_address (str): The IP address as a string.

    """

    ip_address: str

    @validator("ip_address")
    def validate(cls: "IpAddress", value: str) -> str:
        """
        Validate the IP address.

        Parameters
        ----------
        value (str): The IP address to validate.

        Returns
        -------
        str:  The validated IP address.

        Raises
        ------
        InvalidArgumentException: If the IP address is not valid.

        """
        ip_address_list = value.split(",")
        ip_address = ip_address_list[0].strip()

        if not IpAddress.validate_ip_address(ip_address):
            raise InvalidArgumentException(
                f'Value "{ip_address}" is not a valid IP address',
            )

        return ip_address

    def get(self: "IpAddress") -> str:
        """
        Get the IP address.

        Returns
        -------
        str: The IP address.

        """
        return self.ip_address

    @staticmethod
    def validate_ip_address(ip: str) -> bool:
        """
        Validate the format of an IP address.

        Parameters
        ----------
        ip (str): The IP address to validate.

        Returns
        -------
        bool: True if the IP address is valid, False otherwise.

        """
        pattern = re.compile(
            r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$|"
            r"^(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$",
        )
        return bool(pattern.match(ip))
