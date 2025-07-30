"""ParametricStudyHistogram"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private._internal import utility
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.report import _1955

_PARAMETRIC_STUDY_HISTOGRAM = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools",
    "ParametricStudyHistogram",
)

if TYPE_CHECKING:
    from typing import Any, Type, TypeVar

    from mastapy._private.utility.report import _1958, _1966

    Self = TypeVar("Self", bound="ParametricStudyHistogram")
    CastSelf = TypeVar(
        "CastSelf", bound="ParametricStudyHistogram._Cast_ParametricStudyHistogram"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ParametricStudyHistogram",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ParametricStudyHistogram:
    """Special nested class for casting ParametricStudyHistogram to subclasses."""

    __parent__: "ParametricStudyHistogram"

    @property
    def custom_report_definition_item(
        self: "CastSelf",
    ) -> "_1955.CustomReportDefinitionItem":
        return self.__parent__._cast(_1955.CustomReportDefinitionItem)

    @property
    def custom_report_nameable_item(
        self: "CastSelf",
    ) -> "_1966.CustomReportNameableItem":
        from mastapy._private.utility.report import _1966

        return self.__parent__._cast(_1966.CustomReportNameableItem)

    @property
    def custom_report_item(self: "CastSelf") -> "_1958.CustomReportItem":
        from mastapy._private.utility.report import _1958

        return self.__parent__._cast(_1958.CustomReportItem)

    @property
    def parametric_study_histogram(self: "CastSelf") -> "ParametricStudyHistogram":
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
class ParametricStudyHistogram(_1955.CustomReportDefinitionItem):
    """ParametricStudyHistogram

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PARAMETRIC_STUDY_HISTOGRAM

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def height(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Height")

        if temp is None:
            return 0

        return temp

    @height.setter
    @exception_bridge
    @enforce_parameter_types
    def height(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Height", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def number_of_bins(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "NumberOfBins")

        if temp is None:
            return 0

        return temp

    @number_of_bins.setter
    @exception_bridge
    @enforce_parameter_types
    def number_of_bins(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "NumberOfBins", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def use_bin_range_for_label(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseBinRangeForLabel")

        if temp is None:
            return False

        return temp

    @use_bin_range_for_label.setter
    @exception_bridge
    @enforce_parameter_types
    def use_bin_range_for_label(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseBinRangeForLabel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def width(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "Width")

        if temp is None:
            return 0

        return temp

    @width.setter
    @exception_bridge
    @enforce_parameter_types
    def width(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "Width", int(value) if value is not None else 0
        )

    @property
    def cast_to(self: "Self") -> "_Cast_ParametricStudyHistogram":
        """Cast to another type.

        Returns:
            _Cast_ParametricStudyHistogram
        """
        return _Cast_ParametricStudyHistogram(self)
