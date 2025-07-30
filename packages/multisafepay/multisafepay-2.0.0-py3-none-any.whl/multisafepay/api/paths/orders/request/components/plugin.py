# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class Plugin(RequestModel):
    """
    Represents the details of a plugin with various optional fields.

    Attributes
    ----------
    plugin_version (Optional[str]): The version of the plugin.
    shop (Optional[str]): The name of the shop.
    shop_version (Optional[str]): The version of the shop.
    partner (Optional[str]): The partner associated with the plugin.
    shop_root_url (Optional[str]): The root URL of the shop.

    """

    plugin_version: Optional[str]
    shop: Optional[str]
    shop_version: Optional[str]
    partner: Optional[str]
    shop_root_url: Optional[str]

    def add_plugin_version(
        self: "Plugin",
        plugin_version: Optional[str],
    ) -> "Plugin":
        """
        Adds the plugin version to the Plugin object.

        Parameters
        ----------
        plugin_version (Optional[str]): The version of the plugin.

        Returns
        -------
        Plugin: The updated Plugin object.

        """
        self.plugin_version = plugin_version
        return self

    def add_shop(
        self: "Plugin",
        shop: Optional[str],
    ) -> "Plugin":
        """
        Adds the shop name to the Plugin object.

        Parameters
        ----------
        shop (Optional[str]): The name of the shop.

        Returns
        -------
        Plugin: The updated Plugin object.

        """
        self.shop = shop
        return self

    def add_shop_version(
        self: "Plugin",
        shop_version: Optional[str],
    ) -> "Plugin":
        """
        Adds the shop version to the Plugin object.

        Parameters
        ----------
        shop_version (Optional[str]): The version of the shop.

        Returns
        -------
        Plugin: The updated Plugin object.

        """
        self.shop_version = shop_version
        return self

    def add_partner(self: "Plugin", partner: Optional[str]) -> "Plugin":
        """
        Adds the partner to the Plugin object.

        Parameters
        ----------
        partner (Optional[str]): The partner associated with the plugin.

        Returns
        -------
        Plugin: The updated Plugin object.

        """
        self.partner = partner
        return self

    def add_shop_root_url(
        self: "Plugin",
        shop_root_url: Optional[str],
    ) -> "Plugin":
        """
        Adds the shop root URL to the Plugin object.

        Parameters
        ----------
        shop_root_url (Optional[str]): The root URL of the shop.

        Returns
        -------
        Plugin: The updated Plugin object.

        """
        self.shop_root_url = shop_root_url
        return self
