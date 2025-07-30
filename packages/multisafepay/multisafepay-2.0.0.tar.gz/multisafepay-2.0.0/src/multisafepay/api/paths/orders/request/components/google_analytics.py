# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class GoogleAnalytics(RequestModel):
    """
    Represents Google Analytics information with an optional account ID.

    Attributes
    ----------
    account_id (Optional[str]): The Google Analytics account ID.

    """

    account_id: Optional[str]

    def add_account_id(
        self: "GoogleAnalytics",
        account_id: str,
    ) -> "GoogleAnalytics":
        """
        Adds the account ID to the Google Analytics information.

        Parameters
        ----------
        account_id (str): The Google Analytics account ID.

        Returns
        -------
        GoogleAnalytics: The updated GoogleAnalytics object.

        """
        self.account_id = account_id
        return self
