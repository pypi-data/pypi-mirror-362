# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Optional

from multisafepay.model.request_model import RequestModel


class Description(RequestModel):
    """
    A class to represent a description, inheriting from RequestModel.

    Attributes
    ----------
    description (Optional[str]): The description text.

    """

    description: Optional[str]

    def get(self: "Description") -> Optional[str]:
        """
        Get the description text.

        Returns
        -------
        Optional[str]: The description text if set, otherwise None.

        """
        return self.description

    def add_description(
        self: "Description",
        description: Optional[str],
    ) -> "Description":
        """
        Add a description text.

        Parameters
        ----------
        description (Optional[str]): The description text to add.

        Returns
        -------
        Description: The updated Description instance.

        """
        self.description = description
        return self

    @staticmethod
    def strip_tags(text: str) -> str:
        """
        Remove HTML tags from a given text.

        Parameters
        ----------
        text (str): The text from which to remove HTML tags.

        Returns
        -------
        str: The text without HTML tags.

        """
        import re

        return re.sub(r"<[^>]*>", "", text)

    @staticmethod
    def from_text(description: str) -> "Description":
        """
        Create a Description instance from a text.

        Parameters
        ----------
        description (str): The description text.

        Returns
        -------
        Description: A new Description instance with the provided text.

        """
        return Description().add_description(description)
