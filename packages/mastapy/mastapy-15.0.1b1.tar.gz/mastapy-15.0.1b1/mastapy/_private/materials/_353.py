"""LubricantViscosityClassification"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_LUBRICANT_VISCOSITY_CLASSIFICATION = python_net_import(
    "SMT.MastaAPI.Materials", "LubricantViscosityClassification"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="LubricantViscosityClassification")
    CastSelf = TypeVar(
        "CastSelf",
        bound="LubricantViscosityClassification._Cast_LubricantViscosityClassification",
    )


__docformat__ = "restructuredtext en"
__all__ = ("LubricantViscosityClassification",)


class LubricantViscosityClassification(Enum):
    """LubricantViscosityClassification

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _LUBRICANT_VISCOSITY_CLASSIFICATION

    ISO = 0
    AGMA = 1
    SAE = 2
    USERSPECIFIED = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


LubricantViscosityClassification.__setattr__ = __enum_setattr
LubricantViscosityClassification.__delattr__ = __enum_delattr
