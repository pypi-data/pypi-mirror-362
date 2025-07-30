"""ComplexPartDisplayOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_COMPLEX_PART_DISPLAY_OPTION = python_net_import(
    "SMT.MastaAPI.MathUtility", "ComplexPartDisplayOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ComplexPartDisplayOption")
    CastSelf = TypeVar(
        "CastSelf", bound="ComplexPartDisplayOption._Cast_ComplexPartDisplayOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ComplexPartDisplayOption",)


class ComplexPartDisplayOption(Enum):
    """ComplexPartDisplayOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _COMPLEX_PART_DISPLAY_OPTION

    AMPLITUDE = 0
    PEAKTOPEAK_AMPLITUDE = 1
    RMS_AMPLITUDE = 2
    PHASE = 3
    REAL = 4
    IMAGINARY = 5


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ComplexPartDisplayOption.__setattr__ = __enum_setattr
ComplexPartDisplayOption.__delattr__ = __enum_delattr
