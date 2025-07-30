# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.util.dict_utils import remove_null_recursive
from pydantic import BaseModel


class RequestModel(BaseModel):
    """
    A base model class for request models that extends Pydantic's BaseModel.

    This class allows extra fields to be included in the model.
    """

    class Config:
        """
        Configuration for the RequestModel class.

        Attributes
        ----------
        extra (str): Specifies how to handle extra fields. Set to "allow" to include extra fields.

        """

        extra = "allow"

    def to_dict(self: "RequestModel") -> dict:
        """
        Convert the model to a dictionary, removing null values recursively.

        Returns
        -------
        dict: The dictionary representation of the model with null values removed.

        """
        return remove_null_recursive(input_data=self.dict())
