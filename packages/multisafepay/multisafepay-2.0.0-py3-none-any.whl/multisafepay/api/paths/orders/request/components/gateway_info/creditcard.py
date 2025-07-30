# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional, Union

from multisafepay.model.request_model import RequestModel
from multisafepay.value_object.creditcard.card_number import CardNumber
from multisafepay.value_object.creditcard.cvc import Cvc


class Creditcard(RequestModel):
    """
    Represents a credit card with various attributes.

    Attributes
    ----------
    card_number (Optional[str]): The card number.
    card_holder_name (Optional[str]): The card holder name.
    card_expiry_date (Optional[str]): The card expiry date.
    cvc (Optional[str]): The CVC code.
    flexible_3d (Optional[bool]): The flexible 3D secure option.
    term_url (Optional[str]): The term URL.

    """

    card_number: Optional[str]
    card_holder_name: Optional[str]
    card_expiry_date: Optional[str]
    cvc: Optional[str]
    flexible_3d: Optional[bool]
    term_url: Optional[str]

    def add_card_number(
        self: "Creditcard",
        card_number: Union[CardNumber, str],
    ) -> "Creditcard":
        """
        Adds a card number to the credit card.

        Parameters
        ----------
        card_number (CardNumber | str): The card number to add. Can be a CardNumber object or a string.

        Returns
        -------
        Creditcard: The updated credit card.

        """
        if isinstance(card_number, str):
            card_number = CardNumber(card_number=card_number)
        self.card_number = card_number.get_card_number()
        return self

    def add_card_holder_name(
        self: "Creditcard",
        card_holder_name: str,
    ) -> "Creditcard":
        """
        Adds a card holder name to the credit card.

        Parameters
        ----------
        card_holder_name (str): The card holder name to add.

        Returns
        -------
        Creditcard: The updated credit card.

        """
        self.card_holder_name = card_holder_name
        return self

    def add_card_expiry_date(
        self: "Creditcard",
        card_expiry_date: str,
    ) -> "Creditcard":
        """
        Adds a card expiry date to the credit card.

        Parameters
        ----------
        card_expiry_date (str): The card expiry date to add.

        Returns
        -------
        Creditcard: The updated credit card.

        """
        self.card_expiry_date = card_expiry_date
        return self

    def add_cvc(self: "Creditcard", cvc: Union[Cvc, str]) -> "Creditcard":
        """
        Adds a CVC code to the credit card.

        Parameters
        ----------
        cvc (Cvc): The CVC code to add.

        Returns
        -------
        Creditcard: The updated credit card.

        """
        if isinstance(cvc, str):
            cvc = Cvc(cvc=cvc)
        self.cvc = cvc.get()
        return self

    def add_flexible_3d(self: "Creditcard", flexible_3d: bool) -> "Creditcard":
        """
        Adds a flexible 3D secure option to the credit card.

        Parameters
        ----------
        flexible_3d (bool): The flexible 3D secure option to add.

        Returns
        -------
        Creditcard: The updated credit card.

        """
        self.flexible_3d = flexible_3d
        return self

    def add_term_url(self: "Creditcard", term_url: str) -> "Creditcard":
        """
        Adds a term URL to the credit card.

        Parameters
        ----------
        term_url (str): The term URL to add.

        Returns
        -------
        Creditcard: The updated credit card.

        """
        self.term_url = term_url
        return self
