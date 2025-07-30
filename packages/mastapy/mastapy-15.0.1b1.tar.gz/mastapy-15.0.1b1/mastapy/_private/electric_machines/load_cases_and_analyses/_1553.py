"""OperatingPointsSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_OPERATING_POINTS_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses",
    "OperatingPointsSpecificationMethod",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="OperatingPointsSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="OperatingPointsSpecificationMethod._Cast_OperatingPointsSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("OperatingPointsSpecificationMethod",)


class OperatingPointsSpecificationMethod(Enum):
    """OperatingPointsSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _OPERATING_POINTS_SPECIFICATION_METHOD

    USERDEFINED = 0
    ALONG_MAXIMUM_SPEED_TORQUE_CURVE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


OperatingPointsSpecificationMethod.__setattr__ = __enum_setattr
OperatingPointsSpecificationMethod.__delattr__ = __enum_delattr
