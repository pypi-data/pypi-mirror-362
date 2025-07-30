# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel


class PaymentDetails(ResponseModel):
    """
    Represents the details of a payment, including various identifiers and transaction information.

    Attributes
    ----------
    account_holder_name (Optional[str]): The name of the account holder.
    account_id (Optional[str]): The ID of the account.
    collecting_flow (Optional[str]): The collecting flow.
    external_transaction_id (Optional[str]): The external transaction ID.
    recurring_flow (Optional[str]): The recurring flow.
    recurring_id (Optional[str]): The recurring ID.
    recurring_model (Optional[str]): The recurring model.
    type (Optional[str]): The type of payment.
    acquirer_reference_number (Optional[str]): The acquirer reference number.
    authorization_code (Optional[str]): The authorization code.
    card_acceptor_id (Optional[str]): The card acceptor ID.
    card_acceptor_location (Optional[str]): The card acceptor location.
    card_acceptor_name (Optional[str]): The card acceptor name.
    card_entry_mode (Optional[str]): The card entry mode.
    card_expiry_date (Optional[str]): The card expiry date.
    card_funding (Optional[str]): The card funding.
    issuer_bin (Optional[str]): The issuer BIN.
    last4 (Optional[str]): The last 4 digits of the card.
    mcc (Optional[str]): The merchant category code.
    response_code (Optional[str]): The response code.
    scheme_reference_id (Optional[str]): The scheme reference ID.

    """

    account_holder_name: Optional[str]
    account_id: Optional[str]
    collecting_flow: Optional[str]
    external_transaction_id: Optional[str]
    recurring_flow: Optional[str]
    recurring_id: Optional[str]
    recurring_model: Optional[str]
    type: Optional[str]
    acquirer_reference_number: Optional[str]
    authorization_code: Optional[str]
    card_acceptor_id: Optional[str]
    card_acceptor_location: Optional[str]
    card_acceptor_name: Optional[str]
    card_entry_mode: Optional[str]
    card_expiry_date: Optional[str]
    card_funding: Optional[str]
    issuer_bin: Optional[str]
    last4: Optional[str]
    mcc: Optional[str]
    response_code: Optional[str]
    scheme_reference_id: Optional[str]

    @staticmethod
    def from_dict(d: Optional[dict]) -> Optional["PaymentDetails"]:
        """
        Creates a PaymentDetails instance from a dictionary.

        Parameters
        ----------
        d (Optional[dict]): A dictionary containing the payment details data.

        Returns
        -------
        Optional[PaymentDetails]:
            An instance of PaymentDetails with the data from the dictionary, or None if the
            input is None.

        """
        if d is None:
            return None
        return PaymentDetails(**d)
