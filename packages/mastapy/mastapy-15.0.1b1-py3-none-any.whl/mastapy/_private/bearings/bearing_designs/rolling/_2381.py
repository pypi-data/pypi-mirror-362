"""SphericalRollerThrustBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings.bearing_designs.rolling import _2352

_SPHERICAL_ROLLER_THRUST_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "SphericalRollerThrustBearing"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.rolling import _2372, _2375

    Self = TypeVar("Self", bound="SphericalRollerThrustBearing")
    CastSelf = TypeVar(
        "CastSelf",
        bound="SphericalRollerThrustBearing._Cast_SphericalRollerThrustBearing",
    )


__docformat__ = "restructuredtext en"
__all__ = ("SphericalRollerThrustBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SphericalRollerThrustBearing:
    """Special nested class for casting SphericalRollerThrustBearing to subclasses."""

    __parent__: "SphericalRollerThrustBearing"

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2352.BarrelRollerBearing":
        return self.__parent__._cast(_2352.BarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2372.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2372

        return self.__parent__._cast(_2372.RollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "_2375.RollingBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2375

        return self.__parent__._cast(_2375.RollingBearing)

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
        from mastapy._private.bearings.bearing_designs import _2341

        return self.__parent__._cast(_2341.DetailedBearing)

    @property
    def non_linear_bearing(self: "CastSelf") -> "_2344.NonLinearBearing":
        from mastapy._private.bearings.bearing_designs import _2344

        return self.__parent__._cast(_2344.NonLinearBearing)

    @property
    def bearing_design(self: "CastSelf") -> "_2340.BearingDesign":
        from mastapy._private.bearings.bearing_designs import _2340

        return self.__parent__._cast(_2340.BearingDesign)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "SphericalRollerThrustBearing":
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
class SphericalRollerThrustBearing(_2352.BarrelRollerBearing):
    """SphericalRollerThrustBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SPHERICAL_ROLLER_THRUST_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_between_roller_end_and_bearing_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngleBetweenRollerEndAndBearingAxis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_to_pressure_point_from_left_face(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceToPressurePointFromLeftFace"
        )

        if temp is None:
            return 0.0

        return temp

    @distance_to_pressure_point_from_left_face.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_to_pressure_point_from_left_face(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceToPressurePointFromLeftFace",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def effective_taper_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveTaperAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_centre_point_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementCentrePointDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def major_diameter_offset_from_roller_centre(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MajorDiameterOffsetFromRollerCentre"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @major_diameter_offset_from_roller_centre.setter
    @exception_bridge
    @enforce_parameter_types
    def major_diameter_offset_from_roller_centre(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MajorDiameterOffsetFromRollerCentre", value
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0.0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", float(value) if value is not None else 0.0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_SphericalRollerThrustBearing":
        """Cast to another type.

        Returns:
            _Cast_SphericalRollerThrustBearing
        """
        return _Cast_SphericalRollerThrustBearing(self)
