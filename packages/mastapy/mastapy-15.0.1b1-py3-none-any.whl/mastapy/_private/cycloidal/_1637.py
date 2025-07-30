"""CrowningSpecificationMethod"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CROWNING_SPECIFICATION_METHOD = python_net_import(
    "SMT.MastaAPI.Cycloidal", "CrowningSpecificationMethod"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="CrowningSpecificationMethod")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CrowningSpecificationMethod._Cast_CrowningSpecificationMethod",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CrowningSpecificationMethod",)


class CrowningSpecificationMethod(Enum):
    """CrowningSpecificationMethod

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CROWNING_SPECIFICATION_METHOD

    CIRCULAR = 0
    LOGARITHMIC = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


CrowningSpecificationMethod.__setattr__ = __enum_setattr
CrowningSpecificationMethod.__delattr__ = __enum_delattr
