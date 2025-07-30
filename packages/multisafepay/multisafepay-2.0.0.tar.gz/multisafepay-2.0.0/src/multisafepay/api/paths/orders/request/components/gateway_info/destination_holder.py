# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.country import Country
from multisafepay.value_object.iban_number import IbanNumber


class DestinationHolder(RequestModel):
    """
    Represents a destination holder with various attributes.

    Attributes
    ----------
    name (Optional[str]): The name of the destination holder.
    city (Optional[str]): The city of the destination holder.
    country (Optional[str]): The country of the destination holder.
    iban (Optional[str]): The IBAN of the destination holder.
    swift (Optional[str]): The SWIFT code of the destination holder.

    """

    name: Optional[str]
    city: Optional[str]
    country: Optional[str]
    iban: Optional[str]
    swift: Optional[str]

    def add_name(self: "DestinationHolder", name: str) -> "DestinationHolder":
        """
        Adds a name to the destination holder.

        Parameters
        ----------
        name (str): The name to add.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        self.name = name
        return self

    def add_city(self: "DestinationHolder", city: str) -> "DestinationHolder":
        """
        Adds a city to the destination holder.

        Parameters
        ----------
        city (str): The city to add.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        self.city = city
        return self

    def add_country(
        self: "DestinationHolder",
        country: Union[Country, str],
    ) -> "DestinationHolder":
        """
        Adds a country to the destination holder.

        Parameters
        ----------
        country (Country | str): The country to add. Can be a Country object or a string.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        if isinstance(country, str):
            country = Country(code=country)
        self.country = country.get_code()
        return self

    def add_iban(
        self: "DestinationHolder",
        iban: Union[IbanNumber, str],
    ) -> "DestinationHolder":
        """
        Adds an IBAN to the destination holder.

        Parameters
        ----------
        iban (IbanNumber | str): The IBAN to add. Can be an IbanNumber object or a string.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        if isinstance(iban, str):
            iban = IbanNumber(iban_number=iban)
        self.iban = iban.get()
        return self

    def add_swift(
        self: "DestinationHolder",
        swift: str,
    ) -> "DestinationHolder":
        """
        Adds a SWIFT code to the destination holder.

        Parameters
        ----------
        swift (str): The SWIFT code to add.

        Returns
        -------
        DestinationHolder: The updated destination holder.

        """
        self.swift = swift
        return self
