# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class Wallet(RequestModel):
    """
    Represents a Wallet in the MultiSafepay API.

    Attributes
    ----------
    payment_token (Optional[str]): The payment token

    """

    payment_token: Optional[str]

    def add_payment_token(self: "Wallet", payment_token: str) -> "Wallet":
        """
        Adds the payment token to the Wallet object.

        Parameters
        ----------
        payment_token (str): The payment token to be added.

        Returns
        -------
        Wallet: The updated Wallet object.

        """
        self.payment_token = payment_token
        return self
