"""GeneralTransmissionProperties"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_get_with_method,
    pythonnet_property_set,
    pythonnet_property_set_with_method,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_DATABASE_WITH_SELECTED_ITEM = python_net_import(
    "SMT.MastaAPI.UtilityGUI.Databases", "DatabaseWithSelectedItem"
)
_GENERAL_TRANSMISSION_PROPERTIES = python_net_import(
    "SMT.MastaAPI.Materials", "GeneralTransmissionProperties"
)

if TYPE_CHECKING:
    from typing import Any, Tuple, Type, TypeVar, Union

    from mastapy._private.materials import (
        _330,
        _344,
        _348,
        _356,
        _377,
        _379,
        _380,
        _381,
    )

    Self = TypeVar("Self", bound="GeneralTransmissionProperties")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GeneralTransmissionProperties._Cast_GeneralTransmissionProperties",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GeneralTransmissionProperties",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GeneralTransmissionProperties:
    """Special nested class for casting GeneralTransmissionProperties to subclasses."""

    __parent__: "GeneralTransmissionProperties"

    @property
    def general_transmission_properties(
        self: "CastSelf",
    ) -> "GeneralTransmissionProperties":
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
class GeneralTransmissionProperties(_0.APIBase):
    """GeneralTransmissionProperties

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GENERAL_TRANSMISSION_PROPERTIES

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def agma_over_load_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AGMAOverLoadFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @agma_over_load_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def agma_over_load_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AGMAOverLoadFactor", value)

    @property
    @exception_bridge
    def application_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "ApplicationFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @application_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def application_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "ApplicationFactor", value)

    @property
    @exception_bridge
    def bearing_iso762006_static_safety_factor_limit(
        self: "Self",
    ) -> "_348.ISO76StaticSafetyFactorLimits":
        """mastapy.materials.ISO76StaticSafetyFactorLimits"""
        temp = pythonnet_property_get(
            self.wrapped, "BearingISO762006StaticSafetyFactorLimit"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.ISO76StaticSafetyFactorLimits"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._348", "ISO76StaticSafetyFactorLimits"
        )(value)

    @bearing_iso762006_static_safety_factor_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def bearing_iso762006_static_safety_factor_limit(
        self: "Self", value: "_348.ISO76StaticSafetyFactorLimits"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.ISO76StaticSafetyFactorLimits"
        )
        pythonnet_property_set(
            self.wrapped, "BearingISO762006StaticSafetyFactorLimit", value
        )

    @property
    @exception_bridge
    def default_shaft_material(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "DefaultShaftMaterial", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @default_shaft_material.setter
    @exception_bridge
    @enforce_parameter_types
    def default_shaft_material(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "DefaultShaftMaterial",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit"
        )

        if temp is None:
            return 0.0

        return temp

    @drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def drawn_cup_needle_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DrawnCupNeedleRollerBearingsISO762006StaticSafetyFactorLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def driven_machine_characteristics(self: "Self") -> "_381.WorkingCharacteristics":
        """mastapy.materials.WorkingCharacteristics"""
        temp = pythonnet_property_get(self.wrapped, "DrivenMachineCharacteristics")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._381", "WorkingCharacteristics"
        )(value)

    @driven_machine_characteristics.setter
    @exception_bridge
    @enforce_parameter_types
    def driven_machine_characteristics(
        self: "Self", value: "_381.WorkingCharacteristics"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )
        pythonnet_property_set(self.wrapped, "DrivenMachineCharacteristics", value)

    @property
    @exception_bridge
    def driving_machine_characteristics(self: "Self") -> "_381.WorkingCharacteristics":
        """mastapy.materials.WorkingCharacteristics"""
        temp = pythonnet_property_get(self.wrapped, "DrivingMachineCharacteristics")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._381", "WorkingCharacteristics"
        )(value)

    @driving_machine_characteristics.setter
    @exception_bridge
    @enforce_parameter_types
    def driving_machine_characteristics(
        self: "Self", value: "_381.WorkingCharacteristics"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.WorkingCharacteristics"
        )
        pythonnet_property_set(self.wrapped, "DrivingMachineCharacteristics", value)

    @property
    @exception_bridge
    def energy_convergence_absolute_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "EnergyConvergenceAbsoluteTolerance"
        )

        if temp is None:
            return 0.0

        return temp

    @energy_convergence_absolute_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def energy_convergence_absolute_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "EnergyConvergenceAbsoluteTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def feed_flow_rate(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FeedFlowRate")

        if temp is None:
            return 0.0

        return temp

    @feed_flow_rate.setter
    @exception_bridge
    @enforce_parameter_types
    def feed_flow_rate(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FeedFlowRate", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def feed_pressure(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FeedPressure")

        if temp is None:
            return 0.0

        return temp

    @feed_pressure.setter
    @exception_bridge
    @enforce_parameter_types
    def feed_pressure(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "FeedPressure", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gearing_type(self: "Self") -> "_344.GearingTypes":
        """mastapy.materials.GearingTypes"""
        temp = pythonnet_property_get(self.wrapped, "GearingType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Materials.GearingTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._344", "GearingTypes"
        )(value)

    @gearing_type.setter
    @exception_bridge
    @enforce_parameter_types
    def gearing_type(self: "Self", value: "_344.GearingTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Materials.GearingTypes")
        pythonnet_property_set(self.wrapped, "GearingType", value)

    @property
    @exception_bridge
    def iso162812025_safety_factor_requirement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "ISO162812025SafetyFactorRequirement"
        )

        if temp is None:
            return 0.0

        return temp

    @iso162812025_safety_factor_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def iso162812025_safety_factor_requirement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ISO162812025SafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def iso2812007_safety_factor_requirement(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ISO2812007SafetyFactorRequirement")

        if temp is None:
            return 0.0

        return temp

    @iso2812007_safety_factor_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def iso2812007_safety_factor_requirement(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ISO2812007SafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def include_ansiabma_ratings(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IncludeANSIABMARatings")

        if temp is None:
            return False

        return temp

    @include_ansiabma_ratings.setter
    @exception_bridge
    @enforce_parameter_types
    def include_ansiabma_ratings(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "IncludeANSIABMARatings",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def linear_bearings_minimum_axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearBearingsMinimumAxialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_axial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_bearings_minimum_axial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearBearingsMinimumAxialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_bearings_minimum_radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearBearingsMinimumRadialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_radial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_bearings_minimum_radial_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearBearingsMinimumRadialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def linear_bearings_minimum_tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LinearBearingsMinimumTiltStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @linear_bearings_minimum_tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def linear_bearings_minimum_tilt_stiffness(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "LinearBearingsMinimumTiltStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def lubrication_detail_database(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get_with_method(
            self.wrapped, "LubricationDetailDatabase", "SelectedItemName"
        )

        if temp is None:
            return ""

        return temp

    @lubrication_detail_database.setter
    @exception_bridge
    @enforce_parameter_types
    def lubrication_detail_database(self: "Self", value: "str") -> None:
        pythonnet_property_set_with_method(
            self.wrapped,
            "LubricationDetailDatabase",
            "SetSelectedItem",
            str(value) if value is not None else "",
        )

    @property
    @exception_bridge
    def mass(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Mass")

        if temp is None:
            return 0.0

        return temp

    @mass.setter
    @exception_bridge
    @enforce_parameter_types
    def mass(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Mass", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def maximum_bearing_life_modification_factor(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumBearingLifeModificationFactor"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_bearing_life_modification_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_bearing_life_modification_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped, "MaximumBearingLifeModificationFactor", value
        )

    @property
    @exception_bridge
    def maximum_iso762006_static_safety_factor_for_a_loaded_bearing(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumISO762006StaticSafetyFactorForALoadedBearing"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_iso762006_static_safety_factor_for_a_loaded_bearing.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_iso762006_static_safety_factor_for_a_loaded_bearing(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumISO762006StaticSafetyFactorForALoadedBearing",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStaticContactSafetyFactorForLoadedGearsInAMesh"
        )

        if temp is None:
            return 0.0

        return temp

    @maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_static_contact_safety_factor_for_loaded_gears_in_a_mesh(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumStaticContactSafetyFactorForLoadedGearsInAMesh",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_force_for_bearing_to_be_considered_loaded(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumForceForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_force_for_bearing_to_be_considered_loaded.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_force_for_bearing_to_be_considered_loaded(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumForceForBearingToBeConsideredLoaded",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_moment_for_bearing_to_be_considered_loaded(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumMomentForBearingToBeConsideredLoaded"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_moment_for_bearing_to_be_considered_loaded.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_moment_for_bearing_to_be_considered_loaded(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumMomentForBearingToBeConsideredLoaded",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def minimum_static_safety_factor_for_maximum_contact_stress(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "MinimumStaticSafetyFactorForMaximumContactStress"
        )

        if temp is None:
            return 0.0

        return temp

    @minimum_static_safety_factor_for_maximum_contact_stress.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_static_safety_factor_for_maximum_contact_stress(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "MinimumStaticSafetyFactorForMaximumContactStress",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def non_linear_bearings_minimum_axial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearBearingsMinimumAxialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_axial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def non_linear_bearings_minimum_axial_stiffness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearBearingsMinimumAxialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def non_linear_bearings_minimum_radial_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearBearingsMinimumRadialStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_radial_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def non_linear_bearings_minimum_radial_stiffness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearBearingsMinimumRadialStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def non_linear_bearings_minimum_tilt_stiffness(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NonLinearBearingsMinimumTiltStiffness"
        )

        if temp is None:
            return 0.0

        return temp

    @non_linear_bearings_minimum_tilt_stiffness.setter
    @exception_bridge
    @enforce_parameter_types
    def non_linear_bearings_minimum_tilt_stiffness(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NonLinearBearingsMinimumTiltStiffness",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def permissible_track_truncation_ball_bearings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleTrackTruncationBallBearings"
        )

        if temp is None:
            return 0.0

        return temp

    @permissible_track_truncation_ball_bearings.setter
    @exception_bridge
    @enforce_parameter_types
    def permissible_track_truncation_ball_bearings(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "PermissibleTrackTruncationBallBearings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def power_convergence_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "PowerConvergenceTolerance")

        if temp is None:
            return 0.0

        return temp

    @power_convergence_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def power_convergence_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "PowerConvergenceTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def required_safety_factor_for_cvt_belt_clamping_force(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "RequiredSafetyFactorForCVTBeltClampingForce"
        )

        if temp is None:
            return 0.0

        return temp

    @required_safety_factor_for_cvt_belt_clamping_force.setter
    @exception_bridge
    @enforce_parameter_types
    def required_safety_factor_for_cvt_belt_clamping_force(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "RequiredSafetyFactorForCVTBeltClampingForce",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def safety_factor_against_plastic_strain(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorAgainstPlasticStrain")

        if temp is None:
            return 0.0

        return temp

    @safety_factor_against_plastic_strain.setter
    @exception_bridge
    @enforce_parameter_types
    def safety_factor_against_plastic_strain(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SafetyFactorAgainstPlasticStrain",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def safety_factor_against_sliding(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SafetyFactorAgainstSliding")

        if temp is None:
            return 0.0

        return temp

    @safety_factor_against_sliding.setter
    @exception_bridge
    @enforce_parameter_types
    def safety_factor_against_sliding(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SafetyFactorAgainstSliding",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped,
            "ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit",
        )

        if temp is None:
            return 0.0

        return temp

    @thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit.setter
    @exception_bridge
    @enforce_parameter_types
    def thrust_spherical_roller_bearings_iso762006_static_safety_factor_limit(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "ThrustSphericalRollerBearingsISO762006StaticSafetyFactorLimit",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def transmission_application(self: "Self") -> "_377.TransmissionApplications":
        """mastapy.materials.TransmissionApplications"""
        temp = pythonnet_property_get(self.wrapped, "TransmissionApplication")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.TransmissionApplications"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._377", "TransmissionApplications"
        )(value)

    @transmission_application.setter
    @exception_bridge
    @enforce_parameter_types
    def transmission_application(
        self: "Self", value: "_377.TransmissionApplications"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.TransmissionApplications"
        )
        pythonnet_property_set(self.wrapped, "TransmissionApplication", value)

    @property
    @exception_bridge
    def volume(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Volume")

        if temp is None:
            return 0.0

        return temp

    @volume.setter
    @exception_bridge
    @enforce_parameter_types
    def volume(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Volume", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def wind_turbine_standard(self: "Self") -> "_380.WindTurbineStandards":
        """mastapy.materials.WindTurbineStandards"""
        temp = pythonnet_property_get(self.wrapped, "WindTurbineStandard")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Materials.WindTurbineStandards"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.materials._380", "WindTurbineStandards"
        )(value)

    @wind_turbine_standard.setter
    @exception_bridge
    @enforce_parameter_types
    def wind_turbine_standard(self: "Self", value: "_380.WindTurbineStandards") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Materials.WindTurbineStandards"
        )
        pythonnet_property_set(self.wrapped, "WindTurbineStandard", value)

    @property
    @exception_bridge
    def zero_speed_tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ZeroSpeedTolerance")

        if temp is None:
            return 0.0

        return temp

    @zero_speed_tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def zero_speed_tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ZeroSpeedTolerance",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def air_properties(self: "Self") -> "_330.AirProperties":
        """mastapy.materials.AirProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AirProperties")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def lubrication_detail(self: "Self") -> "_356.LubricationDetail":
        """mastapy.materials.LubricationDetail

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LubricationDetail")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def vehicle_dynamics(self: "Self") -> "_379.VehicleDynamicsProperties":
        """mastapy.materials.VehicleDynamicsProperties

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "VehicleDynamics")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_GeneralTransmissionProperties":
        """Cast to another type.

        Returns:
            _Cast_GeneralTransmissionProperties
        """
        return _Cast_GeneralTransmissionProperties(self)
