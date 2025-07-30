"""ToothFlankFractureAnalysisPoint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
)

_TOOTH_FLANK_FRACTURE_ANALYSIS_POINT = python_net_import(
    "SMT.MastaAPI.Gears.Rating.Cylindrical.ISO6336", "ToothFlankFractureAnalysisPoint"
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    Self = TypeVar("Self", bound="ToothFlankFractureAnalysisPoint")
    CastSelf = TypeVar(
        "CastSelf",
        bound="ToothFlankFractureAnalysisPoint._Cast_ToothFlankFractureAnalysisPoint",
    )


__docformat__ = "restructuredtext en"
__all__ = ("ToothFlankFractureAnalysisPoint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ToothFlankFractureAnalysisPoint:
    """Special nested class for casting ToothFlankFractureAnalysisPoint to subclasses."""

    __parent__: "ToothFlankFractureAnalysisPoint"

    @property
    def tooth_flank_fracture_analysis_point(
        self: "CastSelf",
    ) -> "ToothFlankFractureAnalysisPoint":
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
class ToothFlankFractureAnalysisPoint(_0.APIBase):
    """ToothFlankFractureAnalysisPoint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _TOOTH_FLANK_FRACTURE_ANALYSIS_POINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def case_hardening_depth_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CaseHardeningDepthInfluenceFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def correction_factor_for_practice_oriented_calculation_approach_first(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CorrectionFactorForPracticeOrientedCalculationApproachFirst"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def correction_factor_for_practice_oriented_calculation_approach_second(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "CorrectionFactorForPracticeOrientedCalculationApproachSecond"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def depth_from_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DepthFromSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hardness_conversion_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HardnessConversionFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def hertzian_pressure_and_residual_stress_influence_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HertzianPressureAndResidualStressInfluenceFactor"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def influence_of_the_residual_stresses_on_the_local_equivalent_stress(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InfluenceOfTheResidualStressesOnTheLocalEquivalentStress"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_equivalent_stress_without_consideration_of_residual_stresses(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LocalEquivalentStressWithoutConsiderationOfResidualStresses"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_material_exposure(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalMaterialExposure")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_material_hardness(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalMaterialHardness")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_material_shear_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalMaterialShearStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_occurring_equivalent_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalOccurringEquivalentStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def local_tensile_strength(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LocalTensileStrength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_exposure_calibration_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialExposureCalibrationFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def material_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaterialFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def normalised_depth_from_surface(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NormalisedDepthFromSurface")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def quasi_stationary_residual_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "QuasiStationaryResidualStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def residual_stress_sensitivity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ResidualStressSensitivity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def tangential_component_of_compressive_residual_stresses(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TangentialComponentOfCompressiveResidualStresses"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    def cast_to(self: "Self") -> "_Cast_ToothFlankFractureAnalysisPoint":
        """Cast to another type.

        Returns:
            _Cast_ToothFlankFractureAnalysisPoint
        """
        return _Cast_ToothFlankFractureAnalysisPoint(self)
