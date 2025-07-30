# Copyright (c) MultiSafepay, Inc. All rights reserved.

# This file is licensed under the Open Software License (OSL) version 3.0.
# For a copy of the license, see the LICENSE.txt file in the project root.

# See the DISCLAIMER.md file for disclaimer details.


from typing import Dict, Iterator, List

from pydantic import BaseModel, Field


class Message(BaseModel):
    """
    A class to represent a message.

    Attributes
    ----------
    message (Optional[str]): The message content as a string.

    """

    message: str


class MessageList(BaseModel):
    """
    A class to represent a list of messages.

    Attributes
    ----------
    __root__ (List[Message]): The root list containing Message objects.

    """

    __root__: List[Message] = Field(default_factory=list)

    def __iter__(self: "MessageList") -> Iterator[Message]:
        """
        Iterate over the messages in the list.

        Returns
        -------
        iterator: An iterator over the Message objects in the list.

        """
        return iter(self.__root__)

    def __getitem__(self: "MessageList", index: int) -> "Message":
        """
        Get a message by index.

        Parameters
        ----------
        index (int): The index of the message to retrieve.

        Returns
        -------
        Message: The Message object at the specified index.

        """
        return self.__root__[index]

    def __len__(self: "MessageList") -> int:
        """
        Get the number of messages in the list.

        Returns
        -------
        int: The number of messages in the list.

        """
        return len(self.__root__)

    def add_message(self: "MessageList", message: str) -> "MessageList":
        """
        Add a message to the list.

        Parameters
        ----------
        message (str): The message content to add.

        Returns
        -------
        MessageList: The updated message list.

        """
        self.__root__.append(Message(message=message))
        return self

    def get_messages(self: "MessageList") -> List[Dict]:
        """
        Get all messages in the list.

        Returns
        -------
        List[Dict]: A list of dictionaries representing the messages in the list.

        """
        return [msg.dict() for msg in self.__root__]


def __could_not_created_template(text: str) -> str:
    """
    Generate a template message for a failed object creation.

    Parameters
    ----------
    text (str): The name of the entity that could not be created.

    Returns
    -------
    str: The template message indicating the failure reason.

    """
    return f"Construction of the {text} object failed due to the structure received in body.data. Please review."


def gen_could_not_created_msg(entity: str) -> str:
    """
    Generate a message indicating that an entity could not be created.

    Parameters
    ----------
    entity (str): The name of the entity that could not be created.

    Returns
    -------
    str: The message indicating the failure reason.

    """
    return __could_not_created_template(entity)
