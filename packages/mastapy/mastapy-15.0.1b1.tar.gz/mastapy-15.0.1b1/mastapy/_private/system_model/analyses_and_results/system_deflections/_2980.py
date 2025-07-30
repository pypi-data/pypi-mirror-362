"""CylindricalGearMeshSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)
from mastapy._private.system_model.analyses_and_results.system_deflections import _3000

_CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "CylindricalGearMeshSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears.rating.cylindrical import _549
    from mastapy._private.nodal_analysis import _58
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7882,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.power_flows import _4341
    from mastapy._private.system_model.analyses_and_results.static_loads import _7732
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2968,
        _2981,
        _2982,
        _2983,
        _2986,
        _2990,
        _3008,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3088,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2530
    from mastapy._private.utility.report import _1981

    Self = TypeVar("Self", bound="CylindricalGearMeshSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshSystemDeflection._Cast_CylindricalGearMeshSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshSystemDeflection:
    """Special nested class for casting CylindricalGearMeshSystemDeflection to subclasses."""

    __parent__: "CylindricalGearMeshSystemDeflection"

    @property
    def gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "_3000.GearMeshSystemDeflection":
        return self.__parent__._cast(_3000.GearMeshSystemDeflection)

    @property
    def inter_mountable_component_connection_system_deflection(
        self: "CastSelf",
    ) -> "_3008.InterMountableComponentConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _3008,
        )

        return self.__parent__._cast(
            _3008.InterMountableComponentConnectionSystemDeflection
        )

    @property
    def connection_system_deflection(
        self: "CastSelf",
    ) -> "_2968.ConnectionSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2968,
        )

        return self.__parent__._cast(_2968.ConnectionSystemDeflection)

    @property
    def connection_fe_analysis(self: "CastSelf") -> "_7882.ConnectionFEAnalysis":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7882,
        )

        return self.__parent__._cast(_7882.ConnectionFEAnalysis)

    @property
    def connection_static_load_analysis_case(
        self: "CastSelf",
    ) -> "_7883.ConnectionStaticLoadAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7883,
        )

        return self.__parent__._cast(_7883.ConnectionStaticLoadAnalysisCase)

    @property
    def connection_analysis_case(self: "CastSelf") -> "_7880.ConnectionAnalysisCase":
        from mastapy._private.system_model.analyses_and_results.analysis_cases import (
            _7880,
        )

        return self.__parent__._cast(_7880.ConnectionAnalysisCase)

    @property
    def connection_analysis(self: "CastSelf") -> "_2890.ConnectionAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2890

        return self.__parent__._cast(_2890.ConnectionAnalysis)

    @property
    def design_entity_single_context_analysis(
        self: "CastSelf",
    ) -> "_2894.DesignEntitySingleContextAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2894

        return self.__parent__._cast(_2894.DesignEntitySingleContextAnalysis)

    @property
    def design_entity_analysis(self: "CastSelf") -> "_2892.DesignEntityAnalysis":
        from mastapy._private.system_model.analyses_and_results import _2892

        return self.__parent__._cast(_2892.DesignEntityAnalysis)

    @property
    def cylindrical_gear_mesh_system_deflection_timestep(
        self: "CastSelf",
    ) -> "_2981.CylindricalGearMeshSystemDeflectionTimestep":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2981,
        )

        return self.__parent__._cast(_2981.CylindricalGearMeshSystemDeflectionTimestep)

    @property
    def cylindrical_gear_mesh_system_deflection_with_ltca_results(
        self: "CastSelf",
    ) -> "_2982.CylindricalGearMeshSystemDeflectionWithLTCAResults":
        from mastapy._private.system_model.analyses_and_results.system_deflections import (
            _2982,
        )

        return self.__parent__._cast(
            _2982.CylindricalGearMeshSystemDeflectionWithLTCAResults
        )

    @property
    def cylindrical_gear_mesh_system_deflection(
        self: "CastSelf",
    ) -> "CylindricalGearMeshSystemDeflection":
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
class CylindricalGearMeshSystemDeflection(_3000.GearMeshSystemDeflection):
    """CylindricalGearMeshSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def angular_misalignment_for_harmonic_analysis(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AngularMisalignmentForHarmonicAnalysis"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_interference_normal_to_the_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageInterferenceNormalToTheFlank"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_operating_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageOperatingBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_load_sharing_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedLoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def calculated_worst_load_sharing_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CalculatedWorstLoadSharingFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_backlash_due_to_tooth_expansion(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInBacklashDueToToothExpansion"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def change_in_operating_backlash_due_to_thermal_effects(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChangeInOperatingBacklashDueToThermalEffects"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def chart_of_misalignment_in_transverse_line_of_action(
        self: "Self",
    ) -> "_1981.SimpleChartDefinition":
        """mastapy.utility.report.SimpleChartDefinition

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ChartOfMisalignmentInTransverseLineOfAction"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def coefficient_of_friction(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CoefficientOfFriction")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def crowning_for_tilt_stiffness_gear_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrowningForTiltStiffnessGearA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def crowning_for_tilt_stiffness_gear_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CrowningForTiltStiffnessGearB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def estimated_operating_tooth_temperature(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "EstimatedOperatingToothTemperature"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def gear_mesh_tilt_stiffness_method(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshTiltStiffnessMethod")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def is_in_contact(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "IsInContact")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def linear_relief_for_tilt_stiffness_gear_a(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearReliefForTiltStiffnessGearA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def linear_relief_for_tilt_stiffness_gear_b(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LinearReliefForTiltStiffnessGearB")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def load_in_loa_from_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadInLOAFromLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_change_in_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumChangeInCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_operating_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumOperatingBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_operating_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumOperatingCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_operating_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumOperatingTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_change_in_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumChangeInCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_operating_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_operating_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumOperatingCentreDistance")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_operating_transverse_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MinimumOperatingTransverseContactRatio"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def node_pair_transverse_separations_for_ltca(self: "Self") -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "NodePairTransverseSeparationsForLTCA"
        )

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def pinion_torque_for_ltca(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinionTorqueForLTCA")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def separation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Separation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def separation_to_inactive_flank(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SeparationToInactiveFlank")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def signed_root_mean_square_planetary_equivalent_misalignment(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SignedRootMeanSquarePlanetaryEquivalentMisalignment"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def smallest_effective_operating_centre_distance(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "SmallestEffectiveOperatingCentreDistance"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transmission_error_including_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransmissionErrorIncludingBacklash"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transmission_error_no_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionErrorNoBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_planetary_misalignment(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstPlanetaryMisalignment")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def rating(self: "Self") -> "_549.CylindricalGearMeshRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Rating")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def component_detailed_analysis(self: "Self") -> "_549.CylindricalGearMeshRating":
        """mastapy.gears.rating.cylindrical.CylindricalGearMeshRating

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ComponentDetailedAnalysis")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_design(self: "Self") -> "_2530.CylindricalGearMesh":
        """mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def connection_load_case(self: "Self") -> "_7732.CylindricalGearMeshLoadCase":
        """mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ConnectionLoadCase")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_a(self: "Self") -> "_2986.CylindricalGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearA")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_b(self: "Self") -> "_2986.CylindricalGearSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearB")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignment_data(self: "Self") -> "_58.CylindricalMisalignmentCalculator":
        """mastapy.nodal_analysis.CylindricalMisalignmentCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentData")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignment_data_left_flank(
        self: "Self",
    ) -> "_58.CylindricalMisalignmentCalculator":
        """mastapy.nodal_analysis.CylindricalMisalignmentCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentDataLeftFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def misalignment_data_right_flank(
        self: "Self",
    ) -> "_58.CylindricalMisalignmentCalculator":
        """mastapy.nodal_analysis.CylindricalMisalignmentCalculator

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MisalignmentDataRightFlank")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def power_flow_results(self: "Self") -> "_4341.CylindricalGearMeshPowerFlow":
        """mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PowerFlowResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gears(
        self: "Self",
    ) -> "List[_2986.CylindricalGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGears")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_meshed_gear_system_deflections(
        self: "Self",
    ) -> "List[_2990.CylindricalMeshedGearSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalMeshedGearSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalMeshedGearSystemDeflections"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mesh_deflections_left_flank(
        self: "Self",
    ) -> "List[_3088.GearMeshResultsAtOffset]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.reporting.GearMeshResultsAtOffset]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshDeflectionsLeftFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mesh_deflections_right_flank(
        self: "Self",
    ) -> "List[_3088.GearMeshResultsAtOffset]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.reporting.GearMeshResultsAtOffset]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeshDeflectionsRightFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(self: "Self") -> "List[CylindricalGearMeshSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Planetaries")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_set(self: "Self") -> "_2983.CylindricalGearSetSystemDeflection":
        """mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearSetSystemDeflection

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearSet")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshSystemDeflection
        """
        return _Cast_CylindricalGearMeshSystemDeflection(self)
