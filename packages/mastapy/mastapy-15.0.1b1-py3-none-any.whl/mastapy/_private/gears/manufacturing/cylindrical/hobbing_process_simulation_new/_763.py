"""CalculateLeadDeviationAccuracy"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_CALCULATE_LEAD_DEVIATION_ACCURACY = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "CalculateLeadDeviationAccuracy",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _781,
    )

    Self = TypeVar("Self", bound="CalculateLeadDeviationAccuracy")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CalculateLeadDeviationAccuracy._Cast_CalculateLeadDeviationAccuracy",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CalculateLeadDeviationAccuracy",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CalculateLeadDeviationAccuracy:
    """Special nested class for casting CalculateLeadDeviationAccuracy to subclasses."""

    __parent__: "CalculateLeadDeviationAccuracy"

    @property
    def calculate_lead_deviation_accuracy(
        self: "CastSelf",
    ) -> "CalculateLeadDeviationAccuracy":
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
class CalculateLeadDeviationAccuracy(_0.APIBase):
    """CalculateLeadDeviationAccuracy

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CALCULATE_LEAD_DEVIATION_ACCURACY

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def achieved_lead_agma20151a01_quality_grade(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AchievedLeadAGMA20151A01QualityGrade"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def achieved_lead_iso132811995e_quality_grade(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "AchievedLeadISO132811995EQualityGrade"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def flank_name(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "FlankName")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def helix_deviation_agma20151a01_quality_grade_designed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixDeviationAGMA20151A01QualityGradeDesigned"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_deviation_iso132811995e_quality_grade_designed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixDeviationISO132811995EQualityGradeDesigned"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_form_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixFormDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_form_deviation_agma20151a01_quality_grade_obtained(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixFormDeviationAGMA20151A01QualityGradeObtained"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_form_deviation_iso132811995e_quality_grade_obtained(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixFormDeviationISO132811995EQualityGradeObtained"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_slope_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "HelixSlopeDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_slope_deviation_agma20151a01_quality_grade_obtained(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixSlopeDeviationAGMA20151A01QualityGradeObtained"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def helix_slope_deviation_iso132811995e_quality_grade_obtained(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "HelixSlopeDeviationISO132811995EQualityGradeObtained"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_helix_deviation(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "TotalHelixDeviation")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_helix_deviation_agma20151a01_quality_grade_obtained(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalHelixDeviationAGMA20151A01QualityGradeObtained"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def total_helix_deviation_iso132811995e_quality_grade_obtained(
        self: "Self",
    ) -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "TotalHelixDeviationISO132811995EQualityGradeObtained"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def manufactured_agma20151a01_quality_grades(
        self: "Self",
    ) -> "List[_781.ManufacturedQualityGrade]":
        """List[mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.ManufacturedQualityGrade]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ManufacturedAGMA20151A01QualityGrades"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def manufactured_iso132811995e_quality_grades(
        self: "Self",
    ) -> "List[_781.ManufacturedQualityGrade]":
        """List[mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.ManufacturedQualityGrade]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ManufacturedISO132811995EQualityGrades"
        )

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
    def cast_to(self: "Self") -> "_Cast_CalculateLeadDeviationAccuracy":
        """Cast to another type.

        Returns:
            _Cast_CalculateLeadDeviationAccuracy
        """
        return _Cast_CalculateLeadDeviationAccuracy(self)
