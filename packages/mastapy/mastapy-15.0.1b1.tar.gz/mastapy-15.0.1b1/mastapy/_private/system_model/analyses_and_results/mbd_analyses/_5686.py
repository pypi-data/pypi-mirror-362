"""ClutchSpringType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CLUTCH_SPRING_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses", "ClutchSpringType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ClutchSpringType")
    CastSelf = TypeVar("CastSelf", bound="ClutchSpringType._Cast_ClutchSpringType")


__docformat__ = "restructuredtext en"
__all__ = ("ClutchSpringType",)


class ClutchSpringType(Enum):
    """ClutchSpringType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CLUTCH_SPRING_TYPE

    NONE = 0
    SPRUNG_APART = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ClutchSpringType.__setattr__ = __enum_setattr
ClutchSpringType.__delattr__ = __enum_delattr
