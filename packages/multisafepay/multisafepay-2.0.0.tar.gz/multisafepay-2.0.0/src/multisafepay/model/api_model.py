# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from abc import abstractmethod

from multisafepay.model.extra_model import ExtraModel
from multisafepay.model.response_model import ResponseModel
from multisafepay.util.dict_utils import remove_null_recursive


class ApiModel(ExtraModel):
    """
    A base class for API models that extends ExtraModel.

    This class provides a method to convert the model to a dictionary
    and an abstract method to create a model from a dictionary.

    """

    class Config:
        """
        Configuration for the ApiModel class.

        Attributes
        ----------
        extra (str):
            Specifies how to handle extra fields. Set to "allow" to include extra fields.

        """

        extra = "allow"

    def to_dict(self: "ApiModel") -> dict:
        """
        Convert the model to a dictionary, removing null values recursively.

        Returns
        -------
        dict: The dictionary representation of the model with null values removed.

        """
        return remove_null_recursive(self.dict())

    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> "ResponseModel":
        """
        Create a model instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary to create the model from.

        Returns
        -------
        ResponseModel: The created model instance.

        """
