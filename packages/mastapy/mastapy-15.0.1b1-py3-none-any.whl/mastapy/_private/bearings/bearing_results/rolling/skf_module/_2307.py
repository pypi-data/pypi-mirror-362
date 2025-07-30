"""SKFModuleResults"""

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

_SKF_MODULE_RESULTS = python_net_import(
    "SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule", "SKFModuleResults"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.bearings.bearing_results.rolling.skf_module import (
        _2285,
        _2287,
        _2288,
        _2289,
        _2290,
        _2292,
        _2296,
        _2300,
        _2308,
        _2309,
    )

    Self = TypeVar("Self", bound="SKFModuleResults")
    CastSelf = TypeVar("CastSelf", bound="SKFModuleResults._Cast_SKFModuleResults")


__docformat__ = "restructuredtext en"
__all__ = ("SKFModuleResults",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_SKFModuleResults:
    """Special nested class for casting SKFModuleResults to subclasses."""

    __parent__: "SKFModuleResults"

    @property
    def skf_module_results(self: "CastSelf") -> "SKFModuleResults":
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
class SKFModuleResults(_0.APIBase):
    """SKFModuleResults

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _SKF_MODULE_RESULTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def adjusted_speed(self: "Self") -> "_2285.AdjustedSpeed":
        """mastapy.bearings.bearing_results.rolling.skf_module.AdjustedSpeed

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "AdjustedSpeed")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_loads(self: "Self") -> "_2287.BearingLoads":
        """mastapy.bearings.bearing_results.rolling.skf_module.BearingLoads

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingLoads")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def bearing_rating_life(self: "Self") -> "_2288.BearingRatingLife":
        """mastapy.bearings.bearing_results.rolling.skf_module.BearingRatingLife

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "BearingRatingLife")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def dynamic_axial_load_carrying_capacity(
        self: "Self",
    ) -> "_2289.DynamicAxialLoadCarryingCapacity":
        """mastapy.bearings.bearing_results.rolling.skf_module.DynamicAxialLoadCarryingCapacity

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "DynamicAxialLoadCarryingCapacity")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def frequencies(self: "Self") -> "_2290.Frequencies":
        """mastapy.bearings.bearing_results.rolling.skf_module.Frequencies

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Frequencies")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def friction(self: "Self") -> "_2292.Friction":
        """mastapy.bearings.bearing_results.rolling.skf_module.Friction

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Friction")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def grease_life_and_relubrication_interval(
        self: "Self",
    ) -> "_2296.GreaseLifeAndRelubricationInterval":
        """mastapy.bearings.bearing_results.rolling.skf_module.GreaseLifeAndRelubricationInterval

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "GreaseLifeAndRelubricationInterval"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def minimum_load(self: "Self") -> "_2300.MinimumLoad":
        """mastapy.bearings.bearing_results.rolling.skf_module.MinimumLoad

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MinimumLoad")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def static_safety_factors(self: "Self") -> "_2308.StaticSafetyFactors":
        """mastapy.bearings.bearing_results.rolling.skf_module.StaticSafetyFactors

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "StaticSafetyFactors")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def viscosities(self: "Self") -> "_2309.Viscosities":
        """mastapy.bearings.bearing_results.rolling.skf_module.Viscosities

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Viscosities")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_SKFModuleResults":
        """Cast to another type.

        Returns:
            _Cast_SKFModuleResults
        """
        return _Cast_SKFModuleResults(self)
