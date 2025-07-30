"""StressResultsType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_STRESS_RESULTS_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "StressResultsType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="StressResultsType")
    CastSelf = TypeVar("CastSelf", bound="StressResultsType._Cast_StressResultsType")


__docformat__ = "restructuredtext en"
__all__ = ("StressResultsType",)


class StressResultsType(Enum):
    """StressResultsType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _STRESS_RESULTS_TYPE

    MAXIMUM_TENSILE_PRINCIPAL_STRESS = 0
    VON_MISES_STRESS = 1
    X_COMPONENT = 2
    Y_COMPONENT = 3
    Z_COMPONENT = 4
    XY_SHEAR_STRESS = 5
    YZ_SHEAR_STRESS = 6
    XZ_SHEAR_STRESS = 7
    _1ST_PRINCIPAL_STRESS = 8
    _2ND_PRINCIPAL_STRESS = 9
    _3RD_PRINCIPAL_STRESS = 10
    STRESS_INTENSITY = 11


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


StressResultsType.__setattr__ = __enum_setattr
StressResultsType.__delattr__ = __enum_delattr
