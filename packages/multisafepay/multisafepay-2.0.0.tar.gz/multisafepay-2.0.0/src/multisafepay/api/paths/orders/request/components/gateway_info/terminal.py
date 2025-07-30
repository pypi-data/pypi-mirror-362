# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class Terminal(RequestModel):
    """
    Represents a Terminal in the MultiSafepay API.

    Attributes
    ----------
    terminal_id (Optional[str]): The ID of the terminal.

    """

    terminal_id: Optional[str]

    def add_terminal_id(self: "Terminal", terminal_id: str) -> "Terminal":
        """
        Adds the terminal ID to the Terminal object.

        Parameters
        ----------
        terminal_id (str): The terminal ID to be added.

        Returns
        -------
        Terminal: The updated Terminal object.

        """
        self.terminal_id = terminal_id
        return self
