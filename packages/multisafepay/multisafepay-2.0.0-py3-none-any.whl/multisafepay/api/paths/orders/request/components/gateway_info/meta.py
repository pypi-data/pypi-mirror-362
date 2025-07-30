# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.bank_account import BankAccount
from multisafepay.value_object.date import Date
from multisafepay.value_object.email_address import EmailAddress
from multisafepay.value_object.gender import Gender
from multisafepay.value_object.phone_number import PhoneNumber


class Meta(RequestModel):
    """
    Represents the Meta information in the MultiSafepay API.

    Attributes
    ----------
    birthday (Optional[str]): The birthday of the user.
    bank_account (Optional[str]): The bank account of the user.
    phone (Optional[str]): The phone number of the user.
    email_address (Optional[str]): The email address of the user.
    gender (Optional[str]): The gender of the user.

    """

    birthday: Optional[str]
    bank_account: Optional[str]
    phone: Optional[str]
    email_address: Optional[str]
    gender: Optional[str]

    def add_birthday(self: "Meta", birthday: Union[Date, str]) -> "Meta":
        """
        Adds a birthday to the Meta object.

        Parameters
        ----------
        birthday (Date | str): The birthday to be added.

        Returns
        -------
        Meta: The updated Meta object.

        """
        if isinstance(birthday, str):
            birthday = Date(date=birthday)
        self.birthday = birthday.get()
        return self

    def add_bank_account(
        self: "Meta",
        bank_account: Union[BankAccount, str],
    ) -> "Meta":
        """
        Adds a bank account to the Meta object.

        Parameters
        ----------
        bank_account (BankAccount | str): The bank account to be added.

        Returns
        -------
        Meta: The updated Meta object.

        """
        if isinstance(bank_account, str):
            bank_account = BankAccount(bank_account=bank_account)
        self.bank_account = bank_account.get()
        return self

    def add_phone(self: "Meta", phone: Union[PhoneNumber, str]) -> "Meta":
        """
        Adds a phone number to the Meta object.

        Parameters
        ----------
        phone (PhoneNumber | str): The phone number to be added.

        Returns
        -------
        Meta: The updated Meta object.

        """
        self.phone = phone
        return self

    def add_email_address(
        self: "Meta",
        email_address: Union[EmailAddress, str],
    ) -> "Meta":
        """
        Adds an email address to the Meta object.

        Parameters
        ----------
        email_address (EmailAddress | str): The email address to be added.

        Returns
        -------
        Meta: The updated Meta object.

        """
        if isinstance(email_address, str):
            email_address = EmailAddress(email_address=email_address)
        self.email_address = email_address.get()
        return self

    def add_gender(self: "Meta", gender: Union[Gender, str]) -> "Meta":
        """
        Adds a gender to the Meta object.

        Parameters
        ----------
        gender (Gender | str): The gender to be added.

        Returns
        -------
        Meta: The updated Meta object.

        """
        if isinstance(gender, str):
            gender = Gender(gender=gender)
        self.gender = gender.get()
        return self
