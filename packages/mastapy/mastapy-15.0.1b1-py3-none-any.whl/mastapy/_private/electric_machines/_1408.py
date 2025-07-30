"""IndividualConductorSpecificationSource"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_INDIVIDUAL_CONDUCTOR_SPECIFICATION_SOURCE = python_net_import(
    "SMT.MastaAPI.ElectricMachines", "IndividualConductorSpecificationSource"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="IndividualConductorSpecificationSource")
    CastSelf = TypeVar(
        "CastSelf",
        bound="IndividualConductorSpecificationSource._Cast_IndividualConductorSpecificationSource",
    )


__docformat__ = "restructuredtext en"
__all__ = ("IndividualConductorSpecificationSource",)


class IndividualConductorSpecificationSource(Enum):
    """IndividualConductorSpecificationSource

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _INDIVIDUAL_CONDUCTOR_SPECIFICATION_SOURCE

    FROM_WINDING_SPECIFICATION = 0
    FROM_CAD_GEOMETRY = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


IndividualConductorSpecificationSource.__setattr__ = __enum_setattr
IndividualConductorSpecificationSource.__delattr__ = __enum_delattr
