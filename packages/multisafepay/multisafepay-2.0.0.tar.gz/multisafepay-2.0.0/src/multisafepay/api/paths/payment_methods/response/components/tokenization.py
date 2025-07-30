# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.api.paths.payment_methods.response.components.tokenizations.models import (
    Models,
)
from multisafepay.model.response_model import ResponseModel


class Tokenization(ResponseModel):
    """
    A class representing tokenization support information.

    Attributes
    ----------
    is_enabled (Optional[bool]): Whether tokenization is enabled.
    models (Optional[Models]): The models associated with tokenization.

    """

    is_enabled: Optional[bool]
    models: Optional[Models]

    @staticmethod
    def from_dict(d: dict) -> Optional["Tokenization"]:
        """
        Create a Tokenization instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the tokenization data.

        Returns
        -------
        Optional[Tokenization]: The Tokenization instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return Tokenization(**d)
