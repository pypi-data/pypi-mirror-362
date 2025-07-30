"""CylindricalGearProfileMeasurement"""

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

_CYLINDRICAL_GEAR_PROFILE_MEASUREMENT = python_net_import(
    "SMT.MastaAPI.Gears.GearDesigns.Cylindrical", "CylindricalGearProfileMeasurement"
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="CylindricalGearProfileMeasurement")
    CastSelf = TypeVar(
        "CastSelf",
        bound="CylindricalGearProfileMeasurement._Cast_CylindricalGearProfileMeasurement",
    )


__docformat__ = "restructuredtext en"
__all__ = ("CylindricalGearProfileMeasurement",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_CylindricalGearProfileMeasurement:
    """Special nested class for casting CylindricalGearProfileMeasurement to subclasses."""

    __parent__: "CylindricalGearProfileMeasurement"

    @property
    def cylindrical_gear_profile_measurement(
        self: "CastSelf",
    ) -> "CylindricalGearProfileMeasurement":
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
class CylindricalGearProfileMeasurement(_0.APIBase):
    """CylindricalGearProfileMeasurement

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _CYLINDRICAL_GEAR_PROFILE_MEASUREMENT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def auto_diameter_show_depending_on_settings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AutoDiameterShowDependingOnSettings"
        )

        if temp is None:
            return 0.0

        return temp

    @auto_diameter_show_depending_on_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_diameter_show_depending_on_settings(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AutoDiameterShowDependingOnSettings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def auto_radius_show_depending_on_settings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "AutoRadiusShowDependingOnSettings")

        if temp is None:
            return 0.0

        return temp

    @auto_radius_show_depending_on_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_radius_show_depending_on_settings(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "AutoRadiusShowDependingOnSettings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def auto_roll_angle_show_depending_on_settings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AutoRollAngleShowDependingOnSettings"
        )

        if temp is None:
            return 0.0

        return temp

    @auto_roll_angle_show_depending_on_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_roll_angle_show_depending_on_settings(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AutoRollAngleShowDependingOnSettings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def auto_rolling_distance_show_depending_on_settings(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(
            self.wrapped, "AutoRollingDistanceShowDependingOnSettings"
        )

        if temp is None:
            return 0.0

        return temp

    @auto_rolling_distance_show_depending_on_settings.setter
    @exception_bridge
    @enforce_parameter_types
    def auto_rolling_distance_show_depending_on_settings(
        self: "Self", value: "float"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "AutoRollingDistanceShowDependingOnSettings",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Diameter")

        if temp is None:
            return 0.0

        return temp

    @diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Diameter", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def radius(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Radius")

        if temp is None:
            return 0.0

        return temp

    @radius.setter
    @exception_bridge
    @enforce_parameter_types
    def radius(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Radius", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def roll_angle(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollAngle")

        if temp is None:
            return 0.0

        return temp

    @roll_angle.setter
    @exception_bridge
    @enforce_parameter_types
    def roll_angle(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RollAngle", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def rolling_distance(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "RollingDistance")

        if temp is None:
            return 0.0

        return temp

    @rolling_distance.setter
    @exception_bridge
    @enforce_parameter_types
    def rolling_distance(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "RollingDistance", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def signed_diameter(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "SignedDiameter")

        if temp is None:
            return 0.0

        return temp

    @signed_diameter.setter
    @exception_bridge
    @enforce_parameter_types
    def signed_diameter(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "SignedDiameter", float(value) if value is not None else 0.0
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
    def cast_to(self: "Self") -> "_Cast_CylindricalGearProfileMeasurement":
        """Cast to another type.

        Returns:
            _Cast_CylindricalGearProfileMeasurement
        """
        return _Cast_CylindricalGearProfileMeasurement(self)
