# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class CaptureRequest(RequestModel):
    """
    A class to represent a capture request.

    Attributes
    ----------
    status (Optional[str]): The status of the capture request.
    reason (Optional[str]): The reason for the capture request.

    """

    status: Optional[str]
    reason: Optional[str]

    def add_status(self: "CaptureRequest", status: str) -> "CaptureRequest":
        """
        Add a status to the capture request.

        Parameters
        ----------
        status (str): The status to be added.

        Returns
        -------
        CaptureRequest: The instance of the capture request with the updated status.

        """
        self.status = status
        return self

    def add_reason(self: "CaptureRequest", reason: str) -> "CaptureRequest":
        """
        Add a reason to the capture request.

        Parameters
        ----------
        reason (str): The reason to be added.

        Returns
        -------
        CaptureRequest: The instance of the capture request with the updated reason.

        """
        self.reason = reason
        return self
