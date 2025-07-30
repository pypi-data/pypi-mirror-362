"""MaterialPropertyClass"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_MATERIAL_PROPERTY_CLASS = python_net_import(
    "SMT.MastaAPI.FETools.Enums", "MaterialPropertyClass"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="MaterialPropertyClass")
    CastSelf = TypeVar(
        "CastSelf", bound="MaterialPropertyClass._Cast_MaterialPropertyClass"
    )


__docformat__ = "restructuredtext en"
__all__ = ("MaterialPropertyClass",)


class MaterialPropertyClass(Enum):
    """MaterialPropertyClass

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _MATERIAL_PROPERTY_CLASS

    ISOTROPIC = 0
    ORTHOTROPIC = 2
    ANISOTROPIC = 3
    HYPERELASTIC = 4
    UNKNOWN_CLASS = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


MaterialPropertyClass.__setattr__ = __enum_setattr
MaterialPropertyClass.__delattr__ = __enum_delattr
