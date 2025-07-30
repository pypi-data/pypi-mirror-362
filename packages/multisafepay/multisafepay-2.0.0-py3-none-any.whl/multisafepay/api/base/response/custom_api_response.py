# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Any, Dict, Optional, Union

from multisafepay.api.base.response.api_response import ApiResponse


class CustomApiResponse(ApiResponse):
    """
    A custom API response class that extends the ApiResponse class and supports generic typing.

    Attributes
    ----------
    data: (Any) The data contained in the response

    """

    data: Optional[Union[dict, list]]

    def __init__(
        self: "CustomApiResponse",
        data: Optional[Union[dict, list]],
        **kwargs: Dict[str, Any],
    ) -> None:
        """
        Initialize the CustomApiResponse with optional data and additional keyword arguments.

        Parameters
        ----------
        data: (Any, optional) The data to be included in the response, by default None.
        **kwargs: Additional keyword arguments to be set as attributes of the response.

        """
        super().__init__(**kwargs)
        self.data = data
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_data(self: "CustomApiResponse") -> Optional[Union[dict, list]]:
        """
        Get the data contained in the response.

        Returns
        -------
        Any: The data contained in the response.

        """
        return self.data
