"""GearMeshLoadDistributionAnalysis"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import constructor, conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call_overload,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.gears.analysis import _1343

_GEAR_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearLoadDistributionAnalysis"
)
_GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS = python_net_import(
    "SMT.MastaAPI.Gears.LTCA", "GearMeshLoadDistributionAnalysis"
)
_GEAR_FLANKS = python_net_import("SMT.MastaAPI.Gears", "GearFlanks")
_STRESS_RESULTS_TYPE = python_net_import(
    "SMT.MastaAPI.NodalAnalysis", "StressResultsType"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private.gears import _415
    from mastapy._private.gears.analysis import _1336, _1342
    from mastapy._private.gears.ltca import _943, _945
    from mastapy._private.gears.ltca.conical import _973
    from mastapy._private.gears.ltca.cylindrical import _960
    from mastapy._private.math_utility import _1697
    from mastapy._private.nodal_analysis import _93

    Self = TypeVar("Self", bound="GearMeshLoadDistributionAnalysis")
    CastSelf = TypeVar(
        "CastSelf",
        bound="GearMeshLoadDistributionAnalysis._Cast_GearMeshLoadDistributionAnalysis",
    )


__docformat__ = "restructuredtext en"
__all__ = ("GearMeshLoadDistributionAnalysis",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_GearMeshLoadDistributionAnalysis:
    """Special nested class for casting GearMeshLoadDistributionAnalysis to subclasses."""

    __parent__: "GearMeshLoadDistributionAnalysis"

    @property
    def gear_mesh_implementation_analysis(
        self: "CastSelf",
    ) -> "_1343.GearMeshImplementationAnalysis":
        return self.__parent__._cast(_1343.GearMeshImplementationAnalysis)

    @property
    def gear_mesh_design_analysis(self: "CastSelf") -> "_1342.GearMeshDesignAnalysis":
        from mastapy._private.gears.analysis import _1342

        return self.__parent__._cast(_1342.GearMeshDesignAnalysis)

    @property
    def abstract_gear_mesh_analysis(
        self: "CastSelf",
    ) -> "_1336.AbstractGearMeshAnalysis":
        from mastapy._private.gears.analysis import _1336

        return self.__parent__._cast(_1336.AbstractGearMeshAnalysis)

    @property
    def cylindrical_gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_960.CylindricalGearMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.cylindrical import _960

        return self.__parent__._cast(_960.CylindricalGearMeshLoadDistributionAnalysis)

    @property
    def conical_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "_973.ConicalMeshLoadDistributionAnalysis":
        from mastapy._private.gears.ltca.conical import _973

        return self.__parent__._cast(_973.ConicalMeshLoadDistributionAnalysis)

    @property
    def gear_mesh_load_distribution_analysis(
        self: "CastSelf",
    ) -> "GearMeshLoadDistributionAnalysis":
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
class GearMeshLoadDistributionAnalysis(_1343.GearMeshImplementationAnalysis):
    """GearMeshLoadDistributionAnalysis

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _GEAR_MESH_LOAD_DISTRIBUTION_ANALYSIS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def actual_total_contact_ratio(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ActualTotalContactRatio")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def analysis_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AnalysisName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def average_actual_contact_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AverageActualContactLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def index_of_roll_angle_with_maximum_contact_stress(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "IndexOfRollAngleWithMaximumContactStress"
        )

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def is_advanced_ltca(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsAdvancedLTCA")

        if temp is None:
            return False

        return temp

    @is_advanced_ltca.setter
    @exception_bridge
    @enforce_parameter_types
    def is_advanced_ltca(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsAdvancedLTCA", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def load_case_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "LoadCaseName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def maximum_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_force_per_unit_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumForcePerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def maximum_pressure_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumPressureVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def minimum_force_per_unit_length(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumForcePerUnitLength")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def moment_about_centre_weighted_harmonic_sum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "MomentAboutCentreWeightedHarmonicSum"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def number_of_roll_angles(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "NumberOfRollAngles")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def peakto_peak_moment_about_centre(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PeaktoPeakMomentAboutCentre")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def transmission_error_weighted_harmonic_sum(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TransmissionErrorWeightedHarmonicSum"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def moment_about_centre_fourier_series(self: "Self") -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MomentAboutCentreFourierSeries")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def transmission_error_fourier_series(self: "Self") -> "_1697.FourierSeries":
        """mastapy.math_utility.FourierSeries

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TransmissionErrorFourierSeries")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def load_distribution_analyses_at_single_rotation(
        self: "Self",
    ) -> "List[_945.GearMeshLoadDistributionAtRotation]":
        """List[mastapy.gears.ltca.GearMeshLoadDistributionAtRotation]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "LoadDistributionAnalysesAtSingleRotation"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @exception_bridge
    @enforce_parameter_types
    def maximum_root_stress_with_flanks(
        self: "Self",
        gear: "_943.GearLoadDistributionAnalysis",
        flank: "_415.GearFlanks",
        stress_type: "_93.StressResultsType",
    ) -> "float":
        """float

        Args:
            gear (mastapy.gears.ltca.GearLoadDistributionAnalysis)
            flank (mastapy.gears.GearFlanks)
            stress_type (mastapy.nodal_analysis.StressResultsType)
        """
        flank = conversion.mp_to_pn_enum(flank, "SMT.MastaAPI.Gears.GearFlanks")
        stress_type = conversion.mp_to_pn_enum(
            stress_type, "SMT.MastaAPI.NodalAnalysis.StressResultsType"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "MaximumRootStress",
            [_GEAR_LOAD_DISTRIBUTION_ANALYSIS, _GEAR_FLANKS, _STRESS_RESULTS_TYPE],
            gear.wrapped if gear else None,
            flank,
            stress_type,
        )
        return method_result

    @exception_bridge
    @enforce_parameter_types
    def maximum_root_stress(
        self: "Self",
        gear: "_943.GearLoadDistributionAnalysis",
        stress_type: "_93.StressResultsType",
    ) -> "float":
        """float

        Args:
            gear (mastapy.gears.ltca.GearLoadDistributionAnalysis)
            stress_type (mastapy.nodal_analysis.StressResultsType)
        """
        stress_type = conversion.mp_to_pn_enum(
            stress_type, "SMT.MastaAPI.NodalAnalysis.StressResultsType"
        )
        method_result = pythonnet_method_call_overload(
            self.wrapped,
            "MaximumRootStress",
            [_GEAR_LOAD_DISTRIBUTION_ANALYSIS, _STRESS_RESULTS_TYPE],
            gear.wrapped if gear else None,
            stress_type,
        )
        return method_result

    @property
    def cast_to(self: "Self") -> "_Cast_GearMeshLoadDistributionAnalysis":
        """Cast to another type.

        Returns:
            _Cast_GearMeshLoadDistributionAnalysis
        """
        return _Cast_GearMeshLoadDistributionAnalysis(self)
