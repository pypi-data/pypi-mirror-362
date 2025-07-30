# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.model.inmutable_model import InmutableModel


class BankAccount(InmutableModel):
    """
    A class to represent a Bank Account.

    Attributes
    ----------
    bank_account (str): The bank account number as a string.

    """

    bank_account: str

    def get(self: "BankAccount") -> str:
        """
        Get the bank account number.

        Returns
        -------
        str: The bank account number.

        """
        return self.bank_account
