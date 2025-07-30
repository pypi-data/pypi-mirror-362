"""StatorToothInterpolator"""

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

_STATOR_TOOTH_INTERPOLATOR = python_net_import(
    "SMT.MastaAPI.ElectricMachines.HarmonicLoadData", "StatorToothInterpolator"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.electric_machines.harmonic_load_data import _1570, _1571
    from mastapy._private.math_utility import _1705

    Self = TypeVar("Self", bound="StatorToothInterpolator")
    CastSelf = TypeVar(
        "CastSelf", bound="StatorToothInterpolator._Cast_StatorToothInterpolator"
    )


__docformat__ = "restructuredtext en"
__all__ = ("StatorToothInterpolator",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_StatorToothInterpolator:
    """Special nested class for casting StatorToothInterpolator to subclasses."""

    __parent__: "StatorToothInterpolator"

    @property
    def stator_tooth_load_interpolator(
        self: "CastSelf",
    ) -> "_1570.StatorToothLoadInterpolator":
        from mastapy._private.electric_machines.harmonic_load_data import _1570

        return self.__parent__._cast(_1570.StatorToothLoadInterpolator)

    @property
    def stator_tooth_moment_interpolator(
        self: "CastSelf",
    ) -> "_1571.StatorToothMomentInterpolator":
        from mastapy._private.electric_machines.harmonic_load_data import _1571

        return self.__parent__._cast(_1571.StatorToothMomentInterpolator)

    @property
    def stator_tooth_interpolator(self: "CastSelf") -> "StatorToothInterpolator":
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
class StatorToothInterpolator(_0.APIBase):
    """StatorToothInterpolator

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _STATOR_TOOTH_INTERPOLATOR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

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
    def multiple_fourier_series_interpolator_for(
        self: "Self", node_index: "int"
    ) -> "_1705.MultipleFourierSeriesInterpolator":
        """mastapy.math_utility.MultipleFourierSeriesInterpolator

        Args:
            node_index (int)
        """
        node_index = int(node_index)
        method_result = pythonnet_method_call(
            self.wrapped,
            "MultipleFourierSeriesInterpolatorFor",
            node_index if node_index else 0,
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
    def cast_to(self: "Self") -> "_Cast_StatorToothInterpolator":
        """Cast to another type.

        Returns:
            _Cast_StatorToothInterpolator
        """
        return _Cast_StatorToothInterpolator(self)
