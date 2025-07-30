"""DoeValueSpecificationOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_DOE_VALUE_SPECIFICATION_OPTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "DoeValueSpecificationOption",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="DoeValueSpecificationOption")
    CastSelf = TypeVar(
        "CastSelf",
        bound="DoeValueSpecificationOption._Cast_DoeValueSpecificationOption",
    )


__docformat__ = "restructuredtext en"
__all__ = ("DoeValueSpecificationOption",)


class DoeValueSpecificationOption(Enum):
    """DoeValueSpecificationOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _DOE_VALUE_SPECIFICATION_OPTION

    ABSOLUTE = 0
    ADDITIVE = 1
    NORMAL_DISTRIBUTION = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


DoeValueSpecificationOption.__setattr__ = __enum_setattr
DoeValueSpecificationOption.__delattr__ = __enum_delattr
