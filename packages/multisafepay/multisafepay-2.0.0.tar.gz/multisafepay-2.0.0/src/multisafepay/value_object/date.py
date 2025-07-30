# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from datetime import datetime

from multisafepay.exception.invalid_argument import InvalidArgumentException
from multisafepay.model.inmutable_model import InmutableModel


class Date(InmutableModel):
    """
    A class to represent a Date.

    Attributes
    ----------
    timestamp (float): The timestamp value of the date.
    str_date (str): The date as a string.

    """

    timestamp: float
    str_date: str

    def __init__(self: "Date", date: str) -> None:
        """
        Initialize a Date object.

        Parameters
        ----------
        date (str): The date string to initialize the object with.

        Raises
        ------
        InvalidArgumentException: If the date string is in an invalid format.

        """
        try:
            if "T" in date:
                timestamp = datetime.fromisoformat(date).timestamp()
            else:
                timestamp = datetime.strptime(date, "%Y-%m-%d").timestamp()
            super().__init__(timestamp=timestamp, str_date=date)
        except ValueError as e:
            raise InvalidArgumentException(
                f'Value "{date}" is an invalid date format',
            ) from e

    def get(self: "Date", date_format: str = "%Y-%m-%d") -> str:
        """
        Get the date as a string in the specified format.

        Parameters
        ----------
        date_format Optional[str]: The format to return the date in (default is "%Y-%m-%d").

        Returns
        -------
        str: The date as a string in the specified format.

        """
        return datetime.fromtimestamp(self.timestamp).strftime(date_format)
