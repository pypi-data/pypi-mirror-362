# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.response_model import ResponseModel

ALLOWED_GATEWAY_CODES = ["mybank"]


class Issuer(ResponseModel):
    """
    A class representing an issuer.

    Attributes
    ----------
    gateway_code (Optional[str]): The gateway code.
    code (Optional[str]): The issuer code.
    description (Optional[str]): The issuer description.

    """

    gateway_code: Optional[str]
    code: Optional[str]
    description: Optional[str]

    @staticmethod
    def from_dict(d: dict) -> Optional["Issuer"]:
        """
        Create an Issuer instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary containing issuer data.

        Returns
        -------
        Optional[Issuer]: An Issuer instance if the dictionary is not None, otherwise None.

        """
        if d is None:
            return None
        return Issuer(**d)
