"""MicroGeometryInputs"""

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar, Generic, TypeVar

from mastapy._private import _0
from mastapy._private._internal import conversion, utility
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

_MICRO_GEOMETRY_INPUTS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "MicroGeometryInputs"
)

if TYPE_CHECKING:
    from typing import Any, List, Type

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical import _737, _738, _739

    Self = TypeVar("Self", bound="MicroGeometryInputs")
    CastSelf = TypeVar(
        "CastSelf", bound="MicroGeometryInputs._Cast_MicroGeometryInputs"
    )

T = TypeVar("T", bound="_739.ModificationSegment")

__docformat__ = "restructuredtext en"
__all__ = ("MicroGeometryInputs",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MicroGeometryInputs:
    """Special nested class for casting MicroGeometryInputs to subclasses."""

    __parent__: "MicroGeometryInputs"

    @property
    def micro_geometry_inputs_lead(self: "CastSelf") -> "_737.MicroGeometryInputsLead":
        from mastapy._private.gears.manufacturing.cylindrical import _737

        return self.__parent__._cast(_737.MicroGeometryInputsLead)

    @property
    def micro_geometry_inputs_profile(
        self: "CastSelf",
    ) -> "_738.MicroGeometryInputsProfile":
        from mastapy._private.gears.manufacturing.cylindrical import _738

        return self.__parent__._cast(_738.MicroGeometryInputsProfile)

    @property
    def micro_geometry_inputs(self: "CastSelf") -> "MicroGeometryInputs":
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
class MicroGeometryInputs(_0.APIBase, Generic[T]):
    """MicroGeometryInputs

    This is a mastapy class.

    Generic Types:
        T
    """

    TYPE: ClassVar["Type"] = _MICRO_GEOMETRY_INPUTS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def modification_at_starting_point(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ModificationAtStartingPoint")

        if temp is None:
            return 0.0

        return temp

    @modification_at_starting_point.setter
    @exception_bridge
    @enforce_parameter_types
    def modification_at_starting_point(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ModificationAtStartingPoint",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def micro_geometry_segments(self: "Self") -> "List[T]":
        """List[T]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MicroGeometrySegments")

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
    def cast_to(self: "Self") -> "_Cast_MicroGeometryInputs":
        """Cast to another type.

        Returns:
            _Cast_MicroGeometryInputs
        """
        return _Cast_MicroGeometryInputs(self)
