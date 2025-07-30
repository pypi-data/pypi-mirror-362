"""ShaftDamageResults"""

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
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private._math.vector_3d import Vector3D

_SHAFT_DAMAGE_RESULTS = python_net_import("SMT.MastaAPI.Shafts", "ShaftDamageResults")

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.math_utility import _1710
    from mastapy._private.nodal_analysis import _88
    from mastapy._private.shafts import _39, _40, _43
    from mastapy._private.utility.report import _1981

    Self = TypeVar("Self", bound="ShaftDamageResults")
    CastSelf = TypeVar("CastSelf", bound="ShaftDamageResults._Cast_ShaftDamageResults")


__docformat__ = "restructuredtext en"
__all__ = ("ShaftDamageResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ShaftDamageResults:
    """Special nested class for casting ShaftDamageResults to subclasses."""

    __parent__: "ShaftDamageResults"

    @property
    def shaft_damage_results(self: "CastSelf") -> "ShaftDamageResults":
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
class ShaftDamageResults(_0.APIBase):
    """ShaftDamageResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SHAFT_DAMAGE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def cyclic_degrees_of_utilisation(self: "Self") -> "List[_1710.RealVector]":
        """List[mastapy.math_utility.RealVector]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CyclicDegreesOfUtilisation")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def displacement_angular(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def displacement_linear(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DisplacementLinear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def displacement_maximum_radial_magnitude(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "DisplacementMaximumRadialMagnitude"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def force_angular(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceAngular")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def force_linear(self: "Self") -> "List[Vector3D]":
        """List[Vector3D]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ForceLinear")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, Vector3D)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def rating_type_for_shaft_reliability(
        self: "Self",
    ) -> "_88.RatingTypeForShaftReliability":
        """mastapy.nodal_analysis.RatingTypeForShaftReliability

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RatingTypeForShaftReliability")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp, "SMT.MastaAPI.NodalAnalysis.RatingTypeForShaftReliability"
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.nodal_analysis._88", "RatingTypeForShaftReliability"
        )(value)

    @property
    @exception_bridge
    def stress_highest_equivalent_fully_reversed(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "StressHighestEquivalentFullyReversed"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def using_fkm_shaft_rating_method(self: "Self") -> "bool":
        """bool

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "UsingFKMShaftRatingMethod")

        if temp is None:
            return False

        return temp

    @property
    @exception_bridge
    def worst_fatigue_damage(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstFatigueDamage")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_fatigue_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstFatigueSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_fatigue_safety_factor_for_infinite_life(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "WorstFatigueSafetyFactorForInfiniteLife"
        )

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_reliability_for_finite_life(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstReliabilityForFiniteLife")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_reliability_for_infinite_life(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstReliabilityForInfiniteLife")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def worst_static_safety_factor(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "WorstStaticSafetyFactor")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def shaft_section_end_with_worst_fatigue_safety_factor(
        self: "Self",
    ) -> "_40.ShaftSectionEndDamageResults":
        """mastapy.shafts.ShaftSectionEndDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstFatigueSafetyFactor"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_section_end_with_worst_fatigue_safety_factor_for_infinite_life(
        self: "Self",
    ) -> "_40.ShaftSectionEndDamageResults":
        """mastapy.shafts.ShaftSectionEndDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstFatigueSafetyFactorForInfiniteLife"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_section_end_with_worst_static_safety_factor(
        self: "Self",
    ) -> "_40.ShaftSectionEndDamageResults":
        """mastapy.shafts.ShaftSectionEndDamageResults

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndWithWorstStaticSafetyFactor"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_settings(self: "Self") -> "_43.ShaftSettingsItem":
        """mastapy.shafts.ShaftSettingsItem

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSettings")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def shaft_section_damage_results(
        self: "Self",
    ) -> "List[_39.ShaftSectionDamageResults]":
        """List[mastapy.shafts.ShaftSectionDamageResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftSectionDamageResults")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaft_section_end_results_by_offset_with_worst_safety_factor(
        self: "Self",
    ) -> "List[_40.ShaftSectionEndDamageResults]":
        """List[mastapy.shafts.ShaftSectionEndDamageResults]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "ShaftSectionEndResultsByOffsetWithWorstSafetyFactor"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp)

        if value is None:
            return None

        return value

    @property
    @exception_bridge
    def shaft_damage_chart_items(self: "Self") -> "List[str]":
        """List[str]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "ShaftDamageChartItems")

        if temp is None:
            return None

        value = conversion.pn_to_mp_objects_in_list(temp, str)

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
    def shaft_damage_chart(
        self: "Self", item: "str", title: "str"
    ) -> "_1981.SimpleChartDefinition":
        """mastapy.utility.report.SimpleChartDefinition

        Args:
            item (str)
            title (str)
        """
        item = str(item)
        title = str(title)
        method_result = pythonnet_method_call(
            self.wrapped,
            "ShaftDamageChart",
            item if item else "",
            title if title else "",
        )
        type_ = method_result.GetType()
        return (
            constructor.new(type_.Namespace, type_.Name)(method_result)
            if method_result is not None
            else None
        )

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
    def cast_to(self: "Self") -> "_Cast_ShaftDamageResults":
        """Cast to another type.

        Returns:
            _Cast_ShaftDamageResults
        """
        return _Cast_ShaftDamageResults(self)
