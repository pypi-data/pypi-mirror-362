"""OilSealMaterialType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OIL_SEAL_MATERIAL_TYPE = python_net_import(
    "SMT.MastaAPI.Materials.Efficiency", "OilSealMaterialType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OilSealMaterialType")
    CastSelf = TypeVar(
        "CastSelf", bound="OilSealMaterialType._Cast_OilSealMaterialType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("OilSealMaterialType",)


class OilSealMaterialType(Enum):
    """OilSealMaterialType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OIL_SEAL_MATERIAL_TYPE

    VITON = 0
    BUNAN = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OilSealMaterialType.__setattr__ = __enum_setattr
OilSealMaterialType.__delattr__ = __enum_delattr
