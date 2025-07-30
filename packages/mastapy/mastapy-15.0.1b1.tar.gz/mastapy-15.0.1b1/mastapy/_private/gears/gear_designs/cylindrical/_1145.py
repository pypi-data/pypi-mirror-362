"""CylindricalGearTableWithMGCharts"""

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
from mastapy._private.utility.report import _1975

_CYLINDRICAL_GEAR_TABLE_WITH_MG_CHARTS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearTableWithMGCharts"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1144
    from mastapy._private.utility.report import _1958, _1964, _1965, _1966

    Self = TypeVar("Self", bound="CylindricalGearTableWithMGCharts")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearTableWithMGCharts._Cast_CylindricalGearTableWithMGCharts",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearTableWithMGCharts",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearTableWithMGCharts:
    """Special nested class for casting CylindricalGearTableWithMGCharts to subclasses."""

    __parent__: "CylindricalGearTableWithMGCharts"

    @property
    def custom_table(self: "CastSelf") -> "_1975.CustomTable":
        return self.__parent__._cast(_1975.CustomTable)

    @property
    def custom_report_multi_property_item(
        self: "CastSelf",
    ) -> "_1964.CustomReportMultiPropertyItem":
        pass

        from mastapy._private.utility.report import _1964

        return self.__parent__._cast(_1964.CustomReportMultiPropertyItem)

    @property
    def custom_report_multi_property_item_base(
        self: "CastSelf",
    ) -> "_1965.CustomReportMultiPropertyItemBase":
        from mastapy._private.utility.report import _1965

        return self.__parent__._cast(_1965.CustomReportMultiPropertyItemBase)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def cylindrical_gear_table_with_mg_charts(
        self: "CastSelf",
    ) -> "CylindricalGearTableWithMGCharts":
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
class CylindricalGearTableWithMGCharts(_1975.CustomTable):
    """CylindricalGearTableWithMGCharts

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_TABLE_WITH_MG_CHARTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def chart_height(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ChartHeight")

        if temp is None:
            return 0

        return temp

    @chart_height.setter
    @exception_bridge
    @enforce_parameter_types
    def chart_height(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ChartHeight", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def chart_width(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ChartWidth")

        if temp is None:
            return 0

        return temp

    @chart_width.setter
    @exception_bridge
    @enforce_parameter_types
    def chart_width(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ChartWidth", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def item_detail(self: "Self") -> "_1144.CylindricalGearTableMGItemDetail":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearTableMGItemDetail"""
        temp = pythonnet_property_get(self.wrapped, "ItemDetail")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearTableMGItemDetail",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1144",
            "CylindricalGearTableMGItemDetail",
        )(value)

    @item_detail.setter
    @exception_bridge
    @enforce_parameter_types
    def item_detail(
        self: "Self", value: "_1144.CylindricalGearTableMGItemDetail"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.CylindricalGearTableMGItemDetail",
        )
        pythonnet_property_set(self.wrapped, "ItemDetail", value)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearTableWithMGCharts":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearTableWithMGCharts
        """
        return _Cast_CylindricalGearTableWithMGCharts(self)
