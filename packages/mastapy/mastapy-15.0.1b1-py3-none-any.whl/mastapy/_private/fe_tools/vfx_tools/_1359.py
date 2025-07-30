"""ProSolveOptions"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    constructor,
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value, overridable
from mastapy._private._internal.overridable_constructor import _unpack_overridable
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.fe_tools.vfx_tools.vfx_enums import _1361, _1362

_PRO_SOLVE_OPTIONS = python_net_import(
    "SMT.MastaAPI.FETools.VfxTools", "ProSolveOptions"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar, Union

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="ProSolveOptions")
    CastSelf = TypeVar("CastSelf", bound="ProSolveOptions._Cast_ProSolveOptions")


__docformat__ = "restructuredtext en"
__all__ = ("ProSolveOptions",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProSolveOptions:
    """Special nested class for casting ProSolveOptions to subclasses."""

    __parent__: "ProSolveOptions"

    @property
    def pro_solve_options(self: "CastSelf") -> "ProSolveOptions":
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
class ProSolveOptions(_0.APIBase):
    """ProSolveOptions

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PRO_SOLVE_OPTIONS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def compensate_for_singularities_in_model(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "CompensateForSingularitiesInModel")

        if temp is None:
            return False

        return temp

    @compensate_for_singularities_in_model.setter
    @exception_bridge
    @enforce_parameter_types
    def compensate_for_singularities_in_model(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CompensateForSingularitiesInModel",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def mpc_type(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ProSolveMpcType":
        """EnumWithSelectedValue[mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveMpcType]"""
        temp = pythonnet_property_get(self.wrapped, "MPCType")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ProSolveMpcType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @mpc_type.setter
    @exception_bridge
    @enforce_parameter_types
    def mpc_type(self: "Self", value: "_1361.ProSolveMpcType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ProSolveMpcType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "MPCType", value)

    @property
    @exception_bridge
    def penalty_factor(self: "Self") -> "overridable.Overridable_float":
        """Overridable[float]"""
        temp = pythonnet_property_get(self.wrapped, "PenaltyFactor")

        if temp is None:
            return 0.0

        return constructor.new_from_mastapy(
            "mastapy._private._internal.implicit.overridable", "Overridable_float"
        )(temp)

    @penalty_factor.setter
    @exception_bridge
    @enforce_parameter_types
    def penalty_factor(self: "Self", value: "Union[float, Tuple[float, bool]]") -> None:
        wrapper_type = overridable.Overridable_float.wrapper_type()
        enclosed_type = overridable.Overridable_float.implicit_type()
        value, is_overridden = _unpack_overridable(value)
        value = wrapper_type[enclosed_type](
            enclosed_type(value) if value is not None else 0.0, is_overridden
        )
        pythonnet_property_set(self.wrapped, "PenaltyFactor", value)

    @property
    @exception_bridge
    def type_of_solver(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_ProSolveSolverType":
        """EnumWithSelectedValue[mastapy.fe_tools.vfx_tools.vfx_enums.ProSolveSolverType]"""
        temp = pythonnet_property_get(self.wrapped, "TypeOfSolver")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_ProSolveSolverType.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @type_of_solver.setter
    @exception_bridge
    @enforce_parameter_types
    def type_of_solver(self: "Self", value: "_1362.ProSolveSolverType") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_ProSolveSolverType.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "TypeOfSolver", value)

    @property
    @exception_bridge
    def use_jacobian_checking(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseJacobianChecking")

        if temp is None:
            return False

        return temp

    @use_jacobian_checking.setter
    @exception_bridge
    @enforce_parameter_types
    def use_jacobian_checking(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseJacobianChecking",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def use_out_of_core_solver(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "UseOutOfCoreSolver")

        if temp is None:
            return False

        return temp

    @use_out_of_core_solver.setter
    @exception_bridge
    @enforce_parameter_types
    def use_out_of_core_solver(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "UseOutOfCoreSolver",
            bool(value) if value is not None else False,
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
    def cast_to(self: "Self") -> "_Cast_ProSolveOptions":
        """Cast to another type.

        Returns:
            _Cast_ProSolveOptions
        """
        return _Cast_ProSolveOptions(self)
