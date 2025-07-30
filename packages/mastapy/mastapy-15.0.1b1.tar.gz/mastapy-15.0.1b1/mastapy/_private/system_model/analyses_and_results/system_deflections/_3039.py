"""RingPinToDiscContactReporting"""

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

_RING_PIN_TO_DISC_CONTACT_REPORTING = python_net_import(
    "SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections",
    "RingPinToDiscContactReporting",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.system_model.analyses_and_results.static_loads import _7778
    from mastapy._private.system_model.analyses_and_results.system_deflections import (
        _3007,
    )
    from mastapy._private.system_model.analyses_and_results.system_deflections.reporting import (
        _3093,
    )

    Self = TypeVar("Self", bound="RingPinToDiscContactReporting")
    CastSelf = TypeVar(
        "CastSelf",
        bound="RingPinToDiscContactReporting._Cast_RingPinToDiscContactReporting",
    )


__docformat__ = "restructuredtext en"
__all__ = ("RingPinToDiscContactReporting",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_RingPinToDiscContactReporting:
    """Special nested class for casting RingPinToDiscContactReporting to subclasses."""

    __parent__: "RingPinToDiscContactReporting"

    @property
    def ring_pin_to_disc_contact_reporting(
        self: "CastSelf",
    ) -> "RingPinToDiscContactReporting":
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
class RingPinToDiscContactReporting(_0.APIBase):
    """RingPinToDiscContactReporting

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _RING_PIN_TO_DISC_CONTACT_REPORTING

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def maximum_contact_stress(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "MaximumContactStress")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def pin_number(self: "Self") -> "int":
        """int

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PinNumber")

        if temp is None:
            return 0

        return temp

    @property
    @exception_bridge
    def pressure_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "PressureVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def sliding_velocity(self: "Self") -> "float":
        """float

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "SlidingVelocity")

        if temp is None:
            return 0.0

        return temp

    @property
    @exception_bridge
    def contact(self: "Self") -> "_3093.SplineFlankContactReporting":
        """mastapy.system_model.analyses_and_results.system_deflections.reporting.SplineFlankContactReporting

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "Contact")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def information_at_ring_pin_to_disc_contact_point_from_geometry(
        self: "Self",
    ) -> "_7778.InformationAtRingPinToDiscContactPointFromGeometry":
        """mastapy.system_model.analyses_and_results.static_loads.InformationAtRingPinToDiscContactPointFromGeometry

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InformationAtRingPinToDiscContactPointFromGeometry"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def information_for_contact_points_along_face_width(
        self: "Self",
    ) -> "List[_3007.InformationForContactAtPointAlongFaceWidth]":
        """List[mastapy.system_model.analyses_and_results.system_deflections.InformationForContactAtPointAlongFaceWidth]

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(
            self.wrapped, "InformationForContactPointsAlongFaceWidth"
        )

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
    def cast_to(self: "Self") -> "_Cast_RingPinToDiscContactReporting":
        """Cast to another type.

        Returns:
            _Cast_RingPinToDiscContactReporting
        """
        return _Cast_RingPinToDiscContactReporting(self)
