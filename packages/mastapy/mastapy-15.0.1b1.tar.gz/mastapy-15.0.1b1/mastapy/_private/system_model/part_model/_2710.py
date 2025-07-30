"""UnbalancedMassInclusionOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_UNBALANCED_MASS_INCLUSION_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel", "UnbalancedMassInclusionOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="UnbalancedMassInclusionOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="UnbalancedMassInclusionOption._Cast_UnbalancedMassInclusionOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("UnbalancedMassInclusionOption",)


class UnbalancedMassInclusionOption(Enum):
    """UnbalancedMassInclusionOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _UNBALANCED_MASS_INCLUSION_OPTION

    ALL_ANALYSES = 0
    ADVANCED_SYSTEM_DEFLECTION_AND_DYNAMICS = 1
    DYNAMIC_ANALYSES = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


UnbalancedMassInclusionOption.__setattr__ = __enum_setattr
UnbalancedMassInclusionOption.__delattr__ = __enum_delattr
