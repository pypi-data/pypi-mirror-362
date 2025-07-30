# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class Issuer(RequestModel):
    """
    Represents an Issuer in the MultiSafepay API.

    Attributes
    ----------
    issuer_id (Optional[str]): The ID of the issuer.

    """

    issuer_id: Optional[str]

    def add_issuer_id(self: "Issuer", issuer_id: str) -> "Issuer":
        """
        Adds an issuer ID to the Issuer object.

        Parameters
        ----------
        issuer_id (str): The ID of the issuer to be added.

        Returns
        -------
        Issuer: The updated Issuer object.

        """
        self.issuer_id = issuer_id
        return self
