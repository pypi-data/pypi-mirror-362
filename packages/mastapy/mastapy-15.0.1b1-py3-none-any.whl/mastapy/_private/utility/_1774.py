"""ExternalFullFEFileOption"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_EXTERNAL_FULL_FE_FILE_OPTION = python_net_import(
    "SMT.MastaAPI.Utility", "ExternalFullFEFileOption"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ExternalFullFEFileOption")
    CastSelf = TypeVar(
        "CastSelf", bound="ExternalFullFEFileOption._Cast_ExternalFullFEFileOption"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ExternalFullFEFileOption",)


class ExternalFullFEFileOption(Enum):
    """ExternalFullFEFileOption

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _EXTERNAL_FULL_FE_FILE_OPTION

    NONE = 0
    MESH = 1
    MESH_AND_EXPANSION_VECTORS = 2


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ExternalFullFEFileOption.__setattr__ = __enum_setattr
ExternalFullFEFileOption.__delattr__ = __enum_delattr
