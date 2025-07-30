"""BearingElementOrbitModel"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEARING_ELEMENT_ORBIT_MODEL = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses",
    "BearingElementOrbitModel",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BearingElementOrbitModel")
    CastSelf = TypeVar(
        "CastSelf", bound="BearingElementOrbitModel._Cast_BearingElementOrbitModel"
    )


__docformat__ = "restructuredtext en"
__all__ = ("BearingElementOrbitModel",)


class BearingElementOrbitModel(Enum):
    """BearingElementOrbitModel

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEARING_ELEMENT_ORBIT_MODEL

    FIXED_ANGLE = 0
    NOMINAL_CONTACT_ANGLE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BearingElementOrbitModel.__setattr__ = __enum_setattr
BearingElementOrbitModel.__delattr__ = __enum_delattr
