# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.request_model import RequestModel


class PaymentOptions(RequestModel):
    """
    Represents payment options with various optional fields.

    Attributes
    ----------
    notification_url (Optional[str]): The URL for notifications.
    settings (Optional[dict]): A dictionary of settings.
    notification_method (Optional[str]): The method for notifications.
    redirect_url (Optional[str]): The URL for redirection.
    cancel_url (Optional[str]): The URL for cancellation.
    close_window (Optional[bool]): Whether to close the window

    """

    notification_url: Optional[str]
    settings: Optional[dict]
    notification_method: Optional[str]
    redirect_url: Optional[str]
    cancel_url: Optional[str]
    close_window: Optional[bool]

    def add_notification_url(
        self: "PaymentOptions",
        notification_url: str,
    ) -> "PaymentOptions":
        """
        Adds the notification URL to the PaymentOptions object.

        Parameters
        ----------
        notification_url (str): The URL for notifications.

        Returns
        -------
        PaymentOptions: The updated PaymentOptions object.

        """
        self.notification_url = notification_url
        return self

    def add_settings(
        self: "PaymentOptions",
        settings: list,
    ) -> "PaymentOptions":
        """
        Adds the settings to the PaymentOptions object.

        Parameters
        ----------
        settings (list): A list of settings.

        Returns
        -------
        PaymentOptions: The updated PaymentOptions object.

        """
        self.settings = settings
        return self

    def add_notification_method(
        self: "PaymentOptions",
        notification_method: str = "POST",
    ) -> "PaymentOptions":
        """
        Adds the notification method to the PaymentOptions object.

        Parameters
        ----------
        notification_method (str): The method for notifications, either "GET" or "POST".

        Raises
        ------
        InvalidArgumentException: If the notification method is not "GET" or "POST".

        Returns
        -------
        PaymentOptions: The updated PaymentOptions object.

        """
        if notification_method not in ["GET", "POST"]:
            raise InvalidArgumentException(
                'Notification method can only be "GET" or "POST"',
            )
        self.notification_method = notification_method
        return self

    def add_redirect_url(
        self: "PaymentOptions",
        redirect_url: str,
    ) -> "PaymentOptions":
        """
        Adds the redirect URL to the PaymentOptions object.

        Parameters
        ----------
        redirect_url (str): The URL for redirection.

        Returns
        -------
        PaymentOptions: The updated PaymentOptions object.

        """
        self.redirect_url = redirect_url
        return self

    def add_cancel_url(
        self: "PaymentOptions",
        cancel_url: str,
    ) -> "PaymentOptions":
        """
        Adds the cancel URL to the PaymentOptions object.

        Parameters
        ----------
        cancel_url (str): The URL for cancellation.

        Returns
        -------
        PaymentOptions: The updated PaymentOptions object.

        """
        self.cancel_url = cancel_url
        return self

    def add_close_window(
        self: "PaymentOptions",
        close_window: bool,
    ) -> "PaymentOptions":
        """
        Adds the close window option to the PaymentOptions object.

        Parameters
        ----------
        close_window (bool): Whether to close the window.

        Returns
        -------
        PaymentOptions: The updated PaymentOptions object.

        """
        self.close_window = close_window
        return self

    def is_close_window(self: "PaymentOptions") -> bool:
        """
        Checks if the close window option is set.

        Returns
        -------
        bool: True if the close window option is set, False otherwise.

        """
        return self.close_window
