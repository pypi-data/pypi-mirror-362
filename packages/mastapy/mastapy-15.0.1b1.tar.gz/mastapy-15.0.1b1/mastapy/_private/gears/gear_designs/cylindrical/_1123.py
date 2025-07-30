"""CylindricalGearDesignConstraint"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from mastapy._private import _0
from mastapy._private._internal import (
    conversion,
    enum_with_selected_value_runtime,
    utility,
)
from mastapy._private._internal.dataclasses import extended_dataclass
from mastapy._private._internal.exception_bridge import exception_bridge
from mastapy._private._internal.exceptions import CastException
from mastapy._private._internal.implicit import enum_with_selected_value
from mastapy._private._internal.python_net import (
    python_net_import,
    pythonnet_method_call,
    pythonnet_property_get,
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types
from mastapy._private.utility.model_validation import _1990

_CYLINDRICAL_GEAR_DESIGN_CONSTRAINT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearDesignConstraint"
)

if TYPE_CHECKING:
    from typing import Any, List, Tuple, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="CylindricalGearDesignConstraint")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearDesignConstraint._Cast_CylindricalGearDesignConstraint",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearDesignConstraint",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearDesignConstraint:
    """Special nested class for casting CylindricalGearDesignConstraint to subclasses."""

    __parent__: "CylindricalGearDesignConstraint"

    @property
    def cylindrical_gear_design_constraint(
        self: "CastSelf",
    ) -> "CylindricalGearDesignConstraint":
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
class CylindricalGearDesignConstraint(_0.APIBase):
    """CylindricalGearDesignConstraint

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_DESIGN_CONSTRAINT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def class_of_error(
        self: "Self",
    ) -> "enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity":
        """EnumWithSelectedValue[mastapy.utility.model_validation.StatusItemSeverity]"""
        temp = pythonnet_property_get(self.wrapped, "ClassOfError")

        if temp is None:
            return None

        value = enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.wrapped_type()
        return enum_with_selected_value_runtime.create(temp, value)

    @class_of_error.setter
    @exception_bridge
    @enforce_parameter_types
    def class_of_error(self: "Self", value: "_1990.StatusItemSeverity") -> None:
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_StatusItemSeverity.implicit_type()
        value = conversion.mp_to_pn_enum(value, enclosed_type)
        value = wrapper_type[enclosed_type](value)
        pythonnet_property_set(self.wrapped, "ClassOfError", value)

    @property
    @exception_bridge
    def integer_range(self: "Self") -> "Tuple[int, int]":
        """Tuple[int, int]"""
        temp = pythonnet_property_get(self.wrapped, "IntegerRange")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @integer_range.setter
    @exception_bridge
    @enforce_parameter_types
    def integer_range(self: "Self", value: "Tuple[int, int]") -> None:
        value = conversion.mp_to_pn_integer_range(value)
        pythonnet_property_set(self.wrapped, "IntegerRange", value)

    @property
    @exception_bridge
    def is_active(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "IsActive")

        if temp is None:
            return False

        return temp

    @is_active.setter
    @exception_bridge
    @enforce_parameter_types
    def is_active(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped, "IsActive", bool(value) if value is not None else False
        )

    @property
    @exception_bridge
    def property_(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Property")

        if temp is None:
            return ""

        return temp

    @property
    @exception_bridge
    def range(self: "Self") -> "Tuple[float, float]":
        """Tuple[float, float]"""
        temp = pythonnet_property_get(self.wrapped, "Range")

        if temp is None:
            return None

        value = conversion.pn_to_mp_range(temp)

        if value is None:
            return None

        return value

    @range.setter
    @exception_bridge
    @enforce_parameter_types
    def range(self: "Self", value: "Tuple[float, float]") -> None:
        value = conversion.mp_to_pn_range(value)
        pythonnet_property_set(self.wrapped, "Range", value)

    @property
    @exception_bridge
    def unit(self: "Self") -> "str":
        """str

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Unit")

        if temp is None:
            return ""

        return temp

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
    def delete(self: "Self") -> None:
        """Method does not return."""
        pythonnet_method_call(self.wrapped, "Delete")

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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearDesignConstraint":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearDesignConstraint
        """
        return _Cast_CylindricalGearDesignConstraint(self)
