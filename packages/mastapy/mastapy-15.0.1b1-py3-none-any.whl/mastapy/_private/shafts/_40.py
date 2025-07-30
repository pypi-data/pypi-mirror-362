"""ShaftSectionEndDamageResults"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
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
from mastapy._private._math.vector_3d import Vector3D

_SHAFT_SECTION_END_DAMAGE_RESULTS = python_net_import(
    "SMT.MastaAPI.Shafts", "ShaftSectionEndDamageResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.materials import _370
    from mastapy._private.nodal_analysis import _90
    from mastapy._private.shafts import _16, _17, _29, _47

    Self = TypeVar("Self", bound="ShaftSectionEndDamageResults")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ShaftSectionEndDamageResults._Cast_ShaftSectionEndDamageResults",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ShaftSectionEndDamageResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftSectionEndDamageResults:
    """Special nested class for casting ShaftSectionEndDamageResults to subclasses."""

    __parent__: "ShaftSectionEndDamageResults"

    @property
    def shaft_section_end_damage_results(
        self: "CastSelf",
    ) -> "ShaftSectionEndDamageResults":
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
class ShaftSectionEndDamageResults(_0.APIBase):
    """ShaftSectionEndDamageResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_SECTION_END_DAMAGE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def displacement_angular(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def displacement_axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementAxial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def displacement_linear(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementLinear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def displacement_radial_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementRadialMagnitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def displacement_radial_tilt_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementRadialTiltMagnitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def displacement_twist(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementTwist")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def equivalent_alternating_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "EquivalentAlternatingStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FatigueSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def fatigue_safety_factor_for_infinite_life(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "FatigueSafetyFactorForInfiniteLife"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_angular(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def force_axial(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAxial")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_linear(self: "Self") -> "Vector3D":
        """Vector3D

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceLinear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def force_radial_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceRadialMagnitude")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_torque(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceTorque")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def offset(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Offset")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def outer_diameter_to_achieve_fatigue_safety_factor_requirement(
        self: "Self",
    ) -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "OuterDiameterToAchieveFatigueSafetyFactorRequirement"
        )

        if temp is None:
            return 0.0

        return temp

    @outer_diameter_to_achieve_fatigue_safety_factor_requirement.setter
    @exception_bridge
    @enforce_parameter_types
    def outer_diameter_to_achieve_fatigue_safety_factor_requirement(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "OuterDiameterToAchieveFatigueSafetyFactorRequirement",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def outer_radius_to_achieve_shaft_fatigue_safety_factor_requirement(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "OuterRadiusToAchieveShaftFatigueSafetyFactorRequirement"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def reliability_for_infinite_life(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ReliabilityForInfiniteLife")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def section_end(self: "Self") -> "_90.SectionEnd":
        """mastapy.nodal_analysis.SectionEnd

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SectionEnd")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(temp, "SMT.MastaAPI.NodalAnalysis.SectionEnd")

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._90", "SectionEnd"
        )(value)

    @property
    @exception_bridge
    def shaft_reliability(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftReliability")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_number_of_cycles(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalNumberOfCycles")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def din743201212_component_fatigue_limit_under_reversed_stress_sigma_zd_wk_sigma_bwk_tau_twk(
        self: "Self",
    ) -> "_47.StressMeasurementShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.StressMeasurementShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DIN743201212ComponentFatigueLimitUnderReversedStressSigmaZdWKSigmaBWKTauTWK",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_component_yield_point_sigma_zd_fk_sigma_bfk_tau_tfk(
        self: "Self",
    ) -> "_47.StressMeasurementShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.StressMeasurementShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DIN743201212ComponentYieldPointSigmaZdFKSigmaBFKTauTFK"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_influence_factor_for_mean_stress_sensitivity_psi_sigma_k_psi_tau_k(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DIN743201212InfluenceFactorForMeanStressSensitivityPsiSigmaKPsiTauK",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fkm_guideline_6th_edition_2012_cyclic_degree_of_utilization_for_finite_life(
        self: "Self",
    ) -> "_17.ShaftAxialBendingXBendingYTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingXBendingYTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForFiniteLife",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def fkm_guideline_6th_edition_2012_cyclic_degree_of_utilization_for_infinite_life(
        self: "Self",
    ) -> "_17.ShaftAxialBendingXBendingYTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingXBendingYTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "FKMGuideline6thEdition2012CyclicDegreeOfUtilizationForInfiniteLife",
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sn_curve(self: "Self") -> "_370.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurve")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sn_curve_axial(self: "Self") -> "_370.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurveAxial")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sn_curve_bending_x(self: "Self") -> "_370.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurveBendingX")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sn_curve_bending_y(self: "Self") -> "_370.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurveBendingY")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def sn_curve_torsional(self: "Self") -> "_370.SNCurve":
        """mastapy.materials.SNCurve

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SNCurveTorsional")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def stress_concentration_factors(
        self: "Self",
    ) -> "_16.ShaftAxialBendingTorsionalComponentValues":
        """mastapy.shafts.ShaftAxialBendingTorsionalComponentValues

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressConcentrationFactors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def din743201212_stress_amplitude_of_component_fatigue_strength_sigma_zd_adk_sigma_badk_tau_tadk(
        self: "Self",
    ) -> "List[_47.StressMeasurementShaftAxialBendingTorsionalComponentValues]":
        """List[mastapy.shafts.StressMeasurementShaftAxialBendingTorsionalComponentValues]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped,
            "DIN743201212StressAmplitudeOfComponentFatigueStrengthSigmaZdADKSigmaBADKTauTADK",
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def stress_cycles(self: "Self") -> "List[_29.ShaftPointStressCycleReporting]":
        """List[mastapy.shafts.ShaftPointStressCycleReporting]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StressCycles")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

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
    def cast_to(self: "Self") -> "_Cast_ShaftSectionEndDamageResults":
        """Cast to another type.

        Returns:
            _Cast_ShaftSectionEndDamageResults
        """
        return _Cast_ShaftSectionEndDamageResults(self)
