"""DensitySpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DENSITY_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.Materials", "DensitySpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DensitySpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="DensitySpecificationMethod._Cast_DensitySpecificationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("DensitySpecificationMethod",)


class DensitySpecificationMethod(Enum):
    """DensitySpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DENSITY_SPECIFICATION_METHOD

    TEMPERATURE_INDEPENDENT_VALUE = 0
    TEMPERATURE_AND_VALUE_AT_TEMPERATURE_SPECIFIED = 1
    USERSPECIFIED_VS_TEMPERATURE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DensitySpecificationMethod.__setattr__ = __enum_setattr
DensitySpecificationMethod.__delattr__ = __enum_delattr
