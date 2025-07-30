"""PropertySpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_PROPERTY_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.Utility.Enums", "PropertySpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="PropertySpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PropertySpecificationMethod._Cast_PropertySpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PropertySpecificationMethod",)


class PropertySpecificationMethod(Enum):
    """PropertySpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _PROPERTY_SPECIFICATION_METHOD

    CONSTANT = 0
    ONEDIMENSIONAL_LOOKUP_TABLE = 1
    TWODIMENSIONAL_LOOKUP_TABLE = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


PropertySpecificationMethod.__setattr__ = __enum_setattr
PropertySpecificationMethod.__delattr__ = __enum_delattr
