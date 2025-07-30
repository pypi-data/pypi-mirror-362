"""BeamSectionType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_BEAM_SECTION_TYPE = python_net_import(
    "SMT.MastaAPI.FETools.VisToolsGlobal.VisToolsGlobalEnums", "BeamSectionType"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="BeamSectionType")
    CastSelf = TypeVar("CastSelf", bound="BeamSectionType._Cast_BeamSectionType")


__docformat__ = "restructuredtext en"
__all__ = ("BeamSectionType",)


class BeamSectionType(Enum):
    """BeamSectionType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _BEAM_SECTION_TYPE

    GENERALISED_SECTION_PROPERTIES = 0
    ARBITRARY_CLOSED_LOOPS = 1
    HOLLOW_BOX = 2
    ANGLE = 3
    I_BEAM = 4
    SOLID_CIRCLE = 5
    TUBE = 6
    PANEL = 7
    RECTANGLE = 8
    TRAPEZOID = 9
    HOLLOW_HEXAGON = 10
    TEE = 11
    ZEE = 12
    CHANNEL = 13
    SOLID_SECTOR = 14
    SOLID_ELLIPSE = 15
    HAT = 16
    CROSS = 17
    DOUBLE_HOLLOW_BOX = 18
    HAT_WITH_BASE = 19
    QUADRILATERAL = 20
    HAT_GENERAL = 21
    SOLID_HEXAGON = 22
    CONNECTED_SEGMENTS = 23


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


BeamSectionType.__setattr__ = __enum_setattr
BeamSectionType.__delattr__ = __enum_delattr
