"""ElementPropertiesShellWallType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELEMENT_PROPERTIES_SHELL_WALL_TYPE = python_net_import(
    "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums",
    "ElementPropertiesShellWallType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElementPropertiesShellWallType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElementPropertiesShellWallType._Cast_ElementPropertiesShellWallType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElementPropertiesShellWallType",)


class ElementPropertiesShellWallType(Enum):
    """ElementPropertiesShellWallType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELEMENT_PROPERTIES_SHELL_WALL_TYPE

    MONOCOQUE = 0
    LAMINATED = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElementPropertiesShellWallType.__setattr__ = __enum_setattr
ElementPropertiesShellWallType.__delattr__ = __enum_delattr
