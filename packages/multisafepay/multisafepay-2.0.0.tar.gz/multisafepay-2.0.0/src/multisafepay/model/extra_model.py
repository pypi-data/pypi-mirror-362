# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from pydantic import BaseModel


class ExtraModel(BaseModel):
    """
    A base model class that extends Pydantic's BaseModel.

    This class allows extra fields to be included in the model.

    """

    class Config:
        """
        Configuration for the ExtraModel class.

        Attributes
        ----------
        extra (str):
            Specifies how to handle extra fields. Set to "allow" to include extra fields.

        """

        extra = "allow"
