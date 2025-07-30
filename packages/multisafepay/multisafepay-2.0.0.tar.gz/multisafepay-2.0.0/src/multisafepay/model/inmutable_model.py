# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from pydantic.main import BaseModel


class InmutableModel(BaseModel):
    """
    A base model class that extends Pydantic's BaseModel.

    This class is immutable, meaning its attributes cannot be changed after initialization.
    """

    class Config:
        """
        Configuration for the InmutableModel class.

        Attributes
        ----------
        allow_mutation (bool):
            Specifies whether mutation of model attributes is allowed. Set to False to make the model immutable.

        """

        allow_mutation = False
