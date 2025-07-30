"""LoadedBolt"""

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
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_LOADED_BOLT = python_net_import("SMT.MastaAPI.Bolts", "LoadedBolt")

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bolts import _1650, _1662, _1666, _1672

    Self = TypeVar("Self", bound="LoadedBolt")
    CastSelf = TypeVar("CastSelf", bound="LoadedBolt._Cast_LoadedBolt")


__docformat__ = "restructuredtext en"
__all__ = ("LoadedBolt",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_LoadedBolt:
    """Special nested class for casting LoadedBolt to subclasses."""

    __parent__: "LoadedBolt"

    @property
    def loaded_bolt(self: "CastSelf") -> "LoadedBolt":
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
class LoadedBolt(_0.APIBase):
    """LoadedBolt

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _LOADED_BOLT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def additional_axial_bolt_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalAxialBoltLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def additional_axial_bolt_load_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AdditionalAxialBoltLoadInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def additional_bending_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalBendingMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def additional_bending_moment_in_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalBendingMomentInBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def additional_bolt_load_after_opening(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdditionalBoltLoadAfterOpening")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def alternating_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlternatingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def alternating_stress_eccentric(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AlternatingStressEccentric")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def assembly_preload(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "AssemblyPreload")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @assembly_preload.setter
    @exception_bridge
    @enforce_parameter_types
    def assembly_preload(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "AssemblyPreload", value)

    @property
    @exception_bridge
    def assembly_temperature(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AssemblyTemperature")

        if temp is None:
            return 0.0

        return temp

    @assembly_temperature.setter
    @exception_bridge
    @enforce_parameter_types
    def assembly_temperature(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AssemblyTemperature",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def average_bolt_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageBoltLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_bolt_load_maximum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageBoltLoadMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_bolt_load_minimum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageBoltLoadMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_load_type(self: "Self") -> "_1650.AxialLoadType":
        """mastapy.bolts.AxialLoadType"""
        temp = pythonnet_property_get(self.wrapped, "AxialLoadType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.AxialLoadType")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1650", "AxialLoadType"
        )(value)

    @axial_load_type.setter
    @exception_bridge
    @enforce_parameter_types
    def axial_load_type(self: "Self", value: "_1650.AxialLoadType") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.AxialLoadType")
        pythonnet_property_set(self.wrapped, "AxialLoadType", value)

    @property
    @exception_bridge
    def axial_load_at_opening_limit_concentric_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AxialLoadAtOpeningLimitConcentricLoading"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_load_at_opening_limit_eccentric_loading(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AxialLoadAtOpeningLimitEccentricLoading"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_load_at_opening_limit_eccentric_loading_from_5329(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AxialLoadAtOpeningLimitEccentricLoadingFrom5329"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def axial_load_at_which_opening_occurs_during_eccentric_loading(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AxialLoadAtWhichOpeningOccursDuringEccentricLoading"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_angle(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BendingAngle")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bending_moment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BendingMoment")

        if temp is None:
            return 0.0

        return temp

    @bending_moment.setter
    @exception_bridge
    @enforce_parameter_types
    def bending_moment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "BendingMoment", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def bending_moment_at_bolting_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "BendingMomentAtBoltingPoint")

        if temp is None:
            return 0.0

        return temp

    @bending_moment_at_bolting_point.setter
    @exception_bridge
    @enforce_parameter_types
    def bending_moment_at_bolting_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "BendingMomentAtBoltingPoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def breaking_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BreakingForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_preload_due_to_thermal_expansion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInPreloadDueToThermalExpansion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_temperature_of_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChangeInTemperatureOfBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_temperature_of_clamped_parts(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ChangeInTemperatureOfClampedParts")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clamp_load_at_opening_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClampLoadAtOpeningLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def clamping_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ClampingLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def comparative_stress_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComparativeStressInAssembledState")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def comparative_stress_in_assembled_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ComparativeStressInAssembledStateMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def comparative_stress_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComparativeStressInWorkingState")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def comparative_stress_in_working_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ComparativeStressInWorkingStateMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def comparative_stress_in_working_state_minimum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ComparativeStressInWorkingStateMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def correction_factor_c1(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CorrectionFactorC1")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def correction_factor_c3(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CorrectionFactorC3")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_between_edge_of_preloading_area_and_force_introduction_point(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceBetweenEdgeOfPreloadingAreaAndForceIntroductionPoint"
        )

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @distance_between_edge_of_preloading_area_and_force_introduction_point.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_between_edge_of_preloading_area_and_force_introduction_point(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(
            self.wrapped,
            "DistanceBetweenEdgeOfPreloadingAreaAndForceIntroductionPoint",
            value,
        )

    @property
    @exception_bridge
    def distance_of_edge_bearing_point_v_from_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DistanceOfEdgeBearingPointVFromCentre"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def distance_of_line_of_action_of_axial_load_from_centre(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "DistanceOfLineOfActionOfAxialLoadFromCentre"
        )

        if temp is None:
            return 0.0

        return temp

    @distance_of_line_of_action_of_axial_load_from_centre.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_of_line_of_action_of_axial_load_from_centre(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceOfLineOfActionOfAxialLoadFromCentre",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def does_tightening_technique_exceed_yield_point(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DoesTighteningTechniqueExceedYieldPoint"
        )

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def edge_distance_of_opening_point_u(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EdgeDistanceOfOpeningPointU")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def effective_diameter_of_friction_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EffectiveDiameterOfFrictionMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ElasticResilienceOfBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_bolt_at_room_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticResilienceOfBoltAtRoomTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_bolt_in_operating_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticResilienceOfBoltInOperatingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def elastic_resilience_of_plates_at_room_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ElasticResilienceOfPlatesAtRoomTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_maximum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueSafetyFactorMaximumRequiredAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_minimum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueSafetyFactorMinimumRequiredAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueSafetyFactorInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueSafetyFactorInWorkingState")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_in_the_assembled_state_maximum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "FatigueSafetyFactorInTheAssembledStateMaximumRequiredAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_in_the_assembled_state_minimum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "FatigueSafetyFactorInTheAssembledStateMinimumRequiredAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def joint_type(self: "Self") -> "_1666.JointTypes":
        """mastapy.bolts.JointTypes"""
        temp = pythonnet_property_get(self.wrapped, "JointType")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Bolts.JointTypes")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1666", "JointTypes"
        )(value)

    @joint_type.setter
    @exception_bridge
    @enforce_parameter_types
    def joint_type(self: "Self", value: "_1666.JointTypes") -> None:
        value = conversion.mp_to_pn_enum(value, "SMT.MastaAPI.Bolts.JointTypes")
        pythonnet_property_set(self.wrapped, "JointType", value)

    @property
    @exception_bridge
    def joint_is_to_be_designed_with_f_qmax(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "JointIsToBeDesignedWithFQmax")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def length_between_basic_solid_and_load_introduction_point_k(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "LengthBetweenBasicSolidAndLoadIntroductionPointK"
        )

        if temp is None:
            return 0.0

        return temp

    @length_between_basic_solid_and_load_introduction_point_k.setter
    @exception_bridge
    @enforce_parameter_types
    def length_between_basic_solid_and_load_introduction_point_k(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "LengthBetweenBasicSolidAndLoadIntroductionPointK",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def limiting_slip_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingSlipForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_surface_pressure_on_head_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingSurfacePressureOnHeadSide")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def limiting_surface_pressure_on_nut_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LimitingSurfacePressureOnNutSide")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor_bending(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadFactorBending")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor_phi_stare_k(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadFactorPhiStareK")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor_for_concentric_clamping(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadFactorForConcentricClamping")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor_for_concentric_clamping_in_operating_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadFactorForConcentricClampingInOperatingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor_for_eccentric_clamping(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadFactorForEccentricClamping")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_factor_for_eccentric_clamping_and_concentric_load_introduction(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadFactorForEccentricClampingAndConcentricLoadIntroduction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_introduction_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "LoadIntroductionFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @load_introduction_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def load_introduction_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "LoadIntroductionFactor", value)

    @property
    @exception_bridge
    def load_at_minimum_yield_point(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadAtMinimumYieldPoint")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def loss_of_preload_due_to_embedding(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LossOfPreloadDueToEmbedding")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_additional_axial_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAdditionalAxialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumAssemblyPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_assembly_preload_during_assembly(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumAssemblyPreloadDuringAssembly"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_axial_load(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumAxialLoad")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_axial_load.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_axial_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumAxialLoad", value)

    @property
    @exception_bridge
    def maximum_head_surface_pressure_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumHeadSurfacePressureInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_head_surface_pressure_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumHeadSurfacePressureInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_nut_surface_pressure_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNutSurfacePressureInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_nut_surface_pressure_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumNutSurfacePressureInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_preload_maximum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPreloadMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_preload_minimum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPreloadMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_preload_in_assembled_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPreloadInAssembledStateMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pressure_to_be_sealed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumPressureToBeSealed")

        if temp is None:
            return 0.0

        return temp

    @maximum_pressure_to_be_sealed.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_pressure_to_be_sealed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumPressureToBeSealed",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_relieving_load_of_plates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumRelievingLoadOfPlates")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_stress_in_bending_tension_of_bolt_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumStressInBendingTensionOfBoltThread"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_surface_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumSurfacePressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_surface_pressure_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSurfacePressureInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_surface_pressure_in_assembled_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSurfacePressureInAssembledStateMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_surface_pressure_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSurfacePressureInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_surface_pressure_in_working_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSurfacePressureInWorkingStateMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_surface_pressure_in_working_state_minimum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumSurfacePressureInWorkingStateMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tensile_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTensileStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tensile_stress_in_working_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumTensileStressInWorkingStateMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_tensile_stress_in_working_state_minimum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumTensileStressInWorkingStateMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_torque_about_bolt_axis(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTorqueAboutBoltAxis")

        if temp is None:
            return 0.0

        return temp

    @maximum_torque_about_bolt_axis.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_torque_about_bolt_axis(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumTorqueAboutBoltAxis",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_torsional_moment(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTorsionalMoment")

        if temp is None:
            return 0.0

        return temp

    @maximum_torsional_moment.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_torsional_moment(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "MaximumTorsionalMoment",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def maximum_torsional_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTorsionalStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_torsional_stress_due_to_fq(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumTorsionalStressDueToFQ")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_transverse_load(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MaximumTransverseLoad")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @maximum_transverse_load.setter
    @exception_bridge
    @enforce_parameter_types
    def maximum_transverse_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MaximumTransverseLoad", value)

    @property
    @exception_bridge
    def minimum_additional_axial_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAdditionalAxialLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumAssemblyPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_assembly_preload_during_assembly(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumAssemblyPreloadDuringAssembly"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_axial_load(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "MinimumAxialLoad")

        if temp is None:
            return 0.0

        return temp

    @minimum_axial_load.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_axial_load(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "MinimumAxialLoad", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def minimum_clamp_load_for_ensuring_a_sealing_function(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumClampLoadForEnsuringASealingFunction"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_clamp_load_at_the_opening_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumClampLoadAtTheOpeningLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_clamp_load_for_transmitting_transverse_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumClampLoadForTransmittingTransverseLoad"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_effective_length_of_engagement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumEffectiveLengthOfEngagement"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_length_of_engagement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLengthOfEngagement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_nominal_diameter(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumNominalDiameter")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_required_clamping_force(
        self: "Self",
    ) -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumRequiredClampingForce")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_required_clamping_force.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_required_clamping_force(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumRequiredClampingForce", value)

    @property
    @exception_bridge
    def minimum_residual_clamp_load(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "MinimumResidualClampLoad")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @minimum_residual_clamp_load.setter
    @exception_bridge
    @enforce_parameter_types
    def minimum_residual_clamp_load(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "MinimumResidualClampLoad", value)

    @property
    @exception_bridge
    def minimum_residual_clamp_load_maximum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumResidualClampLoadMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_residual_clamp_load_minimum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumResidualClampLoadMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_residual_clamp_load_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumResidualClampLoadInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_stress_in_bending_tension_of_bolt_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumStressInBendingTensionOfBoltThread"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_alternating_cycles_during_continuous_loading(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfAlternatingCyclesDuringContinuousLoading"
        )

        if temp is None:
            return 0.0

        return temp

    @number_of_alternating_cycles_during_continuous_loading.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_alternating_cycles_during_continuous_loading(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfAlternatingCyclesDuringContinuousLoading",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_alternating_cycles_during_loading_within_fatigue_range(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "NumberOfAlternatingCyclesDuringLoadingWithinFatigueRange"
        )

        if temp is None:
            return 0.0

        return temp

    @number_of_alternating_cycles_during_loading_within_fatigue_range.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_alternating_cycles_during_loading_within_fatigue_range(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "NumberOfAlternatingCyclesDuringLoadingWithinFatigueRange",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def number_of_bearing_areas(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfBearingAreas")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_steps_for_f_mmax_table_a7(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsForFMmaxTableA7")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def number_of_steps_for_f_mmin_table_a7(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfStepsForFMminTableA7")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def operating_temperature_of_bolt(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "OperatingTemperatureOfBolt")

        if temp is None:
            return 0.0

        return temp

    @operating_temperature_of_bolt.setter
    @exception_bridge
    @enforce_parameter_types
    def operating_temperature_of_bolt(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OperatingTemperatureOfBolt",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def operating_temperature_of_clamped_parts(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "OperatingTemperatureOfClampedParts"
        )

        if temp is None:
            return 0.0

        return temp

    @operating_temperature_of_clamped_parts.setter
    @exception_bridge
    @enforce_parameter_types
    def operating_temperature_of_clamped_parts(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OperatingTemperatureOfClampedParts",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def parameter_of_circle_equation_mk(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterOfCircleEquationMK")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def parameter_of_circle_equation_nk(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ParameterOfCircleEquationNK")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleAssemblyPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_assembly_preload_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PermissibleAssemblyPreloadAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permissible_shearing_force_of_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermissibleShearingForceOfBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def permitted_assembly_reduced_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PermittedAssemblyReducedStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def plastic_deformation_due_to_embedding(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PlasticDeformationDueToEmbedding")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def polar_moment_of_resistance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PolarMomentOfResistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def preload(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Preload")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @property
    @exception_bridge
    def preload_at_opening_limit(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PreloadAtOpeningLimit")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def preload_at_room_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PreloadAtRoomTemperature")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def preload_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PreloadInAssembledState")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def present_effective_length_of_engagement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "PresentEffectiveLengthOfEngagement"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def present_length_of_engagement(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PresentLengthOfEngagement")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def proportion_of_tightening_torque_in_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ProportionOfTighteningTorqueInThread"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def relieving_load_of_plates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RelievingLoadOfPlates")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def residual_transverse_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResidualTransverseLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def resulting_moment_in_clamping_area(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResultingMomentInClampingArea")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shearing_cross_section_of_bolt_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearingCrossSectionOfBoltThread")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shearing_cross_section_of_nut_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearingCrossSectionOfNutThread")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shearing_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShearingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlippingSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_safety_factor_maximum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlippingSafetyFactorMaximumRequiredAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_safety_factor_minimum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlippingSafetyFactorMinimumRequiredAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_safety_factor_in_the_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SlippingSafetyFactorInTheAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_safety_factor_in_the_assembled_state_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SlippingSafetyFactorInTheAssembledStateMaximumAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def slipping_safety_factor_in_the_assembled_state_minimum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SlippingSafetyFactorInTheAssembledStateMinimumAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def strength_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrengthRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_endurance_limit_sg(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressAmplitudeOfEnduranceLimitSG")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_endurance_limit_sg_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAmplitudeOfEnduranceLimitSGMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_endurance_limit_sg_minimum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAmplitudeOfEnduranceLimitSGMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_endurance_limit_sv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressAmplitudeOfEnduranceLimitSV")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_fatigue_strength_sg(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAmplitudeOfFatigueStrengthSG"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_fatigue_strength_sg_maximum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAmplitudeOfFatigueStrengthSGMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_fatigue_strength_sg_minimum_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAmplitudeOfFatigueStrengthSGMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_amplitude_of_fatigue_strength_sv(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressAmplitudeOfFatigueStrengthSV"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stress_in_bending_tension_of_bolt_thread(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressInBendingTensionOfBoltThread"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def stripping_force(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StrippingForce")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SurfacePressureSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_maximum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorMaximumRequiredAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_minimum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorMinimumRequiredAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_in_the_assembled_state_minimum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "SurfacePressureSafetyFactorInTheAssembledStateMinimumRequiredAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_on_head_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorOnHeadSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_on_head_side_in_working_state(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorOnHeadSideInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_on_nut_side(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorOnNutSide"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def surface_pressure_safety_factor_on_nut_side_in_working_state(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SurfacePressureSafetyFactorOnNutSideInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tabular_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TabularAssemblyPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tabular_tightening_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TabularTighteningTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tensile_stress_due_to_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TensileStressDueToAssemblyPreload")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def theoretical_load_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TheoreticalLoadFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tightening_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "TighteningFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @tightening_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def tightening_factor(
        self: "Self", value: "Union[float, Tuple[float, bool]]"
    ) -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "TighteningFactor", value)

    @property
    @exception_bridge
    def tightening_technique(self: "Self") -> "_1672.TighteningTechniques":
        """mastapy.bolts.TighteningTechniques"""
        temp = pythonnet_property_get(self.wrapped, "TighteningTechnique")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.Bolts.TighteningTechniques"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.bolts._1672", "TighteningTechniques"
        )(value)

    @tightening_technique.setter
    @exception_bridge
    @enforce_parameter_types
    def tightening_technique(self: "Self", value: "_1672.TighteningTechniques") -> None:
        value = conversion.mp_to_pn_enum(
            value, "SMT.MastaAPI.Bolts.TighteningTechniques"
        )
        pythonnet_property_set(self.wrapped, "TighteningTechnique", value)

    @property
    @exception_bridge
    def tightening_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TighteningTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tightening_torque_maximum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TighteningTorqueMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tightening_torque_minimum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TighteningTorqueMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torsional_stress_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorsionalStressInAssembledState")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bending_moment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalBendingMoment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bending_moment_in_bolt(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalBendingMomentInBolt")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bending_moment_in_plates(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalBendingMomentInPlates")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bolt_load(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalBoltLoad")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bolt_load_maximum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalBoltLoadMaximumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_bolt_load_minimum_assembly_preload(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalBoltLoadMinimumAssemblyPreload"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yield_point_safety_factor_in_assembled_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "YieldPointSafetyFactorInAssembledState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yield_point_safety_factor_in_assembled_state_maximum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "YieldPointSafetyFactorInAssembledStateMaximumRequiredAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yield_point_safety_factor_in_working_state(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "YieldPointSafetyFactorInWorkingState"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yield_point_safety_factor_in_working_state_maximum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "YieldPointSafetyFactorInWorkingStateMaximumRequiredAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def yield_point_safety_factor_in_working_state_minimum_required_assembly_preload(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "YieldPointSafetyFactorInWorkingStateMinimumRequiredAssemblyPreload",
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def bolt(self: "Self") -> "_1662.DetailedBoltDesign":
        """mastapy.bolts.DetailedBoltDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Bolt")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_vector(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "LoadVector")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @load_vector.setter
    @exception_bridge
    @enforce_parameter_types
    def load_vector(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "LoadVector", value)

    @property
    @exception_bridge
    def report_names(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReportNames")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def output_default_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputDefaultReportTo", file_path)

    @exception_bridge
    def get_default_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetDefaultReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportTo", file_path)

    @exception_bridge
    @enforce_parameter_types
    def output_active_report_as_text_to(self: "Self", file_path: "PathLike") -> None:
        """Method does not return.

        Args:
            file_path (PathLike)
        """
        file_path = str(file_path)
        pythonnet_method_call(self.wrapped, "OutputActiveReportAsTextTo", file_path)

    @exception_bridge
    def get_active_report_with_encoded_images(self: "Self") -> "str":
        """str"""
        method_result = pythonnet_method_call(
            self.wrapped, "GetActiveReportWithEncodedImages"
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_masta_report(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsMastaReport",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def output_named_report_as_text_to(
        self: "Self", report_name: "str", file_path: "PathLike"
    ) -> None:
        """Method does not return.

        Args:
            report_name (str)
            file_path (PathLike)
        """
        report_name = str(report_name)
        file_path = str(file_path)
        pythonnet_method_call(
            self.wrapped,
            "OutputNamedReportAsTextTo",
            report_name if report_name else "",
            file_path,
        )

    @exception_bridge
    @enforce_parameter_types
    def get_named_report_with_encoded_images(self: "Self", report_name: "str") -> "str":
        """str

        Args:
            report_name (str)
        """
        report_name = str(report_name)
        method_result = pythonnet_method_call(
            self.wrapped,
            "GetNamedReportWithEncodedImages",
            report_name if report_name else "",
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_LoadedBolt":
        """Cast to another type.

        Returns:
            _Cast_LoadedBolt
        """
        return _Cast_LoadedBolt(self)
