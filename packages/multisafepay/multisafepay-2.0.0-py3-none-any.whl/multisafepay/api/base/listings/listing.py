# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.

from typing import Any, Dict, Generic, Iterator, List, TypeVar

from pydantic.main import BaseModel

T = TypeVar("T")


class Listing(Generic[T], BaseModel):
    """
    A generic class to represent a listing of items.

    Attributes
    ----------
    data (List[T]): A list of items of type T.

    """

    data: List[T]

    def __init__(
        self: "Listing",
        data: List[Any],
        class_type: type,
        **kwargs: Dict[str, Any],
    ) -> None:
        """
        Initialize the Listing with data and a class type.

        Parameters
        ----------
        data (List[Any]): A list of data to be converted into items of type T.
        class_type (type): The class type to convert the data into.
        **kwargs: Additional keyword arguments to pass to the class type constructor.

        """
        elements: List[T] = []
        if data:
            for item_data in data:
                if item_data:
                    if kwargs:
                        elements.append(class_type(**item_data, **kwargs))
                    elif isinstance(item_data, dict):
                        elements.append(class_type(**item_data))
                    elif isinstance(item_data, class_type):
                        elements.append(item_data)

        super().__init__(data=elements)

    def __iter__(self: "Listing") -> Iterator[T]:
        """
        Return an iterator over the items in the listing.

        Returns
        -------
        Iterator[T]: An iterator over the items in the listing.

        """
        return iter(self.data)

    def __getitem__(self: "Listing", index: int) -> T:
        """
        Get an item by index.

        Parameters
        ----------
        index (int): The index of the item to retrieve.

        Returns
        -------
        T: The item at the specified index.

        """
        return self.data[index]

    def __len__(self: "Listing") -> int:
        """
        Get the number of items in the listing.

        Returns
        -------
        int: The number of items in the listing.

        """
        return len(self.data)

    def get_data(self: "Listing") -> List[T]:
        """
        Get the list of items in the listing.

        Returns
        -------
        List[T]: The list of items in the listing.

        """
        return self.data

    def append(self: "Listing", item: T) -> None:
        """
        Append an item to the listing.

        Parameters
        ----------
        item (T): The item to append to the listing.

        """
        self.data.append(item)
