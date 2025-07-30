"""CylindricalGearHobShape"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _833

_CYLINDRICAL_GEAR_HOB_SHAPE = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.Cutters.Tangibles",
    "CylindricalGearHobShape",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.gears.manufacturing.cylindrical.cutters import _812
    from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import _826

    Self = TypeVar("Self", bound="CylindricalGearHobShape")
    CastSelf = TypeVar(
        "CastSelf", bound="CylindricalGearHobShape._Cast_CylindricalGearHobShape"
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearHobShape",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearHobShape:
    """Special nested class for casting CylindricalGearHobShape to subclasses."""

    __parent__: "CylindricalGearHobShape"

    @property
    def rack_shape(self: "CastSelf") -> "_833.RackShape":
        return self.__parent__._cast(_833.RackShape)

    @property
    def cutter_shape_definition(self: "CastSelf") -> "_826.CutterShapeDefinition":
        from mastapy._private.gears.manufacturing.cylindrical.cutters.tangibles import (
            _826,
        )

        return self.__parent__._cast(_826.CutterShapeDefinition)

    @property
    def cylindrical_gear_hob_shape(self: "CastSelf") -> "CylindricalGearHobShape":
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
class CylindricalGearHobShape(_833.RackShape):
    """CylindricalGearHobShape

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_HOB_SHAPE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def design(self: "Self") -> "_812.CylindricalGearHobDesign":
        """mastapy.gears.manufacturing.cylindrical.cutters.CylindricalGearHobDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Design")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearHobShape":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearHobShape
        """
        return _Cast_CylindricalGearHobShape(self)
