"""ContactPairConstrainedSurfaceType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CONTACT_PAIR_CONSTRAINED_SURFACE_TYPE = python_net_import(
    "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums",
    "ContactPairConstrainedSurfaceType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ContactPairConstrainedSurfaceType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ContactPairConstrainedSurfaceType._Cast_ContactPairConstrainedSurfaceType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ContactPairConstrainedSurfaceType",)


class ContactPairConstrainedSurfaceType(Enum):
    """ContactPairConstrainedSurfaceType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CONTACT_PAIR_CONSTRAINED_SURFACE_TYPE

    NONE = 0
    NODE = 1
    ELEMENT_EDGE = 2
    ELEMENT_FACE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ContactPairConstrainedSurfaceType.__setattr__ = __enum_setattr
ContactPairConstrainedSurfaceType.__delattr__ = __enum_delattr
