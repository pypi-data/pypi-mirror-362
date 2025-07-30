"""FEExportFormat"""

from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from mastapy._private._internal.python_net import python_net_import

_FE_EXPORT_FORMAT = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.FeExportUtility", "FEExportFormat"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="FEExportFormat")
    CastSelf = TypeVar("CastSelf", bound="FEExportFormat._Cast_FEExportFormat")


__docformat__ = "restructuredtext en"
__all__ = ("FEExportFormat",)


class FEExportFormat(Enum):
    """FEExportFormat

    This is a mastapy class.

    Note:
        This class is an Enum.
    """

    @classmethod
    def type_(cls) -> "Type":
        return _FE_EXPORT_FORMAT

    ANSYS_APDL_INPUT_FILE = 0
    ANSYS_WORKBENCH_COMMANDS = 1
    NASTRAN_BULK_DATA_FILE = 2
    ABAQUS_INPUT_FILE = 3


def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
    raise AttributeError("Cannot set the attributes of an Enum.") from None


def __enum_delattr(self: "Self", attr: str) -> None:
    raise AttributeError("Cannot delete the attributes of an Enum.") from None


FEExportFormat.__setattr__ = __enum_setattr
FEExportFormat.__delattr__ = __enum_delattr
