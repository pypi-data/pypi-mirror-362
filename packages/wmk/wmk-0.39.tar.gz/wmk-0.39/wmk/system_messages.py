# Automatically generated file from a JSON schema
from typing import Literal, TypedDict, Union

from typing_extensions import Required


class PlayerConnected(TypedDict, total=False):
    """
    PlayerConnected.

    Visitor connected to the world
    """

    type: Required[Literal["PlayerConnected"]]
    """


    Required property
    """

    name: str
    """ Name of the visitor """

    playerId: str
    """ ID of the visitor """


class PlayerDisconnected(TypedDict, total=False):
    """
    PlayerDisconnected.

    Visitor disconnected from the world
    """

    type: Required[Literal["PlayerConnected"]]
    """


    Required property
    """

    name: str
    """ Name of the visitor """

    playerId: str
    """ ID of the visitor """


SystemMessages = Union["PlayerConnected", "PlayerDisconnected"]
"""
Aggregation type: anyOf
Subtype: "PlayerConnected", "PlayerDisconnected"
"""
