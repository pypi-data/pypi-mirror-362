# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from pydantic import BaseModel


class Version(BaseModel):
    """
    A class to represent the version information of a plugin and SDK.

    Attributes
    ----------
    plugin_version (Optional[str]): The version of the plugin, default is "unknown".

    """

    plugin_version: Optional[str] = "unknown"

    def get_plugin_version(self: "Version") -> str:
        """
        Get the plugin version.

        Returns
        -------
        str: The plugin version.

        """
        return self.plugin_version

    def set_plugin_version(self: "Version", version: Optional[str]) -> None:
        """
        Set the plugin version.

        Parameters
        ----------
        version (Optional[str]): The version to set for the plugin.

        """
        self.plugin_version = version

    def get_version(self: "Version") -> Optional[str]:
        """
        Get the combined version information of the plugin and SDK.

        Returns
        -------
        Optional[str]: The combined version information in the format "Plugin {plugin_version}; Python-Sdk {sdk_version}".

        Raises
        ------
        MissingPluginVersionException: If the plugin version is "unknown".

        """
        return f"Plugin {self.plugin_version}"
