"""ProcessSimulationInput"""

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

_PROCESS_SIMULATION_INPUT = python_net_import(
    "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew",
    "ProcessSimulationInput",
)

if TYPE_CHECKING:
    from typing import Any, List, Type, TypeVar

    from mastapy._private._internal.typing import PathLike
    from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
        _762,
        _766,
        _767,
        _768,
        _775,
        _793,
        _802,
    )
    from mastapy._private.math_utility import _1718

    Self = TypeVar("Self", bound="ProcessSimulationInput")
    CastSelf = TypeVar(
        "CastSelf", bound="ProcessSimulationInput._Cast_ProcessSimulationInput"
    )


__docformat__ = "restructuredtext en"
__all__ = ("ProcessSimulationInput",)


@extended_dataclass(frozen=True, slots=True, weakref_slot=True)
class _Cast_ProcessSimulationInput:
    """Special nested class for casting ProcessSimulationInput to subclasses."""

    __parent__: "ProcessSimulationInput"

    @property
    def hobbing_process_simulation_input(
        self: "CastSelf",
    ) -> "_775.HobbingProcessSimulationInput":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _775,
        )

        return self.__parent__._cast(_775.HobbingProcessSimulationInput)

    @property
    def worm_grinding_process_simulation_input(
        self: "CastSelf",
    ) -> "_802.WormGrindingProcessSimulationInput":
        from mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
            _802,
        )

        return self.__parent__._cast(_802.WormGrindingProcessSimulationInput)

    @property
    def process_simulation_input(self: "CastSelf") -> "ProcessSimulationInput":
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
class ProcessSimulationInput(_0.APIBase):
    """ProcessSimulationInput

    This is a mastapy class.
    """

    TYPE: ClassVar["Type"] = _PROCESS_SIMULATION_INPUT

    wrapped: "Any"

    def __post_init__(self: "Self") -> None:
        """Override of the post initialisation magic method."""
        if not hasattr(self.wrapped, "reference_count"):
            self.wrapped.reference_count = 0

        self.wrapped.reference_count += 1

    @property
    @exception_bridge
    def analysis_setting(self: "Self") -> "_762.AnalysisMethod":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.AnalysisMethod"""
        temp = pythonnet_property_get(self.wrapped, "AnalysisSetting")

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew.AnalysisMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new._762",
            "AnalysisMethod",
        )(value)

    @analysis_setting.setter
    @exception_bridge
    @enforce_parameter_types
    def analysis_setting(self: "Self", value: "_762.AnalysisMethod") -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew.AnalysisMethod",
        )
        pythonnet_property_set(self.wrapped, "AnalysisSetting", value)

    @property
    @exception_bridge
    def centre_distance_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "CentreDistanceOffset")

        if temp is None:
            return 0.0

        return temp

    @centre_distance_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "CentreDistanceOffset",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def centre_distance_offset_specification_method(
        self: "Self",
    ) -> "_766.CentreDistanceOffsetMethod":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.CentreDistanceOffsetMethod"""
        temp = pythonnet_property_get(
            self.wrapped, "CentreDistanceOffsetSpecificationMethod"
        )

        if temp is None:
            return None

        value = conversion.pn_to_mp_enum(
            temp,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew.CentreDistanceOffsetMethod",
        )

        if value is None:
            return None

        return constructor.new_from_mastapy(
            "mastapy._private.gears.manufacturing.cylindrical.hobbing_process_simulation_new._766",
            "CentreDistanceOffsetMethod",
        )(value)

    @centre_distance_offset_specification_method.setter
    @exception_bridge
    @enforce_parameter_types
    def centre_distance_offset_specification_method(
        self: "Self", value: "_766.CentreDistanceOffsetMethod"
    ) -> None:
        value = conversion.mp_to_pn_enum(
            value,
            "SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew.CentreDistanceOffsetMethod",
        )
        pythonnet_property_set(
            self.wrapped, "CentreDistanceOffsetSpecificationMethod", value
        )

    @property
    @exception_bridge
    def feed(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "Feed")

        if temp is None:
            return 0.0

        return temp

    @feed.setter
    @exception_bridge
    @enforce_parameter_types
    def feed(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "Feed", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def gear_design_lead_crown_modification(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearDesignLeadCrownModification")

        if temp is None:
            return 0.0

        return temp

    @gear_design_lead_crown_modification.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_design_lead_crown_modification(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearDesignLeadCrownModification",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def gear_designed_lead_crown_length(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "GearDesignedLeadCrownLength")

        if temp is None:
            return 0.0

        return temp

    @gear_designed_lead_crown_length.setter
    @exception_bridge
    @enforce_parameter_types
    def gear_designed_lead_crown_length(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "GearDesignedLeadCrownLength",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def shaft_angle_offset(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "ShaftAngleOffset")

        if temp is None:
            return 0.0

        return temp

    @shaft_angle_offset.setter
    @exception_bridge
    @enforce_parameter_types
    def shaft_angle_offset(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped, "ShaftAngleOffset", float(value) if value is not None else 0.0
        )

    @property
    @exception_bridge
    def start_height_above_the_gear_center(self: "Self") -> "float":
        """float"""
        temp = pythonnet_property_get(self.wrapped, "StartHeightAboveTheGearCenter")

        if temp is None:
            return 0.0

        return temp

    @start_height_above_the_gear_center.setter
    @exception_bridge
    @enforce_parameter_types
    def start_height_above_the_gear_center(self: "Self", value: "float") -> None:
        pythonnet_property_set(
            self.wrapped,
            "StartHeightAboveTheGearCenter",
            float(value) if value is not None else 0.0,
        )

    @property
    @exception_bridge
    def tooth_index(self: "Self") -> "int":
        """int"""
        temp = pythonnet_property_get(self.wrapped, "ToothIndex")

        if temp is None:
            return 0

        return temp

    @tooth_index.setter
    @exception_bridge
    @enforce_parameter_types
    def tooth_index(self: "Self", value: "int") -> None:
        pythonnet_property_set(
            self.wrapped, "ToothIndex", int(value) if value is not None else 0
        )

    @property
    @exception_bridge
    def user_specified_center_distance_offset_relative_to_cutter_height(
        self: "Self",
    ) -> "_1718.Vector2DListAccessor":
        """mastapy.math_utility.Vector2DListAccessor"""
        temp = pythonnet_property_get(
            self.wrapped, "UserSpecifiedCenterDistanceOffsetRelativeToCutterHeight"
        )

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @user_specified_center_distance_offset_relative_to_cutter_height.setter
    @exception_bridge
    @enforce_parameter_types
    def user_specified_center_distance_offset_relative_to_cutter_height(
        self: "Self", value: "_1718.Vector2DListAccessor"
    ) -> None:
        pythonnet_property_set(
            self.wrapped,
            "UserSpecifiedCenterDistanceOffsetRelativeToCutterHeight",
            value.wrapped,
        )

    @property
    @exception_bridge
    def cutter_head_slide_error(self: "Self") -> "_767.CutterHeadSlideError":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.CutterHeadSlideError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterHeadSlideError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def cutter_mounting_error(self: "Self") -> "_793.RackMountingError":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.RackMountingError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "CutterMountingError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

    @property
    @exception_bridge
    def gear_mounting_error(self: "Self") -> "_768.GearMountingError":
        """mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new.GearMountingError

        Note:
            This property is readonly.
        """
        temp = pythonnet_property_get(self.wrapped, "GearMountingError")

        if temp is None:
            return None

        type_ = temp.GetType()
        return constructor.new(type_.Namespace, type_.Name)(temp)

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
    def cast_to(self: "Self") -> "_Cast_ProcessSimulationInput":
        """Cast to another type.

        Returns:
            _Cast_ProcessSimulationInput
        """
        return _Cast_ProcessSimulationInput(self)
