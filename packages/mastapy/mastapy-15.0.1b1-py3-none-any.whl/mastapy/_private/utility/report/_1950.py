"""CustomReportCadDrawing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1966

_CUSTOM_REPORT_CAD_DRAWING = python_net_import(
    "SMT.MastaAPI.Utility.Report", "CustomReportCadDrawing"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.cad_export import _2036
    from mastapy._private.utility.report import _1958

    Self = TypeVar("Self", bound="CustomReportCadDrawing")
    CastSelf = TypeVar(
        "CastSelf", bound="CustomReportCadDrawing._Cast_CustomReportCadDrawing"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CustomReportCadDrawing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CustomReportCadDrawing:
    """Special nested class for casting CustomReportCadDrawing to subclasses."""

    __parent__: "CustomReportCadDrawing"

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def custom_report_cad_drawing(self: "CastSelf") -> "CustomReportCadDrawing":
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
class CustomReportCadDrawing(_1966.CustomReportNameableItem):
    """CustomReportCadDrawing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CUSTOM_REPORT_CAD_DRAWING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def scale(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Scale")

        if temp is None:
            return 0.0

        return temp

    @scale.setter
    @exception_bridge
    @enforce_parameter_types
    def scale(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Scale", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def stock_drawing(self: "Self") -> "_2036.StockDrawings":
        """mastapy.utility.cad_export.StockDrawings"""
        temp = pythonnet_property_get(self.wrapped, "StockDrawing")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Utility.CadExport.StockDrawings"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.utility.cad_export._2036", "StockDrawings"
        )(value)

    @stock_drawing.setter
    @exception_bridge
    @enforce_parameter_types
    def stock_drawing(self: "Self", value: "_2036.StockDrawings") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Utility.CadExport.StockDrawings"
        )
        pythonnet_property_set(self.wrapped, "StockDrawing", value)

    @property
    @exception_bridge
    def use_stock_drawing(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseStockDrawing")

        if temp is None:
            return False

        return temp

    @use_stock_drawing.setter
    @exception_bridge
    @enforce_parameter_types
    def use_stock_drawing(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseStockDrawing", bool(value) if value is not None else False
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CustomReportCadDrawing":
        """Cast to another type.

        Returns:
            _Cast_CustomReportCadDrawing
        """
        return _Cast_CustomReportCadDrawing(self)
