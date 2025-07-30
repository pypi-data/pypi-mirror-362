"""StraightBevelDiffGearDesign"""

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
from mastapy._private.gears.gear_designs.bevel import _1300

_STRAIGHT_BEVEL_DIFF_GEAR_DESIGN = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.StraightBevelDiff", "StraightBevelDiffGearDesign"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.gear_designs import _1051, _1052
    from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313
    from mastapy._private.gears.gear_designs.bevel import _1305
    from mastapy._private.gears.gear_designs.conical import _1274

    Self = TypeVar("Self", bound="StraightBevelDiffGearDesign")
    CastSelf = TypeVar(
        "CastSelf",
        bound="StraightBevelDiffGearDesign._Cast_StraightBevelDiffGearDesign",
    )


__docformat__ = "restructuredtext en"
__all__ = ("StraightBevelDiffGearDesign",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StraightBevelDiffGearDesign:
    """Special nested class for casting StraightBevelDiffGearDesign to subclasses."""

    __parent__: "StraightBevelDiffGearDesign"

    @property
    def bevel_gear_design(self: "CastSelf") -> "_1300.BevelGearDesign":
        return self.__parent__._cast(_1300.BevelGearDesign)

    @property
    def agma_gleason_conical_gear_design(
        self: "CastSelf",
    ) -> "_1313.AGMAGleasonConicalGearDesign":
        from mastapy._private.gears.gear_designs.agma_gleason_conical import _1313

        return self.__parent__._cast(_1313.AGMAGleasonConicalGearDesign)

    @property
    def conical_gear_design(self: "CastSelf") -> "_1274.ConicalGearDesign":
        from mastapy._private.gears.gear_designs.conical import _1274

        return self.__parent__._cast(_1274.ConicalGearDesign)

    @property
    def gear_design(self: "CastSelf") -> "_1051.GearDesign":
        from mastapy._private.gears.gear_designs import _1051

        return self.__parent__._cast(_1051.GearDesign)

    @property
    def gear_design_component(self: "CastSelf") -> "_1052.GearDesignComponent":
        from mastapy._private.gears.gear_designs import _1052

        return self.__parent__._cast(_1052.GearDesignComponent)

    @property
    def straight_bevel_diff_gear_design(
        self: "CastSelf",
    ) -> "StraightBevelDiffGearDesign":
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
class StraightBevelDiffGearDesign(_1300.BevelGearDesign):
    """StraightBevelDiffGearDesign

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STRAIGHT_BEVEL_DIFF_GEAR_DESIGN

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def allowable_peak_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowablePeakBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def allowable_performance_bending_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AllowablePerformanceBendingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def edge_radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "EdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @edge_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "EdgeRadius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def edge_radius_from(self: "Self") -> "_1305.EdgeRadiusType":
        """mastapy.gears.gear_designs.bevel.EdgeRadiusType"""
        temp = pythonnet_property_get(self.wrapped, "EdgeRadiusFrom")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Gears.GearDesigns.Bevel.EdgeRadiusType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.gear_designs.bevel._1305", "EdgeRadiusType"
        )(value)

    @edge_radius_from.setter
    @exception_bridge
    @enforce_parameter_types
    def edge_radius_from(self: "Self", value: "_1305.EdgeRadiusType") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Gears.GearDesigns.Bevel.EdgeRadiusType"
        )
        pythonnet_property_set(self.wrapped, "EdgeRadiusFrom", value)

    @property
    @exception_bridge
    def limited_point_width_large_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitedPointWidthLargeEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limited_point_width_small_end(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitedPointWidthSmallEnd")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max_radius_cutter_blades(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxRadiusCutterBlades")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def max_radius_interference(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaxRadiusInterference")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_edge_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_chordal_addendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterChordalAddendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_chordal_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterChordalThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_StraightBevelDiffGearDesign":
        """Cast to another type.

        Returns:
            _Cast_StraightBevelDiffGearDesign
        """
        return _Cast_StraightBevelDiffGearDesign(self)
