"""LoadedBearingResults"""

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
from mastapy._private.bearings import _2078

_LOADED_BEARING_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults", "LoadedBearingResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.bearings.bearing_designs import _2340
    from mastapy._private.bearings.bearing_results import (
        _2157,
        _2158,
        _2159,
        _2160,
        _2161,
        _2163,
        _2166,
    )
    from mastapy._private.bearings.bearing_results.fluid_film import (
        _2329,
        _2330,
        _2331,
        _2332,
        _2334,
        _2337,
        _2338,
    )
    from mastapy._private.bearings.bearing_results.rolling import (
        _2191,
        _2194,
        _2197,
        _2202,
        _2205,
        _2210,
        _2213,
        _2217,
        _2220,
        _2225,
        _2229,
        _2232,
        _2237,
        _2241,
        _2244,
        _2248,
        _2251,
        _2256,
        _2259,
        _2262,
        _2265,
        _2276,
    )
    from mastapy._private.math_utility.measured_vectors import _1748

    Self = TypeVar("Self", bound="LoadedBearingResults")
    CastSelf = TypeVar(
        "CastSelf", bound="LoadedBearingResults._Cast_LoadedBearingResults"
    )


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBearingResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBearingResults:
    """Special nested class for casting LoadedBearingResults to subclasses."""

    __parent__: "LoadedBearingResults"

    @property
    def bearing_load_case_results_lightweight(
        self: "CastSelf",
    ) -> "_2078.BearingLoadCaseResultsLightweight":
        return self.__parent__._cast(_2078.BearingLoadCaseResultsLightweight)

    @property
    def loaded_concept_axial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2157.LoadedConceptAxialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2157

        return self.__parent__._cast(_2157.LoadedConceptAxialClearanceBearingResults)

    @property
    def loaded_concept_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2158.LoadedConceptClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2158

        return self.__parent__._cast(_2158.LoadedConceptClearanceBearingResults)

    @property
    def loaded_concept_radial_clearance_bearing_results(
        self: "CastSelf",
    ) -> "_2159.LoadedConceptRadialClearanceBearingResults":
        from mastapy._private.bearings.bearing_results import _2159

        return self.__parent__._cast(_2159.LoadedConceptRadialClearanceBearingResults)

    @property
    def loaded_detailed_bearing_results(
        self: "CastSelf",
    ) -> "_2160.LoadedDetailedBearingResults":
        from mastapy._private.bearings.bearing_results import _2160

        return self.__parent__._cast(_2160.LoadedDetailedBearingResults)

    @property
    def loaded_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2161.LoadedLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2161

        return self.__parent__._cast(_2161.LoadedLinearBearingResults)

    @property
    def loaded_non_linear_bearing_results(
        self: "CastSelf",
    ) -> "_2163.LoadedNonLinearBearingResults":
        from mastapy._private.bearings.bearing_results import _2163

        return self.__parent__._cast(_2163.LoadedNonLinearBearingResults)

    @property
    def loaded_angular_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2191.LoadedAngularContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2191

        return self.__parent__._cast(_2191.LoadedAngularContactBallBearingResults)

    @property
    def loaded_angular_contact_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2194.LoadedAngularContactThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2194

        return self.__parent__._cast(_2194.LoadedAngularContactThrustBallBearingResults)

    @property
    def loaded_asymmetric_spherical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2197.LoadedAsymmetricSphericalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2197

        return self.__parent__._cast(
            _2197.LoadedAsymmetricSphericalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2202.LoadedAxialThrustCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2202

        return self.__parent__._cast(
            _2202.LoadedAxialThrustCylindricalRollerBearingResults
        )

    @property
    def loaded_axial_thrust_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2205.LoadedAxialThrustNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2205

        return self.__parent__._cast(_2205.LoadedAxialThrustNeedleRollerBearingResults)

    @property
    def loaded_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2210.LoadedBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2210

        return self.__parent__._cast(_2210.LoadedBallBearingResults)

    @property
    def loaded_crossed_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2213.LoadedCrossedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2213

        return self.__parent__._cast(_2213.LoadedCrossedRollerBearingResults)

    @property
    def loaded_cylindrical_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2217.LoadedCylindricalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2217

        return self.__parent__._cast(_2217.LoadedCylindricalRollerBearingResults)

    @property
    def loaded_deep_groove_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2220.LoadedDeepGrooveBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2220

        return self.__parent__._cast(_2220.LoadedDeepGrooveBallBearingResults)

    @property
    def loaded_four_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2225.LoadedFourPointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2225

        return self.__parent__._cast(_2225.LoadedFourPointContactBallBearingResults)

    @property
    def loaded_needle_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2229.LoadedNeedleRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2229

        return self.__parent__._cast(_2229.LoadedNeedleRollerBearingResults)

    @property
    def loaded_non_barrel_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2232.LoadedNonBarrelRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2232

        return self.__parent__._cast(_2232.LoadedNonBarrelRollerBearingResults)

    @property
    def loaded_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2237.LoadedRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2237

        return self.__parent__._cast(_2237.LoadedRollerBearingResults)

    @property
    def loaded_rolling_bearing_results(
        self: "CastSelf",
    ) -> "_2241.LoadedRollingBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2241

        return self.__parent__._cast(_2241.LoadedRollingBearingResults)

    @property
    def loaded_self_aligning_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2244.LoadedSelfAligningBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2244

        return self.__parent__._cast(_2244.LoadedSelfAligningBallBearingResults)

    @property
    def loaded_spherical_roller_radial_bearing_results(
        self: "CastSelf",
    ) -> "_2248.LoadedSphericalRollerRadialBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2248

        return self.__parent__._cast(_2248.LoadedSphericalRollerRadialBearingResults)

    @property
    def loaded_spherical_roller_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2251.LoadedSphericalRollerThrustBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2251

        return self.__parent__._cast(_2251.LoadedSphericalRollerThrustBearingResults)

    @property
    def loaded_taper_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2256.LoadedTaperRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2256

        return self.__parent__._cast(_2256.LoadedTaperRollerBearingResults)

    @property
    def loaded_three_point_contact_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2259.LoadedThreePointContactBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2259

        return self.__parent__._cast(_2259.LoadedThreePointContactBallBearingResults)

    @property
    def loaded_thrust_ball_bearing_results(
        self: "CastSelf",
    ) -> "_2262.LoadedThrustBallBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2262

        return self.__parent__._cast(_2262.LoadedThrustBallBearingResults)

    @property
    def loaded_toroidal_roller_bearing_results(
        self: "CastSelf",
    ) -> "_2265.LoadedToroidalRollerBearingResults":
        from mastapy._private.bearings.bearing_results.rolling import _2265

        return self.__parent__._cast(_2265.LoadedToroidalRollerBearingResults)

    @property
    def loaded_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2329.LoadedFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2329

        return self.__parent__._cast(_2329.LoadedFluidFilmBearingResults)

    @property
    def loaded_grease_filled_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2330.LoadedGreaseFilledJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2330

        return self.__parent__._cast(_2330.LoadedGreaseFilledJournalBearingResults)

    @property
    def loaded_pad_fluid_film_bearing_results(
        self: "CastSelf",
    ) -> "_2331.LoadedPadFluidFilmBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2331

        return self.__parent__._cast(_2331.LoadedPadFluidFilmBearingResults)

    @property
    def loaded_plain_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2332.LoadedPlainJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2332

        return self.__parent__._cast(_2332.LoadedPlainJournalBearingResults)

    @property
    def loaded_plain_oil_fed_journal_bearing(
        self: "CastSelf",
    ) -> "_2334.LoadedPlainOilFedJournalBearing":
        from mastapy._private.bearings.bearing_results.fluid_film import _2334

        return self.__parent__._cast(_2334.LoadedPlainOilFedJournalBearing)

    @property
    def loaded_tilting_pad_journal_bearing_results(
        self: "CastSelf",
    ) -> "_2337.LoadedTiltingPadJournalBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2337

        return self.__parent__._cast(_2337.LoadedTiltingPadJournalBearingResults)

    @property
    def loaded_tilting_pad_thrust_bearing_results(
        self: "CastSelf",
    ) -> "_2338.LoadedTiltingPadThrustBearingResults":
        from mastapy._private.bearings.bearing_results.fluid_film import _2338

        return self.__parent__._cast(_2338.LoadedTiltingPadThrustBearingResults)

    @property
    def loaded_bearing_results(self: "CastSelf") -> "LoadedBearingResults":
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
class LoadedBearingResults(_2078.BearingLoadCaseResultsLightweight):
    """LoadedBearingResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BEARING_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angle_of_gravity_from_z_axis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AngleOfGravityFromZAxis")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_displacement_preload(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AxialDisplacementPreload")

        if temp is None:
            return 0.0

        return temp

    @axial_displacement_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_displacement_preload(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AxialDisplacementPreload",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def duration(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Duration")

        if temp is None:
            return 0.0

        return temp

    @duration.setter
    @exception_bridge
    @enforce_parameter_types
    def duration(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Duration", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def force_results_are_overridden(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceResultsAreOverridden")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def inner_ring_angular_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingAngularRotation")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_angular_rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_angular_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingAngularRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def inner_ring_angular_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "InnerRingAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @inner_ring_angular_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def inner_ring_angular_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "InnerRingAngularVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def orientation(self: "Self") -> "_2166.Orientations":
        """mastapy.bearings.bearing_results.Orientations"""
        temp = pythonnet_property_get(self.wrapped, "Orientation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bearings.bearing_results._2166", "Orientations"
        )(value)

    @orientation.setter
    @exception_bridge
    @enforce_parameter_types
    def orientation(self: "Self", value: "_2166.Orientations") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bearings.BearingResults.Orientations"
        )
        pythonnet_property_set(self.wrapped, "Orientation", value)

    @property
    @exception_bridge
    def outer_ring_angular_rotation(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingAngularRotation")

        if temp is None:
            return 0.0

        return temp

    @outer_ring_angular_rotation.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_angular_rotation(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRingAngularRotation",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_ring_angular_velocity(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OuterRingAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @outer_ring_angular_velocity.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_ring_angular_velocity(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterRingAngularVelocity",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def relative_angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_axial_displacement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeAxialDisplacement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relative_radial_displacement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelativeRadialDisplacement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def signed_relative_angular_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SignedRelativeAngularVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def specified_axial_internal_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedAxialInternalClearance")

        if temp is None:
            return 0.0

        return temp

    @specified_axial_internal_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_axial_internal_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedAxialInternalClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def specified_radial_internal_clearance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SpecifiedRadialInternalClearance")

        if temp is None:
            return 0.0

        return temp

    @specified_radial_internal_clearance.setter
    @exception_bridge
    @enforce_parameter_types
    def specified_radial_internal_clearance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SpecifiedRadialInternalClearance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def bearing(self: "Self") -> "_2340.BearingDesign":
        """mastapy.bearings.bearing_designs.BearingDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bearing")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def force_on_inner_race(
        self: "Self",
    ) -> "_1748.VectorWithLinearAndAngularComponents":
        """mastapy.math_utility.measured_vectors.VectorWithLinearAndAngularComponents

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceOnInnerRace")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def ring_results(self: "Self") -> "List[_2276.RingForceAndDisplacement]":
        """List[mastapy.bearings.bearing_results.rolling.RingForceAndDisplacement]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RingResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBearingResults":
        """Cast to another type.

        Returns:
            _Cast_LoadedBearingResults
        """
        return _Cast_LoadedBearingResults(self)
