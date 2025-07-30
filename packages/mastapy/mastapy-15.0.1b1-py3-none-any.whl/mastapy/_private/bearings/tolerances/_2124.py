"""SupportMaterialSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SUPPORT_MATERIAL_SOURCE = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "SupportMaterialSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SupportMaterialSource")
    CastSelf = TypeVar(
        "CastSelf", bound="SupportMaterialSource._Cast_SupportMaterialSource"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SupportMaterialSource",)


class SupportMaterialSource(Enum):
    """SupportMaterialSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SUPPORT_MATERIAL_SOURCE

    SHAFT = 0
    DESIGN_HOUSING = 1
    FE_COMPONENT = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SupportMaterialSource.__setattr__ = __enum_setattr
SupportMaterialSource.__delattr__ = __enum_delattr
