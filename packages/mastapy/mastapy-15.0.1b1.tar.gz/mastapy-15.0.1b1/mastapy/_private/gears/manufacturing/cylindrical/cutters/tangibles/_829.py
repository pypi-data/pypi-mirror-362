"""CylindricalGearShaperTangible"""

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

_CYLINDRICAL_GEAR_SHAPER_TANGIBLE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles",
    "CylindricalGearShaperTangible",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _817

    Self = TypeVar("Self", bound="CylindricalGearShaperTangible")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearShaperTangible._Cast_CylindricalGearShaperTangible",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearShaperTangible",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearShaperTangible:
    """Special nested class for casting CylindricalGearShaperTangible to subclasses."""

    __parent__: "CylindricalGearShaperTangible"

    @property
    def cutter_shape_definition(self: "CastSelf") -> "_826.CutterShapeDefinition":
        return self.__parent__._cast(_826.CutterShapeDefinition)

    @property
    def cylindrical_gear_shaper_tangible(
        self: "CastSelf",
    ) -> "CylindricalGearShaperTangible":
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
class CylindricalGearShaperTangible(_826.CutterShapeDefinition):
    """CylindricalGearShaperTangible

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_SHAPER_TANGIBLE

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
    def base_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseDiameter")

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
    def helix_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "HelixAngle")

        if temp is None:
            return 0.0

        return temp

    @helix_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def helix_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "HelixAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_blade_control_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumBladeControlDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_protuberance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumProtuberance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_protuberance_height_for_single_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumProtuberanceHeightForSingleCircle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tip_control_distance_for_zero_protuberance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumTipControlDistanceForZeroProtuberance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tip_diameter_to_avoid_pointed_teeth_no_protuberance(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumTipDiameterToAvoidPointedTeethNoProtuberance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_protuberance_having_pointed_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumProtuberanceHavingPointedTeeth"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_protuberance_height_for_single_circle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumProtuberanceHeightForSingleCircle"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normal_tooth_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "NormalToothThickness")

        if temp is None:
            return 0.0

        return temp

    @normal_tooth_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def normal_tooth_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "NormalToothThickness",
            float(value) if value is not None else 0.0,
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
    def protuberance_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ProtuberanceAngle")

        if temp is None:
            return 0.0

        return temp

    @protuberance_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def protuberance_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ProtuberanceAngle",
            float(value) if value is not None else 0.0,
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
    def root_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RootDiameter")

        if temp is None:
            return 0.0

        return temp

    @root_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def root_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RootDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def semi_topping_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SemiToppingDiameter")

        if temp is None:
            return 0.0

        return temp

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
    def single_circle_maximum_edge_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SingleCircleMaximumEdgeRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tip_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TipDiameter")

        if temp is None:
            return 0.0

        return temp

    @tip_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TipDiameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def tip_thickness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TipThickness")

        if temp is None:
            return 0.0

        return temp

    @tip_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def tip_thickness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "TipThickness", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def design(self: "Self") -> "_817.CylindricalGearShaper":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearShaper

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearShaperTangible":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearShaperTangible
        """
        return _Cast_CylindricalGearShaperTangible(self)
