"""ISO6336GeometryForShapedGears"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.gear_designs.cylindrical import _1165

_ISO6336_GEOMETRY_FOR_SHAPED_GEARS = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "ISO6336GeometryForShapedGears"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ISO6336GeometryForShapedGears")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ISO6336GeometryForShapedGears._Cast_ISO6336GeometryForShapedGears",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ISO6336GeometryForShapedGears",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ISO6336GeometryForShapedGears:
    """Special nested class for casting ISO6336GeometryForShapedGears to subclasses."""

    __parent__: "ISO6336GeometryForShapedGears"

    @property
    def iso6336_geometry_base(self: "CastSelf") -> "_1165.ISO6336GeometryBase":
        return self.__parent__._cast(_1165.ISO6336GeometryBase)

    @property
    def iso6336_geometry_for_shaped_gears(
        self: "CastSelf",
    ) -> "ISO6336GeometryForShapedGears":
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
class ISO6336GeometryForShapedGears(_1165.ISO6336GeometryBase):
    """ISO6336GeometryForShapedGears

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ISO6336_GEOMETRY_FOR_SHAPED_GEARS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auxiliary_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AuxiliaryAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def base_radius_of_the_tool(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BaseRadiusOfTheTool")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutting_pitch_radius_of_the_gear(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CuttingPitchRadiusOfTheGear")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cutting_pitch_radius_of_the_tool(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CuttingPitchRadiusOfTheTool")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_the_point_m_to_the_point_of_contact_of_the_pitch_circles(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DistanceOfThePointMToThePointOfContactOfThePitchCircles"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_numbers_of_teeth(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentNumbersOfTeeth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def half_angle_of_thickness_at_point_m(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HalfAngleOfThicknessAtPointM")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def manufacturing_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def manufacturing_tooth_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ManufacturingToothRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def radius_of_point_m(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RadiusOfPointM")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theta(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Theta")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_fillet_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootFilletRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tooth_root_thickness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ToothRootThickness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transverse_pressure_angle_for_radius_of_point_m(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransversePressureAngleForRadiusOfPointM"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def virtual_tip_diameter_of_tool(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VirtualTipDiameterOfTool")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def working_pressure_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorkingPressureAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ISO6336GeometryForShapedGears":
        """Cast to another type.

        Returns:
            _Cast_ISO6336GeometryForShapedGears
        """
        return _Cast_ISO6336GeometryForShapedGears(self)
