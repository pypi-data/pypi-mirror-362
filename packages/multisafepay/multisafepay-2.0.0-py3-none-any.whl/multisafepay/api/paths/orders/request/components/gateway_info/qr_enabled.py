# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class QrEnabled(RequestModel):
    """
    Represents the QR Enabled status in the MultiSafepay API.

    Attributes
    ----------
    qr_enabled (Optional[bool]): The QR enabled status.

    """

    qr_enabled: Optional[bool]

    def add_qr_enabled(self: "QrEnabled", qr_enabled: bool) -> "QrEnabled":
        """
        Adds the QR enabled status to the QrEnabled object.

        Parameters
        ----------
        qr_enabled (bool): The QR enabled status to be added.

        Returns
        -------
        QrEnabled: The updated QrEnabled object.

        """
        self.qr_enabled = qr_enabled
        return self
