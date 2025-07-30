"""RotorDynamicsViewable"""

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

_ROTOR_DYNAMICS_VIEWABLE = python_net_import(
    "SMT.MastaAPI.SystemModel.Drawing", "RotorDynamicsViewable"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.rotor_dynamics import _4287
    from mastapy._private.system_model.drawing import _2468, _2478, _2479

    Self = TypeVar("Self", bound="RotorDynamicsViewable")
    CastSelf = TypeVar(
        "CastSelf", bound="RotorDynamicsViewable._Cast_RotorDynamicsViewable"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RotorDynamicsViewable",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RotorDynamicsViewable:
    """Special nested class for casting RotorDynamicsViewable to subclasses."""

    __parent__: "RotorDynamicsViewable"

    @property
    def critical_speed_analysis_viewable(
        self: "CastSelf",
    ) -> "_2468.CriticalSpeedAnalysisViewable":
        from mastapy._private.system_model.drawing import _2468

        return self.__parent__._cast(_2468.CriticalSpeedAnalysisViewable)

    @property
    def stability_analysis_viewable(
        self: "CastSelf",
    ) -> "_2478.StabilityAnalysisViewable":
        from mastapy._private.system_model.drawing import _2478

        return self.__parent__._cast(_2478.StabilityAnalysisViewable)

    @property
    def steady_state_synchronous_response_viewable(
        self: "CastSelf",
    ) -> "_2479.SteadyStateSynchronousResponseViewable":
        from mastapy._private.system_model.drawing import _2479

        return self.__parent__._cast(_2479.SteadyStateSynchronousResponseViewable)

    @property
    def rotor_dynamics_viewable(self: "CastSelf") -> "RotorDynamicsViewable":
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
class RotorDynamicsViewable(_0.APIBase):
    """RotorDynamicsViewable

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _ROTOR_DYNAMICS_VIEWABLE

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def rotor_dynamics(self: "Self") -> "_4287.RotorDynamicsDrawStyle":
        """mastapy.system_model.analyses_and_results.rotor_dynamics.RotorDynamicsDrawStyle

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "RotorDynamics")

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
    def cast_to(self: "Self") -> "_Cast_RotorDynamicsViewable":
        """Cast to another type.

        Returns:
            _Cast_RotorDynamicsViewable
        """
        return _Cast_RotorDynamicsViewable(self)
