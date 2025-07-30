"""TransmissionApplications"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_TRANSMISSION_APPLICATIONS = python_net_import(
    "SMT.MastaAPI.Materials", "TransmissionApplications"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="TransmissionApplications")
    CastSelf = TypeVar(
        "CastSelf", bound="TransmissionApplications._Cast_TransmissionApplications"
    )


__docformat__ = "restructuredtext en"
__all__ = ("TransmissionApplications",)


class TransmissionApplications(Enum):
    """TransmissionApplications

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _TRANSMISSION_APPLICATIONS

    GENERAL_INDUSTRIAL = 0
    AUTOMOTIVE = 1
    AIRCRAFT = 2
    MARINE = 3
    WIND_TURBINE = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


TransmissionApplications.__setattr__ = __enum_setattr
TransmissionApplications.__delattr__ = __enum_delattr
