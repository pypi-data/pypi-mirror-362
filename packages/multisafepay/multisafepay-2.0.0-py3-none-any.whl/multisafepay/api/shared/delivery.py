# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.api_model import ApiModel
from multisafepay.value_object.country import Country
from multisafepay.value_object.email_address import EmailAddress
from multisafepay.value_object.phone_number import PhoneNumber


class Delivery(ApiModel):
    """
    A class to represent delivery information, inheriting from ApiModel.

    Attributes
    ----------
    first_name (Optional[str]): The first name of the recipient.
    last_name (Optional[str]): The last name of the recipient.
    address1 (Optional[str]): The primary address line.
    address2 (Optional[str]): The secondary address line.
    house_number (Optional[str]): The house number.
    zip_code (Optional[str]): The postal code.
    city (Optional[str]): The city.
    state (Optional[str]): The state or province.
    country (Optional[str]): The country code.
    phone (Optional[str]): The phone number.
    email (Optional[str]): The email address.

    """

    first_name: Optional[str]
    last_name: Optional[str]
    address1: Optional[str]
    address2: Optional[str]
    house_number: Optional[str]
    zip_code: Optional[str]
    city: Optional[str]
    state: Optional[str]
    country: Optional[str]
    phone: Optional[str]
    email: Optional[str]

    def add_first_name(
        self: "Delivery",
        first_name: Optional[str],
    ) -> "Delivery":
        """
        Add the first name to the delivery information.

        Parameters
        ----------
        first_name (Optional[str]): The first name to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.first_name = first_name
        return self

    def add_last_name(
        self: "Delivery",
        last_name: Optional[str],
    ) -> "Delivery":
        """
        Add the last name to the delivery information.

        Parameters
        ----------
        last_name (Optional[str]): The last name to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.last_name = last_name
        return self

    def add_address1(self: "Delivery", address1: Optional[str]) -> "Delivery":
        """
        Add the primary address line to the delivery information.

        Parameters
        ----------
        address1 (Optional[str]): The primary address line to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.address1 = address1
        return self

    def add_address2(self: "Delivery", address2: Optional[str]) -> "Delivery":
        """
        Add the secondary address line to the delivery information.

        Parameters
        ----------
        address2 (Optional[str]): The secondary address line to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.address2 = address2
        return self

    def add_house_number(
        self: "Delivery",
        house_number: Optional[str],
    ) -> "Delivery":
        """
        Add the house number to the delivery information.

        Parameters
        ----------
        house_number (Optional[str]): The house number to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.house_number = house_number
        return self

    def add_zip_code(self: "Delivery", zip_code: Optional[str]) -> "Delivery":
        """
        Add the postal code to the delivery information.

        Parameters
        ----------
        zip_code (Optional[str]): The postal code to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.zip_code = zip_code
        return self

    def add_city(self: "Delivery", city: Optional[str]) -> "Delivery":
        """
        Add the city to the delivery information.

        Parameters
        ----------
        city (Optional[str]): The city to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.city = city
        return self

    def add_state(self: "Delivery", state: Optional[str]) -> "Delivery":
        """
        Add the state or province to the delivery information.

        Parameters
        ----------
        state (Optional[str]): The state or province to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        self.state = state
        return self

    def add_country(
        self: "Delivery",
        country: Optional[Union[Country, str]],
    ) -> "Delivery":
        """
        Add the country to the delivery information.

        Parameters
        ----------
        country (Optional[Country] | str): The country to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        if isinstance(country, str):
            country = Country(code=country)
        self.country = country.get_code()
        return self

    def add_phone(
        self: "Delivery",
        phone: Optional[Union[PhoneNumber, str]],
    ) -> "Delivery":
        """
        Add the phone number to the delivery information.

        Parameters
        ----------
        phone (Optional[PhoneNumber] | str): The phone number to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        if isinstance(phone, str):
            phone = PhoneNumber(phone_number=phone)
        self.phone = phone.get()
        return self

    def add_email(
        self: "Delivery",
        email: Optional[Union[EmailAddress, str]],
    ) -> "Delivery":
        """
        Add the email address to the delivery information.

        Parameters
        ----------
        email (Optional[EmailAddress]): The email address to add.

        Returns
        -------
        Delivery: The updated Delivery instance.

        """
        if isinstance(email, str):
            email = EmailAddress(email_address=email)
        self.email = email.get()
        return self

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["Delivery"]:
        """
        Create a Delivery instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the delivery details.

        Returns
        -------
        Optional[Delivery]: A Delivery instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Delivery(**d)
