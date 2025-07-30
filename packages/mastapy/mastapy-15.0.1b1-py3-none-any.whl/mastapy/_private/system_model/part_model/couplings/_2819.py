"""ClutchType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_CLUTCH_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Couplings", "ClutchType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ClutchType")
    CastSelf = TypeVar("CastSelf", bound="ClutchType._Cast_ClutchType")


__docformat__ = "restructuredtext en"
__all__ = ("ClutchType",)


class ClutchType(Enum):
    """ClutchType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _CLUTCH_TYPE

    CONCEPT_CLUTCH = 0
    MULTIPLATE_CLUTCH = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ClutchType.__setattr__ = __enum_setattr
ClutchType.__delattr__ = __enum_delattr
