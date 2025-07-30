# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.model.request_model import RequestModel


class SecondChance(RequestModel):
    """
    Represents the SecondChance component with an option to send an email.

    Attributes
    ----------
    send_email (bool): Whether to send an email.

    """

    send_email: bool

    def add_send_email(
        self: "SecondChance",
        send_email: bool,
    ) -> "SecondChance":
        """
        Adds the send_email option to the SecondChance object.

        Parameters
        ----------
        send_email (bool): Whether to send an email.

        Returns
        -------
        SecondChance: The updated SecondChance object.

        """
        self.send_email = send_email
        return self
