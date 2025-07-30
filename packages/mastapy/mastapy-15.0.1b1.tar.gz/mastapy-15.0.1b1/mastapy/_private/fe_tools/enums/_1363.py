"""ElementPropertyClass"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELEMENT_PROPERTY_CLASS = python_net_import(
    "SMT.MastaAPI.FETools.Enums", "ElementPropertyClass"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementPropertyClass")
    CastSelf = TypeVar(
        "CastSelf", bound="ElementPropertyClass._Cast_ElementPropertyClass"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertyClass",)


class ElementPropertyClass(Enum):
    """ElementPropertyClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELEMENT_PROPERTY_CLASS

    UNDEFINED = 0
    SOLID = 1
    SHELL = 2
    MEMBRANE = 3
    BEAM = 4
    TRUSS = 5
    INFINITE = 6
    GAP = 7
    JOINT = 8
    SPRING_DASHPOT = 9
    RIGID = 10
    CONSTRAINT = 11
    PLOT = 12
    MASS = 13
    INTERFACE = 14
    SUPERELEMENT = 15


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElementPropertyClass.__setattr__ = __enum_setattr
ElementPropertyClass.__delattr__ = __enum_delattr
