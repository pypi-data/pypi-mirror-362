"""RollerBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2094
from mastapy._private.bearings.bearing_designs.rolling import _2375

_ROLLER_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "RollerBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings.bearing_designs import _2340, _2341, _2344
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2347,
        _2348,
        _2349,
        _2352,
        _2358,
        _2359,
        _2370,
        _2371,
        _2380,
        _2381,
        _2382,
        _2385,
    )
    from mastapy._private.bearings.roller_bearing_profiles import _2131, _2144

    Self = TypeVar("Self", bound="RollerBearing")
    CastSelf = TypeVar("CastSelf", bound="RollerBearing._Cast_RollerBearing")


__docformat__ = "restructuredtext en"
__all__ = ("RollerBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollerBearing:
    """Special nested class for casting RollerBearing to subclasses."""

    __parent__: "RollerBearing"

    @property
    def rolling_bearing(self: "CastSelf") -> "_2375.RollingBearing":
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
    def asymmetric_spherical_roller_bearing(
        self: "CastSelf",
    ) -> "_2347.AsymmetricSphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2347

        return self.__parent__._cast(_2347.AsymmetricSphericalRollerBearing)

    @property
    def axial_thrust_cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2348.AxialThrustCylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2348

        return self.__parent__._cast(_2348.AxialThrustCylindricalRollerBearing)

    @property
    def axial_thrust_needle_roller_bearing(
        self: "CastSelf",
    ) -> "_2349.AxialThrustNeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2349

        return self.__parent__._cast(_2349.AxialThrustNeedleRollerBearing)

    @property
    def barrel_roller_bearing(self: "CastSelf") -> "_2352.BarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2352

        return self.__parent__._cast(_2352.BarrelRollerBearing)

    @property
    def crossed_roller_bearing(self: "CastSelf") -> "_2358.CrossedRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2358

        return self.__parent__._cast(_2358.CrossedRollerBearing)

    @property
    def cylindrical_roller_bearing(
        self: "CastSelf",
    ) -> "_2359.CylindricalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2359

        return self.__parent__._cast(_2359.CylindricalRollerBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2370.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2370

        return self.__parent__._cast(_2370.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2371.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2371

        return self.__parent__._cast(_2371.NonBarrelRollerBearing)

    @property
    def spherical_roller_bearing(self: "CastSelf") -> "_2380.SphericalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2380

        return self.__parent__._cast(_2380.SphericalRollerBearing)

    @property
    def spherical_roller_thrust_bearing(
        self: "CastSelf",
    ) -> "_2381.SphericalRollerThrustBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2381

        return self.__parent__._cast(_2381.SphericalRollerThrustBearing)

    @property
    def taper_roller_bearing(self: "CastSelf") -> "_2382.TaperRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2382

        return self.__parent__._cast(_2382.TaperRollerBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2385.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2385

        return self.__parent__._cast(_2385.ToroidalRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "RollerBearing":
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
class RollerBearing(_2375.RollingBearing):
    """RollerBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLER_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def corner_radii(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CornerRadii")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @corner_radii.setter
    @exception_bridge
    @enforce_parameter_types
    def corner_radii(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CornerRadii", value)

    @property
    @exception_bridge
    def effective_roller_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveRollerLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def element_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementDiameter", value)

    @property
    @exception_bridge
    def kl(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KL")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @kl.setter
    @exception_bridge
    @enforce_parameter_types
    def kl(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KL", value)

    @property
    @exception_bridge
    def roller_length(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RollerLength")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @roller_length.setter
    @exception_bridge
    @enforce_parameter_types
    def roller_length(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RollerLength", value)

    @property
    @exception_bridge
    def roller_profile(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes":
        """EnumWithSelectedValue[mastapy.bearings.RollerBearingProfileTypes]"""
        temp = pythonnet_property_get(self.wrapped, "RollerProfile")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @roller_profile.setter
    @exception_bridge
    @enforce_parameter_types
    def roller_profile(self: "Self", value: "_2094.RollerBearingProfileTypes") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollerBearingProfileTypes.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "RollerProfile", value)

    @property
    @exception_bridge
    def inner_race_profile_set(self: "Self") -> "_2131.ProfileSet":
        """mastapy.bearings.roller_bearing_profiles.ProfileSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceProfileSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_race_profile_set(self: "Self") -> "_2131.ProfileSet":
        """mastapy.bearings.roller_bearing_profiles.ProfileSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceProfileSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def roller_profile_set(self: "Self") -> "_2131.ProfileSet":
        """mastapy.bearings.roller_bearing_profiles.ProfileSet

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RollerProfileSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_race_and_roller_profiles(
        self: "Self",
    ) -> "List[_2144.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceAndRollerProfiles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def inner_race_and_roller_profiles_for_first_row(
        self: "Self",
    ) -> "List[_2144.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerRaceAndRollerProfilesForFirstRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def inner_race_and_roller_profiles_for_second_row(
        self: "Self",
    ) -> "List[_2144.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InnerRaceAndRollerProfilesForSecondRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def outer_race_and_roller_profiles(
        self: "Self",
    ) -> "List[_2144.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceAndRollerProfiles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def outer_race_and_roller_profiles_for_first_row(
        self: "Self",
    ) -> "List[_2144.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRaceAndRollerProfilesForFirstRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def outer_race_and_roller_profiles_for_second_row(
        self: "Self",
    ) -> "List[_2144.RollerRaceProfilePoint]":
        """List[mastapy.bearings.roller_bearing_profiles.RollerRaceProfilePoint]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRaceAndRollerProfilesForSecondRow"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_RollerBearing":
        """Cast to another type.

        Returns:
            _Cast_RollerBearing
        """
        return _Cast_RollerBearing(self)
