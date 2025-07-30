"""AcousticEnvelopeType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ACOUSTIC_ENVELOPE_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.PartModel.Acoustics", "AcousticEnvelopeType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="AcousticEnvelopeType")
    CastSelf = TypeVar(
        "CastSelf", bound="AcousticEnvelopeType._Cast_AcousticEnvelopeType"
    )


__docformat__ = "restructuredtext en"
__all__ = ("AcousticEnvelopeType",)


class AcousticEnvelopeType(Enum):
    """AcousticEnvelopeType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ACOUSTIC_ENVELOPE_TYPE

    NO_ENVELOPE = 0
    SPHERICAL_ENVELOPE = 1


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


AcousticEnvelopeType.__setattr__ = __enum_setattr
AcousticEnvelopeType.__delattr__ = __enum_delattr
