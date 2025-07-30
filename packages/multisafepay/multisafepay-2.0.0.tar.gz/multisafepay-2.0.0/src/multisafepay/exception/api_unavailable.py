# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from multisafepay.exception.api import ApiException


class ApiUnavailableException(ApiException):
    """
    Exception raised when the API is unavailable.

    This exception is raised when the MultiSafepay API is not reachable or unavailable.
    """
