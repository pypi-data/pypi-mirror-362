# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from abc import ABC
from typing import Optional

from multisafepay.api.paths.payment_methods.response.components.qr import Qr
from multisafepay.model.response_model import ResponseModel


class App(ResponseModel, ABC):
    """
    A class representing an application with optional QR code, enabled status, and fields status.

    Attributes
    ----------
    is_enabled (Optional[bool]): The enabled status of the application.
    has_fields (Optional[bool]): The fields status of the application.
    qr (Optional[Qr]): The QR code of the application.

    """

    is_enabled: Optional[bool]
    has_fields: Optional[bool]
    qr: Optional[Qr]

    @staticmethod
    def from_dict(d: dict) -> Optional["App"]:
        """
        Create an App instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the application data.

        Returns
        -------
        Optional[App]: The App instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return App(**d)
