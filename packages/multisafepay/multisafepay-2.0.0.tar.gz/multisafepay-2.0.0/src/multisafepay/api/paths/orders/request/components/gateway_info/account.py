# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.iban_number import IbanNumber


class Account(RequestModel):
    """
    Represents an account with various attributes.

    Attributes
    ----------
    account_id (Optional[str]): The ID of the account.
    account_holder_name (Optional[str]): The name of the account holder.
    account_holder_iban (Optional[str]): The IBAN of the account holder.
    emandate (Optional[str]): The e-mandate associated with the account.

    """

    account_id: Optional[str]
    account_holder_name: Optional[str]
    account_holder_iban: Optional[str]
    emandate: Optional[str]

    def add_account_id(
        self: "Account",
        account_id: Union[IbanNumber, str],
    ) -> "Account":
        """
        Adds an account ID to the account.

        Parameters
        ----------
        account_id (IbanNumber | str): The account ID to add. Can be an IbanNumber object or a string.

        Returns
        -------
        Account: The updated account.

        """
        if isinstance(account_id, str):
            account_id = IbanNumber(iban_number=account_id)
        self.account_id = account_id.get()
        return self

    def add_account_holder_name(
        self: "Account",
        account_holder_name: str,
    ) -> "Account":
        """
        Adds an account holder name to the account.

        Parameters
        ----------
        account_holder_name (str): The account holder name to add.

        Returns
        -------
        Account: The updated account.

        """
        self.account_holder_name = account_holder_name
        return self

    def add_account_holder_iban(
        self: "Account",
        account_holder_iban: IbanNumber,
    ) -> "Account":
        """
        Adds an account holder IBAN to the account.

        Parameters
        ----------
        account_holder_iban (IbanNumber): The account holder IBAN to add. Can be an IbanNumber object or a string.

        Returns
        -------
        Account: The updated account.

        """
        if isinstance(account_holder_iban, str):
            account_holder_iban = IbanNumber(iban_number=account_holder_iban)
        self.account_holder_iban = account_holder_iban.get()
        return self

    def add_emandate(self: "Account", emandate: str) -> "Account":
        """
        Adds an e-mandate to the account.

        Parameters
        ----------
        emandate (str): The e-mandate to add.

        Returns
        -------
        Account: The updated account.

        """
        self.emandate = emandate
        return self
