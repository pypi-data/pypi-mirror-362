"""RollingBearing"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    overridable_enum_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.bearings import _2073, _2074, _2095, _2098
from mastapy._private.bearings.bearing_designs import _2341
from mastapy._private.bearings.bearing_designs.rolling import _2361, _2362, _2368, _2386

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_ROLLING_BEARING = python_net_import(
    "SMT.MastaAPI.Bearings.BearingDesigns.Rolling", "RollingBearing"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private.bearings import _2072, _2075, _2080
    from mastapy._private.bearings.bearing_designs import _2340, _2344
    from mastapy._private.bearings.bearing_designs.rolling import (
        _2345,
        _2346,
        _2347,
        _2348,
        _2349,
        _2350,
        _2352,
        _2353,
        _2356,
        _2357,
        _2358,
        _2359,
        _2360,
        _2364,
        _2365,
        _2369,
        _2370,
        _2371,
        _2372,
        _2376,
        _2377,
        _2378,
        _2379,
        _2380,
        _2381,
        _2382,
        _2383,
        _2384,
        _2385,
    )
    from mastapy._private.bearings.bearing_results.rolling import _2184
    from mastapy._private.materials import _332
    from mastapy._private.utility import _1775

    Self = TypeVar("Self", bound="RollingBearing")
    CastSelf = TypeVar("CastSelf", bound="RollingBearing._Cast_RollingBearing")


__docformat__ = "restructuredtext en"
__all__ = ("RollingBearing",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RollingBearing:
    """Special nested class for casting RollingBearing to subclasses."""

    __parent__: "RollingBearing"

    @property
    def detailed_bearing(self: "CastSelf") -> "_2341.DetailedBearing":
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
    def angular_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2345.AngularContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2345

        return self.__parent__._cast(_2345.AngularContactBallBearing)

    @property
    def angular_contact_thrust_ball_bearing(
        self: "CastSelf",
    ) -> "_2346.AngularContactThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2346

        return self.__parent__._cast(_2346.AngularContactThrustBallBearing)

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
    def ball_bearing(self: "CastSelf") -> "_2350.BallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2350

        return self.__parent__._cast(_2350.BallBearing)

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
    def deep_groove_ball_bearing(self: "CastSelf") -> "_2360.DeepGrooveBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2360

        return self.__parent__._cast(_2360.DeepGrooveBallBearing)

    @property
    def four_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2364.FourPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2364

        return self.__parent__._cast(_2364.FourPointContactBallBearing)

    @property
    def multi_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2369.MultiPointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2369

        return self.__parent__._cast(_2369.MultiPointContactBallBearing)

    @property
    def needle_roller_bearing(self: "CastSelf") -> "_2370.NeedleRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2370

        return self.__parent__._cast(_2370.NeedleRollerBearing)

    @property
    def non_barrel_roller_bearing(self: "CastSelf") -> "_2371.NonBarrelRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2371

        return self.__parent__._cast(_2371.NonBarrelRollerBearing)

    @property
    def roller_bearing(self: "CastSelf") -> "_2372.RollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2372

        return self.__parent__._cast(_2372.RollerBearing)

    @property
    def self_aligning_ball_bearing(self: "CastSelf") -> "_2377.SelfAligningBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2377

        return self.__parent__._cast(_2377.SelfAligningBallBearing)

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
    def three_point_contact_ball_bearing(
        self: "CastSelf",
    ) -> "_2383.ThreePointContactBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2383

        return self.__parent__._cast(_2383.ThreePointContactBallBearing)

    @property
    def thrust_ball_bearing(self: "CastSelf") -> "_2384.ThrustBallBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2384

        return self.__parent__._cast(_2384.ThrustBallBearing)

    @property
    def toroidal_roller_bearing(self: "CastSelf") -> "_2385.ToroidalRollerBearing":
        from mastapy._private.bearings.bearing_designs.rolling import _2385

        return self.__parent__._cast(_2385.ToroidalRollerBearing)

    @property
    def rolling_bearing(self: "CastSelf") -> "RollingBearing":
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
class RollingBearing(_2341.DetailedBearing):
    """RollingBearing

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROLLING_BEARING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def are_the_inner_rings_a_single_piece_of_metal(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "AreTheInnerRingsASinglePieceOfMetal"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @are_the_inner_rings_a_single_piece_of_metal.setter
    @exception_bridge
    @enforce_parameter_types
    def are_the_inner_rings_a_single_piece_of_metal(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AreTheInnerRingsASinglePieceOfMetal", value
        )

    @property
    @exception_bridge
    def are_the_outer_rings_a_single_piece_of_metal(
        self: "Self",
    ) -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(
            self.wrapped, "AreTheOuterRingsASinglePieceOfMetal"
        )

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @are_the_outer_rings_a_single_piece_of_metal.setter
    @exception_bridge
    @enforce_parameter_types
    def are_the_outer_rings_a_single_piece_of_metal(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "AreTheOuterRingsASinglePieceOfMetal", value
        )

    @property
    @exception_bridge
    def arrangement(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement":
        """EnumWithSelectedValue[mastapy.bearings.RollingBearingArrangement]"""
        temp = pythonnet_property_get(self.wrapped, "Arrangement")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @arrangement.setter
    @exception_bridge
    @enforce_parameter_types
    def arrangement(self: "Self", value: "_2095.RollingBearingArrangement") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingArrangement.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "Arrangement", value)

    @property
    @exception_bridge
    def basic_dynamic_load_rating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BasicDynamicLoadRating")

        if temp is None:
            return 0.0

        return temp

    @basic_dynamic_load_rating.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_dynamic_load_rating(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BasicDynamicLoadRating",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def basic_dynamic_load_rating_calculation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod":
        """EnumWithSelectedValue[mastapy.bearings.BasicDynamicLoadRatingCalculationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "BasicDynamicLoadRatingCalculation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @basic_dynamic_load_rating_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_dynamic_load_rating_calculation(
        self: "Self", value: "_2073.BasicDynamicLoadRatingCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BasicDynamicLoadRatingCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BasicDynamicLoadRatingCalculation", value)

    @property
    @exception_bridge
    def basic_dynamic_load_rating_divided_by_correction_factors(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "BasicDynamicLoadRatingDividedByCorrectionFactors"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_dynamic_load_rating_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicDynamicLoadRatingSource")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def basic_static_load_rating(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRating")

        if temp is None:
            return 0.0

        return temp

    @basic_static_load_rating.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_static_load_rating(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BasicStaticLoadRating",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def basic_static_load_rating_calculation(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod":
        """EnumWithSelectedValue[mastapy.bearings.BasicStaticLoadRatingCalculationMethod]"""
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRatingCalculation")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @basic_static_load_rating_calculation.setter
    @exception_bridge
    @enforce_parameter_types
    def basic_static_load_rating_calculation(
        self: "Self", value: "_2074.BasicStaticLoadRatingCalculationMethod"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_BasicStaticLoadRatingCalculationMethod.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "BasicStaticLoadRatingCalculation", value)

    @property
    @exception_bridge
    def basic_static_load_rating_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRatingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def basic_static_load_rating_source(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BasicStaticLoadRatingSource")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def cage_bridge_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_bridge_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_bridge_angle(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageBridgeAngle", value)

    @property
    @exception_bridge
    def cage_bridge_axial_surface_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeAxialSurfaceRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_bridge_axial_surface_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_bridge_axial_surface_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageBridgeAxialSurfaceRadius", value)

    @property
    @exception_bridge
    def cage_bridge_radial_surface_radius(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeRadialSurfaceRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_bridge_radial_surface_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_bridge_radial_surface_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageBridgeRadialSurfaceRadius", value)

    @property
    @exception_bridge
    def cage_bridge_shape(self: "Self") -> "_2357.CageBridgeShape":
        """mastapy.bearings.bearing_designs.rolling.CageBridgeShape"""
        temp = pythonnet_property_get(self.wrapped, "CageBridgeShape")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.CageBridgeShape"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2357", "CageBridgeShape"
        )(value)

    @cage_bridge_shape.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_bridge_shape(self: "Self", value: "_2357.CageBridgeShape") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.CageBridgeShape"
        )
        pythonnet_property_set(self.wrapped, "CageBridgeShape", value)

    @property
    @exception_bridge
    def cage_bridge_width(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CageBridgeWidth")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def cage_guiding_ring_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageGuidingRingWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_guiding_ring_width.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_guiding_ring_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageGuidingRingWidth", value)

    @property
    @exception_bridge
    def cage_mass(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageMass")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_mass.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_mass(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageMass", value)

    @property
    @exception_bridge
    def cage_material(self: "Self") -> "_2075.BearingCageMaterial":
        """mastapy.bearings.BearingCageMaterial"""
        temp = pythonnet_property_get(self.wrapped, "CageMaterial")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingCageMaterial"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2075", "BearingCageMaterial"
        )(value)

    @cage_material.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_material(self: "Self", value: "_2075.BearingCageMaterial") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingCageMaterial"
        )
        pythonnet_property_set(self.wrapped, "CageMaterial", value)

    @property
    @exception_bridge
    def cage_pitch_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CagePitchRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_pitch_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_pitch_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CagePitchRadius", value)

    @property
    @exception_bridge
    def cage_pocket_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CagePocketClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_pocket_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_pocket_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CagePocketClearance", value)

    @property
    @exception_bridge
    def cage_thickness(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageThickness")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_thickness.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_thickness(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageThickness", value)

    @property
    @exception_bridge
    def cage_to_inner_ring_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageToInnerRingClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_to_inner_ring_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_to_inner_ring_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageToInnerRingClearance", value)

    @property
    @exception_bridge
    def cage_to_outer_ring_clearance(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageToOuterRingClearance")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_to_outer_ring_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_to_outer_ring_clearance(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageToOuterRingClearance", value)

    @property
    @exception_bridge
    def cage_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "CageWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @cage_width.setter
    @exception_bridge
    @enforce_parameter_types
    def cage_width(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "CageWidth", value)

    @property
    @exception_bridge
    def catalogue(self: "Self") -> "_2072.BearingCatalog":
        """mastapy.bearings.BearingCatalog

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Catalogue")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingCatalog")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2072", "BearingCatalog"
        )(value)

    @property
    @exception_bridge
    def combined_surface_roughness_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedSurfaceRoughnessInner")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def combined_surface_roughness_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CombinedSurfaceRoughnessOuter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_angle(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ContactAngle")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @contact_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def contact_angle(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ContactAngle", value)

    @property
    @exception_bridge
    def contact_radius_in_rolling_direction_inner(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusInRollingDirectionInner"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact_radius_in_rolling_direction_outer(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactRadiusInRollingDirectionOuter"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def designation(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Designation")

        if temp is None:
            return ""

        return temp

    @designation.setter
    @exception_bridge
    @enforce_parameter_types
    def designation(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Designation", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def diameter_series(self: "Self") -> "overridable.Overridable_DiameterSeries":
        """Overridable[mastapy.bearings.bearing_designs.rolling.DiameterSeries]"""
        temp = pythonnet_property_get(self.wrapped, "DiameterSeries")

        if temp is None:
            return None

        value = overridable.Overridable_DiameterSeries.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @diameter_series.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter_series(
        self: "Self",
        value: "Union[_2361.DiameterSeries, Tuple[_2361.DiameterSeries, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_DiameterSeries.wrapper_type()
        enclosed_type = overridable.Overridable_DiameterSeries.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DiameterSeries", value)

    @property
    @exception_bridge
    def distance_between_element_centres(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenElementCentres")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_between_element_centres.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_between_element_centres(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "DistanceBetweenElementCentres", value)

    @property
    @exception_bridge
    def dynamic_axial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicAxialLoadFactorForHighAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_axial_load_factor_for_high_axial_radial_load_ratios.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_axial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicAxialLoadFactorForHighAxialRadialLoadRatios", value
        )

    @property
    @exception_bridge
    def dynamic_axial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicAxialLoadFactorForLowAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_axial_load_factor_for_low_axial_radial_load_ratios.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_axial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicAxialLoadFactorForLowAxialRadialLoadRatios", value
        )

    @property
    @exception_bridge
    def dynamic_equivalent_load_factors_can_be_specified(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DynamicEquivalentLoadFactorsCanBeSpecified"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def dynamic_radial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicRadialLoadFactorForHighAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_radial_load_factor_for_high_axial_radial_load_ratios.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_radial_load_factor_for_high_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicRadialLoadFactorForHighAxialRadialLoadRatios", value
        )

    @property
    @exception_bridge
    def dynamic_radial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DynamicRadialLoadFactorForLowAxialRadialLoadRatios"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @dynamic_radial_load_factor_for_low_axial_radial_load_ratios.setter
    @exception_bridge
    @enforce_parameter_types
    def dynamic_radial_load_factor_for_low_axial_radial_load_ratios(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "DynamicRadialLoadFactorForLowAxialRadialLoadRatios", value
        )

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
    def element_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "ElementMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @element_material_reportable.setter
    @exception_bridge
    @enforce_parameter_types
    def element_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "ElementMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def element_offset(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementOffset")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def element_offset(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementOffset", value)

    @property
    @exception_bridge
    def element_radius(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementRadius")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def element_surface_roughness_rms(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSurfaceRoughnessRMS")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_surface_roughness_rms.setter
    @exception_bridge
    @enforce_parameter_types
    def element_surface_roughness_rms(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSurfaceRoughnessRMS", value)

    @property
    @exception_bridge
    def element_surface_roughness_ra(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ElementSurfaceRoughnessRa")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @element_surface_roughness_ra.setter
    @exception_bridge
    @enforce_parameter_types
    def element_surface_roughness_ra(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ElementSurfaceRoughnessRa", value)

    @property
    @exception_bridge
    def extra_information(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ExtraInformation")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def factor_for_basic_dynamic_load_rating_in_ansiabma(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FactorForBasicDynamicLoadRatingInANSIABMA"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_load_limit(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "FatigueLoadLimit")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @fatigue_load_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_load_limit(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "FatigueLoadLimit", value)

    @property
    @exception_bridge
    def fatigue_load_limit_calculation_method(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum":
        """EnumWithSelectedValue[mastapy.bearings.bearing_designs.rolling.FatigueLoadLimitCalculationMethodEnum]"""
        temp = pythonnet_property_get(self.wrapped, "FatigueLoadLimitCalculationMethod")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @fatigue_load_limit_calculation_method.setter
    @exception_bridge
    @enforce_parameter_types
    def fatigue_load_limit_calculation_method(
        self: "Self", value: "_2362.FatigueLoadLimitCalculationMethodEnum"
    ) -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_FatigueLoadLimitCalculationMethodEnum.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "FatigueLoadLimitCalculationMethod", value)

    @property
    @exception_bridge
    def free_space_between_elements(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FreeSpaceBetweenElements")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def height_series(self: "Self") -> "overridable.Overridable_HeightSeries":
        """Overridable[mastapy.bearings.bearing_designs.rolling.HeightSeries]"""
        temp = pythonnet_property_get(self.wrapped, "HeightSeries")

        if temp is None:
            return None

        value = overridable.Overridable_HeightSeries.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @height_series.setter
    @exception_bridge
    @enforce_parameter_types
    def height_series(
        self: "Self",
        value: "Union[_2368.HeightSeries, Tuple[_2368.HeightSeries, bool]]",
    ) -> None:
        wrapper_type = overridable.Overridable_HeightSeries.wrapper_type()
        enclosed_type = overridable.Overridable_HeightSeries.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "HeightSeries", value)

    @property
    @exception_bridge
    def iso_material_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ISOMaterialFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @iso_material_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def iso_material_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ISOMaterialFactor", value)

    @property
    @exception_bridge
    def inner_race_hardness_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRaceHardnessDepth")

        if temp is None:
            return 0.0

        return temp

    @inner_race_hardness_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_race_hardness_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRaceHardnessDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_race_outer_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRaceOuterDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def inner_ring_left_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingLeftCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_left_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_left_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingLeftCornerRadius", value)

    @property
    @exception_bridge
    def inner_ring_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "InnerRingMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @inner_ring_material_reportable.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "InnerRingMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def inner_ring_right_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingRightCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_right_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_right_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingRightCornerRadius", value)

    @property
    @exception_bridge
    def inner_ring_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType":
        """EnumWithSelectedValue[mastapy.bearings.RollingBearingRaceType]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @inner_ring_type.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_type(self: "Self", value: "_2098.RollingBearingRaceType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "InnerRingType", value)

    @property
    @exception_bridge
    def inner_ring_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @inner_ring_width.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "InnerRingWidth", value)

    @property
    @exception_bridge
    def is_full_complement(self: "Self") -> "overridable.Overridable_bool":
        """Overridable[bool]"""
        temp = pythonnet_property_get(self.wrapped, "IsFullComplement")

        if temp is None:
            return False

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_bool"
        )(temp)

    @is_full_complement.setter
    @exception_bridge
    @enforce_parameter_types
    def is_full_complement(
        self: "Self", value: "Union[bool, Tuple[bool, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_bool.wrapper_type()
        enclosed_type = overridable.Overridable_bool.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else False, is_overridden
        )
        pythonnet_property_set(self.wrapped, "IsFullComplement", value)

    @property
    @exception_bridge
    def is_network_item(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsNetworkItem")

        if temp is None:
            return False

        return temp

    @is_network_item.setter
    @exception_bridge
    @enforce_parameter_types
    def is_network_item(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsNetworkItem", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def kz(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "KZ")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @kz.setter
    @exception_bridge
    @enforce_parameter_types
    def kz(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "KZ", value)

    @property
    @exception_bridge
    def limiting_value_for_axial_load_ratio(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LimitingValueForAxialLoadRatio")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @limiting_value_for_axial_load_ratio.setter
    @exception_bridge
    @enforce_parameter_types
    def limiting_value_for_axial_load_ratio(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LimitingValueForAxialLoadRatio", value)

    @property
    @exception_bridge
    def manufacturer(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Manufacturer")

        if temp is None:
            return ""

        return temp

    @manufacturer.setter
    @exception_bridge
    @enforce_parameter_types
    def manufacturer(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Manufacturer", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def maximum_grease_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumGreaseSpeed")

        if temp is None:
            return 0.0

        return temp

    @maximum_grease_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_grease_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumGreaseSpeed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_oil_speed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumOilSpeed")

        if temp is None:
            return 0.0

        return temp

    @maximum_oil_speed.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_oil_speed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MaximumOilSpeed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_permissible_contact_stress_for_static_failure_inner(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureInner"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_permissible_contact_stress_for_static_failure_inner.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_permissible_contact_stress_for_static_failure_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureInner", value
        )

    @property
    @exception_bridge
    def maximum_permissible_contact_stress_for_static_failure_outer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureOuter"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_permissible_contact_stress_for_static_failure_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_permissible_contact_stress_for_static_failure_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumPermissibleContactStressForStaticFailureOuter", value
        )

    @property
    @exception_bridge
    def minimum_surface_roughness_rms(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSurfaceRoughnessRMS")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_surface_roughness_ra(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumSurfaceRoughnessRa")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def model(self: "Self") -> "_2080.BearingModel":
        """mastapy.bearings.BearingModel

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Model")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bearings.BearingModel")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings._2080", "BearingModel"
        )(value)

    @property
    @exception_bridge
    def no_history(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NoHistory")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def number_of_elements(self: "Self") -> "overridable.Overridable_int":
        """Overridable[int]"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfElements")

        if temp is None:
            return 0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_int"
        )(temp)

    @number_of_elements.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_elements(self: "Self", value: "Union[int, Tuple[int, bool]]") -> None:
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "NumberOfElements", value)

    @property
    @exception_bridge
    def number_of_rows(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfRows")

        if temp is None:
            return 0

        return temp

    @number_of_rows.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_rows(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfRows", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def outer_race_hardness_depth(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRaceHardnessDepth")

        if temp is None:
            return 0.0

        return temp

    @outer_race_hardness_depth.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_race_hardness_depth(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRaceHardnessDepth",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_race_inner_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRaceInnerDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def outer_ring_left_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingLeftCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_left_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_left_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingLeftCornerRadius", value)

    @property
    @exception_bridge
    def outer_ring_material_reportable(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "OuterRingMaterialReportable", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @outer_ring_material_reportable.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_material_reportable(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "OuterRingMaterialReportable",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def outer_ring_offset(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingOffset")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_offset(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingOffset", value)

    @property
    @exception_bridge
    def outer_ring_right_corner_radius(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingRightCornerRadius")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_right_corner_radius.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_right_corner_radius(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingRightCornerRadius", value)

    @property
    @exception_bridge
    def outer_ring_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType":
        """EnumWithSelectedValue[mastapy.bearings.RollingBearingRaceType]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @outer_ring_type.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_type(self: "Self", value: "_2098.RollingBearingRaceType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_RollingBearingRaceType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "OuterRingType", value)

    @property
    @exception_bridge
    def outer_ring_width(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingWidth")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @outer_ring_width.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_width(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "OuterRingWidth", value)

    @property
    @exception_bridge
    def pitch_circle_diameter(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PitchCircleDiameter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @pitch_circle_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def pitch_circle_diameter(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PitchCircleDiameter", value)

    @property
    @exception_bridge
    def power_for_maximum_contact_stress_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PowerForMaximumContactStressSafetyFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def raceway_surface_roughness_rms_inner(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRMSInner")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_rms_inner.setter
    @exception_bridge
    @enforce_parameter_types
    def raceway_surface_roughness_rms_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRMSInner", value)

    @property
    @exception_bridge
    def raceway_surface_roughness_rms_outer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRMSOuter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_rms_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def raceway_surface_roughness_rms_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRMSOuter", value)

    @property
    @exception_bridge
    def raceway_surface_roughness_ra_inner(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRaInner")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_ra_inner.setter
    @exception_bridge
    @enforce_parameter_types
    def raceway_surface_roughness_ra_inner(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRaInner", value)

    @property
    @exception_bridge
    def raceway_surface_roughness_ra_outer(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "RacewaySurfaceRoughnessRaOuter")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @raceway_surface_roughness_ra_outer.setter
    @exception_bridge
    @enforce_parameter_types
    def raceway_surface_roughness_ra_outer(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "RacewaySurfaceRoughnessRaOuter", value)

    @property
    @exception_bridge
    def sleeve_type(self: "Self") -> "_2379.SleeveType":
        """mastapy.bearings.bearing_designs.rolling.SleeveType

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SleeveType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.SleeveType"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2379", "SleeveType"
        )(value)

    @property
    @exception_bridge
    def theoretical_maximum_number_of_elements(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TheoreticalMaximumNumberOfElements"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_free_space_between_elements(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalFreeSpaceBetweenElements")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def type_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Type")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def type_information(self: "Self") -> "_2356.BearingTypeExtraInformation":
        """mastapy.bearings.bearing_designs.rolling.BearingTypeExtraInformation

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TypeInformation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Bearings.BearingDesigns.Rolling.BearingTypeExtraInformation",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_designs.rolling._2356",
            "BearingTypeExtraInformation",
        )(value)

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
    @exception_bridge
    def width_series(self: "Self") -> "overridable.Overridable_WidthSeries":
        """Overridable[mastapy.bearings.bearing_designs.rolling.WidthSeries]"""
        temp = pythonnet_property_get(self.wrapped, "WidthSeries")

        if temp is None:
            return None

        value = overridable.Overridable_WidthSeries.wrapped_type()
        return overridable_enum_runtime.create(temp, value)

    @width_series.setter
    @exception_bridge
    @enforce_parameter_types
    def width_series(
        self: "Self", value: "Union[_2386.WidthSeries, Tuple[_2386.WidthSeries, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_WidthSeries.wrapper_type()
        enclosed_type = overridable.Overridable_WidthSeries.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](
            value if value is not None else None, is_overridden
        )
        pythonnet_property_set(self.wrapped, "WidthSeries", value)

    @property
    @exception_bridge
    def element_material(self: "Self") -> "_332.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElementMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def geometric_constants(self: "Self") -> "_2365.GeometricConstants":
        """mastapy.bearings.bearing_designs.rolling.GeometricConstants

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GeometricConstants")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def history(self: "Self") -> "_1775.FileHistory":
        """mastapy.utility.FileHistory

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "History")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def iso153122018(self: "Self") -> "_2184.ISO153122018Results":
        """mastapy.bearings.bearing_results.rolling.ISO153122018Results

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ISO153122018")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def inner_ring_material(self: "Self") -> "_332.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InnerRingMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def outer_ring_material(self: "Self") -> "_332.BearingMaterial":
        """mastapy.materials.BearingMaterial

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "OuterRingMaterial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def protection(self: "Self") -> "_2353.BearingProtection":
        """mastapy.bearings.bearing_designs.rolling.BearingProtection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Protection")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def skf_seal_frictional_moment_constants(
        self: "Self",
    ) -> "_2378.SKFSealFrictionalMomentConstants":
        """mastapy.bearings.bearing_designs.rolling.SKFSealFrictionalMomentConstants

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SKFSealFrictionalMomentConstants")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def elements(self: "Self") -> "List[_2376.RollingBearingElement]":
        """List[mastapy.bearings.bearing_designs.rolling.RollingBearingElement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Elements")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    def remove_inner_ring_while_keeping_other_geometry_constant(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "RemoveInnerRingWhileKeepingOtherGeometryConstant"
        )

    @exception_bridge
    def remove_outer_ring_while_keeping_other_geometry_constant(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "RemoveOuterRingWhileKeepingOtherGeometryConstant"
        )

    @exception_bridge
    def __copy__(self: "Self") -> "RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing"""
        method_result = pythonnet_method_call(self.wrapped, "Copy")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def __deepcopy__(self: "Self", memo) -> "RollingBearing":
        """mastapy.bearings.bearing_designs.rolling.RollingBearing"""
        method_result = pythonnet_method_call(self.wrapped, "Copy")
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

    @exception_bridge
    def link_to_online_catalogue(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "LinkToOnlineCatalogue")

    @property
    def cast_to(self: "Self") -> "_Cast_RollingBearing":
        """Cast to another type.

        Returns:
            _Cast_RollingBearing
        """
        return _Cast_RollingBearing(self)
