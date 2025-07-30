"""LoadCaseType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LOAD_CASE_TYPE = python_net_import(
    "SMT.MastaAPI.ElectricMachines.LoadCasesAndAnalyses", "LoadCaseType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LoadCaseType")
    CastSelf = TypeVar("CastSelf", bound="LoadCaseType._Cast_LoadCaseType")


__docformat__ = "restructuredtext en"
__all__ = ("LoadCaseType",)


class LoadCaseType(Enum):
    """LoadCaseType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LOAD_CASE_TYPE

    SINGLE_OPERATING_POINT_WITHOUT_NONLINEAR_DQ_MODEL = 0
    SINGLE_OPERATING_POINT_WITH_NONLINEAR_DQ_MODEL = 1
    EFFICIENCY_MAP = 2
    MAXIMUM_SPEED_TORQUE_CURVE = 3
    DYNAMIC_FORCES = 4
    DYNAMIC_FORCES_WITHOUT_NONLINEAR_DQ_MODEL = 5
    MECHANICAL = 6


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LoadCaseType.__setattr__ = __enum_setattr
LoadCaseType.__delattr__ = __enum_delattr
