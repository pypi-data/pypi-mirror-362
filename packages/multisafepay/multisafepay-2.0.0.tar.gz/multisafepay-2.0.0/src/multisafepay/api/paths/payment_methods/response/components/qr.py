# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Optional

from multisafepay.model.response_model import ResponseModel


class Qr(ResponseModel):
    """
    A class representing QR code support information.

    Attributes
    ----------
    supported (Optional[bool]): Whether QR code is supported.

    """

    supported: Optional[bool]

    @staticmethod
    def from_dict(d: dict) -> Optional["Qr"]:
        """
        Create a Qr instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing the QR code support data.

        Returns
        -------
        Optional[Qr]: The Qr instance or None if the dictionary is None.

        """
        if d is None:
            return None
        return Qr(**d)
