"""ModificationSegment"""

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
    pythonnet_property_set,
)
from mastapy._private._internal.type_enforcement import enforce_parameter_types

_MODIFICATION_SEGMENT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical", "ModificationSegment"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical import _735, _740

    Self = TypeVar("Self", bound="ModificationSegment")
    CastSelf = TypeVar(
        "CastSelf", bound="ModificationSegment._Cast_ModificationSegment"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ModificationSegment",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ModificationSegment:
    """Special nested class for casting ModificationSegment to subclasses."""

    __parent__: "ModificationSegment"

    @property
    def lead_modification_segment(self: "CastSelf") -> "_735.LeadModificationSegment":
        from mastapy._private.gears.manufacturing.cylindrical import _735

        return self.__parent__._cast(_735.LeadModificationSegment)

    @property
    def profile_modification_segment(
        self: "CastSelf",
    ) -> "_740.ProfileModificationSegment":
        from mastapy._private.gears.manufacturing.cylindrical import _740

        return self.__parent__._cast(_740.ProfileModificationSegment)

    @property
    def modification_segment(self: "CastSelf") -> "ModificationSegment":
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
class ModificationSegment(_0.APIBase):
    """ModificationSegment

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MODIFICATION_SEGMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def crown(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Crown")

        if temp is None:
            return 0.0

        return temp

    @crown.setter
    @exception_bridge
    @enforce_parameter_types
    def crown(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Crown", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def slope(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Slope")

        if temp is None:
            return 0.0

        return temp

    @slope.setter
    @exception_bridge
    @enforce_parameter_types
    def slope(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Slope", float(value) if value is not None else 0.0
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
    def cast_to(self: "Self") -> "_Cast_ModificationSegment":
        """Cast to another type.

        Returns:
            _Cast_ModificationSegment
        """
        return _Cast_ModificationSegment(self)
