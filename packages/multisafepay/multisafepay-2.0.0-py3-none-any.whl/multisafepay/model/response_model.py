# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from abc import abstractmethod
from typing import Optional

from pydantic import BaseModel


class ResponseModel(BaseModel):
    """
    A base model class for response models that extends Pydantic's BaseModel.

    This class is immutable and allows extra fields to be included in the model.

    """

    class Config:
        """
        Configuration for the ResponseModel class.

        Attributes
        ----------
        allow_mutation (bool): Specifies whether mutation of model attributes is allowed.
            Set to False to make the model immutable.
        extra (str): Specifies how to handle extra fields. Set to "allow" to include extra fields.

        """

        allow_mutation = False
        extra = "allow"

    @staticmethod
    @abstractmethod
    def from_dict(d: dict) -> Optional["ResponseModel"]:
        """
        Create a model instance from a dictionary.

        Parameters
        ----------
        d (dict): The dictionary to create the model from.

        Returns
        -------
        Optional[ResponseModel]: The created model instance or None if the dictionary is invalid.

        """
