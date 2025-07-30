# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.api.base.abstract_manager import AbstractManager
from multisafepay.api.base.response.custom_api_response import (
    CustomApiResponse,
)
from multisafepay.api.paths.categories.response.category import Category
from multisafepay.client.client import Client
from multisafepay.util.message import MessageList, gen_could_not_created_msg


class CategoryManager(AbstractManager):
    """
    A manager class for handling category-related API requests.
    """

    def __init__(self: "CategoryManager", client: Client) -> None:
        """
        Initialize the CategoryManager with a client.

        Parameters
        ----------
        client (Client): The client used to make API requests.

        """
        super().__init__(client)

    def get_categories(self: "CategoryManager") -> CustomApiResponse:
        """
        Retrieve the list of categories.

        This method makes an API request to retrieve the list of categories and
        returns a CustomApiResponse object containing the response data.

        Returns
        -------
        CustomApiResponse: The response object containing the list of categories and any warnings.

        """
        response = self.client.create_get_request("json/categories")

        args: dict = {
            **response.dict(),
            "data": None,
        }

        if isinstance(response.get_body_data(), list):
            try:
                args["data"] = [
                    Category.from_dict(category)
                    for category in response.get_body_data().copy()
                ]
            except Exception as e:
                args["warnings"] = (
                    MessageList()
                    .add_message(str(e))
                    .add_message(gen_could_not_created_msg("Category"))
                    .get_messages()
                )

        return CustomApiResponse(**args)
