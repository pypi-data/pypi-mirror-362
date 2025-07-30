"""ElectricMachineDataImportType"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_ELECTRIC_MACHINE_DATA_IMPORT_TYPE = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads",
    "ElectricMachineDataImportType",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ElectricMachineDataImportType")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ElectricMachineDataImportType._Cast_ElectricMachineDataImportType",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ElectricMachineDataImportType",)


class ElectricMachineDataImportType(Enum):
    """ElectricMachineDataImportType

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _ELECTRIC_MACHINE_DATA_IMPORT_TYPE

    MASTA = 0
    ALTAIR_FLUX = 1
    EXCEL = 2
    JMAG = 3
    MOTORCAD = 4


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


ElectricMachineDataImportType.__setattr__ = __enum_setattr
ElectricMachineDataImportType.__delattr__ = __enum_delattr
