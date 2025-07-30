# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from abc import ABC
from typing import Optional

from multisafepay.api.paths.payment_methods.response.components.app import App
from multisafepay.model.response_model import ResponseModel


class Apps(ResponseModel, ABC):
    """
    A class representing a collection of applications with optional fast checkout and payment components.

    Attributes
    ----------
    fastcheckout (Optional[App]): The fast checkout application.
    payment_components (Optional[App]): The payment components application.

    """

    fastcheckout: Optional[App]
    payment_components: Optional[App]

    @staticmethod
    def from_dict(d: dict) -> Optional["Apps"]:
        """
        Create an Apps instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the applications data.

        Returns
        -------
        Optional[Apps]: The Apps instance or None if the dictionary is None.

        """
        if d is None:
            return None
        d_adapted = {}
        for key in d:
            if d[key] is not None:
                d_adapted[key] = App(**(d.get(key) or {}))
        return Apps(**d_adapted)
