"""RackShape"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _826

_RACK_SHAPE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles", "RackShape"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _815
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
        _828,
        _831,
    )

    Self = TypeVar("Self", bound="RackShape")
    CastSelf = TypeVar("CastSelf", bound="RackShape._Cast_RackShape")


__docformat__ = "restructuredtext en"
__all__ = ("RackShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RackShape:
    """Special nested class for casting RackShape to subclasses."""

    __parent__: "RackShape"

    @property
    def cutter_shape_definition(self: "CastSelf") -> "_826.CutterShapeDefinition":
        return self.__parent__._cast(_826.CutterShapeDefinition)

    @property
    def cylindrical_gear_hob_shape(self: "CastSelf") -> "_828.CylindricalGearHobShape":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _828,
        )

        return self.__parent__._cast(_828.CylindricalGearHobShape)

    @property
    def cylindrical_gear_worm_grinder_shape(
        self: "CastSelf",
    ) -> "_831.CylindricalGearWormGrinderShape":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _831,
        )

        return self.__parent__._cast(_831.CylindricalGearWormGrinderShape)

    @property
    def rack_shape(self: "CastSelf") -> "RackShape":
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
class RackShape(_826.CutterShapeDefinition):
    """RackShape

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RACK_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual_protuberance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualProtuberance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def addendum(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Addendum")

        if temp is None:
            return 0.0

        return temp

    @addendum.setter
    @exception_bridge
    @enforce_parameter_types
    def addendum(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Addendum", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def addendum_form(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AddendumForm")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def dedendum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Dedendum")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def edge_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EdgeHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def edge_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flat_root_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlatRootWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flat_tip_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlatTipWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def has_semi_topping_blade(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HasSemiToppingBlade")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def hob_whole_depth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HobWholeDepth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def main_blade_pressure_angle_nearest_hob_root(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MainBladePressureAngleNearestHobRoot"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def main_blade_pressure_angle_nearest_hob_tip(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MainBladePressureAngleNearestHobTip"
        )

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
    def maximum_protuberance_blade_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumProtuberanceBladePressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_protuberance_blade_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumProtuberanceBladePressureAngle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_protuberance_height(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumProtuberanceHeight")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalThickness")

        if temp is None:
            return 0.0

        return temp

    @normal_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "NormalThickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def protuberance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Protuberance")

        if temp is None:
            return 0.0

        return temp

    @protuberance.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Protuberance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def protuberance_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceHeight")

        if temp is None:
            return 0.0

        return temp

    @protuberance_height.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def protuberance_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def protuberance_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ProtuberancePressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def protuberance_relative_to_main_blade_pressure_angle_nearest_hob_tip(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProtuberanceRelativeToMainBladePressureAngleNearestHobTip"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def semi_topping_height(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingHeight")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_height.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_height(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiToppingHeight",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_pressure_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_pressure_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_pressure_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SemiToppingPressureAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def semi_topping_start(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SemiToppingStart")

        if temp is None:
            return 0.0

        return temp

    @semi_topping_start.setter
    @exception_bridge
    @enforce_parameter_types
    def semi_topping_start(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SemiToppingStart", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def design(self: "Self") -> "_815.CylindricalGearRackDesign":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearRackDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_RackShape":
        """Cast to another type.

        Returns:
            _Cast_RackShape
        """
        return _Cast_RackShape(self)
