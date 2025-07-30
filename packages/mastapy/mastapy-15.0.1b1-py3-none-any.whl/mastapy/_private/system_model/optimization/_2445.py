"""OptimizationStep"""

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

_OPTIMIZATION_STEP = python_net_import(
    "SMT.MastaAPI.SystemModel.Optimization", "OptimizationStep"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.optimization import _2438, _2441, _2443

    Self = TypeVar("Self", bound="OptimizationStep")
    CastSelf = TypeVar("CastSelf", bound="OptimizationStep._Cast_OptimizationStep")


__docformat__ = "restructuredtext en"
__all__ = ("OptimizationStep",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_OptimizationStep:
    """Special nested class for casting OptimizationStep to subclasses."""

    __parent__: "OptimizationStep"

    @property
    def conical_gear_optimization_step(
        self: "CastSelf",
    ) -> "_2438.ConicalGearOptimizationStep":
        from mastapy._private.system_model.optimization import _2438

        return self.__parent__._cast(_2438.ConicalGearOptimizationStep)

    @property
    def cylindrical_gear_optimization_step(
        self: "CastSelf",
    ) -> "_2441.CylindricalGearOptimizationStep":
        from mastapy._private.system_model.optimization import _2441

        return self.__parent__._cast(_2441.CylindricalGearOptimizationStep)

    @property
    def optimization_step(self: "CastSelf") -> "OptimizationStep":
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
class OptimizationStep(_0.APIBase):
    """OptimizationStep

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _OPTIMIZATION_STEP

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def name(self: "Self") -> "str":
        """str"""
        temp = pythonnet_property_get(self.wrapped, "Name")

        if temp is None:
            return ""

        return temp

    @name.setter
    @exception_bridge
    @enforce_parameter_types
    def name(self: "Self", value: "str") -> None:
        pythonnet_property_set(
            self.wrapped, "Name", str(value) if value is not None else ""
        )

    @property
    @exception_bridge
    def optimisation_target(self: "Self") -> "_2443.MicroGeometryOptimisationTarget":
        """mastapy.system_model.optimization.MicroGeometryOptimisationTarget"""
        temp = pythonnet_property_get(self.wrapped, "OptimisationTarget")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.SystemModel.Optimization.MicroGeometryOptimisationTarget",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.system_model.optimization._2443",
            "MicroGeometryOptimisationTarget",
        )(value)

    @optimisation_target.setter
    @exception_bridge
    @enforce_parameter_types
    def optimisation_target(
        self: "Self", value: "_2443.MicroGeometryOptimisationTarget"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.SystemModel.Optimization.MicroGeometryOptimisationTarget",
        )
        pythonnet_property_set(self.wrapped, "OptimisationTarget", value)

    @property
    @exception_bridge
    def target_edge_stress_factor(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "TargetEdgeStressFactor")

        if temp is None:
            return 0.0

        return temp

    @target_edge_stress_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def target_edge_stress_factor(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "TargetEdgeStressFactor",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tolerance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Tolerance")

        if temp is None:
            return 0.0

        return temp

    @tolerance.setter
    @exception_bridge
    @enforce_parameter_types
    def tolerance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Tolerance", float(value) if value is not None else 0.0
        )

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
    def cast_to(self: "Self") -> "_Cast_OptimizationStep":
        """Cast to another type.

        Returns:
            _Cast_OptimizationStep
        """
        return _Cast_OptimizationStep(self)
