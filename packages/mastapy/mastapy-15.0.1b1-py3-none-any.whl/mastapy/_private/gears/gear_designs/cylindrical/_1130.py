"""CylindricalGearMicroGeometrySettings"""

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
from mastapy._private.utility import _1779

_CYLINDRICAL_GEAR_MICRO_GEOMETRY_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearMicroGeometrySettings"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs.cylindrical import _1155
    from mastapy._private.gears.gear_designs.cylindrical.micro_geometry import _1237
    from mastapy._private.gears.micro_geometry import _662

    Self = TypeVar("Self", bound="CylindricalGearMicroGeometrySettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMicroGeometrySettings._Cast_CylindricalGearMicroGeometrySettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMicroGeometrySettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMicroGeometrySettings:
    """Special nested class for casting CylindricalGearMicroGeometrySettings to subclasses."""

    __parent__: "CylindricalGearMicroGeometrySettings"

    @property
    def independent_reportable_properties_base(
        self: "CastSelf",
    ) -> "_1779.IndependentReportablePropertiesBase":
        pass

        return self.__parent__._cast(_1779.IndependentReportablePropertiesBase)

    @property
    def cylindrical_gear_micro_geometry_settings(
        self: "CastSelf",
    ) -> "CylindricalGearMicroGeometrySettings":
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
class CylindricalGearMicroGeometrySettings(
    _1779.IndependentReportablePropertiesBase["CylindricalGearMicroGeometrySettings"]
):
    """CylindricalGearMicroGeometrySettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MICRO_GEOMETRY_SETTINGS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def flank_side_with_zero_face_width(self: "Self") -> "_662.FlankSide":
        """mastapy.gears.micro_geometry.FlankSide"""
        temp = pythonnet_property_get(self.wrapped, "FlankSideWithZeroFaceWidth")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.MicroGeometry.FlankSide"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.micro_geometry._662", "FlankSide"
        )(value)

    @flank_side_with_zero_face_width.setter
    @exception_bridge
    @enforce_parameter_types
    def flank_side_with_zero_face_width(self: "Self", value: "_662.FlankSide") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.MicroGeometry.FlankSide"
        )
        pythonnet_property_set(self.wrapped, "FlankSideWithZeroFaceWidth", value)

    @property
    @exception_bridge
    def micro_geometry_lead_tolerance_chart_view(
        self: "Self",
    ) -> "_1237.MicroGeometryLeadToleranceChartView":
        """mastapy.gears.gear_designs.cylindrical.micro_geometry.MicroGeometryLeadToleranceChartView"""
        temp = pythonnet_property_get(
            self.wrapped, "MicroGeometryLeadToleranceChartView"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.MicroGeometryLeadToleranceChartView",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical.micro_geometry._1237",
            "MicroGeometryLeadToleranceChartView",
        )(value)

    @micro_geometry_lead_tolerance_chart_view.setter
    @exception_bridge
    @enforce_parameter_types
    def micro_geometry_lead_tolerance_chart_view(
        self: "Self", value: "_1237.MicroGeometryLeadToleranceChartView"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.MicroGeometry.MicroGeometryLeadToleranceChartView",
        )
        pythonnet_property_set(
            self.wrapped, "MicroGeometryLeadToleranceChartView", value
        )

    @property
    @exception_bridge
    def scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts(
        self: "Self",
    ) -> "_1155.DoubleAxisScaleAndRange":
        """mastapy.gears.gear_designs.cylindrical.DoubleAxisScaleAndRange"""
        temp = pythonnet_property_get(
            self.wrapped,
            "ScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DoubleAxisScaleAndRange"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.cylindrical._1155",
            "DoubleAxisScaleAndRange",
        )(value)

    @scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts.setter
    @exception_bridge
    @enforce_parameter_types
    def scale_and_range_of_flank_relief_axes_for_micro_geometry_tolerance_charts(
        self: "Self", value: "_1155.DoubleAxisScaleAndRange"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Cylindrical.DoubleAxisScaleAndRange"
        )
        pythonnet_property_set(
            self.wrapped,
            "ScaleAndRangeOfFlankReliefAxesForMicroGeometryToleranceCharts",
            value,
        )

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMicroGeometrySettings":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMicroGeometrySettings
        """
        return _Cast_CylindricalGearMicroGeometrySettings(self)
