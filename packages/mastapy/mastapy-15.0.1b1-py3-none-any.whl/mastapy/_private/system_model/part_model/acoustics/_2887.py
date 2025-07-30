"""SphericalEnvelopeType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_SPHERICAL_ENVELOPE_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "SphericalEnvelopeType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SphericalEnvelopeType")
    CastSelf = TypeVar(
        "CastSelf", bound="SphericalEnvelopeType._Cast_SphericalEnvelopeType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SphericalEnvelopeType",)


class SphericalEnvelopeType(Enum):
    """SphericalEnvelopeType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _SPHERICAL_ENVELOPE_TYPE

    ISO_3745 = 0
    UNIFORM = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


SphericalEnvelopeType.__setattr__ = __enum_setattr
SphericalEnvelopeType.__delattr__ = __enum_delattr
