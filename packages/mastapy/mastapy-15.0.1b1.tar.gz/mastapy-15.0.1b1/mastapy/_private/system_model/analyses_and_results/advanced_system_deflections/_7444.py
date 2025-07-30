"""CylindricalGearMeshAdvancedSystemDeflection"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from PIL.Image import Image

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
    _7456,
)

_CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections",
    "CylindricalGearMeshAdvancedSystemDeflection",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _412
    from mastapy._private.gears.cylindrical import _1334
    from mastapy._private.gears.gear_designs.cylindrical import _1122, _1128
    from mastapy._private.gears.rating.cylindrical import _549
    from mastapy._private.math_utility import _1697
    from mastapy._private.system_model.analyses_and_results import _2890, _2892, _2894
    from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
        _7430,
        _7432,
        _7443,
        _7462,
    )
    from mastapy._private.system_model.analyses_and_results.analysis_cases import (
        _7880,
        _7883,
    )
    from mastapy._private.system_model.analyses_and_results.static_loads import _7732
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _2981,
    )
    from mastapy._private.system_model.connections_and_sockets.gears import _2530

    Self = TypeVar("Self", bound="CylindricalGearMeshAdvancedSystemDeflection")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearMeshAdvancedSystemDeflection._Cast_CylindricalGearMeshAdvancedSystemDeflection",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearMeshAdvancedSystemDeflection",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearMeshAdvancedSystemDeflection:
    """Special nested class for casting CylindricalGearMeshAdvancedSystemDeflection to subclasses."""

    __parent__: "CylindricalGearMeshAdvancedSystemDeflection"

    @property
    def gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7456.GearMeshAdvancedSystemDeflection":
        return self.__parent__._cast(_7456.GearMeshAdvancedSystemDeflection)

    @property
    def inter_mountable_component_connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7462.InterMountableComponentConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7462,
        )

        return self.__parent__._cast(
            _7462.InterMountableComponentConnectionAdvancedSystemDeflection
        )

    @property
    def connection_advanced_system_deflection(
        self: "CastSelf",
    ) -> "_7430.ConnectionAdvancedSystemDeflection":
        from mastapy._private.system_model.analyses_and_results.advanced_system_deflections import (
            _7430,
        )

        return self.__parent__._cast(_7430.ConnectionAdvancedSystemDeflection)

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
    def cylindrical_gear_mesh_advanced_system_deflection(
        self: "CastSelf",
    ) -> "CylindricalGearMeshAdvancedSystemDeflection":
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
class CylindricalGearMeshAdvancedSystemDeflection(
    _7456.GearMeshAdvancedSystemDeflection
):
    """CylindricalGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def active_flank(self: "Self") -> "_412.CylindricalFlanks":
        """mastapy.gears.CylindricalFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.CylindricalFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._412", "CylindricalFlanks"
        )(value)

    @property
    @exception_bridge
    def average_operating_axial_contact_ratio_for_first_tooth_passing_period(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AverageOperatingAxialContactRatioForFirstToothPassingPeriod"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def average_operating_transverse_contact_ratio_for_first_tooth_passing_period(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "AverageOperatingTransverseContactRatioForFirstToothPassingPeriod",
        )

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
    def contact_chart_gap_to_loaded_flank_gear_a(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactChartGapToLoadedFlankGearA")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_chart_gap_to_loaded_flank_gear_b(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactChartGapToLoadedFlankGearB")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_chart_gap_to_unloaded_flank_gear_a(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactChartGapToUnloadedFlankGearA"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_chart_gap_to_unloaded_flank_gear_b(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ContactChartGapToUnloadedFlankGearB"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_chart_max_pressure_gear_a(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactChartMaxPressureGearA")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def contact_chart_max_pressure_gear_b(self: "Self") -> "Image":
        """Image

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ContactChartMaxPressureGearB")

        if temp is None:
            return None

        value = conversion.pn_to_mp_smt_bitmap(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def face_load_factor_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FaceLoadFactorContact")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def inactive_flank(self: "Self") -> "_412.CylindricalFlanks":
        """mastapy.gears.CylindricalFlanks

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "InactiveFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.Gears.CylindricalFlanks")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears._412", "CylindricalFlanks"
        )(value)

    @property
    @exception_bridge
    def maximum_contact_pressure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactPressure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_edge_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumEdgeStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_edge_stress_including_tip_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumEdgeStressIncludingTipContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_edge_stress_on_gear_a_including_tip_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumEdgeStressOnGearAIncludingTipContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_edge_stress_on_gear_b_including_tip_contact(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumEdgeStressOnGearBIncludingTipContact"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_principal_root_stress_on_tension_side_from_gear_fe_model(
        self: "Self",
    ) -> "List[float]":
        """List[float]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaximumPrincipalRootStressOnTensionSideFromGearFEModel"
        )

        if temp is None:
            return None

        value = conversion.to_list_any(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def mean_mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanMeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_mesh_tilt_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanMeshTiltStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_te_excluding_backlash(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanTEExcludingBacklash")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def mean_total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MeanTotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_to_peak_mesh_stiffness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakMeshStiffness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def peak_to_peak_te(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeakToPeakTE")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def torque_share(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TorqueShare")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def use_advanced_ltca(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseAdvancedLTCA")

        if temp is None:
            return False

        return temp

    @use_advanced_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def use_advanced_ltca(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "UseAdvancedLTCA", bool(value) if value is not None else False
        )

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
    def gear_mesh_design(self: "Self") -> "_1128.CylindricalGearMeshDesign":
        """mastapy.gears.gear_designs.cylindrical.CylindricalGearMeshDesign

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMeshDesign")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def points_with_worst_results(self: "Self") -> "_1334.PointsWithWorstResults":
        """mastapy.gears.cylindrical.PointsWithWorstResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PointsWithWorstResults")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transmission_error_fourier_series_for_first_tooth_passing_period(
        self: "Self",
    ) -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransmissionErrorFourierSeriesForFirstToothPassingPeriod"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cylindrical_gear_advanced_analyses(
        self: "Self",
    ) -> "List[_7443.CylindricalGearAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CylindricalGearAdvancedAnalyses")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def cylindrical_gear_mesh_system_deflection_results(
        self: "Self",
    ) -> "List[_2981.CylindricalGearMeshSystemDeflectionTimestep]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.CylindricalGearMeshSystemDeflectionTimestep]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CylindricalGearMeshSystemDeflectionResults"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def gear_designs(self: "Self") -> "List[_1122.CylindricalGearDesign]":
        """List[mastapy.gears.gear_designs.cylindrical.CylindricalGearDesign]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearDesigns")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def max_pressure_contact_chart_for_each_tooth_pass_for_gear_a(
        self: "Self",
    ) -> "List[_7432.ContactChartPerToothPass]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.ContactChartPerToothPass]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MaxPressureContactChartForEachToothPassForGearA"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def planetaries(
        self: "Self",
    ) -> "List[CylindricalGearMeshAdvancedSystemDeflection]":
        """List[mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection]

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

    @exception_bridge
    def animation_of_max_pressure_contact_chart_for_each_tooth_pass_for_gear_a(
        self: "Self",
    ) -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "AnimationOfMaxPressureContactChartForEachToothPassForGearA"
        )

    @exception_bridge
    def contact_chart_gap_to_loaded_flank_gear_a_as_text_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ContactChartGapToLoadedFlankGearAAsTextFile"
        )

    @exception_bridge
    def contact_chart_gap_to_loaded_flank_gear_b_as_text_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ContactChartGapToLoadedFlankGearBAsTextFile"
        )

    @exception_bridge
    def contact_chart_gap_to_unloaded_flank_gear_a_as_text_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ContactChartGapToUnloadedFlankGearAAsTextFile"
        )

    @exception_bridge
    def contact_chart_gap_to_unloaded_flank_gear_b_as_text_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(
            self.wrapped, "ContactChartGapToUnloadedFlankGearBAsTextFile"
        )

    @exception_bridge
    def contact_chart_max_pressure_gear_a_as_text_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ContactChartMaxPressureGearAAsTextFile")

    @exception_bridge
    def contact_chart_max_pressure_gear_b_as_text_file(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "ContactChartMaxPressureGearBAsTextFile")

    @property
    def cast_to(self: "Self") -> "_Cast_CylindricalGearMeshAdvancedSystemDeflection":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearMeshAdvancedSystemDeflection
        """
        return _Cast_CylindricalGearMeshAdvancedSystemDeflection(self)
