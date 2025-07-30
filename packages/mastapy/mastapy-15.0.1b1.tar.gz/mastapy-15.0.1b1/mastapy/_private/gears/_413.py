"""CylindricalMisalignmentDataSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CYLINDRICAL_MISALIGNMENT_DATA_SOURCE = python_net_import(
    "SMT.MastaAPI.Gears", "CylindricalMisalignmentDataSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CylindricalMisalignmentDataSource")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalMisalignmentDataSource._Cast_CylindricalMisalignmentDataSource",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalMisalignmentDataSource",)


class CylindricalMisalignmentDataSource(Enum):
    """CylindricalMisalignmentDataSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CYLINDRICAL_MISALIGNMENT_DATA_SOURCE

    STANDARD = 0
    USERSPECIFIED = 1
    SYSTEM_DEFLECTION = 2
    ADVANCED_SYSTEM_DEFLECTION = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CylindricalMisalignmentDataSource.__setattr__ = __enum_setattr
CylindricalMisalignmentDataSource.__delattr__ = __enum_delattr
