"""MountingError"""

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

_MOUNTING_ERROR = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "MountingError",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _768,
        _793,
    )

    Self = TypeVar("Self", bound="MountingError")
    CastSelf = TypeVar("CastSelf", bound="MountingError._Cast_MountingError")


__docformat__ = "restructuredtext en"
__all__ = ("MountingError",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_MountingError:
    """Special nested class for casting MountingError to subclasses."""

    __parent__: "MountingError"

    @property
    def gear_mounting_error(self: "CastSelf") -> "_768.GearMountingError":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _768,
        )

        return self.__parent__._cast(_768.GearMountingError)

    @property
    def rack_mounting_error(self: "CastSelf") -> "_793.RackMountingError":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _793,
        )

        return self.__parent__._cast(_793.RackMountingError)

    @property
    def mounting_error(self: "CastSelf") -> "MountingError":
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
class MountingError(_0.APIBase):
    """MountingError

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _MOUNTING_ERROR

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def distance_between_two_sections(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "DistanceBetweenTwoSections")

        if temp is None:
            return 0.0

        return temp

    @distance_between_two_sections.setter
    @exception_bridge
    @enforce_parameter_types
    def distance_between_two_sections(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "DistanceBetweenTwoSections",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def first_section_phase_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstSectionPhaseAngle")

        if temp is None:
            return 0.0

        return temp

    @first_section_phase_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def first_section_phase_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstSectionPhaseAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def first_section_radial_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "FirstSectionRadialRunout")

        if temp is None:
            return 0.0

        return temp

    @first_section_radial_runout.setter
    @exception_bridge
    @enforce_parameter_types
    def first_section_radial_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "FirstSectionRadialRunout",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def second_section_phase_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SecondSectionPhaseAngle")

        if temp is None:
            return 0.0

        return temp

    @second_section_phase_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def second_section_phase_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SecondSectionPhaseAngle",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def second_section_radial_runout(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SecondSectionRadialRunout")

        if temp is None:
            return 0.0

        return temp

    @second_section_radial_runout.setter
    @exception_bridge
    @enforce_parameter_types
    def second_section_radial_runout(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "SecondSectionRadialRunout",
            float(value) if value is not None else 0.0,
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
    def cast_to(self: "Self") -> "_Cast_MountingError":
        """Cast to another type.

        Returns:
            _Cast_MountingError
        """
        return _Cast_MountingError(self)
