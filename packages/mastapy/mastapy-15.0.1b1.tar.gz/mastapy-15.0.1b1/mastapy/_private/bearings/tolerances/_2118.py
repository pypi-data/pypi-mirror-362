"""RadialSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_RADIAL_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.Bearings.Tolerances", "RadialSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="RadialSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf", bound="RadialSpecificationMethod._Cast_RadialSpecificationMethod"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RadialSpecificationMethod",)


class RadialSpecificationMethod(Enum):
    """RadialSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _RADIAL_SPECIFICATION_METHOD

    X_AND_Y = 0
    IN_DIRECTION_OF_ECCENTRICITY = 1
    IN_OPPOSITE_DIRECTION_TO_ECCENTRICITY = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


RadialSpecificationMethod.__setattr__ = __enum_setattr
RadialSpecificationMethod.__delattr__ = __enum_delattr
