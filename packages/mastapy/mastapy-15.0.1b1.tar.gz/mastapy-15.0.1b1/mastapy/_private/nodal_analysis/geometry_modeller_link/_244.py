"""RepositionComponentDetails"""

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
from mastapy._private._math.vector_3d import Vector3D

_REPOSITION_COMPONENT_DETAILS = python_net_import(
    "SMT.MastaAPI.NodalAnalysis.GeometryModellerLink", "RepositionComponentDetails"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="RepositionComponentDetails")
    CastSelf = TypeVar(
        "CastSelf", bound="RepositionComponentDetails._Cast_RepositionComponentDetails"
    )


__docformat__ = "restructuredtext en"
__all__ = ("RepositionComponentDetails",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RepositionComponentDetails:
    """Special nested class for casting RepositionComponentDetails to subclasses."""

    __parent__: "RepositionComponentDetails"

    @property
    def reposition_component_details(self: "CastSelf") -> "RepositionComponentDetails":
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
class RepositionComponentDetails(_0.APIBase):
    """RepositionComponentDetails

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _REPOSITION_COMPONENT_DETAILS

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def only_move_concentric_components(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "OnlyMoveConcentricComponents")

        if temp is None:
            return False

        return temp

    @only_move_concentric_components.setter
    @exception_bridge
    @enforce_parameter_types
    def only_move_concentric_components(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "OnlyMoveConcentricComponents",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def reverse_axis_direction(self: "Self") -> "bool":
        """bool"""
        temp = pythonnet_property_get(self.wrapped, "ReverseAxisDirection")

        if temp is None:
            return False

        return temp

    @reverse_axis_direction.setter
    @exception_bridge
    @enforce_parameter_types
    def reverse_axis_direction(self: "Self", value: "bool") -> None:
        pythonnet_property_set(
            self.wrapped,
            "ReverseAxisDirection",
            bool(value) if value is not None else False,
        )

    @property
    @exception_bridge
    def direction(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Direction")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @direction.setter
    @exception_bridge
    @enforce_parameter_types
    def direction(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Direction", value)

    @property
    @exception_bridge
    def origin(self: "Self") -> "Vector3D":
        """Vector3D"""
        temp = pythonnet_property_get(self.wrapped, "Origin")

        if temp is None:
            return None

        value = conversion.pn_to_mp_vector3d(temp)

        if value is None:
            return None

        return value

    @origin.setter
    @exception_bridge
    @enforce_parameter_types
    def origin(self: "Self", value: "Vector3D") -> None:
        value = conversion.mp_to_pn_vector3d(value)
        pythonnet_property_set(self.wrapped, "Origin", value)

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
    def cast_to(self: "Self") -> "_Cast_RepositionComponentDetails":
        """Cast to another type.

        Returns:
            _Cast_RepositionComponentDetails
        """
        return _Cast_RepositionComponentDetails(self)
