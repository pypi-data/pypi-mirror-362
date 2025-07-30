"""SelectableTransferPath"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_SELECTABLE_TRANSFER_PATH = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.HarmonicAnalyses.TransferPathAnalyses",
    "SelectableTransferPath",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="SelectableTransferPath")
    CastSelf = TypeVar(
        "CastSelf", bound="SelectableTransferPath._Cast_SelectableTransferPath"
    )


__docformat__ = "restructuredtext en"
__all__ = ("SelectableTransferPath",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SelectableTransferPath:
    """Special nested class for casting SelectableTransferPath to subclasses."""

    __parent__: "SelectableTransferPath"

    @property
    def selectable_transfer_path(self: "CastSelf") -> "SelectableTransferPath":
        return self.__parent__

    def __getattr__(self: "CastSelf", name: str) -> "Any":
        try:
            return self.__getattribute__(name)
        except AttributeError:
            class_name = utility.camel(name)
            raise CastException(
                f'Detected an invalid cast. Cannot cast to type "{class_name}"'
            ) from None


@extended_dataclass(frozen=True, slots=True, weakref_slot=True, eq=False)
class SelectableTransferPath(_0.APIBase):
    """SelectableTransferPath

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SELECTABLE_TRANSFER_PATH

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def show(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "Show")

        if temp is None:
            return False

        return temp

    @show.setter
    @exception_bridge
    @enforce_parameter_types
    def show(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "Show", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SelectableTransferPath":
        """Cast to another type.

        Returns:
            _Cast_SelectableTransferPath
        """
        return _Cast_SelectableTransferPath(self)
