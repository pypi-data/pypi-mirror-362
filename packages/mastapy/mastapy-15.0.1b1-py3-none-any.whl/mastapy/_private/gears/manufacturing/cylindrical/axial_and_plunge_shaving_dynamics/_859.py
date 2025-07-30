"""PlungeShaverDynamicSettings"""

from __future__ import annotations

from enum import Enum
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

_PLUNGE_SHAVER_DYNAMIC_SETTINGS = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics",
    "PlungeShaverDynamicSettings",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike

    Self = TypeVar("Self", bound="PlungeShaverDynamicSettings")
    CastSelf = TypeVar(
        "CastSelf",
        bound="PlungeShaverDynamicSettings._Cast_PlungeShaverDynamicSettings",
    )


__docformat__ = "restructuredtext en"
__all__ = ("PlungeShaverDynamicSettings",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_PlungeShaverDynamicSettings:
    """Special nested class for casting PlungeShaverDynamicSettings to subclasses."""

    __parent__: "PlungeShaverDynamicSettings"

    @property
    def plunge_shaver_dynamic_settings(
        self: "CastSelf",
    ) -> "PlungeShaverDynamicSettings":
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
class PlungeShaverDynamicSettings(_0.APIBase):
    """PlungeShaverDynamicSettings

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PLUNGE_SHAVER_DYNAMIC_SETTINGS

    class PlungeShavingDynamicAccuracy(Enum):
        """PlungeShavingDynamicAccuracy is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _PLUNGE_SHAVER_DYNAMIC_SETTINGS.PlungeShavingDynamicAccuracy

        LOW_ACCURACY = 0
        HIGH_ACCURACY = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    PlungeShavingDynamicAccuracy.__setattr__ = __enum_setattr
    PlungeShavingDynamicAccuracy.__delattr__ = __enum_delattr

    class PlungeShavingDynamicFlank(Enum):
        """PlungeShavingDynamicFlank is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _PLUNGE_SHAVER_DYNAMIC_SETTINGS.PlungeShavingDynamicFlank

        LEFT_FLANK = 0
        RIGHT_FLANK = 1

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    PlungeShavingDynamicFlank.__setattr__ = __enum_setattr
    PlungeShavingDynamicFlank.__delattr__ = __enum_delattr

    class PlungeShavingDynamicsSection(Enum):
        """PlungeShavingDynamicsSection is a nested enum."""

        @classmethod
        def type_(cls) -> "Type":
            return _PLUNGE_SHAVER_DYNAMIC_SETTINGS.PlungeShavingDynamicsSection

        CENTER_SECTION = 0
        TOPCENTERBOTTOM_SECTION_125_FACE_WIDTH_FROM_TOPBOTTOM_END = 1
        SPECIFIED_ZPLANE = 2

    def __enum_setattr(self: "Self", attr: str, value: "Any") -> None:
        raise AttributeError("Cannot set the attributes of an Enum.") from None

    def __enum_delattr(self: "Self", attr: str) -> None:
        raise AttributeError("Cannot delete the attributes of an Enum.") from None

    PlungeShavingDynamicsSection.__setattr__ = __enum_setattr
    PlungeShavingDynamicsSection.__delattr__ = __enum_delattr

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def calculation_accuracy(
        self: "Self",
    ) -> "PlungeShaverDynamicSettings.PlungeShavingDynamicAccuracy":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings.PlungeShavingDynamicAccuracy"""
        temp = pythonnet_property_get(self.wrapped, "CalculationAccuracy")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics.PlungeShaverDynamicSettings+PlungeShavingDynamicAccuracy",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings.PlungeShaverDynamicSettings",
            "PlungeShavingDynamicAccuracy",
        )(value)

    @calculation_accuracy.setter
    @exception_bridge
    @enforce_parameter_types
    def calculation_accuracy(
        self: "Self", value: "PlungeShaverDynamicSettings.PlungeShavingDynamicAccuracy"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics.PlungeShaverDynamicSettings+PlungeShavingDynamicAccuracy",
        )
        pythonnet_property_set(self.wrapped, "CalculationAccuracy", value)

    @property
    @exception_bridge
    def calculation_flank(
        self: "Self",
    ) -> "PlungeShaverDynamicSettings.PlungeShavingDynamicFlank":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings.PlungeShavingDynamicFlank"""
        temp = pythonnet_property_get(self.wrapped, "CalculationFlank")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics.PlungeShaverDynamicSettings+PlungeShavingDynamicFlank",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings.PlungeShaverDynamicSettings",
            "PlungeShavingDynamicFlank",
        )(value)

    @calculation_flank.setter
    @exception_bridge
    @enforce_parameter_types
    def calculation_flank(
        self: "Self", value: "PlungeShaverDynamicSettings.PlungeShavingDynamicFlank"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics.PlungeShaverDynamicSettings+PlungeShavingDynamicFlank",
        )
        pythonnet_property_set(self.wrapped, "CalculationFlank", value)

    @property
    @exception_bridge
    def section_locations(
        self: "Self",
    ) -> "PlungeShaverDynamicSettings.PlungeShavingDynamicsSection":
        """mastapy.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings.PlungeShavingDynamicsSection"""
        temp = pythonnet_property_get(self.wrapped, "SectionLocations")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics.PlungeShaverDynamicSettings+PlungeShavingDynamicsSection",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.axial_and_plunge_shaving_dynamics.PlungeShaverDynamicSettings.PlungeShaverDynamicSettings",
            "PlungeShavingDynamicsSection",
        )(value)

    @section_locations.setter
    @exception_bridge
    @enforce_parameter_types
    def section_locations(
        self: "Self", value: "PlungeShaverDynamicSettings.PlungeShavingDynamicsSection"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.AxialAndPlungeShavingDynamics.PlungeShaverDynamicSettings+PlungeShavingDynamicsSection",
        )
        pythonnet_property_set(self.wrapped, "SectionLocations", value)

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
    def cast_to(self: "Self") -> "_Cast_PlungeShaverDynamicSettings":
        """Cast to another type.

        Returns:
            _Cast_PlungeShaverDynamicSettings
        """
        return _Cast_PlungeShaverDynamicSettings(self)
